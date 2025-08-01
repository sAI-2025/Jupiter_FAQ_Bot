# # # chatbot.py

# import os
# import logging
# from datetime import datetime

# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.chains import create_retrieval_chain, create_history_aware_retriever
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.messages import HumanMessage, AIMessage
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from dotenv import load_dotenv

# load_dotenv()

# # Optional: disable Chroma telemetry
# os.environ["CHROMA_TELEMETRY_ENABLED"] = "FALSE"

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # --- 1. Initialize Embeddings and Vectorstore ---
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2",
#     model_kwargs={"device": "cpu"},
#     encode_kwargs={"normalize_embeddings": True}
# )

# vectorstore_path = "./jupiter_vectordb_enhanced"
# vectorstore = Chroma(
#     persist_directory=vectorstore_path,
#     embedding_function=embeddings
# )

# retriever = vectorstore.as_retriever(search_kwargs={"k": 5})


# # --- 2. Initialize the LLM ---
# llm = ChatGroq(
#     groq_api_key= os.environ.get("GROQ_API_KEY", ""),
#     model_name="llama3-8b-8192",
#     temperature=0.3,
#     max_tokens=300
# )

# # --- 3. Prompt Templates ---
# # Contextualize Follow-Up Questions
# contextualize_q_prompt = ChatPromptTemplate.from_messages([
#     ("system", (
#         "As JupiterBot, rewrite the user's follow-up message into a clear, standalone question. "
#         "Include relevant chat history, domain-specific terms (e.g., 'Jupiter card', 'Jewels'), "
#         "and clarify any ambiguity to make it fully self-contained."
#     )),
#     MessagesPlaceholder("chat_history"),
#     ("human", "{input}")
# ])

# # Main Answering Prompt
# qa_prompt = ChatPromptTemplate.from_messages([
#     ("system", (
#         "You are Jupiter’s Tier‑1 Support Bot. Provide friendly, professional responses (2–3 sentences) "
#         "using the provided context.\n"
#         "If relevant, include clear actionable steps like app navigation (e.g., 'Go to Settings > Card > Block Card') "
#         "or links to the Help Center.\n"
#         "If unsure, reply: 'I'm not certain—let me escalate this or check with our team.'\n"
#         "Avoid using internal system terms. Always prioritize clarity and customer understanding.\n\n"
#         "{context}"
#     )),
#     MessagesPlaceholder("chat_history"),
#     ("human", "{input}")
# ])

# # --- 4. Build RAG Chain with Memory ---
# history_aware_retriever = create_history_aware_retriever(
#     llm=llm,
#     retriever=retriever,
#     prompt=contextualize_q_prompt
# )

# question_answer_chain = create_stuff_documents_chain(
#     llm=llm,
#     prompt=qa_prompt
# )

# rag_chain = create_retrieval_chain(
#     retriever=history_aware_retriever,
#     combine_docs_chain=question_answer_chain
# )

# # --- 5. In-memory Chat History per Session ---
# store = {}

# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = ChatMessageHistory()
#     return store[session_id]

# # Wrap the chain with session-aware message memory
# conversational_rag_chain = RunnableWithMessageHistory(
#     rag_chain,
#     get_session_history,
#     input_messages_key="input",
#     history_messages_key="chat_history",
#     output_messages_key="answer"
# )

# # --- 6. Exposed Function for UI or CLI Integration ---
# def query_jupiter(question: str, session_id: str = "default") -> dict:
#     try:
#         logger.info(f"💬 Query: {question} (Session: {session_id})")
#         start = datetime.now()

#         result = conversational_rag_chain.invoke(
#             {"input": question},
#             config={"configurable": {"session_id": session_id}}
#         )

#         return {
#             "question": question,
#             "answer": result["answer"],
#             "session_id": session_id,
#             "processing_time": (datetime.now() - start).total_seconds()
#         }

#     except Exception as e:
#         logger.error(f"❌ Error: {e}")
#         return {
#             "error": str(e),
#             "session_id": session_id
#         }

# # --- 7. Test Runner (Optional for Local Testing) ---
# def main():
#     if "GROQ_API_KEY" not in os.environ:
#         print("❌ GROQ_API_KEY environment variable is not set")
#         return

#     print("✅ Jupiter RAG chatbot initialized\n")

#     test_queries = [
#         "Im sai krishna ,How do I activate my Jupiter card?",
#         "Bill payment failed",
#         "What are Jewels?",
#         "KYC verification process",
#         "What my name ?",
#         "what services you providing for me ?",
#         "How can I activate my Jupiter card, and what are the common issues users face during activation?",
#         "What steps should I follow if my bill payment fails? Are there alternative payment methods outside the app?",
#         "What exactly are “Jewels” in Jupiter, and how can I earn, redeem, or track them effectively?",
#         "What is the detailed KYC (Know Your Customer) verification process, and how long does it usually take to complete?",
#         "What types of financial services and products does Jupiter currently offer (e.g., debit cards, credit cards, savings accounts, investments)?",
#         "Can Jupiter be used internationally? If yes, what are the restrictions or fees for using the card abroad?",
#         "What triggers automatic fund deductions from savings or “Pots” to pay dues, and how can users control or disable this feature?",
#         "What is the process and expected timeline for resolving account freezes or blocks due to KYC or suspicious activities?",
#         "How does Jupiter handle customer support escalations? What are the official channels, response times, and escalation paths?",
#         "What security measures are in place to protect user data and transactions, and how does Jupiter comply with financial regulations like RBI guidelines?"
#     ]

#     # for i, q in enumerate(test_queries, 1):
#     #     print(f"\n{'='*60}")
#     #     print(f"🧪 Test {i}: {q}")
#     #     result = query_jupiter(q, session_id=f"test_session_{i}")
#     #     print(f"✅ Answer: {result.get('answer')}")
#     #     print(f"⏱ Time: {result.get('processing_time'):.2f}s")

# if __name__ == "__main__":
#     main()
# enhanced_chatbot.py

import os
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jupiter_chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ValidationResult(Enum):
    IN_SCOPE = "in_scope"
    OUT_OF_SCOPE = "out_of_scope"
    ERROR = "error"

class JupiterChatbot:
    def __init__(self):
        """Initialize the enhanced Jupiter chatbot with improved prompting"""
        self.embeddings = None
        self.vectorstore = None
        self.retriever = None
        self.validator_llm = None
        self.contextualizer_llm = None
        self.qa_llm = None
        self.session_store = {}

        # Performance metrics
        self.metrics = {
            "total_queries": 0,
            "out_of_scope_queries": 0,
            "successful_queries": 0,
            "error_queries": 0,
            "greeting_queries": 0,
            "escalated_queries": 0
        }

        self._initialize_components()
        self._setup_enhanced_chains()

    def _initialize_components(self):
        """Initialize embeddings, vectorstore, and LLMs"""
        try:
            logger.info("🔧 Initializing enhanced chatbot components...")

            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True}
            )

            # Initialize vectorstore
            vectorstore_path = "./jupiter_vectordb_enhanced"
            self.vectorstore = Chroma(
                persist_directory=vectorstore_path,
                embedding_function=self.embeddings
            )
            self.retriever = self.vectorstore.as_retriever(
                search_type="mmr",  # Maximum Marginal Relevance for diverse results
                search_kwargs={"k": 6, "fetch_k": 20}
            )

            # Initialize LLMs with optimized configurations
            groq_api_key = os.environ.get("GROQ_API_KEY", "")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY environment variable is not set")

            # Validator LLM - Fast and efficient
            self.validator_llm = ChatGroq(
                groq_api_key=groq_api_key,
                model_name="llama3-8b-8192",
                temperature=0.0,
                max_tokens=50
            )

            # Contextualizer LLM - Moderate creativity
            self.contextualizer_llm = ChatGroq(
                groq_api_key=groq_api_key,
                model_name="llama3-8b-8192",
                temperature=0.2,
                max_tokens=200
            )

            # QA LLM - Balanced for comprehensive answers
            self.qa_llm = ChatGroq(
                groq_api_key=groq_api_key,
                model_name="llama3-8b-8192",
                temperature=0.3,
                max_tokens=500
            )

            logger.info("✅ All components initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize components: {e}")
            raise

    def _setup_enhanced_chains(self):
        """Setup enhanced processing chains with improved prompts"""
        try:
            # 1. Enhanced Validator Chain
            self.validator_prompt = ChatPromptTemplate.from_messages([
                ("system", (
                    "You are a scope validator for JupiterBot. Determine if a user question is about Jupiter.money services.\n\n"

                    "✅ ALWAYS ALLOW (Jupiter.money related):\n"
                    "- App features: Pots, Jewels, Cards, UPI, bill payments, transfers\n"
                    "- Account help: KYC, linking, profiles, statements, troubleshooting\n"
                    "- Card services: activation, PIN, blocking, limits, transactions\n"
                    "- General Jupiter inquiries, onboarding, how-to questions\n"
                    "- Friendly greetings, small talk, 'What can you do?' questions\n\n"

                    "🚫 BLOCK (Not Jupiter.money related):\n"
                    "- Other banks/financial services (HDFC, SBI, PayTM, etc.)\n"
                    "- Investment advice, tax planning, personal finance guidance\n"
                    "- Unrelated topics: cooking, movies, politics, general knowledge\n\n"

                    "Respond with exactly ONE word:\n"
                    "- 'ALLOWED' if question is Jupiter.money related OR friendly interaction\n"
                    "- 'BLOCKED' if question is completely unrelated to Jupiter.money"
                )),
                ("human", "{input}")
            ])

            self.validator_chain = self.validator_prompt | self.validator_llm | StrOutputParser()

            # 2. Enhanced Contextualizer Chain
            self.contextualizer_prompt = ChatPromptTemplate.from_messages([
                ("system", (
                    "You are JupiterBot's conversation contextualizer. Your job is to rewrite follow-up questions "
                    "into clear, standalone queries that incorporate relevant chat history.\n\n"

                    "GUIDELINES:\n"
                    "- Make questions self-contained and specific\n"
                    "- Include Jupiter-specific terms when relevant (Jewels, Pots, Jupiter card, etc.)\n"
                    "- Resolve pronouns and references using chat history\n"
                    "- If question is already clear, return it unchanged\n"
                    "- Maintain the user's intent and tone\n\n"

                    "EXAMPLES:\n"
                    "User: 'How do I activate it?' (after asking about Jupiter card)\n"
                    "Output: 'How do I activate my Jupiter debit card?'\n\n"

                    "User: 'What about the rewards?' (after asking about Jupiter features)\n"
                    "Output: 'What are Jupiter Jewels rewards and how do they work?'"
                )),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ])

            self.contextualizer_chain = self.contextualizer_prompt | self.contextualizer_llm | StrOutputParser()

            # 3. Enhanced History-aware retriever
            self.history_aware_retriever = create_history_aware_retriever(
                llm=self.contextualizer_llm,
                retriever=self.retriever,
                prompt=self.contextualizer_prompt
            )

            # 4. Enhanced QA Chain with improved prompt
            self.qa_prompt = ChatPromptTemplate.from_messages([
                ("system", (
                    "You are JupiterBot, Jupiter.money's AI Assistant — your friendly guide to India's most delightful money app.\n\n"

                    "🎯 PRIMARY ROLE:\n"
                    "You provide instant, helpful support for Jupiter.money users with a warm, professional tone that reflects our brand values of simplicity, delight, and customer-first service.\n\n"

                    "✅ IN-SCOPE TOPICS (Always Help With):\n"
                    "• Jupiter App Features: Pots, Jewels, Cards, UPI payments, bill payments, money transfers\n"
                    "• Account Management: KYC verification, account linking, profile updates, statements\n"
                    "• Card Services: Debit card activation, PIN reset, card blocking/unblocking, transaction limits\n"
                    "• Troubleshooting: Login issues, payment failures, app crashes, transaction disputes\n"
                    "• Onboarding: Account opening, document upload, verification status\n"
                    "• General Inquiries: Features explanation, benefits, how-to guides\n"
                    "• Friendly Interactions: Greetings, small talk, 'What can you do?', casual questions\n\n"

                    "📋 RESPONSE GUIDELINES:\n"
                    "1. TONE: Warm, friendly, professional but conversational\n"
                    "2. LENGTH: 2-3 sentences for simple queries, up to 4-5 for complex ones\n"
                    "3. STRUCTURE: Clear, actionable steps when relevant (e.g., 'Go to App → Settings → Cards')\n"
                    "4. LANGUAGE: Simple, jargon-free, easy to understand\n"
                    "5. BRAND VOICE: Helpful buddy who knows Jupiter inside-out\n\n"

                    "🔄 INTERACTION PATTERNS:\n"
                    "• Greetings: Respond warmly and ask how you can help\n"
                    "• Vague Questions: Gently guide users to be more specific\n"
                    "• Complex Issues: Break down into simple steps or offer escalation\n\n"

                    "⚠️ WHEN UNCERTAIN:\n"
                    "Say: 'I want to make sure I give you the right information. Let me connect you with our support team who can help with the specifics, or you can check the Help section in your Jupiter app.'\n\n"

                    "🎨 BRAND PERSONALITY:\n"
                    "• Curious and genuinely helpful\n"
                    "• Optimistic and solution-focused\n"
                    "• Knowledgeable but humble\n"
                    "• Professional yet approachable\n\n"

                    "Use the provided context to answer accurately. If context doesn't contain the answer, be honest about limitations and offer to escalate.\n\n"

                    "CONTEXT:\n{context}"
                )),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ])

            self.question_answer_chain = create_stuff_documents_chain(
                llm=self.qa_llm,
                prompt=self.qa_prompt
            )

            # 5. Complete RAG Chain
            self.rag_chain = create_retrieval_chain(
                retriever=self.history_aware_retriever,
                combine_docs_chain=self.question_answer_chain
            )

            # 6. Conversational RAG Chain with memory
            self.conversational_rag_chain = RunnableWithMessageHistory(
                self.rag_chain,
                self._get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer"
            )

            logger.info("✅ Enhanced chains setup successfully")

        except Exception as e:
            logger.error(f"❌ Failed to setup enhanced chains: {e}")
            raise

    def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Get or create chat history for a session"""
        if session_id not in self.session_store:
            self.session_store[session_id] = ChatMessageHistory()
        return self.session_store[session_id]

    def _sanitize_input(self, text: str) -> str:
        """Enhanced input sanitization"""
        if not text or not isinstance(text, str):
            return ""

        # Remove excessive whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())

        # Remove potentially harmful patterns
        text = re.sub(r'[<>{}]', '', text)  # Remove HTML-like tags

        # Limit length
        max_length = 500
        if len(text) > max_length:
            text = text[:max_length] + "..."
            logger.warning(f"Input truncated to {max_length} characters")

        return text

    def _is_greeting_or_casual(self, question: str) -> bool:
        """Check if question is a greeting or casual interaction"""
        greeting_patterns = [
            r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
            r'\bwhat can you do\b',
            r'\bwho are you\b',
            r'\bhelp me\b',
            r'\bhow are you\b',
            r'\bthanks?\b',
            r'\bthank you\b'
        ]

        question_lower = question.lower()
        return any(re.search(pattern, question_lower) for pattern in greeting_patterns)

    def _validate_question(self, question: str) -> ValidationResult:
        """Enhanced validation with greeting detection"""
        try:
            logger.info(f"🛡️ Validating question scope...")

            # Always allow greetings and casual interactions
            if self._is_greeting_or_casual(question):
                logger.info("👋 Detected greeting/casual interaction - allowing")
                self.metrics["greeting_queries"] += 1
                return ValidationResult.IN_SCOPE

            result = self.validator_chain.invoke({"input": question})
            result = result.strip().upper()

            if "ALLOWED" in result:
                logger.info("✅ Question is in scope")
                return ValidationResult.IN_SCOPE
            elif "BLOCKED" in result:
                logger.info("🚫 Question is out of scope")
                return ValidationResult.OUT_OF_SCOPE
            else:
                logger.warning(f"⚠️ Ambiguous validation result: {result}")
                return ValidationResult.IN_SCOPE  # Default to allowing

        except Exception as e:
            logger.error(f"❌ Validation error: {e}")
            return ValidationResult.ERROR

    def _contextualize_question(self, question: str, session_id: str) -> str:
        """Enhanced question contextualization"""
        try:
            logger.info("🔄 Contextualizing question...")

            chat_history = self._get_session_history(session_id).messages
            if not chat_history or len(chat_history) < 2:
                return question  # No meaningful history to contextualize with

            result = self.contextualizer_chain.invoke({
                "input": question,
                "chat_history": chat_history[-10:]  # Use last 10 messages for context
            })

            logger.info(f"📝 Contextualized: {result}")
            return result.strip()

        except Exception as e:
            logger.error(f"❌ Contextualization error: {e}")
            return question  # Fallback to original question

    # def _generate_answer(self, question: str, session_id: str) -> Dict[str, Any]:
        """Enhanced answer generation with better error handling"""
        try:
            logger.info("🧠 Generating answer...")

            result = self.conversational_rag_chain.invoke(
                {"input": question},
                config={"configurable": {"session_id": session_id}}
            )

            # Extract and process source documents
            source_docs = result.get("context", [])
            sources = []
            for doc in source_docs:
                source = doc.metadata.get("source", "Unknown")
                if source != "Unknown":
                    sources.append(source)

            # Determine if escalation is needed
            answer_text = result["answer"].lower()
            needs_escalation = any(keyword in answer_text for keyword in [
                "not sure", "uncertain", "don't know", "can't help",
                "contact support", "escalate", "technical team"
            ])

            if needs_escalation:
                self.metrics["escalated_queries"] += 1

            return {
                "answer": result["answer"],
                "sources": list(set(sources)),  # Remove duplicates
                "confidence": len(source_docs),
                "needs_escalation": needs_escalation
            }

        except Exception as e:
            logger.error(f"❌ Answer generation error: {e}")
            return {
                "answer": "I'm experiencing technical difficulties right now. Please try again in a moment, or you can reach out to our support team through the Jupiter app for immediate assistance! 😊",
                "sources": [],
                "confidence": 0,
                "needs_escalation": True
            }

    def _generate_answer(self, question: str, session_id: str) -> Dict[str, Any]:
        """Enhanced answer generation + suggest similar questions"""
        try:
            logger.info("🧠 Generating answer and retrieving similar questions...")

            result = self.conversational_rag_chain.invoke(
                {"input": question},
                config={"configurable": {"session_id": session_id}}
            )

            # Extract and process source documents
            source_docs = result.get("context", [])
            sources = []
            for doc in source_docs:
                source = doc.metadata.get("source", "Unknown")
                if source != "Unknown":
                    sources.append(source)

            # Determine if escalation is needed
            answer_text = result["answer"].lower()
            needs_escalation = any(keyword in answer_text for keyword in [
                "not sure", "uncertain", "don't know", "can't help",
                "contact support", "escalate", "technical team"
            ])

            if needs_escalation:
                self.metrics["escalated_queries"] += 1

            # Fetch similar questions with similarity score
            similar_docs = self.vectorstore.similarity_search_with_relevance_scores(
                query=question, k=3  # fetch top 3
            )

            similar_questions = []
            for doc, score in similar_docs:
                if score >= 0.75:
                    question_text = doc.page_content.strip()
                    similar_questions.append({
                        "question": question_text,
                        "score": round(score, 2)
                    })

            return {
                "answer": result["answer"],
                "sources": list(set(sources)),  # Remove duplicates
                "confidence": len(source_docs),
                "needs_escalation": needs_escalation,
                "similar_questions": similar_questions  # NEW FIELD
            }

        except Exception as e:
            logger.error(f"❌ Answer generation error: {e}")
            return {
                "answer": "I'm experiencing technical difficulties right now. Please try again in a moment, or you can reach out to our support team through the Jupiter app for immediate assistance! 😊",
                "sources": [],
                "confidence": 0,
                "needs_escalation": True,
                "similar_questions": []
            }



    def query(self, question: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Enhanced main query method with improved processing pipeline
        """
        start_time = datetime.now()
        self.metrics["total_queries"] += 1

        try:
            logger.info(f"💬 New query: '{question}' (Session: {session_id})")

            # Stage 1: Input sanitization
            sanitized_question = self._sanitize_input(question)
            if not sanitized_question:
                return {
                    "answer": "I'd love to help! Could you please ask me a question about Jupiter.money? 😊",
                    "session_id": session_id,
                    "processing_time": 0,
                    "stage": "input_validation",
                    "status": "error"
                }

            # Stage 2: Enhanced scope validation
            validation_result = self._validate_question(sanitized_question)

            if validation_result == ValidationResult.OUT_OF_SCOPE:
                self.metrics["out_of_scope_queries"] += 1
                return {
                    "answer": "Hi there! 👋 I can only help with questions about Jupiter.money services, features, and your account. What would you like to know about Jupiter today?",
                    "session_id": session_id,
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "stage": "validation",
                    "status": "out_of_scope"
                }

            elif validation_result == ValidationResult.ERROR:
                self.metrics["error_queries"] += 1
                return {
                    "answer": "I'm having a small technical hiccup. Could you try rephrasing your question? I'm here to help with anything Jupiter.money related! 😊",
                    "session_id": session_id,
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "stage": "validation",
                    "status": "error"
                }

            # Stage 3: Question contextualization
            contextualized_question = self._contextualize_question(sanitized_question, session_id)

            # Stage 4: Enhanced RAG-based answer generation
            answer_result = self._generate_answer(contextualized_question, session_id)

            processing_time = (datetime.now() - start_time).total_seconds()
            self.metrics["successful_queries"] += 1

            result = {
                "question": sanitized_question,
                "contextualized_question": contextualized_question,
                "answer": answer_result["answer"],
                "sources": answer_result["sources"],
                "confidence": answer_result["confidence"],
                "needs_escalation": answer_result.get("needs_escalation", False),
                "session_id": session_id,
                "processing_time": processing_time,
                "stage": "complete",
                "status": "success"
            }

            logger.info(f"✅ Query completed in {processing_time:.2f}s")
            return result

        except Exception as e:
            self.metrics["error_queries"] += 1
            logger.error(f"❌ Unexpected error in query processing: {e}")

            return {
                "answer": "Oops! I'm experiencing some technical difficulties. Please try again in a moment, or reach out to our support team through the Jupiter app for immediate help! 🛠️",
                "session_id": session_id,
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "stage": "error",
                "status": "error",
                "error": str(e)
            }

    def get_enhanced_metrics(self) -> Dict[str, Any]:
        """Get enhanced chatbot performance metrics"""
        total = max(self.metrics["total_queries"], 1)
        return {
            **self.metrics,
            "success_rate": (self.metrics["successful_queries"] / total) * 100,
            "out_of_scope_rate": (self.metrics["out_of_scope_queries"] / total) * 100,
            "greeting_rate": (self.metrics["greeting_queries"] / total) * 100,
            "escalation_rate": (self.metrics["escalated_queries"] / total) * 100,
            "error_rate": (self.metrics["error_queries"] / total) * 100
        }

    def clear_session(self, session_id: str) -> bool:
        """Clear chat history for a specific session"""
        try:
            if session_id in self.session_store:
                del self.session_store[session_id]
                logger.info(f"🗑️ Cleared session: {session_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error clearing session {session_id}: {e}")
            return False

    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs"""
        return list(self.session_store.keys())

# --- Enhanced Convenience Functions ---

_chatbot_instance = None

def get_chatbot() -> JupiterChatbot:
    """Get or create global chatbot instance"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = JupiterChatbot()
    return _chatbot_instance

def query_jupiter(question: str, session_id: str = "default") -> Dict[str, Any]:
    """
    Enhanced convenience function for querying Jupiter chatbot
    """
    chatbot = get_chatbot()
    return chatbot.query(question, session_id)

def clear_chat_session(session_id: str = "default") -> bool:
    """Clear chat history for a session"""
    chatbot = get_chatbot()
    return chatbot.clear_session(session_id)

def get_chatbot_metrics() -> Dict[str, Any]:
    """Get enhanced chatbot performance metrics"""
    chatbot = get_chatbot()
    return chatbot.get_enhanced_metrics()

# --- Enhanced Test Runner ---
def main():
    """Test the enhanced chatbot with comprehensive scenarios"""
    if "GROQ_API_KEY" not in os.environ:
        print("❌ GROQ_API_KEY environment variable is not set")
        return

    print("🚀 Initializing Enhanced Jupiter RAG Chatbot v2.0...\n")

    # try:
    #     chatbot = JupiterChatbot()
    #     print("✅ Enhanced chatbot initialized successfully!\n")

        # Enhanced test scenarios
    #     test_scenarios = [
    #         # Greetings and casual interactions
    #         ("Hi there!", "user_1"),
    #         ("Hello, what can you do?", "user_1"),
    #         ("Good morning! I need help", "user_2"),

    #         # In-scope Jupiter questions
    #         ("How do I activate my Jupiter debit card?", "user_1"),
    #         ("What are Jewels and how do I earn them?", "user_3"),
    #         ("My payment failed yesterday, what should I do?", "user_1"),
    #         ("Tell me about KYC verification process", "user_4"),
    #         ("How can I block my card if it's lost?", "user_5"),
    #         ("What is a Pot and how do I create one?", "user_3"),

    #         # Follow-up questions (testing contextualization)
    #         ("How long does it take?", "user_4"),  # Follow-up to KYC
    #         ("What documents do I need?", "user_4"),  # Another follow-up

    #         # Edge cases and out-of-scope
    #         ("What's the weather today?", "user_6"),
    #         ("Tell me about HDFC bank services", "user_7"),
    #         ("How do I cook pasta?", "user_8"),

    #         # Complex scenarios
    #         ("I can't login to my app and my card is not working", "user_9"),
    #         ("", "user_10"),  # Empty input
    #         ("a" * 100, "user_10"),  # Long input
    #     ]

    #     for i, (question, session_id) in enumerate(test_scenarios, 1):
    #         print(f"\n{'='*80}")
    #         print(f"🧪 Test {i}: {question[:100]}{'...' if len(question) > 100 else ''}")
    #         print(f"👤 Session: {session_id}")

    #         result = chatbot.query(question, session_id)

    #         print(f"✅ Answer: {result['answer']}")
    #         print(f"📊 Status: {result['status']} | Stage: {result['stage']}")
    #         print(f"⏱️ Time: {result['processing_time']:.2f}s")

    #         if result.get('sources'):
    #             print(f"📚 Sources: {', '.join(result['sources'][:3])}...")  # Show first 3 sources

    #         if result.get('needs_escalation'):
    #             print("🚨 Escalation recommended")

    #     # Show enhanced metrics
    #     print(f"\n{'='*80}")
    #     print("📈 ENHANCED METRICS:")
    #     metrics = chatbot.get_enhanced_metrics()
    #     for key, value in metrics.items():
    #         if isinstance(value, float):
    #             print(f"  {key}: {value:.2f}%")
    #         else:
    #             print(f"  {key}: {value}")

    #     print(f"\n🔄 Active Sessions: {len(chatbot.get_active_sessions())}")

    # except Exception as e:
    #     print(f"❌ Error during testing: {e}")
    #     logger.error(f"Test error: {e}")

if __name__ == "__main__":
    main()




# optimized_chatbot.py

# import os
# import logging
# import re
# import hashlib
# import time
# from datetime import datetime, timedelta
# from typing import Dict, List, Optional, Any, Tuple, Set
# from enum import Enum
# from functools import lru_cache
# from threading import Lock
# import json
# import pickle
# from collections import deque

# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.chains import create_retrieval_chain, create_history_aware_retriever
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.messages import HumanMessage, AIMessage
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv

# load_dotenv()

# # Optimized logging
# logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# class ScopeResult(Enum):
#     IN_SCOPE = "in_scope"
#     OUT_OF_SCOPE = "out_of_scope"
#     GREETING = "greeting"
#     UNCLEAR = "unclear"

# class UltraFastJupiterChatbot:
#     def __init__(self):
#         """Ultra-fast Jupiter chatbot with advanced scope validation and caching"""

#         # Core components
#         self.embeddings = None
#         self.vectorstore = None
#         self.retriever = None
#         self.llm = None
#         self.session_store = {}

#         # Multi-layer caching system
#         self.instant_responses = {}  # Pre-computed responses
#         self.faq_cache = {}          # FAQ cache
#         self.semantic_cache = {}     # Semantic similarity cache
#         self.scope_cache = {}        # Scope validation cache
#         self.embedding_cache = {}    # Embedding cache
#         self.cache_lock = Lock()

#         # Performance settings
#         self.CACHE_EXPIRY_HOURS = 6
#         self.SEMANTIC_THRESHOLD = 0.90
#         self.MAX_CACHE_SIZE = 200
#         self.MAX_SESSION_MESSAGES = 8

#         # Enhanced scope validation patterns
#         self._setup_scope_patterns()

#         # Performance metrics
#         self.metrics = {
#             "total_queries": 0, "instant_hits": 0, "faq_hits": 0, "semantic_hits": 0,
#             "scope_blocks": 0, "rag_queries": 0, "avg_response_time": 0.0,
#             "cache_hit_rate": 0.0, "scope_accuracy": 0.0
#         }

#         self._initialize_components()
#         self._setup_chains()
#         self._preload_instant_responses()

#     def _setup_scope_patterns(self):
#         """Setup enhanced scope validation patterns"""

#         # Jupiter-specific keywords (comprehensive)
#         jupiter_terms = [
#             'jupiter', 'jewels', 'pot', 'pots', 'card', 'debit', 'upi', 'kyc',
#             'account', 'savings', 'transaction', 'payment', 'bill', 'recharge',
#             'transfer', 'money', 'bank', 'banking', 'finance', 'invest', 'loan',
#             'credit', 'balance', 'statement', 'pin', 'otp', 'verification',
#             'activation', 'app', 'mobile', 'digital', 'wallet', 'cashback',
#             'reward', 'offer', 'promo', 'discount', 'merchant', 'shopping'
#         ]

#         # Strict out-of-scope patterns
#         out_of_scope_terms = [
#             # Other banks/fintech
#             'hdfc', 'sbi', 'icici', 'axis', 'kotak', 'paytm', 'phonepe', 'googlepay',
#             'bharatpe', 'cred', 'razorpay', 'payu', 'mobikwik', 'freecharge',

#             # Non-financial topics
#             'weather', 'cricket', 'bollywood', 'politics', 'election', 'government',
#             'cooking', 'recipe', 'movie', 'music', 'sports', 'travel', 'hotel',
#             'restaurant', 'food', 'game', 'entertainment', 'celebrity', 'news',

#             # Technical/Academic
#             'python', 'code', 'programming', 'algorithm', 'math', 'physics',
#             'chemistry', 'biology', 'history', 'geography', 'science', 'study',
#             'homework', 'assignment', 'exam', 'university', 'college', 'school',

#             # General queries
#             'translate', 'definition', 'meaning', 'wikipedia', 'google', 'search',
#             'time', 'date', 'calendar', 'reminder', 'alarm', 'timer'
#         ]

#         # Compile patterns for speed
#         self.jupiter_pattern = re.compile(
#             r'\b(' + '|'.join(jupiter_terms) + r')\b',
#             re.IGNORECASE
#         )

#         self.out_of_scope_pattern = re.compile(
#             r'\b(' + '|'.join(out_of_scope_terms) + r')\b',
#             re.IGNORECASE
#         )

#         self.greeting_pattern = re.compile(
#             r'\b(hi|hello|hey|hii|hlo|namaste|good\s+(morning|afternoon|evening)|'
#             r'what\s+can\s+you\s+do|who\s+are\s+you|help\s+me|how\s+are\s+you|'
#             r'thanks?|thank\s+you|bye|goodbye)\b',
#             re.IGNORECASE
#         )

#         # Programming/code detection
#         self.code_pattern = re.compile(
#             r'(write|create|generate|make|build)\s+(code|program|script|function|class|'
#             r'algorithm|app|application|website|html|css|javascript|python|java|c\+\+)',
#             re.IGNORECASE
#         )

#     def _initialize_components(self):
#         """Initialize components with ultra-fast settings"""
#         try:
#             # Lightweight embeddings
#             self.embeddings = HuggingFaceEmbeddings(
#                 model_name="sentence-transformers/all-MiniLM-L6-v2",
#                 model_kwargs={"device": "cpu"},
#                 encode_kwargs={"normalize_embeddings": True, "batch_size": 64}
#             )

#             # Optimized vectorstore
#             self.vectorstore = Chroma(
#                 persist_directory="./jupiter_vectordb_enhanced",
#                 embedding_function=self.embeddings
#             )

#             # Fast retriever (reduced k for speed)
#             self.retriever = self.vectorstore.as_retriever(
#                 search_type="similarity",
#                 search_kwargs={"k": 2}  # Reduced from 3
#             )

#             # Optimized LLM
#             self.llm = ChatGroq(
#                 groq_api_key=os.environ.get("GROQ_API_KEY"),
#                 model_name="llama3-8b-8192",
#                 temperature=0.2,
#                 max_tokens=250,  # Reduced for speed
#                 timeout=8
#             )

#         except Exception as e:
#             logger.error(f"Component initialization failed: {e}")
#             raise

#     def _setup_chains(self):
#         """Setup ultra-optimized chains"""

#         # Minimal contextualizer
#         self.contextualizer_prompt = ChatPromptTemplate.from_messages([
#             ("system", "Rewrite as standalone Jupiter.money query using history. If clear, return unchanged."),
#             MessagesPlaceholder("chat_history"),
#             ("human", "{input}")
#         ])

#         # Focused QA prompt
#         self.qa_prompt = ChatPromptTemplate.from_messages([
#             ("system", (
#                 "You are JupiterBot for Jupiter.money. Give brief, helpful answers (1-2 sentences) using context.\n"
#                 "Focus on: Cards, Jewels, Pots, UPI, KYC, Payments, Account features.\n"
#                 "If unsure, suggest contacting support.\n\n"
#                 "CONTEXT:\n{context}"
#             )),
#             MessagesPlaceholder("chat_history"),
#             ("human", "{input}")
#         ])

#         # Build chains
#         self.history_aware_retriever = create_history_aware_retriever(
#             llm=self.llm, retriever=self.retriever, prompt=self.contextualizer_prompt
#         )

#         self.question_answer_chain = create_stuff_documents_chain(
#             llm=self.llm, prompt=self.qa_prompt
#         )

#         self.rag_chain = create_retrieval_chain(
#             retriever=self.history_aware_retriever,
#             combine_docs_chain=self.question_answer_chain
#         )

#         self.conversational_rag_chain = RunnableWithMessageHistory(
#             self.rag_chain,
#             self._get_session_history,
#             input_messages_key="input",
#             history_messages_key="chat_history",
#             output_messages_key="answer"
#         )

#     def _preload_instant_responses(self):
#         """Preload instant responses for maximum speed"""
#         self.instant_responses = {
#             # Greetings - Ultra fast responses
#             "hi": "Hi! 👋 I'm JupiterBot, your Jupiter.money assistant. How can I help you today?",
#             "hello": "Hello! 😊 I'm here to help with Jupiter.money queries. What do you need?",
#             "hey": "Hey there! 🚀 Ask me anything about Jupiter.money!",
#             "hii": "Hi! 👋 I'm JupiterBot, your Jupiter.money assistant. How can I help you today?",
#             "hlo": "Hello! 😊 I'm here to help with Jupiter.money queries. What do you need?",

#             # Core Jupiter queries
#             "what is jupiter": "Jupiter.money is India's most delightful digital banking app with smart savings (Pots), rewards (Jewels), and a beautiful debit card! 💳✨",
#             "jupiter card activation": "To activate: 1) Open Jupiter app 2) Go to Cards 3) Tap 'Activate Card' 4) Enter last 4 digits 5) Set PIN. Done! 🎉",
#             "jewels": "Jewels are Jupiter's reward points! ✨ Earn on transactions, redeem for cashback & vouchers in the Jewels section!",
#             "pots": "Pots are smart savings goals! 🏺 Create multiple Pots, set auto-save rules, earn better interest rates!",
#             "kyc": "KYC takes 2-3 business days. Upload clear Aadhaar, PAN, and selfie photos. Check status in Profile > KYC Status! 📱",
#             "payment failed": "Try: 1) Check balance 2) Verify details 3) Retry after 30 mins 4) Contact support if needed! 💳",
#             "forgot pin": "Reset PIN: Cards > Change PIN > Authenticate > Set new 4-digit PIN. Active immediately! 🔐",

#             # Quick help
#             "help": "I can help with Jupiter card, Jewels rewards, Pots savings, UPI payments, KYC, bills & more! What do you need? 🌟",
#             "what can you do": "I help with Jupiter card activation, Jewels rewards, Pots savings, UPI payments, KYC verification, bill payments & more! 🚀"
#         }

#     def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
#         """Optimized session management"""
#         with self.cache_lock:
#             if session_id not in self.session_store:
#                 self.session_store[session_id] = ChatMessageHistory()

#             # Keep only recent messages
#             history = self.session_store[session_id]
#             if len(history.messages) > self.MAX_SESSION_MESSAGES:
#                 history.messages = history.messages[-self.MAX_SESSION_MESSAGES:]

#             return history

#     @lru_cache(maxsize=500)
#     def _ultra_fast_scope_check(self, question: str) -> ScopeResult:
#         """Ultra-fast scope validation with multiple checks"""
#         q_lower = question.lower().strip()

#         # 1. Greeting check (always allow)
#         if self.greeting_pattern.search(q_lower):
#             return ScopeResult.GREETING

#         # 2. Explicit out-of-scope check (block immediately)
#         if self.out_of_scope_pattern.search(q_lower):
#             return ScopeResult.OUT_OF_SCOPE

#         # 3. Code/programming check (block)
#         if self.code_pattern.search(q_lower):
#             return ScopeResult.OUT_OF_SCOPE

#         # 4. Jupiter keywords check (allow)
#         if self.jupiter_pattern.search(q_lower):
#             return ScopeResult.IN_SCOPE

#         # 5. Short questions (likely follow-ups, allow)
#         if len(question.split()) <= 4 and len(question) <= 30:
#             return ScopeResult.IN_SCOPE

#         # 6. Question patterns (banking context)
#         question_patterns = ['how', 'what', 'when', 'where', 'why', 'can', 'is', 'do', 'does']
#         if any(q_lower.startswith(p) for p in question_patterns):
#             return ScopeResult.UNCLEAR  # Let it through for context check

#         # 7. Default: be restrictive for unclear queries
#         return ScopeResult.OUT_OF_SCOPE

#     def _sanitize_input(self, text: str) -> str:
#         """Fast input sanitization"""
#         if not text or not isinstance(text, str):
#             return ""

#         # Quick cleanup
#         text = re.sub(r'\s+', ' ', text.strip())
#         text = re.sub(r'[<>{}]', '', text)

#         # Length limit
#         if len(text) > 200:
#             text = text[:200] + "..."

#         return text

#     def _check_instant_cache(self, question: str) -> Optional[str]:
#         """Check instant response cache"""
#         q_lower = question.lower().strip()

#         # Direct match
#         if q_lower in self.instant_responses:
#             self.metrics["instant_hits"] += 1
#             return self.instant_responses[q_lower]

#         # Fuzzy matching for variations
#         for key, response in self.instant_responses.items():
#             if key in q_lower and len(q_lower) < len(key) * 2:
#                 self.metrics["instant_hits"] += 1
#                 return response

#         return None

#     # def _generate_rag_response(self, question: str, session_id: str) -> Dict[str, Any]:
#     #     """Generate RAG response with error handling"""
#     #     try:
#     #         result = self.conversational_rag_chain.invoke(
#     #             {"input": question},
#     #             config={"configurable": {"session_id": session_id}}
#     #         )

#     #         return {
#     #             "answer": result["answer"],
#     #             "sources": [doc.metadata.get("source", "") for doc in result.get("context", [])[:2]],
#     #             "confidence": len(result.get("context", [])),
#     #             "needs_escalation": any(word in result["answer"].lower()
#     #                                  for word in ["support", "contact", "help"])
#     #         }

#     #     except Exception as e:
#     #         logger.error(f"RAG generation error: {e}")
#     #         return {
#     #             "answer": "I'm having technical difficulties. Please contact Jupiter support through the app! 🛠️",
#     #             "sources": [],
#     #             "confidence": 0,
#     #             "needs_escalation": True
#     #         }
#     def _generate_rag_response(self, question: str, session_id: str) -> Dict[str, Any]:
#         """
#         Generate RAG response with error handling.
#         Additionally returns top similar question and list of all similar questions
#         if similarity >= 70%, else returns None, None.
#         """
#         try:
#             # Step 1: Get similar questions from vector DB (not chat history)
#             top_match, similar_questions = self._get_similar_questions_from_vectorstore(question)

#             # Step 2: Generate the RAG response from conversational chain
#             result = self.conversational_rag_chain.invoke(
#                 {"input": question},
#                 config={"configurable": {"session_id": session_id}}
#             )

#             return {
#                 "answer": result["answer"],
#                 "sources": [doc.metadata.get("source", "") for doc in result.get("context", [])[:2]],
#                 "confidence": len(result.get("context", [])),
#                 "needs_escalation": any(word in result["answer"].lower()
#                                         for word in ["support", "contact", "help"]),
#                 "top_similar_question": top_match,
#                 "all_similar_questions": similar_questions
#             }

#         except Exception as e:
#             logger.error(f"RAG generation error: {e}")
#             return {
#                 "answer": "I'm having technical difficulties. Please contact Jupiter support through the app! 🛠️",
#                 "sources": [],
#                 "confidence": 0,
#                 "needs_escalation": True,
#                 "top_similar_question": None,
#                 "all_similar_questions": None
#             }


#         except Exception as e:
#             logger.error(f"RAG generation error: {e}")
#             return {
#                 "answer": "I'm having technical difficulties. Please contact Jupiter support through the app! 🛠️",
#                 "sources": [],
#                 "confidence": 0,
#                 "needs_escalation": True
#             }

#     def query(self, question: str, session_id: str = "default") -> Dict[str, Any]:
#         """
#         Ultra-fast query processing with multi-stage optimization
#         """
#         start_time = time.time()
#         self.metrics["total_queries"] += 1

#         try:
#             # Stage 1: Input validation & sanitization
#             clean_question = self._sanitize_input(question)
#             if not clean_question:
#                 return self._create_response(
#                     "Please ask me something about Jupiter.money! 😊",
#                     start_time, "input_error"
#                 )

#             # Stage 2: Instant response cache (< 1ms)
#             instant_response = self._check_instant_cache(clean_question)
#             if instant_response:
#                 return self._create_response(
#                     instant_response, start_time, "instant_cache",
#                     cache_hit=True, question=clean_question
#                 )

#             # Stage 3: Ultra-fast scope validation (< 2ms)
#             scope_result = self._ultra_fast_scope_check(clean_question)

#             if scope_result == ScopeResult.OUT_OF_SCOPE:
#                 self.metrics["scope_blocks"] += 1
#                 return self._create_response(
#                     "I can only help with Jupiter.money services like cards, Jewels, Pots, payments, and account features. Please ask about Jupiter.money! 🏦",
#                     start_time, "scope_blocked"
#                 )

#             if scope_result == ScopeResult.GREETING:
#                 return self._create_response(
#                     "Hi there! 👋 I'm JupiterBot, your Jupiter.money assistant. What would you like to know about Jupiter today?",
#                     start_time, "greeting"
#                 )

#             # Stage 4: RAG processing (for valid queries)
#             self.metrics["rag_queries"] += 1
#             rag_result = self._generate_rag_response(clean_question, session_id)

#             response_time = time.time() - start_time

#             # Update metrics
#             self._update_metrics(response_time)

#             return {
#                 "question": clean_question,
#                 "answer": rag_result["answer"],
#                 "sources": rag_result["sources"],
#                 "confidence": rag_result["confidence"],
#                 "needs_escalation": rag_result["needs_escalation"],
#                 "session_id": session_id,
#                 "processing_time": response_time,
#                 "stage": "rag_complete",
#                 "status": "success",
#                 "cache_hit": False
#             }

#         except Exception as e:
#             logger.error(f"Query processing error: {e}")
#             return self._create_response(
#                 "I'm experiencing technical issues. Please try again or contact Jupiter support! 🛠️",
#                 start_time, "error", error=str(e)
#             )

#     def _create_response(self, answer: str, start_time: float, stage: str,
#                         cache_hit: bool = False, question: str = "", error: str = "") -> Dict[str, Any]:
#         """Helper to create consistent response format"""
#         processing_time = time.time() - start_time

#         return {
#             "question": question,
#             "answer": answer,
#             "session_id": "default",
#             "processing_time": processing_time,
#             "stage": stage,
#             "status": "error" if error else "success",
#             "cache_hit": cache_hit,
#             "error": error if error else None
#         }

#     def _update_metrics(self, response_time: float):
#         """Update performance metrics"""
#         total = self.metrics["total_queries"]
#         self.metrics["avg_response_time"] = (
#             (self.metrics["avg_response_time"] * (total - 1) + response_time) / total
#         )

#         cache_hits = (self.metrics["instant_hits"] + self.metrics["faq_hits"] +
#                      self.metrics["semantic_hits"])
#         self.metrics["cache_hit_rate"] = (cache_hits / total) * 100 if total > 0 else 0

#     def get_performance_metrics(self) -> Dict[str, Any]:
#         """Get comprehensive performance metrics"""
#         total = max(self.metrics["total_queries"], 1)

#         return {
#             **self.metrics,
#             "instant_hit_rate": (self.metrics["instant_hits"] / total) * 100,
#             "scope_block_rate": (self.metrics["scope_blocks"] / total) * 100,
#             "rag_usage_rate": (self.metrics["rag_queries"] / total) * 100,
#             "avg_response_time_ms": self.metrics["avg_response_time"] * 1000,
#             "active_sessions": len(self.session_store)
#         }

#     def clear_session(self, session_id: str) -> bool:
#         """Clear specific session"""
#         try:
#             if session_id in self.session_store:
#                 del self.session_store[session_id]
#                 return True
#             return False
#         except Exception:
#             return False

#     def warm_up_cache(self, questions: List[str]):
#         """Warm up caches for better performance"""
#         for question in questions:
#             try:
#                 self.query(question, "warmup")
#             except Exception:
#                 continue

# # Global instance management
# _chatbot_instance = None

# def get_ultra_fast_chatbot() -> UltraFastJupiterChatbot:
#     """Get or create ultra-fast chatbot instance"""
#     global _chatbot_instance
#     if _chatbot_instance is None:
#         _chatbot_instance = UltraFastJupiterChatbot()
#     return _chatbot_instance

# def query_jupiter_fast(question: str, session_id: str = "default") -> Dict[str, Any]:
#     """Ultra-fast Jupiter query function"""
#     chatbot = get_ultra_fast_chatbot()
#     return chatbot.query(question, session_id)

# def get_chatbot_metrics() -> Dict[str, Any]:
#     """Get performance metrics"""
#     chatbot = get_ultra_fast_chatbot()
#     return chatbot.get_performance_metrics()

# # Backwards compatibility
# JupiterChatbot = UltraFastJupiterChatbot
# OptimizedJupiterChatbot = UltraFastJupiterChatbot
# def query_jupiter(question: str, session_id: str = "default") -> Dict[str, Any]:
#     """Alias for backwards compatibility"""
#     chatbot = get_ultra_fast_chatbot()
#     return chatbot.query(question, session_id)

# if __name__ == "__main__":
#     # Quick test
#     if "GROQ_API_KEY" not in os.environ:
#         print("❌ Set GROQ_API_KEY environment variable")
#         exit(1)

#     # print("🚀 Testing Ultra-Fast Jupiter Chatbot...\n")
#     # test_queries = [
#     #     "Hi",  # Instant cache
#     #     "What is Jupiter?",  # Instant cache
#     #     "Write Python code for sum",  # Should block
#     #     "Tell me about cricket",  # Should block
#     #     "How do I activate my card?",  # Should process
#     #     "KYC verification process"  # Should process
#     # ]



#     # for i, query in enumerate(test_queries, 1):
#     #     print(f"Test {i}: {query}")
#     #     result = chatbot.query(query)
#     #     print(f"✅ {result['answer'][:80]}...")
#     #     print(f"⚡ {result['processing_time']*1000:.1f}ms | {result['stage']} | Cache: {result.get('cache_hit', False)}\n")

#     # print("📊 Final Metrics:")
#     # metrics = chatbot.get_performance_metrics()
#     # for key, value in metrics.items():
#     #     if isinstance(value, float):
#     #         print(f"  • {key}: {value:.2f}")
#     #     else:
#     #         print(f"  • {key}: {value}")
