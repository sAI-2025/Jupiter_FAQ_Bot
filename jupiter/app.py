import uuid
import streamlit as st
from chatbot import query_jupiter

# Page Configuration
st.set_page_config(
    page_title="Jupiter FAQ Assistant 🚀",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
def init_session_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False
    if "recommended_questions" not in st.session_state:
        st.session_state.recommended_questions = [
            "🔒 How do I secure my account?",
            "💳 What are the card benefits?",
            "💰 What are transaction limits?",
            "✅ How to complete KYC?",
            "💎 How to earn Jewels?",
            "🏦 How to open Jupiter account?",
            "📱 How to use Jupiter app?",
            "💸 How to transfer money?"
        ]

init_session_state()

# Enhanced CSS with improved layout and design
st.markdown("""
<style>
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    .stToolbar {display: none;}

    /* Global styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        min-height: 100vh;
    }

    /* Main container */
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }

    /* Header - Enhanced oval design */
    .header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: white;
        padding: 30px;
        text-align: center;
        border-radius: 50px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }

    .header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 3s infinite;
    }

    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }

    .header-title {
        font-size: 32px;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .header-subtitle {
        font-size: 18px;
        margin: 10px 0 0 0;
        color: #4ddbb7;
        font-weight: 500;
    }

    /* Chat container - Two column layout */
    .chat-container {
        display: grid;
        grid-template-columns: 2fr 1fr;
        gap: 30px;
        margin-bottom: 30px;
    }

    /* Left column - Chat messages */
    .chat-messages {
        background: rgba(255,255,255,0.95);
        border-radius: 30px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        min-height: 500px;
        max-height: 600px;
        overflow-y: auto;
    }

    /* Right column - Recommendations */
    .recommendations-panel {
        background: rgba(255,255,255,0.95);
        border-radius: 30px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        height: fit-content;
        position: sticky;
        top: 20px;
    }

    /* Welcome screen */
    .welcome-screen {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 30px;
        color: white;
        margin-bottom: 20px;
    }

    .welcome-title {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    .welcome-text {
        font-size: 18px;
        margin-bottom: 30px;
        opacity: 0.9;
    }

    /* Quick action buttons */
    .quick-actions {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }

    .quick-action-btn {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #333;
        padding: 15px 20px;
        border-radius: 25px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    .quick-action-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 154, 158, 0.4);
    }

    /* Chat messages styling */
    .user-message {
        background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 25px 25px 8px 25px;
        margin: 20px 0 20px auto;
        max-width: 75%;
        text-align: right;
        box-shadow: 0 5px 15px rgba(241, 132, 59, 0.3);
        font-size: 16px;
        line-height: 1.4;
    }

    .bot-message {
        display: flex;
        align-items: flex-start;
        gap: 15px;
        margin: 20px 0;
    }

    .bot-avatar {
        background: linear-gradient(135deg, #1e3a5c 0%, #4a8cb5 100%);
        color: white;
        width: 45px;
        height: 45px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        flex-shrink: 0;
    }

    .bot-bubble {
        background: linear-gradient(135deg, #4ddbb7 0%, #42c9a7 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 25px 25px 25px 8px;
        max-width: 75%;
        box-shadow: 0 5px 15px rgba(77, 219, 183, 0.3);
        font-size: 16px;
        line-height: 1.5;
    }

    /* Recommended questions panel */
    .recommendations-title {
        font-size: 20px;
        font-weight: bold;
        color: #1e3a5c;
        margin-bottom: 20px;
        text-align: center;
        padding-bottom: 10px;
        border-bottom: 2px solid #e0e0e0;
    }

    .recommended-item {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
        border: none;
        font-weight: 500;
        margin-bottom: 10px;
        width: 100%;
        text-align: left;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
    }

    .recommended-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }

    /* Input section */
    .input-section {
        background: rgba(255,255,255,0.95);
        padding: 25px;
        border-radius: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: 20px;
    }

    /* Trust badges */
    .trust-badges {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 30px 0;
        flex-wrap: wrap;
    }

    .badge {
        background: rgba(255,255,255,0.95);
        padding: 12px 25px;
        border-radius: 30px;
        font-size: 14px;
        font-weight: 600;
        color: #1e3a5c;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }

    .badge:hover {
        transform: translateY(-3px);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 15px 30px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(241, 132, 59, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(241, 132, 59, 0.4) !important;
    }

    /* Text input styling */
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 15px 25px !important;
        font-size: 16px !important;
        background: white !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #4a8cb5 !important;
        box-shadow: 0 0 0 3px rgba(74, 140, 181, 0.2) !important;
    }

    /* Footer */
    .footer {
        background: rgba(255,255,255,0.9);
        text-align: center;
        margin-top: 30px;
        padding: 20px;
        font-size: 14px;
        color: #666;
        border-radius: 30px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }

    .footer-tip {
        font-weight: bold;
        margin-bottom: 10px;
        color: #1e3a5c;
        font-size: 16px;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .chat-container {
            grid-template-columns: 1fr;
        }

        .recommendations-panel {
            position: static;
        }

        .header-title {
            font-size: 24px;
        }

        .welcome-title {
            font-size: 22px;
        }
    }

    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def add_message(role: str, content: str):
    st.session_state.chat_history.append({"role": role, "content": content})

def get_bot_response(question: str) -> str:
    try:
        with st.spinner("🤔 Thinking..."):
            response = query_jupiter(question, session_id=st.session_state.session_id)
            return response.get("answer", "❌ Something went wrong. Please try again!")
    except Exception as e:
        return "🚨 Sorry, I'm having technical difficulties. Please try again!"

def handle_recommended_question(question):
    """Handle when user clicks a recommended question"""
    add_message("user", question)
    st.session_state.is_loading = True
    st.rerun()

# Header
st.markdown("""
<div class="header">
    <div class="header-title">🚀 Jupiter FAQ Assistant</div>
    <div class="header-subtitle">Ask about accounts, cards, Jewels & more!</div>
</div>
""", unsafe_allow_html=True)

# Main Layout
if not st.session_state.chat_history:
    # Welcome Screen
    st.markdown("""
    <div class="welcome-screen">
        <div class="welcome-title">🚀 Welcome to Jupiter Support!</div>
        <div class="welcome-text">I'm your AI assistant for all Jupiter Money questions. Choose a topic below or ask me anything!</div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Action Buttons
    st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("💳 Credit Card", key="cc", help="Learn about Jupiter credit cards"):
            add_message("user", "How do I apply for a Jupiter credit card?")
            st.rerun()

    with col2:
        if st.button("✅ KYC Process", key="kyc", help="Complete your KYC verification"):
            add_message("user", "How do I complete KYC verification?")
            st.rerun()

    with col3:
        if st.button("💎 Jupiter Jewels", key="jewels", help="Learn about earning Jewels"):
            add_message("user", "What are Jupiter Jewels and how do I earn them?")
            st.rerun()

    with col4:
        if st.button("⭐ Pro Benefits", key="pro", help="Discover Jupiter Pro features"):
            add_message("user", "What are the benefits of Jupiter Pro?")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Chat Layout - Two columns
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Left Column - Chat Messages
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

        # Display chat history
        for i, msg in enumerate(st.session_state.chat_history):
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="bot-message">
                    <div class="bot-avatar">🤖</div>
                    <div class="bot-bubble">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)

        # Show loading if processing
        if st.session_state.is_loading:
            st.markdown("""
            <div class="bot-message">
                <div class="bot-avatar">🤖</div>
                <div class="bot-bubble">
                    <div class="loading"></div> Processing your question...
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Right Column - Recommended Questions
    with col2:
        if st.session_state.recommended_questions:
            st.markdown("""
            <div class="recommendations-panel">
                <div class="recommendations-title">💡 Recommended Questions</div>
            """, unsafe_allow_html=True)

            # Display recommended questions
            for i, question in enumerate(st.session_state.recommended_questions):
                if st.button(question, key=f"rec_{i}", help="Click to ask this question"):
                    handle_recommended_question(question)

            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Process pending response
if st.session_state.is_loading and st.session_state.chat_history:
    last_message = st.session_state.chat_history[-1]
    if last_message["role"] == "user":
        response = get_bot_response(last_message["content"])
        add_message("bot", response)
        st.session_state.is_loading = False
        st.rerun()

# Trust Badges
st.markdown("""
<div class="trust-badges">
    <div class="badge">🔒 Bank-Grade Security</div>
    <div class="badge">⚡ Instant Responses</div>
    <div class="badge">🛡️ RBI Regulated</div>
    <div class="badge">🏆 Award Winning</div>
</div>
""", unsafe_allow_html=True)

# Chat Input Section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("", placeholder="Ask me anything about Jupiter Money...", label_visibility="collapsed")
    with col2:
        send_clicked = st.form_submit_button("Send 🚀")

# Handle Input
if send_clicked and user_input.strip():
    add_message("user", user_input.strip())
    st.session_state.is_loading = True
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-tip">💡 Pro Tip: Ask about account features, card benefits, transactions, or any Jupiter service!</div>
    <div>Made with ❤️ for Jupiter users | Powered by AI | jupiter.money</div>
</div>
""", unsafe_allow_html=True)


# import uuid
# import streamlit as st
# from chatbot import query_jupiter

# # Page Configuration
# st.set_page_config(
#     page_title="Jupiter FAQ Assistant 🚀",
#     page_icon="🚀",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # Initialize Session State
# def init_session_state():
#     if "session_id" not in st.session_state:
#         st.session_state.session_id = str(uuid.uuid4())
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []
#     if "is_loading" not in st.session_state:
#         st.session_state.is_loading = False

# init_session_state()

# # Simplified CSS
# st.markdown("""
# <style>
#     /* Hide Streamlit elements */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
#     .stDeployButton {display: none;}

#     /* Global styling */
#     .stApp {
#         background: linear-gradient(135deg, #f6e1a2 0%, #ffffff 50%, #e8f4f8 100%);
#         font-family: 'Inter', sans-serif;
#     }

#     /* Header - No spacing */
#     .header {
#         background: linear-gradient(135deg, #1e3a5c 0%, #4a8cb5 100%);
#         color: white;
#         padding: 15px;
#         text-align: center;
#         margin: -1rem -1rem 1rem -1rem;
#     }

#     .header-title {
#         font-size: 20px;
#         font-weight: bold;
#         margin: 0;
#     }

#     .header-subtitle {
#         font-size: 12px;
#         margin: 2px 0 0 0;
#         color: #4ddbb7;
#     }

#     /* Welcome section */
#     .welcome {
#         background: white;
#         padding: 20px;
#         border-radius: 12px;
#         text-align: center;
#         margin-bottom: 15px;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.1);
#     }

#     .welcome-title {
#         font-size: 18px;
#         font-weight: bold;
#         color: #1e3a5c;
#         margin-bottom: 8px;
#     }

#     .welcome-text {
#         font-size: 14px;
#         color: #666;
#         margin-bottom: 15px;
#     }

#     /* Questions section */
#     .questions-title {
#         font-size: 16px;
#         font-weight: bold;
#         color: #1e3a5c;
#         margin-bottom: 10px;
#     }

#     /* Trust badges - single line */
#     .trust-badges {
#         display: flex;
#         justify-content: center;
#         gap: 15px;
#         margin: 15px 0;
#         flex-wrap: wrap;
#     }

#     .badge {
#         background: rgba(255,255,255,0.9);
#         padding: 5px 10px;
#         border-radius: 8px;
#         font-size: 12px;
#         font-weight: 600;
#         color: #1e3a5c;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.1);
#     }

#     /* Chat messages */
#     .user-message {
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%);
#         color: white;
#         padding: 10px 15px;
#         border-radius: 15px 15px 5px 15px;
#         margin: 10px 0 10px auto;
#         max-width: 80%;
#         text-align: right;
#     }

#     .bot-message {
#         display: flex;
#         align-items: flex-start;
#         gap: 10px;
#         margin: 10px 0;
#     }

#     .bot-avatar {
#         background: linear-gradient(135deg, #1e3a5c 0%, #4a8cb5 100%);
#         color: white;
#         width: 30px;
#         height: 30px;
#         border-radius: 50%;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 12px;
#     }

#     .bot-bubble {
#         background: linear-gradient(135deg, #4ddbb7 0%, #42c9a7 100%);
#         color: white;
#         padding: 10px 15px;
#         border-radius: 15px 15px 15px 5px;
#         max-width: 80%;
#     }

#     /* Recommended questions - single line */
#     .recommended {
#         background: #f8f9fa;
#         padding: 8px 12px;
#         border-radius: 8px;
#         margin: 10px 0;
#         font-size: 12px;
#         color: #666;
#         text-align: center;
#     }

#     /* Footer */
#     .footer {
#         text-align: center;
#         margin-top: 20px;
#         padding: 10px;
#         font-size: 12px;
#         color: #666;
#     }

#     .footer-tip {
#         font-weight: bold;
#         margin-bottom: 5px;
#     }

#     /* Button styling */
#     .stButton > button {
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%) !important;
#         color: white !important;
#         border: none !important;
#         border-radius: 10px !important;
#         padding: 8px 16px !important;
#         font-weight: 600 !important;
#         width: 100% !important;
#     }

#     .stButton > button:hover {
#         transform: translateY(-1px) !important;
#         box-shadow: 0 4px 8px rgba(241, 132, 59, 0.3) !important;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Helper Functions
# def add_message(role: str, content: str):
#     st.session_state.chat_history.append({"role": role, "content": content})

# def get_bot_response(question: str) -> str:
#     try:
#         response = query_jupiter(question, session_id=st.session_state.session_id)
#         return response.get("answer", "❌ Something went wrong. Please try again!")
#     except Exception as e:
#         return "🚨 Sorry, I'm having technical difficulties. Please try again!"

# # Header (No spacing)
# st.markdown("""
# <div class="header">
#     <div class="header-title">🚀 Jupiter FAQ Assistant</div>
#     <div class="header-subtitle">Ask about accounts, cards, Jewels & more!</div>
# </div>
# """, unsafe_allow_html=True)

# # Main Content
# if not st.session_state.chat_history:
#     # Welcome Screen
#     st.markdown("""
#     <div class="welcome">
#         <div class="welcome-title">🚀 Welcome to Jupiter Support!</div>
#         <div class="welcome-text">I'm your AI assistant for all Jupiter Money questions. Choose a topic below or ask me anything!</div>
#         <div class="questions-title">💡 Popular Questions</div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Quick Question Buttons
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("💳 Credit Card"):
#             add_message("user", "How do I apply for a Jupiter credit card?")
#             st.rerun()
#         if st.button("✅ KYC Process"):
#             add_message("user", "How do I complete KYC verification?")
#             st.rerun()

#     with col2:
#         if st.button("💎 Jupiter Jewels"):
#             add_message("user", "What are Jupiter Jewels and how do I earn them?")
#             st.rerun()
#         if st.button("⭐ Pro Benefits"):
#             add_message("user", "What are the benefits of Jupiter Pro?")
#             st.rerun()

# else:
#     # Chat History
#     for msg in st.session_state.chat_history:
#         if msg["role"] == "user":
#             st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
#         else:
#             st.markdown(f"""
#             <div class="bot-message">
#                 <div class="bot-avatar">🤖</div>
#                 <div class="bot-bubble">{msg["content"]}</div>
#             </div>
#             """, unsafe_allow_html=True)

#     # Recommended questions (single line)
#     st.markdown("""
#     <div class="recommended">
#         🔒 Recommended: Account opening • Card benefits • Transaction limits • KYC help • Jewels earning
#     </div>
#     """, unsafe_allow_html=True)

# # Trust Badges (Single Line)
# st.markdown("""
# <div class="trust-badges">
#     <div class="badge">🔒 Secure</div>
#     <div class="badge">⚡ Fast</div>
#     <div class="badge">🛡️ RBI Regulated</div>
# </div>
# """, unsafe_allow_html=True)

# # Chat Input
# with st.form("chat_form", clear_on_submit=True):
#     col1, col2 = st.columns([5, 1])
#     with col1:
#         user_input = st.text_input("", placeholder="Ask me anything about Jupiter Money...", label_visibility="collapsed")
#     with col2:
#         send_clicked = st.form_submit_button("Send")

# # Handle Input
# if send_clicked and user_input.strip():
#     add_message("user", user_input.strip())
#     with st.spinner("Thinking..."):
#         response = get_bot_response(user_input.strip())
#         add_message("bot", response)
#     st.rerun()

# # Footer
# st.markdown("""
# <div class="footer">
#     <div class="footer-tip">💡 Tip: Ask about account features, card benefits, or transactions!</div>
#     <div>Made with ❤️ for Jupiter users | jupiter.money</div>
# </div>
# """, unsafe_allow_html=True)

# # # #═══════════════════════════════════════════════════════════════════════════════════
# # # #═══════════════════════════════════════════════════════════════════════════════════

# import uuid
# import streamlit as st
# import time
# from chatbot import query_jupiter

# # ═══════════════════════════════════════════════════════════════════════════════════
# # PAGE CONFIGURATION & SESSION STATE
# # ═══════════════════════════════════════════════════════════════════════════════════

# st.set_page_config(
#     page_title="Jupiter FAQ Assistant 🚀",
#     page_icon="🚀",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Initialize session state
# def init_session_state():
#     if "session_id" not in st.session_state:
#         st.session_state.session_id = str(uuid.uuid4())
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []
#     if "is_loading" not in st.session_state:
#         st.session_state.is_loading = False
#     if "pending_message" not in st.session_state:
#         st.session_state.pending_message = ""
#     if "show_recommendations" not in st.session_state:
#         st.session_state.show_recommendations = True

# init_session_state()

# # ═══════════════════════════════════════════════════════════════════════════════════
# # ENHANCED CSS STYLING WITH IMPROVED ALIGNMENT
# # ═══════════════════════════════════════════════════════════════════════════════════

# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

#     /* Hide Streamlit elements */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
#     .stDeployButton {display: none;}

#     /* Remove default margins */
#     .element-container {margin: 0 !important;}
#     .stMarkdown {margin: 0 !important;}
#     .block-container {padding-top: 1rem !important;}

#     /* Global styling with improved alignment */
#     .stApp {
#         background: linear-gradient(135deg, #f6e1a2 0%, #ffffff 50%, #e8f4f8 100%);
#         font-family: 'Inter', sans-serif;
#         max-width: 1400px;
#         margin: 0 auto;
#         padding: 0;
#     }

#     /* Header with perfect centering */
#     .chat-header {
#         background: linear-gradient(135deg, #1e3a5c 0%, #4a8cb5 100%);
#         color: white;
#         padding: 2rem;
#         border-radius: 0 0 24px 24px;
#         text-align: center;
#         margin-bottom: 1.5rem;
#         box-shadow: 0 8px 32px rgba(30, 58, 92, 0.3);
#         position: relative;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#     }

#     .header-content {
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         gap: 1rem;
#         flex-direction: row;
#     }

#     .header-icon {
#         font-size: 2.5rem;
#         animation: pulse 2s ease-in-out infinite alternate;
#         display: flex;
#         align-items: center;
#     }

#     @keyframes pulse {
#         0% { transform: scale(1); }
#         100% { transform: scale(1.08); }
#     }

#     .header-text {
#         text-align: left;
#     }

#     .header-title {
#         font-size: 2rem;
#         font-weight: 700;
#         margin: 0;
#         line-height: 1.2;
#     }

#     .header-subtitle {
#         font-size: 1rem;
#         opacity: 0.9;
#         color: #4ddbb7;
#         margin-top: 0.5rem;
#         font-weight: 400;
#     }

#     /* Main content with improved grid layout */
#     .main-content {
#         display: grid;
#         grid-template-columns: 2fr 1fr;
#         gap: 1.5rem;
#         margin: 0 1.5rem;
#         min-height: 70vh;
#         align-items: start;
#     }

#     /* Chat section with better structure */
#     .chat-section {
#         background: white;
#         border-radius: 20px;
#         box-shadow: 0 8px 32px rgba(0,0,0,0.1);
#         display: flex;
#         flex-direction: column;
#         overflow: hidden;
#         height: fit-content;
#         min-height: 600px;
#     }

#     .chat-content {
#         flex: 1;
#         padding: 1.5rem;
#         overflow-y: auto;
#         min-height: 450px;
#         max-height: 500px;
#         scroll-behavior: smooth;
#         display: flex;
#         flex-direction: column;
#         gap: 1rem;
#     }

#     /* Recommendations with improved alignment */
#     .recommendations-section {
#         background: white;
#         border-radius: 20px;
#         box-shadow: 0 8px 32px rgba(0,0,0,0.1);
#         padding: 1.5rem;
#         height: fit-content;
#         max-height: 600px;
#         overflow-y: auto;
#         position: sticky;
#         top: 1rem;
#     }

#     .recommendations-header {
#         font-size: 1.25rem;
#         font-weight: 700;
#         color: #1e3a5c;
#         margin-bottom: 1rem;
#         display: flex;
#         align-items: center;
#         gap: 0.5rem;
#         text-align: center;
#         justify-content: center;
#     }

#     .recommendation-card {
#         background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
#         border: 2px solid #e9ecef;
#         border-radius: 16px;
#         padding: 1rem;
#         margin-bottom: 0.75rem;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         position: relative;
#         overflow: hidden;
#         text-align: left;
#     }

#     .recommendation-card:hover {
#         border-color: #f1843b;
#         transform: translateY(-2px);
#         box-shadow: 0 8px 24px rgba(241, 132, 59, 0.15);
#         background: linear-gradient(135deg, #fff8f3 0%, #ffffff 100%);
#     }

#     .recommendation-card::before {
#         content: '';
#         position: absolute;
#         top: 0;
#         left: 0;
#         width: 4px;
#         height: 100%;
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%);
#         opacity: 0;
#         transition: opacity 0.3s ease;
#     }

#     .recommendation-card:hover::before {
#         opacity: 1;
#     }

#     /* Welcome screen with perfect centering */
#     .welcome-screen {
#         text-align: center;
#         padding: 3rem 2rem;
#         color: #1e3a5c;
#         display: flex;
#         flex-direction: column;
#         align-items: center;
#         justify-content: center;
#         height: 100%;
#     }

#     .welcome-icon {
#         font-size: 4rem;
#         margin-bottom: 1.5rem;
#         animation: float 3s ease-in-out infinite;
#     }

#     @keyframes float {
#         0%, 100% { transform: translateY(0px); }
#         50% { transform: translateY(-8px); }
#     }

#     .welcome-title {
#         font-size: 2rem;
#         font-weight: 700;
#         margin-bottom: 1rem;
#         color: #1e3a5c;
#     }

#     .welcome-text {
#         font-size: 1rem;
#         opacity: 0.8;
#         margin-bottom: 2rem;
#         line-height: 1.6;
#         max-width: 500px;
#     }

#     /* Quick buttons with improved grid alignment */
#     .quick-buttons-section {
#         margin-top: 2rem;
#         width: 100%;
#     }

#     .quick-buttons-title {
#         font-size: 1.5rem;
#         font-weight: 600;
#         color: #1e3a5c;
#         margin-bottom: 1rem;
#         text-align: center;
#     }

#     .quick-buttons {
#         display: grid;
#         grid-template-columns: repeat(2, 1fr);
#         gap: 1rem;
#         width: 100%;
#         max-width: 600px;
#         margin: 0 auto;
#     }

#     /* Enhanced button styling */
#     .stButton > button {
#         background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
#         color: #1e3a5c !important;
#         border: 2px solid #f1843b !important;
#         border-radius: 20px !important;
#         padding: 1rem 1.5rem !important;
#         font-weight: 600 !important;
#         font-size: 0.9rem !important;
#         transition: all 0.3s ease !important;
#         box-shadow: 0 4px 16px rgba(241, 132, 59, 0.15) !important;
#         width: 100% !important;
#         min-height: 60px !important;
#         display: flex !important;
#         align-items: center !important;
#         justify-content: center !important;
#         text-align: center !important;
#     }

#     .stButton > button:hover {
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%) !important;
#         color: white !important;
#         transform: translateY(-2px) scale(1.02) !important;
#         box-shadow: 0 8px 24px rgba(241, 132, 59, 0.3) !important;
#     }

#     /* Message bubbles with improved alignment */
#     .message-wrapper {
#         margin-bottom: 1.5rem;
#         animation: slideIn 0.4s ease-out;
#         width: 100%;
#     }

#     @keyframes slideIn {
#         from { opacity: 0; transform: translateY(12px); }
#         to { opacity: 1; transform: translateY(0); }
#     }

#     .user-message {
#         display: flex;
#         justify-content: flex-end;
#         width: 100%;
#         margin-bottom: 1rem;
#     }

#     .bot-message {
#         display: flex;
#         justify-content: flex-start;
#         align-items: flex-start;
#         gap: 0.75rem;
#         width: 100%;
#         margin-bottom: 1rem;
#     }

#     .user-bubble {
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%);
#         color: white;
#         padding: 1rem 1.25rem;
#         border-radius: 24px 24px 8px 24px;
#         max-width: 80%;
#         font-size: 0.95rem;
#         line-height: 1.5;
#         box-shadow: 0 4px 16px rgba(241, 132, 59, 0.25);
#         font-weight: 500;
#         word-wrap: break-word;
#     }

#     .bot-bubble {
#         background: linear-gradient(135deg, #4ddbb7 0%, #42c9a7 100%);
#         color: white;
#         padding: 1rem 1.25rem;
#         border-radius: 24px 24px 24px 8px;
#         max-width: 80%;
#         font-size: 0.95rem;
#         line-height: 1.5;
#         box-shadow: 0 4px 16px rgba(77, 219, 183, 0.25);
#         font-weight: 500;
#         word-wrap: break-word;
#     }

#     .bot-avatar {
#         width: 40px;
#         height: 40px;
#         background: linear-gradient(135deg, #1e3a5c 0%, #4a8cb5 100%);
#         border-radius: 50%;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 1rem;
#         color: white;
#         flex-shrink: 0;
#         box-shadow: 0 4px 12px rgba(30, 58, 92, 0.25);
#     }

#     /* Input section with improved alignment */
#     .input-section {
#         padding: 1.5rem;
#         background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
#         border-top: 1px solid #e9ecef;
#         border-radius: 0 0 20px 20px;
#         position: sticky;
#         bottom: 0;
#         z-index: 100;
#     }

#     .input-form {
#         display: flex;
#         gap: 0.75rem;
#         align-items: center;
#         width: 100%;
#     }

#     .stTextInput > div > div > input {
#         border: 2px solid #e9ecef !important;
#         border-radius: 24px !important;
#         padding: 1rem 1.25rem !important;
#         font-size: 0.95rem !important;
#         background: white !important;
#         color: #1e3a5c !important;
#         transition: all 0.3s ease !important;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
#         width: 100% !important;
#     }

#     .stTextInput > div > div > input:focus {
#         border-color: #f1843b !important;
#         box-shadow: 0 0 0 4px rgba(241, 132, 59, 0.1) !important;
#         outline: none !important;
#     }

#     .stFormSubmitButton > button {
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%) !important;
#         color: white !important;
#         border: none !important;
#         border-radius: 50% !important;
#         width: 52px !important;
#         height: 52px !important;
#         min-width: 52px !important;
#         min-height: 52px !important;
#         padding: 0 !important;
#         display: flex !important;
#         align-items: center !important;
#         justify-content: center !important;
#         font-size: 1.25rem !important;
#         font-weight: bold !important;
#         transition: all 0.2s ease !important;
#         box-shadow: 0 4px 12px rgba(241, 132, 59, 0.3) !important;
#         flex-shrink: 0 !important;
#     }

#     .stFormSubmitButton > button:hover {
#         transform: scale(1.05) !important;
#         box-shadow: 0 6px 20px rgba(241, 132, 59, 0.4) !important;
#     }

#     /* Loading animation */
#     .loading-message {
#         background: #f8f9fa;
#         color: #6c757d;
#         padding: 1rem 1.25rem;
#         border-radius: 24px 24px 24px 8px;
#         display: flex;
#         align-items: center;
#         gap: 0.75rem;
#         font-size: 0.9rem;
#         font-style: italic;
#         max-width: 80%;
#     }

#     .typing-dots {
#         display: flex;
#         gap: 4px;
#     }

#     .dot {
#         width: 6px;
#         height: 6px;
#         background: #4ddbb7;
#         border-radius: 50%;
#         animation: bounce 1.4s infinite both;
#     }

#     .dot:nth-child(1) { animation-delay: -0.32s; }
#     .dot:nth-child(2) { animation-delay: -0.16s; }
#     .dot:nth-child(3) { animation-delay: 0s; }

#     @keyframes bounce {
#         0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
#         40% { transform: scale(1.2); opacity: 1; }
#     }

#     /* Trust indicators with centered alignment */
#     .trust-section {
#         display: flex;
#         justify-content: center;
#         align-items: center;
#         gap: 1rem;
#         margin: 1.5rem;
#         flex-wrap: wrap;
#     }

#     .trust-badge {
#         background: rgba(255,255,255,0.95);
#         padding: 0.5rem 1rem;
#         border-radius: 16px;
#         font-size: 0.8rem;
#         font-weight: 600;
#         color: #1e3a5c;
#         box-shadow: 0 4px 12px rgba(0,0,0,0.08);
#         display: flex;
#         align-items: center;
#         gap: 0.5rem;
#     }

#     /* Responsive design improvements */
#     @media (max-width: 1200px) {
#         .main-content {
#             grid-template-columns: 1fr;
#             gap: 1rem;
#         }

#         .recommendations-section {
#             position: relative;
#             top: auto;
#             max-height: 300px;
#         }

#         .header-content {
#             flex-direction: column;
#             gap: 0.5rem;
#         }

#         .header-text {
#             text-align: center;
#         }
#     }

#     @media (max-width: 768px) {
#         .quick-buttons {
#             grid-template-columns: 1fr;
#         }

#         .main-content {
#             margin: 0 1rem;
#         }

#         .chat-header {
#             padding: 1.5rem;
#         }

#         .header-title {
#             font-size: 1.5rem;
#         }
#     }

#     /* Scrollbar styling */
#     .chat-content::-webkit-scrollbar,
#     .recommendations-section::-webkit-scrollbar {
#         width: 6px;
#     }

#     .chat-content::-webkit-scrollbar-track,
#     .recommendations-section::-webkit-scrollbar-track {
#         background: #f1f1f1;
#         border-radius: 10px;
#     }

#     .chat-content::-webkit-scrollbar-thumb,
#     .recommendations-section::-webkit-scrollbar-thumb {
#         background: #4ddbb7;
#         border-radius: 10px;
#     }

#     /* No recommendations styling */
#     .no-recommendations {
#         text-align: center;
#         padding: 2rem 1rem;
#         color: #6c757d;
#         font-style: italic;
#     }

#     .no-recommendations-icon {
#         font-size: 3rem;
#         margin-bottom: 0.75rem;
#         opacity: 0.5;
#     }
# </style>
# """, unsafe_allow_html=True)

# # ═══════════════════════════════════════════════════════════════════════════════════
# # HELPER FUNCTIONS
# # ═══════════════════════════════════════════════════════════════════════════════════

# def add_message(role: str, content: str, similar_questions: list = None):
#     """Add message to chat history with similar questions"""
#     message_data = {
#         "role": role,
#         "content": content,
#         "similar_questions": similar_questions or []
#     }
#     st.session_state.chat_history.append(message_data)

# def get_bot_response(question: str) -> dict:
#     """Get response from chatbot with error handling"""
#     try:
#         response = query_jupiter(question, session_id=st.session_state.session_id)
#         return response
#     except Exception as e:
#         st.error(f"Error: {str(e)}")
#         return {
#             "answer": "🚨 Sorry, I'm having technical difficulties. Please try again!",
#             "similar_questions": []
#         }

# def handle_quick_question(question: str):
#     """Handle quick question button clicks"""
#     st.session_state.pending_message = question

# def handle_recommendation_click(question: str):
#     """Handle recommendation question clicks"""
#     st.session_state.pending_message = question

# def get_latest_recommendations():
#     """Get recommendations from the latest bot response"""
#     if st.session_state.chat_history:
#         for message in reversed(st.session_state.chat_history):
#             if message["role"] == "bot" and message.get("similar_questions"):
#                 return message["similar_questions"]
#     return []

# # ═══════════════════════════════════════════════════════════════════════════════════
# # MAIN UI COMPONENTS
# # ═══════════════════════════════════════════════════════════════════════════════════

# # Header with improved alignment
# st.markdown("""
# <div class="chat-header">
#     <div class="header-content">
#         <div class="header-icon">🚀</div>
#         <div class="header-text">
#             <div class="header-title">Jupiter FAQ Assistant</div>
#             <div class="header-subtitle">Ask about accounts, cards, Jewels & more!</div>
#         </div>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Main content with improved grid layout
# st.markdown('<div class="main-content">', unsafe_allow_html=True)

# # Chat section
# col1, col2 = st.columns([2, 1], gap="large")

# with col1:
#     st.markdown('<div class="chat-section">', unsafe_allow_html=True)
#     st.markdown('<div class="chat-content">', unsafe_allow_html=True)

#     # Show welcome screen or chat history
#     if not st.session_state.chat_history:
#         st.markdown("""
#         <div class="welcome-screen">
#             <div class="welcome-icon">🚀</div>
#             <div class="welcome-title">Welcome to Jupiter Support!</div>
#             <div class="welcome-text">
#                 I'm your AI assistant for all Jupiter Money questions.
#                 Choose a topic below or ask me anything!
#             </div>
#             <div class="quick-buttons-section">
#                 <div class="quick-buttons-title">💡 Popular Questions</div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#         # Quick question buttons with improved layout
#         st.markdown('<div class="quick-buttons">', unsafe_allow_html=True)

#         col_a, col_b = st.columns(2)

#         with col_a:
#             if st.button("💳 Credit Card", key="card", use_container_width=True):
#                 handle_quick_question("How do I apply for a Jupiter credit card?")
#                 st.rerun()

#             if st.button("✅ KYC Process", key="kyc", use_container_width=True):
#                 handle_quick_question("How do I complete KYC verification?")
#                 st.rerun()

#         with col_b:
#             if st.button("💎 Jupiter Jewels", key="jewels", use_container_width=True):
#                 handle_quick_question("What are Jupiter Jewels and how do I earn them?")
#                 st.rerun()

#             if st.button("⭐ Pro Benefits", key="pro", use_container_width=True):
#                 handle_quick_question("What are the benefits of Jupiter Pro?")
#                 st.rerun()

#         st.markdown('</div>', unsafe_allow_html=True)

#     else:
#         # Display chat history with improved alignment
#         for msg in st.session_state.chat_history:
#             if msg["role"] == "user":
#                 st.markdown(f"""
#                 <div class="message-wrapper">
#                     <div class="user-message">
#                         <div class="user-bubble">{msg['content']}</div>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
#             else:
#                 st.markdown(f"""
#                 <div class="message-wrapper">
#                     <div class="bot-message">
#                         <div class="bot-avatar">🤖</div>
#                         <div class="bot-bubble">{msg['content']}</div>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)

#         # Show loading animation
#         if st.session_state.is_loading:
#             st.markdown("""
#             <div class="message-wrapper">
#                 <div class="bot-message">
#                     <div class="bot-avatar">🤖</div>
#                     <div class="loading-message">
#                         <div class="typing-dots">
#                             <div class="dot"></div>
#                             <div class="dot"></div>
#                             <div class="dot"></div>
#                         </div>
#                         <span>Thinking...</span>
#                     </div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)

#     # Input section with improved form layout
#     st.markdown('<div class="input-section">', unsafe_allow_html=True)

#     with st.form("chat_form", clear_on_submit=True, border=False):
#         st.markdown('<div class="input-form">', unsafe_allow_html=True)

#         col_input, col_send = st.columns([6, 1])

#         with col_input:
#             user_input = st.text_input(
#                 "",
#                 placeholder="Ask me anything about Jupiter Money...",
#                 label_visibility="collapsed",
#                 key="chat_input"
#             )

#         with col_send:
#             send_clicked = st.form_submit_button("↑")

#         st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)

# # Recommendations section with improved alignment
# with col2:
#     st.markdown('<div class="recommendations-section">', unsafe_allow_html=True)

#     st.markdown("""
#     <div class="recommendations-header">
#         <span>💡</span>
#         <span>Related Questions</span>
#     </div>
#     """, unsafe_allow_html=True)

#     # Get current recommendations
#     current_recommendations = get_latest_recommendations()

#     if current_recommendations:
#         for i, rec in enumerate(current_recommendations):
#             question_text = rec.get('question', '')
#             score = rec.get('score', 0)
#             source = rec.get('source', 'unknown')

#             # Create unique key for each recommendation button
#             rec_key = f"rec_{i}_{hash(question_text)}"

#             st.markdown(f"""
#             <div class="recommendation-card" onclick="document.getElementById('{rec_key}').click()">
#                 <div class="recommendation-text">{question_text}</div>
#                 <div class="recommendation-source">Score: {score} | {source.replace('_', ' ').title()}</div>
#             </div>
#             """, unsafe_allow_html=True)

#             # Hidden button for functionality
#             if st.button(question_text, key=rec_key, help=f"Source: {source} | Score: {score}",
#                         type="secondary", use_container_width=True):
#                 handle_recommendation_click(question_text)
#                 st.rerun()
#     else:
#         st.markdown("""
#         <div class="no-recommendations">
#             <div class="no-recommendations-icon">🤔</div>
#             <div>Ask a question to see related suggestions!</div>
#         </div>
#         """, unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)

# # ═══════════════════════════════════════════════════════════════════════════════════
# # MESSAGE PROCESSING LOGIC
# # ═══════════════════════════════════════════════════════════════════════════════════

# # Handle pending message from quick buttons or recommendations
# if st.session_state.pending_message:
#     add_message("user", st.session_state.pending_message)
#     st.session_state.is_loading = True
#     st.session_state.pending_message = ""
#     st.rerun()

# # Handle form submission
# if send_clicked and user_input.strip():
#     add_message("user", user_input.strip())
#     st.session_state.is_loading = True
#     st.rerun()

# # Process bot response
# if st.session_state.is_loading and st.session_state.chat_history:
#     last_message = st.session_state.chat_history[-1]["content"]

#     with st.spinner(""):
#         try:
#             response_data = get_bot_response(last_message)
#             bot_answer = response_data.get("answer", "Sorry, I couldn't process your request.")
#             similar_questions = response_data.get("similar_questions", [])

#             # Add bot message with similar questions
#             add_message("bot", bot_answer, similar_questions)

#         except Exception as e:
#             add_message("bot", "🚨 Sorry, I'm having technical difficulties. Please try again!")
#             st.error(f"Error processing request: {str(e)}")

#     st.session_state.is_loading = False
#     st.rerun()

# # Trust indicators with perfect centering
# st.markdown("""
# <div class="trust-section">
#     <div class="trust-badge">
#         <span class="trust-icon">🔒</span>
#         <span>Secure</span>
#     </div>
#     <div class="trust-badge">
#         <span class="trust-icon">⚡</span>
#         <span>Fast</span>
#     </div>
#     <div class="trust-badge">
#         <span class="trust-icon">🛡️</span>
#         <span>RBI Regulated</span>
#     </div>
#     <div class="trust-badge">
#         <span class="trust-icon">🤖</span>
#         <span>AI Powered</span>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Auto-scroll to bottom
# st.markdown("""
# <script>
#     setTimeout(function() {
#         const container = document.querySelector('.chat-content');
#         if (container) {
#             container.scrollTop = container.scrollHeight;
#         }
#     }, 100);
# </script>
# """, unsafe_allow_html=True)
