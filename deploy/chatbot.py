# import os
# import logging
# import re
# import asyncio
# import time
# from datetime import datetime
# from typing import Dict, List, Optional, Any, Tuple
# from enum import Enum
# from concurrent.futures import ThreadPoolExecutor, as_completed
# from functools import lru_cache
# import hashlib

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

# # Enhanced logging configuration
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('jupiter_chatbot_enhanced.log'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)

# class ValidationResult(Enum):
#     IN_SCOPE = "in_scope"
#     OUT_OF_SCOPE = "out_of_scope"
#     ERROR = "error"

# class LLMType(Enum):
#     VALIDATOR = "validator"
#     CONTEXTUALIZER = "contextualizer"
#     QA_PRIMARY = "qa_primary"
#     QA_SECONDARY = "qa_secondary"
#     SIMILAR_QUESTIONS = "similar_questions"

# class JupiterChatbot:
#     def __init__(self):
#         """Initialize the enhanced Jupiter chatbot with improved performance"""
#         self.embeddings = None
#         self.vectorstore = None
#         self.retrievers = {}
#         self.llms = {}
#         self.session_store = {}
#         self.executor = ThreadPoolExecutor(max_workers=4)

#         # Enhanced caching
#         self.retrieval_cache = {}
#         self.cache_max_size = 1000
#         self.cache_ttl = 3600  # 1 hour

#         # Performance metrics
#         self.metrics = {
#             "total_queries": 0,
#             "out_of_scope_queries": 0,
#             "successful_queries": 0,
#             "error_queries": 0,
#             "greeting_queries": 0,
#             "escalated_queries": 0,
#             "cache_hits": 0,
#             "avg_retrieval_time": 0,
#             "avg_response_time": 0
#         }

#         self._initialize_components()
#         self._setup_enhanced_chains()

#     def _initialize_components(self):
#         """Initialize embeddings, vectorstore, and multiple LLMs"""
#         try:
#             logger.info("🔧 Initializing enhanced chatbot components...")

#             # Initialize optimized embeddings
#             self.embeddings = HuggingFaceEmbeddings(
#                 model_name="sentence-transformers/all-MiniLM-L6-v2",
#                 model_kwargs={"device": "cpu"},
#                 encode_kwargs={"normalize_embeddings": True, "batch_size": 32}
#             )

#             # Initialize vectorstore with optimized settings
#             vectorstore_path = "./jupiter_vectordb_enhanced"
#             self.vectorstore = Chroma(
#                 persist_directory=vectorstore_path,
#                 embedding_function=self.embeddings
#             )

#             # Setup multiple specialized retrievers
#             self._setup_retrievers()

#             # Initialize multiple LLMs for different tasks
#             self._initialize_llms()

#             logger.info("✅ All enhanced components initialized successfully")

#         except Exception as e:
#             logger.error(f"❌ Failed to initialize components: {e}")
#             raise

#     def _setup_retrievers(self):
#         """Setup multiple specialized retrievers for different tasks"""
#         # Primary retriever for main answers
#         self.retrievers['primary'] = self.vectorstore.as_retriever(
#             search_type="mmr",
#             search_kwargs={"k": 6, "fetch_k": 20, "lambda_mult": 0.7}
#         )

#         # Secondary retriever for similar questions
#         self.retrievers['similar'] = self.vectorstore.as_retriever(
#             search_type="similarity_score_threshold",
#             search_kwargs={"k": 5, "score_threshold": 0.75}
#         )

#         # Fast retriever for quick context
#         self.retrievers['fast'] = self.vectorstore.as_retriever(
#             search_type="similarity",
#             search_kwargs={"k": 3}
#         )

#     def _initialize_llms(self):
#         """Initialize multiple LLMs for different tasks"""
#         groq_api_key = os.environ.get("GROQ_API_KEY", "")
#         if not groq_api_key:
#             raise ValueError("GROQ_API_KEY environment variable is not set")

#         # Validator LLM - Ultra fast
#         self.llms[LLMType.VALIDATOR] = ChatGroq(
#             groq_api_key=groq_api_key,
#             model_name="llama3-8b-8192",
#             temperature=0.0,
#             max_tokens=30
#         )

#         # Contextualizer LLM - Fast
#         self.llms[LLMType.CONTEXTUALIZER] = ChatGroq(
#             groq_api_key=groq_api_key,
#             model_name="llama3-8b-8192",
#             temperature=0.1,
#             max_tokens=150
#         )

#         # Primary QA LLM - Balanced
#         self.llms[LLMType.QA_PRIMARY] = ChatGroq(
#             groq_api_key=groq_api_key,
#             model_name="llama3-70b-8192",
#             temperature=0.3,
#             max_tokens=600
#         )

#         # Secondary QA LLM - Backup
#         self.llms[LLMType.QA_SECONDARY] = ChatGroq(
#             groq_api_key=groq_api_key,
#             model_name="llama3-8b-8192",
#             temperature=0.3,
#             max_tokens=500
#         )

#         # Similar Questions LLM - Creative
#         self.llms[LLMType.SIMILAR_QUESTIONS] = ChatGroq(
#             groq_api_key=groq_api_key,
#             model_name="llama3-8b-8192",
#             temperature=0.4,
#             max_tokens=200
#         )

#     def _setup_enhanced_chains(self):
#         """Setup enhanced processing chains with improved prompts"""
#         try:
#             # Enhanced Validator Chain
#             self.validator_prompt = ChatPromptTemplate.from_messages([
#                 ("system", (
#                     "You are a scope validator for JupiterBot. Determine if a user question is about Jupiter.money services.\n\n"
#                     "✅ ALWAYS ALLOW (Jupiter.money related):\n"
#                     "- App features: Pots, Jewels, Cards, UPI, bill payments, transfers\n"
#                     "- Account help: KYC, linking, profiles, statements, troubleshooting\n"
#                     "- Card services: activation, PIN, blocking, limits, transactions\n"
#                     "- General Jupiter inquiries, onboarding, how-to questions\n"
#                     "- Friendly greetings, small talk, 'What can you do?' questions\n\n"
#                     "🚫 BLOCK (Not Jupiter.money related):\n"
#                     "- Other banks/financial services (HDFC, SBI, PayTM, etc.)\n"
#                     "- Investment advice, tax planning, personal finance guidance\n"
#                     "- Unrelated topics: cooking, movies, politics, general knowledge\n\n"
#                     "Respond with exactly ONE word: 'ALLOWED' or 'BLOCKED'"
#                 )),
#                 ("human", "{input}")
#             ])

#             self.validator_chain = self.validator_prompt | self.llms[LLMType.VALIDATOR] | StrOutputParser()

#             # Enhanced Contextualizer Chain
#             self.contextualizer_prompt = ChatPromptTemplate.from_messages([
#                 ("system", (
#                     "You are JupiterBot's conversation contextualizer. Rewrite follow-up questions "
#                     "into clear, standalone queries using chat history.\n\n"
#                     "GUIDELINES:\n"
#                     "- Make questions self-contained and specific\n"
#                     "- Include Jupiter-specific terms (Jewels, Pots, Jupiter card, etc.)\n"
#                     "- Resolve pronouns using chat history\n"
#                     "- If question is clear, return unchanged\n"
#                     "- Maintain user's intent and tone\n\n"
#                     "EXAMPLES:\n"
#                     "User: 'How do I activate it?' (after Jupiter card question)\n"
#                     "Output: 'How do I activate my Jupiter debit card?'\n\n"
#                     "User: 'What about rewards?' (after Jupiter features)\n"
#                     "Output: 'What are Jupiter Jewels rewards and how do they work?'"
#                 )),
#                 MessagesPlaceholder("chat_history"),
#                 ("human", "{input}")
#             ])

#             self.contextualizer_chain = self.contextualizer_prompt | self.llms[LLMType.CONTEXTUALIZER] | StrOutputParser()

#             # Enhanced QA Chain
#             self.qa_prompt = ChatPromptTemplate.from_messages([
#                 ("system", (
#                     "You are JupiterBot, Jupiter.money's AI Assistant — your friendly guide to India's most delightful money app.\n\n"
#                     "🎯 PRIMARY ROLE:\n"
#                     "Provide instant, helpful support for Jupiter.money users with warmth and professionalism.\n\n"
#                     "✅ IN-SCOPE TOPICS:\n"
#                     "• Jupiter App Features: Pots, Jewels, Cards, UPI payments, bill payments, transfers\n"
#                     "• Account Management: KYC, linking, profiles, statements\n"
#                     "• Card Services: activation, PIN reset, blocking, limits\n"
#                     "• Troubleshooting: Login issues, payment failures, app problems\n"
#                     "• Onboarding: Account opening, verification\n"
#                     "• General Inquiries: Features, benefits, how-to guides\n\n"
#                     "📋 RESPONSE GUIDELINES:\n"
#                     "1. TONE: Warm, friendly, professional\n"
#                     "2. LENGTH: 2-3 sentences for simple, 4-5 for complex\n"
#                     "3. STRUCTURE: Clear, actionable steps\n"
#                     "4. LANGUAGE: Simple, jargon-free\n"
#                     "5. BRAND VOICE: Helpful buddy who knows Jupiter\n\n"
#                     "Use provided context to answer accurately. If uncertain, offer escalation.\n\n"
#                     "CONTEXT:\n{context}"
#                 )),
#                 MessagesPlaceholder("chat_history"),
#                 ("human", "{input}")
#             ])

#             # Setup RAG chains with primary and secondary LLMs
#             self._setup_rag_chains()

#             logger.info("✅ Enhanced chains setup successfully")

#         except Exception as e:
#             logger.error(f"❌ Failed to setup enhanced chains: {e}")
#             raise

#     def _setup_rag_chains(self):
#         """Setup RAG chains with multiple LLMs"""
#         # Primary RAG chain
#         self.primary_qa_chain = create_stuff_documents_chain(
#             llm=self.llms[LLMType.QA_PRIMARY],
#             prompt=self.qa_prompt
#         )

#         self.primary_rag_chain = create_retrieval_chain(
#             retriever=self.retrievers['primary'],
#             combine_docs_chain=self.primary_qa_chain
#         )

#         # Secondary RAG chain (backup)
#         self.secondary_qa_chain = create_stuff_documents_chain(
#             llm=self.llms[LLMType.QA_SECONDARY],
#             prompt=self.qa_prompt
#         )

#         self.secondary_rag_chain = create_retrieval_chain(
#             retriever=self.retrievers['fast'],
#             combine_docs_chain=self.secondary_qa_chain
#         )

#         # Setup conversational chains
#         self.primary_conversational_chain = RunnableWithMessageHistory(
#             self.primary_rag_chain,
#             self._get_session_history,
#             input_messages_key="input",
#             history_messages_key="chat_history",
#             output_messages_key="answer"
#         )

#         self.secondary_conversational_chain = RunnableWithMessageHistory(
#             self.secondary_rag_chain,
#             self._get_session_history,
#             input_messages_key="input",
#             history_messages_key="chat_history",
#             output_messages_key="answer"
#         )

#     @lru_cache(maxsize=1000)
#     def _get_cache_key(self, question: str, session_id: str) -> str:
#         """Generate cache key for retrieval results"""
#         return hashlib.md5(f"{question}:{session_id}".encode()).hexdigest()

#     def _get_cached_retrieval(self, cache_key: str) -> Optional[Dict]:
#         """Get cached retrieval results if valid"""
#         if cache_key in self.retrieval_cache:
#             cached_data, timestamp = self.retrieval_cache[cache_key]
#             if time.time() - timestamp < self.cache_ttl:
#                 self.metrics["cache_hits"] += 1
#                 return cached_data
#             else:
#                 del self.retrieval_cache[cache_key]
#         return None

#     def _cache_retrieval(self, cache_key: str, data: Dict):
#         """Cache retrieval results"""
#         if len(self.retrieval_cache) >= self.cache_max_size:
#             # Remove oldest entry
#             oldest_key = min(self.retrieval_cache.keys(),
#                            key=lambda k: self.retrieval_cache[k][1])
#             del self.retrieval_cache[oldest_key]

#         self.retrieval_cache[cache_key] = (data, time.time())

#     def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
#         """Get or create chat history for a session"""
#         if session_id not in self.session_store:
#             self.session_store[session_id] = ChatMessageHistory()
#         return self.session_store[session_id]

#     def _sanitize_input(self, text: str) -> str:
#         """Enhanced input sanitization"""
#         if not text or not isinstance(text, str):
#             return ""

#         text = re.sub(r'\s+', ' ', text.strip())
#         text = re.sub(r'[<>{}]', '', text)

#         max_length = 500
#         if len(text) > max_length:
#             text = text[:max_length] + "..."
#             logger.warning(f"Input truncated to {max_length} characters")

#         return text

#     def _is_greeting_or_casual(self, question: str) -> bool:
#         """Check if question is a greeting or casual interaction"""
#         greeting_patterns = [
#             r'\b(hi|hello|hey|good morning|good afternoon|good evening)\b',
#             r'\bwhat can you do\b',
#             r'\bwho are you\b',
#             r'\bhelp me\b',
#             r'\bhow are you\b',
#             r'\bthanks?\b',
#             r'\bthank you\b'
#         ]

#         question_lower = question.lower()
#         return any(re.search(pattern, question_lower) for pattern in greeting_patterns)

#     def _validate_question(self, question: str) -> ValidationResult:
#         """Enhanced validation with greeting detection"""
#         try:
#             logger.info("🛡️ Validating question scope...")

#             if self._is_greeting_or_casual(question):
#                 logger.info("👋 Detected greeting/casual interaction - allowing")
#                 self.metrics["greeting_queries"] += 1
#                 return ValidationResult.IN_SCOPE

#             result = self.validator_chain.invoke({"input": question})
#             result = result.strip().upper()

#             if "ALLOWED" in result:
#                 logger.info("✅ Question is in scope")
#                 return ValidationResult.IN_SCOPE
#             elif "BLOCKED" in result:
#                 logger.info("🚫 Question is out of scope")
#                 return ValidationResult.OUT_OF_SCOPE
#             else:
#                 logger.warning(f"⚠️ Ambiguous validation result: {result}")
#                 return ValidationResult.IN_SCOPE

#         except Exception as e:
#             logger.error(f"❌ Validation error: {e}")
#             return ValidationResult.ERROR

#     def _contextualize_question(self, question: str, session_id: str) -> str:
#         """Enhanced question contextualization"""
#         try:
#             logger.info("🔄 Contextualizing question...")

#             chat_history = self._get_session_history(session_id).messages
#             if not chat_history or len(chat_history) < 2:
#                 return question

#             result = self.contextualizer_chain.invoke({
#                 "input": question,
#                 "chat_history": chat_history[-10:]
#             })

#             logger.info(f"📝 Contextualized: {result}")
#             return result.strip()

#         except Exception as e:
#             logger.error(f"❌ Contextualization error: {e}")
#             return question

#     def _generate_similar_questions_enhanced(self, question: str) -> List[Dict[str, Any]]:
#         """Generate enhanced similar questions with multiple strategies"""
#         try:
#             similar_questions = []

#             # Strategy 1: Vector similarity search
#             similar_docs = self.vectorstore.similarity_search_with_relevance_scores(
#                 query=question, k=8
#             )

#             for doc, score in similar_docs:
#                 if score >= 0.7:  # Higher threshold for quality
#                     question_text = doc.page_content.strip()
#                     if len(question_text) > 10 and question_text not in [q["question"] for q in similar_questions]:
#                         similar_questions.append({
#                             "question": question_text,
#                             "score": round(score, 3),
#                             "source": "vector_similarity"
#                         })

#             # Strategy 2: Semantic clustering (group by topic)
#             topic_groups = self._group_questions_by_topic(similar_questions)

#             # Strategy 3: LLM-generated related questions
#             llm_questions = self._generate_llm_similar_questions(question)
#             similar_questions.extend(llm_questions)

#             # Sort by relevance and limit to top 3
#             similar_questions = sorted(similar_questions, key=lambda x: x["score"], reverse=True)[:3]

#             return similar_questions

#         except Exception as e:
#             logger.error(f"❌ Error generating similar questions: {e}")
#             return []

#     def _group_questions_by_topic(self, questions: List[Dict]) -> Dict[str, List[Dict]]:
#         """Group questions by topic for better diversity"""
#         topics = {
#             "cards": ["card", "debit", "credit", "pin", "block", "activate"],
#             "payments": ["payment", "upi", "transfer", "bill", "pay"],
#             "account": ["account", "kyc", "profile", "statement", "balance"],
#             "features": ["pots", "jewels", "rewards", "savings", "features"],
#             "troubleshooting": ["error", "problem", "issue", "not working", "failed"]
#         }

#         grouped = {topic: [] for topic in topics}

#         for question in questions:
#             question_text = question["question"].lower()
#             for topic, keywords in topics.items():
#                 if any(keyword in question_text for keyword in keywords):
#                     grouped[topic].append(question)
#                     break

#         return grouped

#     def _generate_llm_similar_questions(self, question: str) -> List[Dict[str, Any]]:
#         """Generate similar questions using LLM"""
#         try:
#             prompt = f"""Based on this Jupiter.money question: "{question}"

# Generate 2 related questions that Jupiter.money users might also ask.
# Focus on the same topic but different aspects.

# Format: Just list the questions, one per line.
# Example:
# How do I activate my Jupiter card?
# What are the benefits of Jupiter Jewels?"""

#             result = self.llms[LLMType.SIMILAR_QUESTIONS].invoke([
#                 {"role": "system", "content": "You are a helpful assistant generating related questions for Jupiter.money users."},
#                 {"role": "user", "content": prompt}
#             ])

#             generated_questions = []
#             for line in result.content.strip().split('\n'):
#                 line = line.strip()
#                 if line and '?' in line:
#                     generated_questions.append({
#                         "question": line,
#                         "score": 0.8,  # High score for LLM generated
#                         "source": "llm_generated"
#                     })

#             return generated_questions[:2]  # Limit to 2

#         except Exception as e:
#             logger.error(f"❌ Error generating LLM questions: {e}")
#             return []

#     def _parallel_answer_generation(self, question: str, session_id: str) -> Dict[str, Any]:
#         """Generate answer and similar questions in parallel"""
#         try:
#             logger.info("🧠 Generating answer with parallel processing...")

#             # Submit parallel tasks
#             future_answer = self.executor.submit(self._generate_primary_answer, question, session_id)
#             future_similar = self.executor.submit(self._generate_similar_questions_enhanced, question)

#             # Collect results with timeout
#             try:
#                 answer_result = future_answer.result(timeout=10)
#                 similar_questions = future_similar.result(timeout=5)
#             except Exception as e:
#                 logger.warning(f"⚠️ Parallel processing timeout, falling back to secondary: {e}")
#                 # Fallback to secondary LLM
#                 answer_result = self._generate_secondary_answer(question, session_id)
#                 similar_questions = []

#             answer_result["similar_questions"] = similar_questions
#             return answer_result

#         except Exception as e:
#             logger.error(f"❌ Parallel answer generation error: {e}")
#             return self._generate_fallback_answer()

#     def _generate_primary_answer(self, question: str, session_id: str) -> Dict[str, Any]:
#         """Generate answer using primary LLM"""
#         try:
#             result = self.primary_conversational_chain.invoke(
#                 {"input": question},
#                 config={"configurable": {"session_id": session_id}}
#             )

#             return self._process_answer_result(result)

#         except Exception as e:
#             logger.error(f"❌ Primary answer generation failed: {e}")
#             raise

#     def _generate_secondary_answer(self, question: str, session_id: str) -> Dict[str, Any]:
#         """Generate answer using secondary LLM"""
#         try:
#             result = self.secondary_conversational_chain.invoke(
#                 {"input": question},
#                 config={"configurable": {"session_id": session_id}}
#             )

#             return self._process_answer_result(result)

#         except Exception as e:
#             logger.error(f"❌ Secondary answer generation failed: {e}")
#             return self._generate_fallback_answer()

#     def _process_answer_result(self, result: Dict) -> Dict[str, Any]:
#         """Process and format answer result"""
#         source_docs = result.get("context", [])
#         sources = []
#         for doc in source_docs:
#             source = doc.metadata.get("source", "Unknown")
#             if source != "Unknown":
#                 sources.append(source)

#         answer_text = result["answer"].lower()
#         needs_escalation = any(keyword in answer_text for keyword in [
#             "not sure", "uncertain", "don't know", "can't help",
#             "contact support", "escalate", "technical team"
#         ])

#         if needs_escalation:
#             self.metrics["escalated_queries"] += 1

#         return {
#             "answer": result["answer"],
#             "sources": list(set(sources)),
#             "confidence": len(source_docs),
#             "needs_escalation": needs_escalation
#         }

#     def _generate_fallback_answer(self) -> Dict[str, Any]:
#         """Generate fallback answer for errors"""
#         return {
#             "answer": "I'm experiencing technical difficulties right now. Please try again in a moment, or you can reach out to our support team through the Jupiter app for immediate assistance! 😊",
#             "sources": [],
#             "confidence": 0,
#             "needs_escalation": True
#         }

#     def query(self, question: str, session_id: str = "default") -> Dict[str, Any]:
#         """
#         Enhanced main query method with:
#         - Faster retrieval with caching
#         - Parallel processing
#         - Multiple LLMs
#         - Enhanced similar questions
#         - Comprehensive error handling
#         """
#         start_time = time.time()
#         self.metrics["total_queries"] += 1

#         try:
#             logger.info(f"💬 New query received: '{question}' | Session: {session_id}")

#             # 1. Input Sanitization
#             sanitized_question = self._sanitize_input(question)
#             if not sanitized_question:
#                 return self._create_error_response("input_validation", start_time, session_id, question)

#             # 2. Check cache first
#             cache_key = self._get_cache_key(sanitized_question, session_id)
#             cached_result = self._get_cached_retrieval(cache_key)
#             if cached_result:
#                 logger.info("🎯 Cache hit - returning cached result")
#                 cached_result["processing_time"] = time.time() - start_time
#                 return cached_result

#             # 3. Scope Validation
#             validation_result = self._validate_question(sanitized_question)
#             if validation_result == ValidationResult.OUT_OF_SCOPE:
#                 self.metrics["out_of_scope_queries"] += 1
#                 return self._create_out_of_scope_response(start_time, session_id, sanitized_question)
#             elif validation_result == ValidationResult.ERROR:
#                 self.metrics["error_queries"] += 1
#                 return self._create_validation_error_response(start_time, session_id, sanitized_question)

#             # 4. Contextualization
#             contextualized_question = self._contextualize_question(sanitized_question, session_id)

#             # 5. Parallel Answer Generation + Similar Questions
#             answer_result = self._parallel_answer_generation(contextualized_question, session_id)
#             processing_time = time.time() - start_time

#             # Update metrics
#             self.metrics["successful_queries"] += 1
#             self._update_performance_metrics(processing_time)

#             # 6. Prepare final response
#             final_response = {
#                 "question": sanitized_question,
#                 "contextualized_question": contextualized_question,
#                 "answer": answer_result["answer"],
#                 "sources": answer_result.get("sources", []),
#                 "confidence": answer_result.get("confidence", 0),
#                 "needs_escalation": answer_result.get("needs_escalation", False),
#                 "similar_questions": answer_result.get("similar_questions", []),
#                 "session_id": session_id,
#                 "processing_time": processing_time,
#                 "stage": "complete",
#                 "status": "success"
#             }

#             # 7. Cache the result
#             self._cache_retrieval(cache_key, final_response)

#             return final_response

#         except Exception as e:
#             self.metrics["error_queries"] += 1
#             logger.error(f"❌ Unexpected error during query: {e}")
#             return self._create_unexpected_error_response(e, start_time, session_id, question)

#     def _create_error_response(self, stage: str, start_time: float, session_id: str, question: str) -> Dict[str, Any]:
#         """Create standardized error response"""
#         return {
#             "answer": "I'd love to help! Could you please ask me a question about Jupiter.money? 😊",
#             "session_id": session_id,
#             "processing_time": time.time() - start_time,
#             "stage": stage,
#             "status": "error",
#             "confidence": 0,
#             "needs_escalation": False,
#             "similar_questions": [],
#             "sources": [],
#             "question": question,
#             "contextualized_question": question
#         }

#     def _create_out_of_scope_response(self, start_time: float, session_id: str, question: str) -> Dict[str, Any]:
#         """Create out of scope response"""
#         return {
#             "answer": "Hi there! 👋 I can only help with questions about Jupiter.money services, features, and your account. What would you like to know about Jupiter today?",
#             "session_id": session_id,
#             "processing_time": time.time() - start_time,
#             "stage": "validation",
#             "status": "out_of_scope",
#             "confidence": 0,
#             "needs_escalation": False,
#             "similar_questions": [],
#             "sources": [],
#             "question": question,
#             "contextualized_question": question
#         }

#     def _create_validation_error_response(self, start_time: float, session_id: str, question: str) -> Dict[str, Any]:
#         """Create validation error response"""
#         return {
#             "answer": "I'm having a small technical hiccup. Could you try rephrasing your question? I'm here to help with anything Jupiter.money related! 😊",
#             "session_id": session_id,
#             "processing_time": time.time() - start_time,
#             "stage": "validation",
#             "status": "error",
#             "confidence": 0,
#             "needs_escalation": True,
#             "similar_questions": [],
#             "sources": [],
#             "question": question,
#             "contextualized_question": question
#         }

#     def _create_unexpected_error_response(self, error: Exception, start_time: float, session_id: str, question: str) -> Dict[str, Any]:
#         """Create unexpected error response"""
#         return {
#             "answer": "Oops! I'm experiencing some technical difficulties. Please try again in a moment, or reach out to our support team through the Jupiter app for immediate help! 🛠️",
#             "session_id": session_id,
#             "processing_time": time.time() - start_time,
#             "stage": "error",
#             "status": "error",
#             "error": str(error),
#             "confidence": 0,
#             "needs_escalation": True,
#             "similar_questions": [],
#             "sources": [],
#             "question": question,
#             "contextualized_question": question
#         }

#     def _update_performance_metrics(self, processing_time: float):
#         """Update performance metrics"""
#         # Update average response time
#         total_successful = self.metrics["successful_queries"]
#         current_avg = self.metrics["avg_response_time"]
#         self.metrics["avg_response_time"] = ((current_avg * (total_successful - 1)) + processing_time) / total_successful

#     def get_enhanced_metrics(self) -> Dict[str, Any]:
#         """Get enhanced chatbot performance metrics"""
#         total = max(self.metrics["total_queries"], 1)
#         return {
#             **self.metrics,
#             "success_rate": (self.metrics["successful_queries"] / total) * 100,
#             "out_of_scope_rate": (self.metrics["out_of_scope_queries"] / total) * 100,
#             "greeting_rate": (self.metrics["greeting_queries"] / total) * 100,
#             "escalation_rate": (self.metrics["escalated_queries"] / total) * 100,
#             "error_rate": (self.metrics["error_queries"] / total) * 100,
#             "cache_hit_rate": (self.metrics["cache_hits"] / total) * 100 if total > 0 else 0
#         }

#     def clear_session(self, session_id: str) -> bool:
#         """Clear chat history for a specific session"""
#         try:
#             if session_id in self.session_store:
#                 del self.session_store[session_id]
#                 logger.info(f"🗑️ Cleared session: {session_id}")
#                 return True
#             return False
#         except Exception as e:
#             logger.error(f"❌ Error clearing session {session_id}: {e}")
#             return False

#     def clear_cache(self) -> bool:
#         """Clear retrieval cache"""
#         try:
#             self.retrieval_cache.clear()
#             logger.info("🗑️ Cleared retrieval cache")
#             return True
#         except Exception as e:
#             logger.error(f"❌ Error clearing cache: {e}")
#             return False

#     def get_active_sessions(self) -> List[str]:
#         """Get list of active session IDs"""
#         return list(self.session_store.keys())

#     def get_cache_stats(self) -> Dict[str, Any]:
#         """Get cache statistics"""
#         return {
#             "cache_size": len(self.retrieval_cache),
#             "cache_max_size": self.cache_max_size,
#             "cache_ttl": self.cache_ttl,
#             "cache_hits": self.metrics["cache_hits"]
#         }

# # --- Enhanced Convenience Functions ---

# _chatbot_instance = None

# def get_chatbot() -> JupiterChatbot:
#     """Get or create global chatbot instance"""
#     global _chatbot_instance
#     if _chatbot_instance is None:
#         _chatbot_instance = JupiterChatbot()
#     return _chatbot_instance

# def query_jupiter(question: str, session_id: str = "default") -> Dict[str, Any]:
#     """Enhanced convenience function for querying Jupiter chatbot"""
#     chatbot = get_chatbot()
#     return chatbot.query(question, session_id)

# def clear_chat_session(session_id: str = "default") -> bool:
#     """Clear chat history for a session"""
#     chatbot = get_chatbot()
#     return chatbot.clear_session(session_id)

# def get_chatbot_metrics() -> Dict[str, Any]:
#     """Get enhanced chatbot performance metrics"""
#     chatbot = get_chatbot()
#     return chatbot.get_enhanced_metrics()

# def clear_chatbot_cache() -> bool:
#     """Clear chatbot retrieval cache"""
#     chatbot = get_chatbot()
#     return chatbot.clear_cache()

# # --- Enhanced Test Runner ---
# def main():
#     """Test the enhanced chatbot with comprehensive scenarios"""
#     if "GROQ_API_KEY" not in os.environ:
#         print("❌ GROQ_API_KEY environment variable is not set")
#         return

#     print("🚀 Initializing Enhanced Jupiter RAG Chatbot v3.0...\n")

#     # try:
#     #     chatbot = JupiterChatbot()

#     #     # Test scenarios
#     #     test_questions = [
#     #         "Hi there! How are you?",
#     #         "How do I activate my Jupiter card?",
#     #         "What are Jupiter Jewels?",
#     #         "How do I transfer money?",
#     #         "Tell me about Pots feature",
#     #         "I'm having trouble with UPI payments"
#     #     ]

#     #     print("🧪 Testing enhanced chatbot...\n")

#     #     for i, question in enumerate(test_questions, 1):
#     #         print(f"{'='*50}")
#     #         print(f"TEST {i}: {question}")
#     #         print(f"{'='*50}")

#     #         start_time = time.time()
#     #         response = chatbot.query(question, f"test_session_{i}")
#     #         end_time = time.time()
#     #         print(response)
#     #         break
#     #         print(f"💬 Answer: {response['answer']}")
#     #         print(f"⏱️  Processing Time: {response['processing_time']:.2f}s")
#     #         print(f"🎯 Confidence: {response['confidence']}")
#     #         print(f"📊 Status: {response['status']}")

#     #         if response.get('similar_questions'):
#     #             print(f"🔗 Similar Questions:")
#     #             for sq in response['similar_questions']:
#     #                 print(f"   • {sq['question']} (Score: {sq['score']})")

#     #         print()

#     #     # # Show metrics
#     #     # print("📈 PERFORMANCE METRICS:")
#     #     # print("="*50)
#     #     # metrics = chatbot.get_enhanced_metrics()
#     #     # for key, value in metrics.items():
#     #     #     if isinstance(value, float):
#     #     #         print(f"{key}: {value:.2f}")
#     #     #     else:
#     #     #         print(f"{key}: {value}")

#     #     # print("\n✅ Enhanced chatbot testing completed!")

#     # except Exception as e:
#     #     print(f"❌ Error during testing: {e}")

# if __name__ == "__main__":
#     main()



import os
import logging
import re
import asyncio
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import hashlib

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

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jupiter_chatbot_enhanced.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ValidationResult(Enum):
    IN_SCOPE = "in_scope"
    OUT_OF_SCOPE = "out_of_scope"
    ERROR = "error"

class LLMType(Enum):
    VALIDATOR = "validator"
    CONTEXTUALIZER = "contextualizer"
    QA_PRIMARY = "qa_primary"
    QA_SECONDARY = "qa_secondary"
    SIMILAR_QUESTIONS = "similar_questions"

# Global embedding model instance to prevent multiple downloads
_embedding_model = None

def get_embedding_model():
    """Get or create global embedding model instance"""
    global _embedding_model
    if _embedding_model is None:
        logger.info("🔄 Loading embedding model (one-time download)...")
        _embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True, "batch_size": 32},
            cache_folder="./embedding_cache"  # Cache locally to avoid re-downloads
        )
        logger.info("✅ Embedding model loaded successfully")
    return _embedding_model

class JupiterChatbot:
    def __init__(self):
        """Initialize the enhanced Jupiter chatbot with improved performance"""
        self.embeddings = None
        self.vectorstore = None
        self.retrievers = {}
        self.llms = {}
        self.session_store = {}
        self.executor = ThreadPoolExecutor(max_workers=4)

        # Enhanced caching
        self.retrieval_cache = {}
        self.cache_max_size = 1000
        self.cache_ttl = 3600  # 1 hour

        # Performance metrics
        self.metrics = {
            "total_queries": 0,
            "out_of_scope_queries": 0,
            "successful_queries": 0,
            "error_queries": 0,
            "greeting_queries": 0,
            "escalated_queries": 0,
            "cache_hits": 0,
            "avg_retrieval_time": 0,
            "avg_response_time": 0
        }

        self._initialize_components()
        self._setup_enhanced_chains()

    def _initialize_components(self):
        """Initialize embeddings, vectorstore, and multiple LLMs"""
        try:
            logger.info("🔧 Initializing enhanced chatbot components...")

            # Use global embedding model to prevent multiple downloads
            self.embeddings = get_embedding_model()

            # Initialize vectorstore wit
            # settings
            vectorstore_path = "./jupiter_vectordb_enhanced"
            self.vectorstore = Chroma(
                persist_directory=vectorstore_path,
                embedding_function=self.embeddings
            )

            # Setup multiple specialized retrievers
            self._setup_retrievers()

            # Initialize multiple LLMs for different tasks
            self._initialize_llms()

            logger.info("✅ All enhanced components initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize components: {e}")
            raise

    def _setup_retrievers(self):
        """Setup multiple specialized retrievers for different tasks"""
        # Primary retriever for main answers
        self.retrievers['primary'] = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 6, "fetch_k": 20, "lambda_mult": 0.7}
        )

        # Secondary retriever for similar questions
        self.retrievers['similar'] = self.vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 5, "score_threshold": 0.75}
        )

        # Fast retriever for quick context
        self.retrievers['fast'] = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )

    def _initialize_llms(self):
        """Initialize multiple LLMs for different tasks"""
        groq_api_key = os.environ.get("GROQ_API_KEY", "")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")

        # Validator LLM - Ultra fast
        self.llms[LLMType.VALIDATOR] = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama3-8b-8192",
            temperature=0.0,
            max_tokens=30
        )

        # Contextualizer LLM - Fast
        self.llms[LLMType.CONTEXTUALIZER] = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama3-8b-8192",
            temperature=0.1,
            max_tokens=150
        )

        # Primary QA LLM - Balanced
        self.llms[LLMType.QA_PRIMARY] = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama3-70b-8192",
            temperature=0.3,
            max_tokens=600
        )

        # Secondary QA LLM - Backup
        self.llms[LLMType.QA_SECONDARY] = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama3-8b-8192",
            temperature=0.3,
            max_tokens=500
        )

        # Similar Questions LLM - Creative
        self.llms[LLMType.SIMILAR_QUESTIONS] = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama3-8b-8192",
            temperature=0.4,
            max_tokens=200
        )

    def _setup_enhanced_chains(self):
        """Setup enhanced processing chains with improved prompts"""
        try:
            # Enhanced Validator Chain
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
                    "Respond with exactly ONE word: 'ALLOWED' or 'BLOCKED'"
                )),
                ("human", "{input}")
            ])

            self.validator_chain = self.validator_prompt | self.llms[LLMType.VALIDATOR] | StrOutputParser()

            # Enhanced Contextualizer Chain
            self.contextualizer_prompt = ChatPromptTemplate.from_messages([
                ("system", (
                    "You are JupiterBot's conversation contextualizer. Rewrite follow-up questions "
                    "into clear, standalone queries using chat history.\n\n"
                    "GUIDELINES:\n"
                    "- Make questions self-contained and specific\n"
                    "- Include Jupiter-specific terms (Jewels, Pots, Jupiter card, etc.)\n"
                    "- Resolve pronouns using chat history\n"
                    "- If question is clear, return unchanged\n"
                    "- Maintain user's intent and tone\n\n"
                    "EXAMPLES:\n"
                    "User: 'How do I activate it?' (after Jupiter card question)\n"
                    "Output: 'How do I activate my Jupiter debit card?'\n\n"
                    "User: 'What about rewards?' (after Jupiter features)\n"
                    "Output: 'What are Jupiter Jewels rewards and how do they work?'"
                )),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ])

            self.contextualizer_chain = self.contextualizer_prompt | self.llms[LLMType.CONTEXTUALIZER] | StrOutputParser()

            # Enhanced QA Chain
            self.qa_prompt = ChatPromptTemplate.from_messages([
                ("system", (
                    "You are JupiterBot, Jupiter.money's AI Assistant — your friendly guide to India's most delightful money app.\n\n"
                    "🎯 PRIMARY ROLE:\n"
                    "Provide instant, helpful support for Jupiter.money users with warmth and professionalism.\n\n"
                    "✅ IN-SCOPE TOPICS:\n"
                    "• Jupiter App Features: Pots, Jewels, Cards, UPI payments, bill payments, transfers\n"
                    "• Account Management: KYC, linking, profiles, statements\n"
                    "• Card Services: activation, PIN reset, blocking, limits\n"
                    "• Troubleshooting: Login issues, payment failures, app problems\n"
                    "• Onboarding: Account opening, verification\n"
                    "• General Inquiries: Features, benefits, how-to guides\n\n"
                    "📋 RESPONSE GUIDELINES:\n"
                    "1. TONE: Warm, friendly, professional\n"
                    "2. LENGTH: 2-3 sentences for simple, 4-5 for complex\n"
                    "3. STRUCTURE: Clear, actionable steps\n"
                    "4. LANGUAGE: Simple, jargon-free\n"
                    "5. BRAND VOICE: Helpful buddy who knows Jupiter\n\n"
                    "Use provided context to answer accurately. If uncertain, offer escalation.\n\n"
                    "CONTEXT:\n{context}"
                )),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ])

            # Setup RAG chains with primary and secondary LLMs
            self._setup_rag_chains()

            logger.info("✅ Enhanced chains setup successfully")

        except Exception as e:
            logger.error(f"❌ Failed to setup enhanced chains: {e}")
            raise

    def _setup_rag_chains(self):
        """Setup RAG chains with multiple LLMs"""
        # Primary RAG chain
        self.primary_qa_chain = create_stuff_documents_chain(
            llm=self.llms[LLMType.QA_PRIMARY],
            prompt=self.qa_prompt
        )

        self.primary_rag_chain = create_retrieval_chain(
            retriever=self.retrievers['primary'],
            combine_docs_chain=self.primary_qa_chain
        )

        # Secondary RAG chain (backup)
        self.secondary_qa_chain = create_stuff_documents_chain(
            llm=self.llms[LLMType.QA_SECONDARY],
            prompt=self.qa_prompt
        )

        self.secondary_rag_chain = create_retrieval_chain(
            retriever=self.retrievers['fast'],
            combine_docs_chain=self.secondary_qa_chain
        )

        # Setup conversational chains
        self.primary_conversational_chain = RunnableWithMessageHistory(
            self.primary_rag_chain,
            self._get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

        self.secondary_conversational_chain = RunnableWithMessageHistory(
            self.secondary_rag_chain,
            self._get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

    @lru_cache(maxsize=1000)
    def _get_cache_key(self, question: str, session_id: str) -> str:
        """Generate cache key for retrieval results"""
        return hashlib.md5(f"{question}:{session_id}".encode()).hexdigest()

    def _get_cached_retrieval(self, cache_key: str) -> Optional[Dict]:
        """Get cached retrieval results if valid"""
        if cache_key in self.retrieval_cache:
            cached_data, timestamp = self.retrieval_cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                self.metrics["cache_hits"] += 1
                return cached_data
            else:
                del self.retrieval_cache[cache_key]
        return None

    def _cache_retrieval(self, cache_key: str, data: Dict):
        """Cache retrieval results"""
        if len(self.retrieval_cache) >= self.cache_max_size:
            # Remove oldest entry
            oldest_key = min(self.retrieval_cache.keys(),
                        key=lambda k: self.retrieval_cache[k][1])
            del self.retrieval_cache[oldest_key]

        self.retrieval_cache[cache_key] = (data, time.time())

    def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Get or create chat history for a session"""
        if session_id not in self.session_store:
            self.session_store[session_id] = ChatMessageHistory()
        return self.session_store[session_id]

    def _sanitize_input(self, text: str) -> str:
        """Enhanced input sanitization"""
        if not text or not isinstance(text, str):
            return ""

        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'[<>{}]', '', text)

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
            logger.info("🛡️ Validating question scope...")

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
                return ValidationResult.IN_SCOPE

        except Exception as e:
            logger.error(f"❌ Validation error: {e}")
            return ValidationResult.ERROR

    def _contextualize_question(self, question: str, session_id: str) -> str:
        """Enhanced question contextualization"""
        try:
            logger.info("🔄 Contextualizing question...")

            chat_history = self._get_session_history(session_id).messages
            if not chat_history or len(chat_history) < 2:
                return question

            result = self.contextualizer_chain.invoke({
                "input": question,
                "chat_history": chat_history[-10:]
            })

            logger.info(f"📝 Contextualized: {result}")
            return result.strip()

        except Exception as e:
            logger.error(f"❌ Contextualization error: {e}")
            return question

    def _generate_similar_questions_enhanced(self, question: str, retrieved_docs: List = None) -> List[Dict[str, Any]]:
        """
        Generate enhanced similar questions using already retrieved documents
        NO ADDITIONAL RETRIEVAL - Uses docs from main answer generation
        """
        try:
            similar_questions = []

            # Strategy 1: Use already retrieved documents (NO ADDITIONAL RETRIEVAL)
            if retrieved_docs:
                logger.info("📋 Using already retrieved documents for similar questions")
                for doc in retrieved_docs[:5]:  # Use first 5 docs
                    question_text = doc.page_content.strip()
                    if len(question_text) > 10 and question_text not in [q["question"] for q in similar_questions]:
                        # Calculate simple similarity score based on document relevance
                        score = 0.8  # Default high score since these are already relevant
                        similar_questions.append({
                            "question": question_text,
                            "score": score,
                            "source": "retrieved_docs"
                        })

            # Strategy 2: LLM-generated related questions (NO RETRIEVAL)
            llm_questions = self._generate_llm_similar_questions(question)
            similar_questions.extend(llm_questions)

            # Sort by relevance and limit to top 3
            similar_questions = sorted(similar_questions, key=lambda x: x["score"], reverse=True)[:3]

            return similar_questions

        except Exception as e:
            logger.error(f"❌ Error generating similar questions: {e}")
            return []

    def _generate_llm_similar_questions(self, question: str) -> List[Dict[str, Any]]:
        """Generate similar questions using LLM"""
        try:
            prompt = f"""Based on this Jupiter.money question: "{question}"

Generate 2 related questions that Jupiter.money users might also ask.
Focus on the same topic but different aspects.

Format: Just list the questions, one per line.
Example:
How do I activate my Jupiter card?
What are the benefits of Jupiter Jewels?"""

            result = self.llms[LLMType.SIMILAR_QUESTIONS].invoke([
                {"role": "system", "content": "You are a helpful assistant generating related questions for Jupiter.money users."},
                {"role": "user", "content": prompt}
            ])

            generated_questions = []
            for line in result.content.strip().split('\n'):
                line = line.strip()
                if line and '?' in line:
                    generated_questions.append({
                        "question": line,
                        "score": 0.8,  # High score for LLM generated
                        "source": "llm_generated"
                    })

            return generated_questions[:2]  # Limit to 2

        except Exception as e:
            logger.error(f"❌ Error generating LLM questions: {e}")
            return []

    def _parallel_answer_generation(self, question: str, session_id: str) -> Dict[str, Any]:
        """
        Generate answer and similar questions in parallel
        OPTIMIZED: Similar questions now use retrieved docs from main answer (NO SECOND RETRIEVAL)
        """
        try:
            logger.info("🧠 Generating answer with optimized parallel processing...")

            # Submit main answer task
            future_answer = self.executor.submit(self._generate_primary_answer, question, session_id)

            # Get answer result with timeout
            try:
                answer_result = future_answer.result(timeout=10)

                # Generate similar questions using already retrieved documents
                retrieved_docs = answer_result.get("retrieved_docs", [])
                similar_questions = self._generate_similar_questions_enhanced(question, retrieved_docs)

            except Exception as e:
                logger.warning(f"⚠️ Primary processing timeout, falling back to secondary: {e}")
                # Fallback to secondary LLM
                answer_result = self._generate_secondary_answer(question, session_id)
                retrieved_docs = answer_result.get("retrieved_docs", [])
                similar_questions = self._generate_similar_questions_enhanced(question, retrieved_docs)

            answer_result["similar_questions"] = similar_questions
            return answer_result

        except Exception as e:
            logger.error(f"❌ Parallel answer generation error: {e}")
            return self._generate_fallback_answer()

    def _generate_primary_answer(self, question: str, session_id: str) -> Dict[str, Any]:
        """Generate answer using primary LLM"""
        try:
            result = self.primary_conversational_chain.invoke(
                {"input": question},
                config={"configurable": {"session_id": session_id}}
            )

            return self._process_answer_result(result)

        except Exception as e:
            logger.error(f"❌ Primary answer generation failed: {e}")
            raise

    def _generate_secondary_answer(self, question: str, session_id: str) -> Dict[str, Any]:
        """Generate answer using secondary LLM"""
        try:
            result = self.secondary_conversational_chain.invoke(
                {"input": question},
                config={"configurable": {"session_id": session_id}}
            )

            return self._process_answer_result(result)

        except Exception as e:
            logger.error(f"❌ Secondary answer generation failed: {e}")
            return self._generate_fallback_answer()

    def _process_answer_result(self, result: Dict) -> Dict[str, Any]:
        """Process and format answer result"""
        source_docs = result.get("context", [])
        sources = []
        for doc in source_docs:
            source = doc.metadata.get("source", "Unknown")
            if source != "Unknown":
                sources.append(source)

        answer_text = result["answer"].lower()
        needs_escalation = any(keyword in answer_text for keyword in [
            "not sure", "uncertain", "don't know", "can't help",
            "contact support", "escalate", "technical team"
        ])

        if needs_escalation:
            self.metrics["escalated_queries"] += 1

        return {
            "answer": result["answer"],
            "sources": list(set(sources)),
            "confidence": len(source_docs),
            "needs_escalation": needs_escalation,
            "retrieved_docs": source_docs  # Include retrieved docs for similar questions
        }

    def _generate_fallback_answer(self) -> Dict[str, Any]:
        """Generate fallback answer for errors"""
        return {
            "answer": "I'm experiencing technical difficulties right now. Please try again in a moment, or you can reach out to our support team through the Jupiter app for immediate assistance! 😊",
            "sources": [],
            "confidence": 0,
            "needs_escalation": True,
            "retrieved_docs": []
        }

    def query(self, question: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Enhanced main query method with:
        - Faster retrieval with caching
        - Parallel processing
        - Multiple LLMs
        - OPTIMIZED: Single retrieval for both answer and similar questions
        - Comprehensive error handling
        """
        start_time = time.time()
        self.metrics["total_queries"] += 1

        try:
            logger.info(f"💬 New query received: '{question}' | Session: {session_id}")

            # 1. Input Sanitization
            sanitized_question = self._sanitize_input(question)
            if not sanitized_question:
                return self._create_error_response("input_validation", start_time, session_id, question)

            # 2. Check cache first
            cache_key = self._get_cache_key(sanitized_question, session_id)
            cached_result = self._get_cached_retrieval(cache_key)
            if cached_result:
                logger.info("🎯 Cache hit - returning cached result")
                cached_result["processing_time"] = time.time() - start_time
                return cached_result

            # 3. Scope Validation
            validation_result = self._validate_question(sanitized_question)
            if validation_result == ValidationResult.OUT_OF_SCOPE:
                self.metrics["out_of_scope_queries"] += 1
                return self._create_out_of_scope_response(start_time, session_id, sanitized_question)
            elif validation_result == ValidationResult.ERROR:
                self.metrics["error_queries"] += 1
                return self._create_validation_error_response(start_time, session_id, sanitized_question)

            # 4. Contextualization
            contextualized_question = self._contextualize_question(sanitized_question, session_id)

            # 5. OPTIMIZED: Single retrieval for both answer and similar questions
            answer_result = self._parallel_answer_generation(contextualized_question, session_id)
            processing_time = time.time() - start_time

            # Update metrics
            self.metrics["successful_queries"] += 1
            self._update_performance_metrics(processing_time)

            # 6. Prepare final response
            final_response = {
                "question": sanitized_question,
                "contextualized_question": contextualized_question,
                "answer": answer_result["answer"],
                "sources": answer_result.get("sources", []),
                "confidence": answer_result.get("confidence", 0),
                "needs_escalation": answer_result.get("needs_escalation", False),
                "similar_questions": answer_result.get("similar_questions", []),
                "session_id": session_id,
                "processing_time": processing_time,
                "stage": "complete",
                "status": "success"
            }

            # 7. Cache the result
            self._cache_retrieval(cache_key, final_response)

            return final_response

        except Exception as e:
            self.metrics["error_queries"] += 1
            logger.error(f"❌ Unexpected error during query: {e}")
            return self._create_unexpected_error_response(e, start_time, session_id, question)

    def _create_error_response(self, stage: str, start_time: float, session_id: str, question: str) -> Dict[str, Any]:
        """Create standardized error response"""
        return {
            "answer": "I'd love to help! Could you please ask me a question about Jupiter.money? 😊",
            "session_id": session_id,
            "processing_time": time.time() - start_time,
            "stage": stage,
            "status": "error",
            "confidence": 0,
            "needs_escalation": False,
            "similar_questions": [],
            "sources": [],
            "question": question,
            "contextualized_question": question
        }

    def _create_out_of_scope_response(self, start_time: float, session_id: str, question: str) -> Dict[str, Any]:
        """Create out of scope response"""
        return {
            "answer": "Hi there! 👋 I can only help with questions about Jupiter.money services, features, and your account. What would you like to know about Jupiter today?",
            "session_id": session_id,
            "processing_time": time.time() - start_time,
            "stage": "validation",
            "status": "out_of_scope",
            "confidence": 0,
            "needs_escalation": False,
            "similar_questions": [],
            "sources": [],
            "question": question,
            "contextualized_question": question
        }

    def _create_validation_error_response(self, start_time: float, session_id: str, question: str) -> Dict[str, Any]:
        """Create validation error response"""
        return {
            "answer": "I'm having a small technical hiccup. Could you try rephrasing your question? I'm here to help with anything Jupiter.money related! 😊",
            "session_id": session_id,
            "processing_time": time.time() - start_time,
            "stage": "validation",
            "status": "error",
            "confidence": 0,
            "needs_escalation": True,
            "similar_questions": [],
            "sources": [],
            "question": question,
            "contextualized_question": question
        }

    def _create_unexpected_error_response(self, error: Exception, start_time: float, session_id: str, question: str) -> Dict[str, Any]:
        """Create unexpected error response"""
        return {
            "answer": "Oops! I'm experiencing some technical difficulties. Please try again in a moment, or reach out to our support team through the Jupiter app for immediate help! 🛠️",
            "session_id": session_id,
            "processing_time": time.time() - start_time,
            "stage": "error",
            "status": "error",
            "error": str(error),
            "confidence": 0,
            "needs_escalation": True,
            "similar_questions": [],
            "sources": [],
            "question": question,
            "contextualized_question": question
        }

    def _update_performance_metrics(self, processing_time: float):
        """Update performance metrics"""
        # Update average response time
        total_successful = self.metrics["successful_queries"]
        current_avg = self.metrics["avg_response_time"]
        self.metrics["avg_response_time"] = ((current_avg * (total_successful - 1)) + processing_time) / total_successful

    def get_enhanced_metrics(self) -> Dict[str, Any]:
        """Get enhanced chatbot performance metrics"""
        total = max(self.metrics["total_queries"], 1)
        return {
            **self.metrics,
            "success_rate": (self.metrics["successful_queries"] / total) * 100,
            "out_of_scope_rate": (self.metrics["out_of_scope_queries"] / total) * 100,
            "greeting_rate": (self.metrics["greeting_queries"] / total) * 100,
            "escalation_rate": (self.metrics["escalated_queries"] / total) * 100,
            "error_rate": (self.metrics["error_queries"] / total) * 100,
            "cache_hit_rate": (self.metrics["cache_hits"] / total) * 100 if total > 0 else 0
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

    def clear_cache(self) -> bool:
        """Clear retrieval cache"""
        try:
            self.retrieval_cache.clear()
            logger.info("🗑️ Cleared retrieval cache")
            return True
        except Exception as e:
            logger.error(f"❌ Error clearing cache: {e}")
            return False

    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs"""
        return list(self.session_store.keys())

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "cache_size": len(self.retrieval_cache),
            "cache_max_size": self.cache_max_size,
            "cache_ttl": self.cache_ttl,
            "cache_hits": self.metrics["cache_hits"]
        }

# --- Enhanced Convenience Functions ---

_chatbot_instance = None

def get_chatbot() -> JupiterChatbot:
    """Get or create global chatbot instance"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = JupiterChatbot()
    return _chatbot_instance

def query_jupiter(question: str, session_id: str = "default") -> Dict[str, Any]:
    """Enhanced convenience function for querying Jupiter chatbot"""
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

def clear_chatbot_cache() -> bool:
    """Clear chatbot retrieval cache"""
    chatbot = get_chatbot()
    return chatbot.clear_cache()

# --- Enhanced Test Runner ---
def main():
    """Test the enhanced chatbot with comprehensive scenarios"""
    if "GROQ_API_KEY" not in os.environ:
        print("❌ GROQ_API_KEY environment variable is not set")
        return

    print("🚀 Initializing Enhanced Jupiter RAG Chatbot v3.0...\n")

if __name__ == "__main__":
    main()
