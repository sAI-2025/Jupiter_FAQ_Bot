import uuid,streamlit as st
import time
from chatbot import query_jupiter

# ═══════════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION & SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Jupiter FAQ Assistant 🚀",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize session state
def init_session_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "is_loading" not in st.session_state:
        st.session_state.is_loading = False
    if "pending_message" not in st.session_state:
        st.session_state.pending_message = ""

init_session_state()

# ═══════════════════════════════════════════════════════════════════════════════════
# ENHANCED CSS STYLING WITH CHATGPT-STYLE INPUT
# ═══════════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Global styling */
    .stApp {
        background: linear-gradient(135deg, #f6e1a2 0%, #ffffff 50%, #e8f4f8 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Header with icon */
    .chat-header {
        background: linear-gradient(135deg, #1e3a5c 0%, #4a8cb5 100%);
        color: white;
        padding: 20px;
        border-radius: 0 0 20px 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(30, 58, 92, 0.3);
        position: relative;
    }

    .header-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }

    .header-icon {
        font-size: 24px;
        animation: pulse 2s ease-in-out infinite alternate;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        100% { transform: scale(1.05); }
    }

    .header-title {
        font-size: 22px;
        font-weight: 700;
        margin: 0;
    }

    .header-subtitle {
        font-size: 13px;
        opacity: 0.9;
        color: #4ddbb7;
        margin-top: 4px;
    }

    /* Chat content - NO CONTAINER */
    .chat-content {
        margin: 0 16px 16px 16px;
        min-height: 300px;
        max-height: 400px;
        overflow-y: auto;
        scroll-behavior: smooth;
    }

    /* Welcome screen */
    .welcome-screen {
        text-align: center;
        padding: 24px 16px;
        color: #1e3a5c;
        background: white;
        border-radius: 16px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    .welcome-icon {
        font-size: 48px;
        margin-bottom: 12px;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
    }

    .welcome-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 6px;
        color: #1e3a5c;
    }

    .welcome-text {
        font-size: 14px;
        opacity: 0.8;
        margin-bottom: 20px;
        line-height: 1.4;
    }

    /* Quick question buttons */
    .quick-buttons {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-top: 20px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
        color: #1e3a5c !important;
        border: 2px solid #f1843b !important;
        border-radius: 16px !important;
        padding: 10px 14px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 3px 10px rgba(241, 132, 59, 0.15) !important;
        width: 100% !important;
        min-height: 42px !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%) !important;
        color: white !important;
        transform: translateY(-1px) scale(1.02) !important;
        box-shadow: 0 5px 16px rgba(241, 132, 59, 0.3) !important;
    }

    /* Message bubbles */
    .message-wrapper {
        margin-bottom: 12px;
        animation: slideIn 0.3s ease-out;
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .user-message {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 12px;
    }

    .bot-message {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 12px;
    }

    .user-bubble {
        background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%);
        color: white;
        padding: 10px 14px;
        border-radius: 18px 18px 4px 18px;
        max-width: 80%;
        font-size: 14px;
        line-height: 1.4;
        box-shadow: 0 2px 6px rgba(241, 132, 59, 0.25);
    }

    .bot-bubble {
        background: linear-gradient(135deg, #4ddbb7 0%, #42c9a7 100%);
        color: white;
        padding: 10px 14px;
        border-radius: 18px 18px 18px 4px;
        max-width: 80%;
        font-size: 14px;
        line-height: 1.4;
        box-shadow: 0 2px 6px rgba(77, 219, 183, 0.25);
    }

    .bot-avatar {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #1e3a5c 0%, #4a8cb5 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        color: white;
        flex-shrink: 0;
        box-shadow: 0 2px 6px rgba(30, 58, 92, 0.25);
    }

    /* Loading animation */
    .loading-message {
        background: #f8f9fa;
        color: #6c757d;
        padding: 10px 14px;
        border-radius: 18px 18px 18px 4px;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        font-style: italic;
    }

    .typing-dots {
        display: flex;
        gap: 3px;
    }

    .dot {
        width: 5px;
        height: 5px;
        background: #4ddbb7;
        border-radius: 50%;
        animation: bounce 1.4s infinite both;
    }

    .dot:nth-child(1) { animation-delay: -0.32s; }
    .dot:nth-child(2) { animation-delay: -0.16s; }
    .dot:nth-child(3) { animation-delay: 0s; }

    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
        40% { transform: scale(1.2); opacity: 1; }
    }

    /* CHATGPT-STYLE INPUT SECTION */
    .input-section {
        padding: 12px 16px;
        margin: 0 16px 16px 16px;
        background: white;
        border-radius: 24px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border: 1px solid rgba(241, 132, 59, 0.1);
        position: relative;
    }

    /* Hide default streamlit form styling */
    .stForm {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
    }

    /* Input field styling */
    .stTextInput > div > div > input {
        border: 2px solid #e9ecef !important;
        border-radius: 24px !important;
        padding: 12px 16px !important;
        font-size: 15px !important;
        background: #f8f9fa !important;
        color: #1e3a5c !important;
        transition: all 0.3s ease !important;
        box-shadow: none !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #f1843b !important;
        box-shadow: 0 0 0 3px rgba(241, 132, 59, 0.1) !important;
        outline: none !important;
        background: white !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #9ca3af !important;
        font-size: 14px !important;
    }

    /* CIRCULAR SEND BUTTON STYLING */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        min-width: 45px !important;
        min-height: 45px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 18px !important;
        font-weight: bold !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(241, 132, 59, 0.3) !important;
        position: relative !important;
    }

    .stFormSubmitButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 4px 12px rgba(241, 132, 59, 0.4) !important;
    }

    .stFormSubmitButton > button:active {
        transform: scale(0.95) !important;
    }

    /* Hide button text and add arrow */
    .stFormSubmitButton > button::before {
        content: "↑" !important;
        font-size: 18px !important;
        font-weight: bold !important;
        color: white !important;
    }

    .stFormSubmitButton > button > div {
        display: none !important;
    }

    /* Trust indicators */
    .trust-section {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin: 12px;
        flex-wrap: wrap;
    }

    .trust-badge {
        background: rgba(255,255,255,0.9);
        padding: 6px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 600;
        color: #1e3a5c;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .trust-icon {
        font-size: 11px;
        color: #f1843b;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin: 20px 16px 16px 16px;
        padding: 12px;
        background: rgba(255,255,255,0.8);
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    .footer-text {
        font-size: 13px;
        color: #1e3a5c;
        margin-bottom: 6px;
    }

    .footer-links {
        font-size: 11px;
        color: #6c757d;
    }

    .footer-links a {
        color: #f1843b;
        text-decoration: none;
        font-weight: 600;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .chat-header {
            margin: -8px -8px 16px -8px;
            border-radius: 0 0 16px 16px;
            padding: 16px;
        }

        .header-title {
            font-size: 20px;
        }

        .chat-content {
            margin: 0 8px 12px 8px;
            max-height: 300px;
            min-height: 250px;
        }

        .quick-buttons {
            grid-template-columns: 1fr;
        }

        .user-bubble, .bot-bubble {
            max-width: 90%;
            font-size: 13px;
        }

        .input-section {
            margin: 0 8px 8px 8px;
        }
    }

    /* Scrollbar */
    .chat-content::-webkit-scrollbar {
        width: 4px;
    }

    .chat-content::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 8px;
    }

    .chat-content::-webkit-scrollbar-thumb {
        background: #4ddbb7;
        border-radius: 8px;
    }

    /* Remove default streamlit margins */
    .element-container {
        margin-bottom: 0 !important;
    }

    .stMarkdown {
        margin-bottom: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════════

def add_message(role: str, content: str):
    """Add message to chat history"""
    st.session_state.chat_history.append({"role": role, "content": content})

def get_bot_response(question: str) -> str:
    """Get response from chatbot with error handling"""
    try:
        response = query_jupiter(question, session_id=st.session_state.session_id)
        return response.get("answer", "❌ Something went wrong. Please try again!")
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "🚨 Sorry, I'm having technical difficulties. Please try again!"

def handle_quick_question(question: str):
    """Handle quick question button clicks"""
    st.session_state.pending_message = question

# Check for query parameters (FIXED: Using new API)
try:
    # Use new query_params API instead of deprecated experimental version
    query_params = dict(st.query_params)
    if "msg" in query_params:
        if query_params["msg"] and query_params["msg"] != st.session_state.pending_message:
            st.session_state.pending_message = query_params["msg"]
            # Clear the query parameter
            del st.query_params["msg"]
except Exception as e:
    # Fallback for older versions
    pass

# ═══════════════════════════════════════════════════════════════════════════════════
# MAIN UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════════

# Header
st.markdown("""
<div class="chat-header">
    <div class="header-content">
        <div class="header-icon">🚀</div>
        <div>
            <div class="header-title">Jupiter FAQ Assistant</div>
            <div class="header-subtitle">Ask about accounts, cards, Jewels & more!</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat Content (NO CONTAINER)
st.markdown('<div class="chat-content">', unsafe_allow_html=True)

# Show welcome screen or chat history
if not st.session_state.chat_history:
    st.markdown("""
    <div class="welcome-screen">
        <div class="welcome-icon">🚀</div>
        <div class="welcome-title">Welcome to Jupiter Support!</div>
        <div class="welcome-text">
            I'm your AI assistant for all Jupiter Money questions.
            Choose a topic below or ask me anything!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick question buttons
    #st.markdown("### 💡 Popular Questions")

    st.markdown("""
        <style>
            #popular-questions {
                color: #FF6347;  # This is an example color (Tomato). You can change it to any color you want.
        }
        </style>
        """, unsafe_allow_html=True)

    # Add the header with the styled id
    st.markdown('<h3 id="popular-questions">💡 Popular Questions</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💳 Credit Card", key="card", use_container_width=True):
            handle_quick_question("How do I apply for a Jupiter credit card?")
            st.rerun()

        if st.button("✅ KYC Process", key="kyc", use_container_width=True):
            handle_quick_question("How do I complete KYC verification?")
            st.rerun()

    with col2:
        if st.button("💎 Jupiter Jewels", key="jewels", use_container_width=True):
            handle_quick_question("What are Jupiter Jewels and how do I earn them?")
            st.rerun()

        if st.button("⭐ Pro Benefits", key="pro", use_container_width=True):
            handle_quick_question("What are the benefits of Jupiter Pro?")
            st.rerun()

else:
    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="message-wrapper">
                <div class="user-message">
                    <div class="user-bubble">{msg['content']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-wrapper">
                <div class="bot-message">
                    <div class="bot-avatar">🤖</div>
                    <div class="bot-bubble">{msg['content']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Show loading animation
    if st.session_state.is_loading:
        st.markdown("""
        <div class="message-wrapper">
            <div class="bot-message">
                <div class="bot-avatar">🤖</div>
                <div class="loading-message">
                    <div class="typing-dots">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                    <span>Thinking...</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# HORIZONTAL INPUT SECTION (SIMPLIFIED AND FIXED)
st.markdown('<div class="input-section">', unsafe_allow_html=True)

# Use native Streamlit form with proper error handling
with st.form("chat_form", clear_on_submit=True, border=False):
    # Horizontal layout: input field + send button
    col1, col2 = st.columns([6, 1])

    with col1:
        user_input = st.text_input(
            "",
            placeholder="Ask me anything about Jupiter Money...",
            label_visibility="collapsed",
            key="chat_input"
        )

    with col2:
        send_clicked = st.form_submit_button("Send")

st.markdown('</div>', unsafe_allow_html=True)

# Handle pending message from quick buttons
if st.session_state.pending_message:
    add_message("user", st.session_state.pending_message)
    st.session_state.is_loading = True
    st.session_state.pending_message = ""
    st.rerun()

# Handle form submission
if send_clicked and user_input.strip():
    add_message("user", user_input.strip())
    st.session_state.is_loading = True
    st.rerun()

# Process bot response
if st.session_state.is_loading and st.session_state.chat_history:
    last_message = st.session_state.chat_history[-1]["content"]

    with st.spinner(""):
        try:
            response = get_bot_response(last_message)
            add_message("bot", response)
        except Exception as e:
            add_message("bot", "🚨 Sorry, I'm having technical difficulties. Please try again!")
            st.error(f"Error processing request: {str(e)}")

    st.session_state.is_loading = False
    st.rerun()

# Trust indicators
st.markdown("""
<div class="trust-section">
    <div class="trust-badge">
        <span class="trust-icon">🔒</span>
        <span>Secure</span>
    </div>
    <div class="trust-badge">
        <span class="trust-icon">⚡</span>
        <span>Fast</span>
    </div>
    <div class="trust-badge">
        <span class="trust-icon">🛡️</span>
        <span>RBI Regulated</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-text">
        <strong>💡 Tip:</strong> Ask about account features, card benefits, or transactions!
    </div>
    <div class="footer-links">
        Made with ❤️ for Jupiter users |
        <a href="https://jupiter.money" target="_blank">jupiter.money</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Auto-scroll to bottom
st.markdown("""
<script>
    setTimeout(function() {
        const container = document.querySelector('.chat-content');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }, 100);
</script>
""", unsafe_allow_html=True)


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
#     layout="centered",
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

# init_session_state()

# # ═══════════════════════════════════════════════════════════════════════════════════
# # ENHANCED MOBILE-FIRST CSS STYLING WITH LOGO
# # ═══════════════════════════════════════════════════════════════════════════════════

# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

#     /* Hide Streamlit elements */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
#     .stDeployButton {display: none;}

#     /* Global styling - Mobile First */
#     .stApp {
#         background: linear-gradient(135deg, #fff7ed 0%, #ffffff 50%, #f0fdfa 100%);
#         font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
#         -webkit-font-smoothing: antialiased;
#         -moz-osx-font-smoothing: grayscale;
#     }

#     /* Logo Section - New Addition */
#     .logo-section {
#         background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
#         padding: 12px 20px;
#         text-align: center;
#         margin: -8px -8px 0 -8px;
#         border-bottom: 2px solid rgba(249, 115, 22, 0.3);
#     }

#     .jupiter-logo {
#         height: 32px;
#         width: auto;
#         filter: brightness(1.1);
#         transition: all 0.3s ease;
#     }

#     .jupiter-logo:hover {
#         transform: scale(1.05);
#         filter: brightness(1.2);
#     }

#     /* Enhanced Header - Mobile Optimized */
#     .chat-header {
#         background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
#         color: white;
#         padding: 16px 20px;
#         border-radius: 0 0 24px 24px;
#         text-align: center;
#         margin: 0 -8px 20px -8px;
#         box-shadow: 0 8px 32px rgba(249, 115, 22, 0.2);
#         position: sticky;
#         top: 0;
#         z-index: 100;
#         backdrop-filter: blur(10px);
#     }

#     .header-content {
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         gap: 12px;
#         max-width: 100%;
#     }

#     .header-logo {
#         width: 32px;
#         height: 32px;
#         background: rgba(255,255,255,0.2);
#         border-radius: 50%;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 18px;
#         animation: float 3s ease-in-out infinite;
#     }

#     @keyframes float {
#         0%, 100% { transform: translateY(0px); }
#         50% { transform: translateY(-4px); }
#     }

#     .header-title {
#         font-size: 20px;
#         font-weight: 700;
#         margin: 0;
#         letter-spacing: -0.5px;
#     }

#     .header-subtitle {
#         font-size: 12px;
#         opacity: 0.9;
#         color: #fef3c7;
#         margin-top: 2px;
#         font-weight: 400;
#     }

#     /* Enhanced Chat Container - Mobile First */
#     .chat-container {
#         max-width: 100%;
#         margin: 0 auto;
#         padding: 0 16px;
#         position: relative;
#     }

#     .chat-content {
#         min-height: 50vh;
#         max-height: 60vh;
#         overflow-y: auto;
#         padding: 8px 0;
#         scroll-behavior: smooth;
#         -webkit-overflow-scrolling: touch;
#     }

#     /* Enhanced Welcome Screen - Mobile Optimized */
#     .welcome-screen {
#         text-align: center;
#         padding: 32px 20px;
#         background: linear-gradient(135deg, #ffffff 0%, #fef7ff 100%);
#         border-radius: 20px;
#         box-shadow: 0 4px 20px rgba(0,0,0,0.06);
#         margin-bottom: 20px;
#         border: 1px solid rgba(249, 115, 22, 0.1);
#     }

#     .welcome-icon {
#         font-size: 56px;
#         margin-bottom: 16px;
#         animation: bounce 2s ease-in-out infinite;
#     }

#     @keyframes bounce {
#         0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
#         40% { transform: translateY(-8px); }
#         60% { transform: translateY(-4px); }
#     }

#     .welcome-title {
#         font-size: 22px;
#         font-weight: 700;
#         margin-bottom: 8px;
#         color: #1f2937;
#         letter-spacing: -0.5px;
#     }

#     .welcome-text {
#         font-size: 15px;
#         color: #6b7280;
#         margin-bottom: 24px;
#         line-height: 1.5;
#         max-width: 280px;
#         margin-left: auto;
#         margin-right: auto;
#     }

#     /* Enhanced Quick Buttons - Mobile First Grid */
#     .quick-buttons {
#         display: grid;
#         grid-template-columns: 1fr 1fr;
#         gap: 12px;
#         margin-top: 24px;
#     }

#     .stButton > button {
#         background: linear-gradient(135deg, #ffffff 0%, #fef7ff 100%) !important;
#         color: #f97316 !important;
#         border: 2px solid #f97316 !important;
#         border-radius: 16px !important;
#         padding: 14px 16px !important;
#         font-weight: 600 !important;
#         font-size: 13px !important;
#         transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
#         box-shadow: 0 2px 8px rgba(249, 115, 22, 0.15) !important;
#         width: 100% !important;
#         min-height: 48px !important;
#         touch-action: manipulation !important;
#         -webkit-tap-highlight-color: transparent !important;
#     }

#     .stButton > button:hover {
#         background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
#         color: white !important;
#         transform: translateY(-2px) scale(1.02) !important;
#         box-shadow: 0 6px 20px rgba(249, 115, 22, 0.3) !important;
#         border-color: #ea580c !important;
#     }

#     .stButton > button:active {
#         transform: translateY(0) scale(0.98) !important;
#         transition: all 0.1s ease !important;
#     }

#     /* Enhanced Message Bubbles - Mobile Optimized */
#     .message-wrapper {
#         margin-bottom: 16px;
#         animation: slideUp 0.3s ease-out;
#     }

#     @keyframes slideUp {
#         from { opacity: 0; transform: translateY(12px); }
#         to { opacity: 1; transform: translateY(0); }
#     }

#     .user-message {
#         display: flex;
#         justify-content: flex-end;
#         margin-bottom: 16px;
#     }

#     .bot-message {
#         display: flex;
#         justify-content: flex-start;
#         align-items: flex-start;
#         gap: 12px;
#         margin-bottom: 16px;
#     }

#     .user-bubble {
#         background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
#         color: white;
#         padding: 12px 16px;
#         border-radius: 20px 20px 6px 20px;
#         max-width: 85%;
#         font-size: 14px;
#         line-height: 1.4;
#         box-shadow: 0 2px 12px rgba(249, 115, 22, 0.25);
#         word-wrap: break-word;
#         font-weight: 500;
#     }

#     .bot-bubble {
#         background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
#         color: white;
#         padding: 12px 16px;
#         border-radius: 20px 20px 20px 6px;
#         max-width: 85%;
#         font-size: 14px;
#         line-height: 1.4;
#         box-shadow: 0 2px 12px rgba(20, 184, 166, 0.25);
#         word-wrap: break-word;
#         font-weight: 500;
#     }

#     .bot-avatar {
#         width: 36px;
#         height: 36px;
#         background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
#         border-radius: 50%;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 16px;
#         color: white;
#         flex-shrink: 0;
#         box-shadow: 0 2px 8px rgba(249, 115, 22, 0.3);
#         border: 2px solid rgba(255,255,255,0.2);
#     }

#     /* Enhanced Loading Animation */
#     .loading-message {
#         background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
#         color: #64748b;
#         padding: 12px 16px;
#         border-radius: 20px 20px 20px 6px;
#         display: flex;
#         align-items: center;
#         gap: 10px;
#         font-size: 13px;
#         font-style: italic;
#         border: 1px solid #e2e8f0;
#     }

#     .typing-dots {
#         display: flex;
#         gap: 4px;
#     }

#     .dot {
#         width: 6px;
#         height: 6px;
#         background: #14b8a6;
#         border-radius: 50%;
#         animation: pulse 1.4s infinite both;
#     }

#     .dot:nth-child(1) { animation-delay: -0.32s; }
#     .dot:nth-child(2) { animation-delay: -0.16s; }
#     .dot:nth-child(3) { animation-delay: 0s; }

#     @keyframes pulse {
#         0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
#         40% { transform: scale(1.2); opacity: 1; }
#     }

#     /* Enhanced Input Section - Mobile First */
#     .input-section {
#         position: sticky;
#         bottom: 0;
#         background: linear-gradient(135deg, #ffffff 0%, #fefefe 100%);
#         padding: 16px;
#         margin: 0 -16px -16px -16px;
#         border-top: 1px solid rgba(249, 115, 22, 0.1);
#         border-radius: 24px 24px 0 0;
#         box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
#         backdrop-filter: blur(10px);
#     }

#     .stForm {
#         border: none !important;
#         background: transparent !important;
#         padding: 0 !important;
#     }

#     /* Enhanced Input Field */
#     .stTextInput > div > div > input {
#         border: 2px solid #e5e7eb !important;
#         border-radius: 24px !important;
#         padding: 14px 20px !important;
#         font-size: 16px !important;
#         background: #f9fafb !important;
#         color: #1f2937 !important;
#         transition: all 0.2s ease !important;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
#         -webkit-appearance: none !important;
#         font-weight: 500 !important;
#     }

#     .stTextInput > div > div > input:focus {
#         border-color: #f97316 !important;
#         box-shadow: 0 0 0 4px rgba(249, 115, 22, 0.1) !important;
#         outline: none !important;
#         background: white !important;
#         transform: translateY(-1px) !important;
#     }

#     .stTextInput > div > div > input::placeholder {
#         color: #9ca3af !important;
#         font-size: 15px !important;
#         font-weight: 400 !important;
#     }

#     /* Enhanced Send Button */
#     .stFormSubmitButton > button {
#         background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
#         color: white !important;
#         border: none !important;
#         border-radius: 50% !important;
#         width: 48px !important;
#         height: 48px !important;
#         min-width: 48px !important;
#         min-height: 48px !important;
#         padding: 0 !important;
#         display: flex !important;
#         align-items: center !important;
#         justify-content: center !important;
#         font-size: 20px !important;
#         font-weight: bold !important;
#         transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
#         box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3) !important;
#         touch-action: manipulation !important;
#         -webkit-tap-highlight-color: transparent !important;
#     }

#     .stFormSubmitButton > button:hover {
#         transform: scale(1.05) translateY(-1px) !important;
#         box-shadow: 0 6px 16px rgba(249, 115, 22, 0.4) !important;
#     }

#     .stFormSubmitButton > button:active {
#         transform: scale(0.95) !important;
#         transition: all 0.1s ease !important;
#     }

#     .stFormSubmitButton > button::before {
#         content: "↑" !important;
#         font-size: 20px !important;
#         font-weight: bold !important;
#         color: white !important;
#     }

#     .stFormSubmitButton > button > div {
#         display: none !important;
#     }

#     /* Trust Indicators - Mobile Optimized */
#     .trust-section {
#         display: flex;
#         justify-content: center;
#         gap: 8px;
#         margin: 16px 0;
#         flex-wrap: wrap;
#     }

#         border-radius: 12px;
#         font-size: 12px;
#         font-weight: 600;
#         color: #1f2937;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.06);
#         display: flex;
#         align-items: center;
#         gap: 6px;
#         border: 1px solid rgba(249, 115, 22, 0.1);
#     }

#     .trust-icon {
#         font-size: 12px;
#         color: #f97316;
#     }

#     /* Enhanced Footer */
#     .footer {
#         text-align: center;
#         margin: 20px 0;
#         padding: 16px;
#         background: rgba(255,255,255,0.8);
#         border-radius: 16px;
#         box-shadow: 0 2px 12px rgba(0,0,0,0.04);
#         border: 1px solid rgba(249, 115, 22, 0.1);
#     }

#     .footer-text {
#         font-size: 14px;
#         color: #1f2937;
#         margin-bottom: 8px;
#         font-weight: 500;
#     }

#     .footer-links {
#         font-size: 12px;
#         color: #6b7280;
#     }

#     .footer-links a {
#         color: #f97316;
#         text-decoration: none;
#         font-weight: 600;
#     }

#     /* Enhanced Scrollbar */
#     .chat-content::-webkit-scrollbar {
#         width: 4px;
#     }

#     .chat-content::-webkit-scrollbar-track {
#         background: transparent;
#     }

#     .chat-content::-webkit-scrollbar-thumb {
#         background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
#         border-radius: 8px;
#     }

#     /* Tablet Styles */
#     @media (min-width: 768px) {
#         .logo-section {
#             margin: -16px -16px 0 -16px;
#             padding: 16px;
#         }

#         .jupiter-logo {
#             height: 36px;
#         }

#         .chat-header {
#             margin: 0 -16px 24px -16px;
#             padding: 20px;
#         }

#         .header-title {
#             font-size: 24px;
#         }

#         .chat-container {
#             max-width: 600px;
#             padding: 0 24px;
#         }

#         .chat-content {
#             max-height: 65vh;
#         }

#         .quick-buttons {
#             grid-template-columns: 1fr 1fr;
#             gap: 16px;
#         }

#         .user-bubble, .bot-bubble {
#             max-width: 80%;
#             font-size: 15px;
#         }

#         .input-section {
#             margin: 0 -24px -24px -24px;
#             padding: 20px 24px;
#         }
#     }

#     /* Desktop Styles */
#     @media (min-width: 1024px) {
#         .logo-section {
#             margin: -24px -24px 0 -24px;
#             padding: 20px;
#         }

#         .jupiter-logo {
#             height: 40px;
#         }

#         .chat-header {
#             margin: 0 -24px 32px -24px;
#             padding: 24px;
#         }

#         .header-title {
#             font-size: 26px;
#         }

#         .chat-container {
#             max-width: 700px;
#             padding: 0 32px;
#         }

#         .chat-content {
#             max-height: 70vh;
#         }

#         .quick-buttons {
#             grid-template-columns: repeat(2, 1fr);
#             gap: 20px;
#         }

#         .input-section {
#             margin: 0 -32px -32px -32px;
#             padding: 24px 32px;
#         }

#         .stButton > button:hover {
#             transform: translateY(-3px) scale(1.03) !important;
#         }
#     }

#     /* Remove default margins */
#     .element-container {
#         margin-bottom: 0 !important;
#     }

#     .stMarkdown {
#         margin-bottom: 0 !important;
#     }

#     /* Smooth transitions for all interactive elements */
#     * {
#         -webkit-tap-highlight-color: transparent;
#     }

#     button, input, .trust-badge, .message-wrapper {
#         transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
#     }
# </style>
# """, unsafe_allow_html=True)

# # ═══════════════════════════════════════════════════════════════════════════════════
# # HELPER FUNCTIONS
# # ═══════════════════════════════════════════════════════════════════════════════════

# def add_message(role: str, content: str):
#     """Add message to chat history"""
#     st.session_state.chat_history.append({"role": role, "content": content})

# def get_bot_response(question: str) -> str:
#     """Get response from chatbot with error handling"""
#     try:
#         response = query_jupiter(question, session_id=st.session_state.session_id)
#         return response.get("answer", "❌ Something went wrong. Please try again!")
#     except Exception as e:
#         st.error(f"Error: {str(e)}")
#         return "🚨 Sorry, I'm having technical difficulties. Please try again!"

# def handle_quick_question(question: str):
#     """Handle quick question button clicks"""
#     st.session_state.pending_message = question

# # Check for query parameters
# try:
#     query_params = dict(st.query_params)
#     if "msg" in query_params:
#         if query_params["msg"] and query_params["msg"] != st.session_state.pending_message:
#             st.session_state.pending_message = query_params["msg"]
#             del st.query_params["msg"]
# except Exception as e:
#     pass

# # ═══════════════════════════════════════════════════════════════════════════════════
# # MAIN UI COMPONENTS
# # ═══════════════════════════════════════════════════════════════════════════════════

# # Jupiter Logo Section - NEW
# st.markdown("""
# <div class="logo-section">
#     <img src="https://jupiter.money/assets/images/website-v2/jupiter-logo-white.svg"
#         alt="Jupiter Money Logo"
#         class="jupiter-logo">
# </div>
# """, unsafe_allow_html=True)

# # Enhanced Header
# st.markdown("""
# <div class="chat-header" style="background-color: #f5f5f5; padding: 20px; border-bottom: 1px solid #ddd;">
#     <div class="header-content" style="display: flex; align-items: center; gap: 15px;">
#         <div class="header-logo" style="font-size: 32px;">🚀</div>
#         <div>
#             <div class="header-title" style="font-size: 20px; font-weight: bold; color: #333;">Jupiter FAQ Assistant</div>
#             <div class="header-subtitle" style="font-size: 14px; color: #777;">Ask about accounts, cards, Jewels & more!</div>
#         </div>
#     </div>
#     <div class="scroll-message" style="text-align: center; margin-top: 15px; font-size: 14px; color: #555; animation: pulse 1.5s infinite;">
#         ⬇️ Scroll down to access the chatbot ⬇️
#     </div>
#     <style>
#         @keyframes pulse {
#             0% { opacity: 0.5; }
#             50% { opacity: 1; }
#             100% { opacity: 0.5; }
#         }
#     </style>
# </div>

# """, unsafe_allow_html=True)

# # Rest of your existing code remains the same...
# # Chat Container
# st.markdown('<div class="chat-container">', unsafe_allow_html=True)
# st.markdown('<div class="chat-content">', unsafe_allow_html=True)

# # Show welcome screen or chat history
# if not st.session_state.chat_history:
#     st.markdown("""
#     <div class="welcome-screen">
#         <div class="welcome-icon">🚀</div>
#         <div class="welcome-title">Welcome to Jupiter Support!</div>
#         <div class="welcome-text">
#             I'm your AI assistant for all Jupiter Money questions.
#             Choose a topic below or ask me anything!
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Enhanced Quick Questions
#     st.markdown('<h3 style="color: #f97316; text-align: center; margin: 24px 0 16px 0; font-size: 18px;">💡 Popular Questions</h3>', unsafe_allow_html=True)

#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("💳 Credit Card", key="card", use_container_width=True):
#             handle_quick_question("How do I apply for a Jupiter credit card?")
#             st.rerun()

#         if st.button("✅ KYC Process", key="kyc", use_container_width=True):
#             handle_quick_question("How do I complete KYC verification?")
#             st.rerun()

#     with col2:
#         if st.button("💎 Jupiter Jewels", key="jewels", use_container_width=True):
#             handle_quick_question("What are Jupiter Jewels and how do I earn them?")
#             st.rerun()

#         if st.button("⭐ Pro Benefits", key="pro", use_container_width=True):
#             handle_quick_question("What are the benefits of Jupiter Pro?")
#             st.rerun()

# else:
#     # Display chat history
#     for msg in st.session_state.chat_history:
#         if msg["role"] == "user":
#             st.markdown(f"""
#             <div class="message-wrapper">
#                 <div class="user-message">
#                     <div class="user-bubble">{msg['content']}</div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
#         else:
#             st.markdown(f"""
#             <div class="message-wrapper">
#                 <div class="bot-message">
#                     <div class="bot-avatar">🤖</div>
#                     <div class="bot-bubble">{msg['content']}</div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

#     # Show loading animation
#     if st.session_state.is_loading:
#         st.markdown("""
#         <div class="message-wrapper">
#             <div class="bot-message">
#                 <div class="bot-avatar">🤖</div>
#                 <div class="loading-message">
#                     <div class="typing-dots">
#                         <div class="dot"></div>
#                         <div class="dot"></div>
#                         <div class="dot"></div>
#                     </div>
#                     <span>Thinking...</span>
#                 </div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)

# # Enhanced Input Section
# st.markdown('<div class="input-section">', unsafe_allow_html=True)

# with st.form("chat_form", clear_on_submit=True, border=False):
#     col1, col2 = st.columns([5, 1])

#     with col1:
#         user_input = st.text_input(
#             "",
#             placeholder="Ask me anything about Jupiter Money...",
#             label_visibility="collapsed",
#             key="chat_input"
#         )

#     with col2:
#         send_clicked = st.form_submit_button("Send")

# st.markdown('</div>', unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)

# # Handle pending message from quick buttons
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
#             response = get_bot_response(last_message)
#             add_message("bot", response)
#         except Exception as e:
#             add_message("bot", "🚨 Sorry, I'm having technical difficulties. Please try again!")
#             st.error(f"Error processing request: {str(e)}")

#     st.session_state.is_loading = False
#     st.rerun()

# # Enhanced Trust Indicators
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
# </div>
# """, unsafe_allow_html=True)

# # Enhanced Footer
# st.markdown("""
# <div class="footer">
#     <div class="footer-text">
#         <strong>💡 Tip:</strong> Ask about account features, card benefits, or transactions!
#     </div>
#     <div class="footer-links">
#         Made with ❤️ for Jupiter users |
#         <a href="https://jupiter.money" target="_blank">jupiter.money</a>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Auto-scroll to bottom with smooth behavior
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



