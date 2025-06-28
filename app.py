import streamlit as st
import os
import logging
from datetime import datetime
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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Optional: disable Chroma telemetry
os.environ["CHROMA_TELEMETRY_ENABLED"] = "FALSE"

# Page configuration
st.set_page_config(
    page_title="Jupiter RAG Chat Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize embeddings (using the same as your second code)
@st.cache_resource
def initialize_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

# Initialize vectorstore
@st.cache_resource
def initialize_vectorstore():
    embeddings = initialize_embeddings()
    vectorstore_path = "./jupiter_vectordb_enhanced"
    try:
        vectorstore = Chroma(
            persist_directory=vectorstore_path,
            embedding_function=embeddings
        )
        return vectorstore.as_retriever(search_kwargs={"k": 5})
    except Exception as e:
        st.error(f"Error loading vectorstore: {e}")
        return None

# Initialize session state
def initialize_session_state():
    if 'store' not in st.session_state:
        st.session_state.store = {}
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'session_id' not in st.session_state:
        st.session_state.session_id = "default_session"

# Get session history function
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id] = ChatMessageHistory()
    return st.session_state.store[session_id]

# Create RAG chain
@st.cache_resource
def create_rag_chain(api_key):
    retriever = initialize_vectorstore()
    if not retriever:
        return None

    # Initialize LLM with provided API key
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama3-8b-8192",
        temperature=0.3,
        max_tokens=300
    )

    # Contextualizing prompt
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "As JupiterBot, rewrite the user's follow-up message into a clear, standalone question. "
         "Include relevant chat history, domain-specific terms (e.g., 'Jupiter card', 'Jewels'), "
         "and clarify any ambiguity to make it fully self-contained."),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    # Main QA prompt
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are Jupiter's Tier-1 Support Bot. Provide friendly, professional responses (2-3 sentences) "
            "using the provided context.\n"
            "If relevant, include clear actionable steps like app navigation (e.g., 'Go to Settings > Card > Block Card') "
            "or links to the Help Center.\n"
            "If unsure, reply: 'I'm not certain—let me escalate this or check with our team.'\n"
            "Avoid using internal system terms. Always prioritize clarity and customer understanding.\n\n"
            "{context}"
        )),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}")
    ])

    # Build RAG chain
    history_aware_retriever = create_history_aware_retriever(
        llm=llm,
        retriever=retriever,
        prompt=contextualize_q_prompt
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    # Wrap with message history
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    return conversational_rag_chain

# Main app
def main():
    st.title("🤖 Jupiter RAG Chat Assistant")
    st.write("Chat with Jupiter's knowledge base using advanced RAG technology")

    # Initialize session state
    initialize_session_state()

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # API Key input
        api_key = st.text_input(
            "Enter your Groq API key:",
            type="password",
            help="Get your API key from https://console.groq.com/"
        )

        # Session ID input
        session_id = st.text_input(
            "Session ID",
            value=st.session_state.session_id,
            help="Change this to start a new conversation"
        )

        if session_id != st.session_state.session_id:
            st.session_state.session_id = session_id
            st.session_state.messages = []

        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            if session_id in st.session_state.store:
                st.session_state.store[session_id] = ChatMessageHistory()
            st.rerun()

        # Display session info
        st.divider()
        st.subheader("📊 Session Info")
        st.write(f"**Current Session:** {session_id}")
        st.write(f"**Messages:** {len(st.session_state.messages)}")

        # Example queries
        st.divider()
        st.subheader("💡 Example Queries")
        example_queries = [
            "How do I activate my Jupiter card?",
            "What are Jewels in Jupiter?",
            "Bill payment failed, what should I do?",
            "KYC verification process",
            "How to block my card?"
        ]

        for query in example_queries:
            if st.button(f"📝 {query}", key=f"example_{query}"):
                st.session_state.example_query = query

    # Check if API key is provided
    if not api_key:
        st.warning("⚠️ Please enter your Groq API key in the sidebar to continue.")
        st.info("You can get a free API key from [Groq Console](https://console.groq.com/)")
        return

    # Initialize RAG chain
    try:
        conversational_rag_chain = create_rag_chain(api_key)
        if not conversational_rag_chain:
            st.error("❌ Failed to initialize the RAG system. Please check your vectorstore.")
            return
    except Exception as e:
        st.error(f"❌ Error initializing RAG chain: {e}")
        return

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle example query
    if hasattr(st.session_state, 'example_query'):
        user_input = st.session_state.example_query
        delattr(st.session_state, 'example_query')
    else:
        user_input = None

    # Chat input
    if prompt := st.chat_input("Ask me anything about Jupiter...") or user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    # Get response from RAG chain
                    start_time = datetime.now()
                    response = conversational_rag_chain.invoke(
                        {"input": prompt},
                        config={"configurable": {"session_id": session_id}}
                    )

                    processing_time = (datetime.now() - start_time).total_seconds()

                    # Extract answer
                    answer = response.get('answer', 'Sorry, I could not generate a response.')

                    # Display response
                    st.markdown(answer)

                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": answer})

                    # Display processing time in sidebar
                    with st.sidebar:
                        st.success(f"⚡ Response generated in {processing_time:.2f}s")

                except Exception as e:
                    error_msg = f"❌ Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    logger.error(f"Error in chat: {e}")

# Run the app
if __name__ == "__main__":
    main()
