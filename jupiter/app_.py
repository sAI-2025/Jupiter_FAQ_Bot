# # app.py

# import streamlit as st
# from chatbot import query_jupiter  # 🧠 Your chatbot logic lives here
# import uuid

# st.set_page_config(page_title="JupiterBot 💬", layout="centered")

# st.title("💬 Jupiter Support Chatbot")
# st.caption("Ask anything about your Jupiter account, card, Jewels, KYC, and more!")

# # Unique session ID per user/chat
# if "session_id" not in st.session_state:
#     st.session_state.session_id = str(uuid.uuid4())

# # Chat message history UI
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Chat input UI
# with st.form("chat_form", clear_on_submit=True):
#     user_input = st.text_input("Ask JupiterBot a question", placeholder="e.g., How do I activate my card?")
#     submitted = st.form_submit_button("Send")

# # Handle the query
# if submitted and user_input:
#     # Add user input to chat
#     st.session_state.chat_history.append({"role": "user", "content": user_input})

#     # Show typing spinner
#     with st.spinner("Thinking..."):
#         result = query_jupiter(user_input, session_id=st.session_state.session_id)
#         bot_reply = result.get("answer", "❌ Something went wrong.")
#         st.session_state.chat_history.append({"role": "bot", "content": bot_reply})

# # Display chat messages
# for message in st.session_state.chat_history:
#     if message["role"] == "user":
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(message["content"])
#     else:
#         with st.chat_message("assistant", avatar="🤖"):
#             st.markdown(message["content"])
#








#======================================================================
# app.py
# import streamlit as st
# import uuid
# import time
# from chatbot import query_jupiter

# # ═══════════════════════════════════════════════════════════════════════════════════
# # PAGE CONFIGURATION & SESSION STATE INITIALIZATION
# # ═══════════════════════════════════════════════════════════════════════════════════

# st.set_page_config(
#     page_title="Jupiter FAQ Assistant 🚀",
#     page_icon="🚀",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # Initialize session state variables
# def init_session_state():
#     """Initialize all session state variables"""
#     if "session_id" not in st.session_state:
#         st.session_state.session_id = str(uuid.uuid4())

#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     if "show_welcome" not in st.session_state:
#         st.session_state.show_welcome = True

#     if "is_loading" not in st.session_state:
#         st.session_state.is_loading = False

# init_session_state()

# # ═══════════════════════════════════════════════════════════════════════════════════
# # ENHANCED CSS STYLING WITH ALL IMPROVEMENTS
# # ═══════════════════════════════════════════════════════════════════════════════════

# st.markdown("""
# <style>
#     /* Import fonts and icons */
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
#     @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');

#     /* Hide Streamlit default elements */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
#     .stDeployButton {display: none;}

#     /* Global app styling */
#     .stApp {
#         background: linear-gradient(135deg, #f6e1a2 0%, #ffffff 40%, #e8f4f8 100%);
#         font-family: 'Inter', sans-serif;
#     }

#     /* HEADER IMPROVEMENTS - Step 1 & 2 */
#     .enhanced-header {
#         background: linear-gradient(135deg, #1e3a5c 0%, #4a8cb5 50%, #5bb4d4 100%);
#         color: white;
#         padding: 28px 25px;
#         border-radius: 0 0 30px 30px;
#         text-align: center;
#         margin-bottom: 25px;
#         box-shadow: 0 6px 25px rgba(30, 58, 92, 0.3);
#         position: relative;
#         overflow: hidden;
#     }

#     .enhanced-header::before {
#         content: '';
#         position: absolute;
#         top: 0;
#         left: 0;
#         right: 0;
#         bottom: 0;
#         background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 20"><defs><radialGradient id="a"><stop offset="20%" stop-color="%23ffffff" stop-opacity="0.1"/><stop offset="100%" stop-color="%23ffffff" stop-opacity="0"/></radialGradient></defs><rect width="100" height="20" fill="url(%23a)"/></svg>');
#         pointer-events: none;
#     }

#     .header-content {
#         position: relative;
#         z-index: 2;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         gap: 15px;
#     }

#     .header-icon {
#         font-size: 32px;
#         filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3));
#         animation: pulse 2s ease-in-out infinite alternate;
#     }

#     @keyframes pulse {
#         0% { transform: scale(1); filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3)); }
#         100% { transform: scale(1.05); filter: drop-shadow(0 4px 12px rgba(77, 219, 183, 0.4)); }
#     }

#     .header-text {
#         display: flex;
#         flex-direction: column;
#         align-items: flex-start;
#         text-align: left;
#     }

#     .header-title {
#         font-size: 30px;
#         font-weight: 700;
#         margin: 0;
#         color: white;
#         text-shadow: 0 2px 4px rgba(0,0,0,0.2);
#     }

#     .header-subtitle {
#         font-size: 16px;
#         opacity: 0.9;
#         color: #4ddbb7;
#         margin: 4px 0 0 0;
#         font-weight: 500;
#     }

#     /* CHAT AREA IMPROVEMENTS - Step 3 */
#     .enhanced-chat-container {
#         background: #f8f9fa;
#         border-radius: 25px;
#         padding: 30px 25px;
#         margin: 0 20px 25px 20px;
#         min-height: 480px;
#         max-height: 550px;
#         overflow-y: auto;
#         scroll-behavior: smooth;
#         box-shadow: 0 10px 40px rgba(0,0,0,0.08);
#         border: 2px solid rgba(255,255,255,0.6);
#         position: relative;
#     }

#     .enhanced-chat-container::before {
#         content: '';
#         position: absolute;
#         top: 0;
#         left: 0;
#         right: 0;
#         bottom: 0;
#         background: linear-gradient(145deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
#         border-radius: 25px;
#         pointer-events: none;
#     }

#     /* Welcome screen enhancements */
#     .welcome-area {
#         text-align: center;
#         padding: 35px 25px;
#         color: #1e3a5c;
#         position: relative;
#         z-index: 2;
#     }

#     .welcome-icon {
#         font-size: 75px;
#         margin-bottom: 25px;
#         animation: float 4s ease-in-out infinite;
#         display: block;
#         filter: drop-shadow(0 4px 8px rgba(241, 132, 59, 0.2));
#     }

#     @keyframes float {
#         0%, 100% { transform: translateY(0px) rotate(0deg); }
#         33% { transform: translateY(-8px) rotate(2deg); }
#         66% { transform: translateY(-4px) rotate(-1deg); }
#     }

#     .welcome-title {
#         font-size: 26px;
#         font-weight: 700;
#         margin-bottom: 12px;
#         color: #1e3a5c;
#         text-shadow: 0 1px 2px rgba(0,0,0,0.1);
#     }

#     .welcome-description {
#         font-size: 17px;
#         opacity: 0.8;
#         margin-bottom: 30px;
#         line-height: 1.6;
#         max-width: 400px;
#         margin-left: auto;
#         margin-right: auto;
#     }

#     /* BUTTON IMPROVEMENTS - Step 4 */
#     .quick-questions-grid {
#         display: grid;
#         grid-template-columns: 1fr 1fr;
#         gap: 15px;
#         margin-top: 25px;
#     }

#     .stButton > button {
#         background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
#         color: #1e3a5c !important;
#         border: 2px solid #f1843b !important;
#         border-radius: 25px !important;
#         padding: 16px 20px !important;
#         font-weight: 600 !important;
#         font-size: 14px !important;
#         transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
#         box-shadow: 0 4px 15px rgba(241, 132, 59, 0.15) !important;
#         width: 100% !important;
#         height: auto !important;
#         min-height: 55px !important;
#         display: flex !important;
#         align-items: center !important;
#         justify-content: center !important;
#         text-align: center !important;
#         line-height: 1.3 !important;
#         position: relative !important;
#         overflow: hidden !important;
#     }

#     .stButton > button::before {
#         content: '';
#         position: absolute;
#         top: 0;
#         left: -100%;
#         width: 100%;
#         height: 100%;
#         background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
#         transition: left 0.5s;
#     }

#     .stButton > button:hover {
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%) !important;
#         color: white !important;
#         transform: translateY(-3px) scale(1.02) !important;
#         box-shadow: 0 8px 25px rgba(241, 132, 59, 0.4) !important;
#         border-color: #f1843b !important;
#     }

#     .stButton > button:hover::before {
#         left: 100%;
#     }

#     .stButton > button:active {
#         transform: translateY(-1px) scale(1.01) !important;
#         transition: all 0.1s !important;
#     }

#     /* Send button special styling */
#     .send-button > button {
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%) !important;
#         color: white !important;
#         border: none !important;
#         border-radius: 25px !important;
#         padding: 14px 25px !important;
#         font-weight: 700 !important;
#         font-size: 15px !important;
#         box-shadow: 0 4px 20px rgba(241, 132, 59, 0.4) !important;
#         position: relative !important;
#         overflow: hidden !important;
#     }

#     .send-button > button:hover {
#         transform: translateY(-2px) scale(1.05) !important;
#         box-shadow: 0 6px 25px rgba(241, 132, 59, 0.5) !important;
#     }

#     .send-button > button::after {
#         content: '✈️';
#         margin-left: 8px;
#     }

#     /* Message bubbles improvements */
#     .message-wrapper {
#         margin-bottom: 20px;
#         animation: messageSlide 0.5s cubic-bezier(0.4, 0, 0.2, 1);
#         position: relative;
#         z-index: 2;
#     }

#     @keyframes messageSlide {
#         from {
#             opacity: 0;
#             transform: translateY(20px) scale(0.95);
#         }
#         to {
#             opacity: 1;
#             transform: translateY(0) scale(1);
#         }
#     }

#     .user-message-container {
#         display: flex;
#         justify-content: flex-end;
#         margin-bottom: 18px;
#     }

#     .bot-message-container {
#         display: flex;
#         justify-content: flex-start;
#         align-items: flex-start;
#         gap: 15px;
#         margin-bottom: 18px;
#     }

#     .user-bubble {
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%);
#         color: white;
#         padding: 16px 22px;
#         border-radius: 25px 25px 8px 25px;
#         max-width: 75%;
#         word-wrap: break-word;
#         font-size: 15px;
#         line-height: 1.5;
#         box-shadow: 0 4px 15px rgba(241, 132, 59, 0.3);
#         position: relative;
#         font-weight: 500;
#     }

#     .bot-bubble {
#         background: linear-gradient(135deg, #4ddbb7 0%, #42c9a7 100%);
#         color: white;
#         padding: 16px 22px;
#         border-radius: 25px 25px 25px 8px;
#         max-width: 75%;
#         word-wrap: break-word;
#         font-size: 15px;
#         line-height: 1.5;
#         box-shadow: 0 4px 15px rgba(77, 219, 183, 0.3);
#         position: relative;
#         font-weight: 500;
#     }

#     .enhanced-bot-avatar {
#         width: 42px;
#         height: 42px;
#         background: linear-gradient(135deg, #1e3a5c 0%, #4a8cb5 100%);
#         border-radius: 50%;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 18px;
#         flex-shrink: 0;
#         color: white;
#         margin-top: 2px;
#         box-shadow: 0 3px 12px rgba(30, 58, 92, 0.3);
#         border: 3px solid rgba(255,255,255,0.9);
#     }

#     /* Loading indicator inside chat */
#     .loading-bubble {
#         background: linear-gradient(135deg, #e9ecef 0%, #f8f9fa 100%);
#         color: #6c757d;
#         padding: 16px 22px;
#         border-radius: 25px 25px 25px 8px;
#         max-width: 200px;
#         display: flex;
#         align-items: center;
#         gap: 10px;
#         font-size: 14px;
#         font-style: italic;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#     }

#     .typing-animation {
#         display: flex;
#         gap: 4px;
#     }

#     .typing-dot {
#         width: 8px;
#         height: 8px;
#         background: #4ddbb7;
#         border-radius: 50%;
#         animation: typingBounce 1.4s infinite both;
#     }

#     .typing-dot:nth-child(1) { animation-delay: -0.32s; }
#     .typing-dot:nth-child(2) { animation-delay: -0.16s; }
#     .typing-dot:nth-child(3) { animation-delay: 0s; }

#     @keyframes typingBounce {
#         0%, 80%, 100% {
#             transform: scale(0.8);
#             opacity: 0.5;
#         }
#         40% {
#             transform: scale(1.2);
#             opacity: 1;
#         }
#     }

#     /* INPUT BOX IMPROVEMENTS - Step 5 */
#     .enhanced-input-section {
#         padding: 20px;
#         margin: 0 20px;
#         background: rgba(255,255,255,0.95);
#         border-radius: 25px;
#         box-shadow: 0 8px 32px rgba(0,0,0,0.1);
#         border: 2px solid rgba(241, 132, 59, 0.1);
#         backdrop-filter: blur(10px);
#     }

#     .stTextInput > div > div > input {
#         border: 2px solid #e9ecef !important;
#         border-radius: 20px !important;
#         padding: 16px 24px !important;
#         font-size: 16px !important;
#         background: white !important;
#         color: #1e3a5c !important;
#         transition: all 0.3s ease !important;
#         box-shadow: inset 0 2px 4px rgba(0,0,0,0.05) !important;
#     }

#     .stTextInput > div > div > input:focus {
#         border-color: #f1843b !important;
#         box-shadow: 0 0 0 4px rgba(241, 132, 59, 0.1), inset 0 2px 4px rgba(0,0,0,0.05) !important;
#         outline: none !important;
#         transform: translateY(-1px) !important;
#     }

#     .stTextInput > div > div > input::placeholder {
#         color: #9ca3af !important;
#         font-style: italic !important;
#     }

#     /* TRUST INDICATORS & FOOTER - Step 6 */
#     .enhanced-trust-section {
#         display: flex;
#         justify-content: center;
#         gap: 20px;
#         margin: 25px 20px;
#         flex-wrap: wrap;
#     }

#     .trust-badge {
#         background: rgba(255,255,255,0.95);
#         padding: 12px 18px;
#         border-radius: 20px;
#         font-size: 13px;
#         font-weight: 600;
#         color: #1e3a5c;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.08);
#         border: 1px solid rgba(241, 132, 59, 0.15);
#         display: flex;
#         align-items: center;
#         gap: 8px;
#         transition: all 0.3s ease;
#         backdrop-filter: blur(5px);
#     }

#     .trust-badge:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.12);
#     }

#     .trust-icon {
#         font-size: 14px;
#         color: #f1843b;
#     }

#     .enhanced-footer {
#         text-align: center;
#         margin: 30px 20px 20px 20px;
#         padding: 25px;
#         background: rgba(255,255,255,0.8);
#         border-radius: 20px;
#         box-shadow: 0 4px 20px rgba(0,0,0,0.05);
#         backdrop-filter: blur(10px);
#     }

#     .footer-tip {
#         font-size: 15px;
#         color: #1e3a5c;
#         margin-bottom: 12px;
#         font-weight: 600;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         gap: 8px;
#     }

#     .footer-links {
#         font-size: 13px;
#         color: #6c757d;
#         font-weight: 500;
#     }

#     .footer-links a {
#         color: #f1843b;
#         text-decoration: none;
#         font-weight: 600;
#         transition: all 0.3s ease;
#     }

#     .footer-links a:hover {
#         color: #ff6b35;
#         text-decoration: underline;
#     }

#     /* MOBILE RESPONSIVENESS IMPROVEMENTS */
#     @media (max-width: 768px) {
#         .enhanced-header {
#             margin: -8px -8px 20px -8px;
#             border-radius: 0 0 25px 25px;
#             padding: 22px 20px;
#         }

#         .header-icon {
#             font-size: 28px;
#         }

#         .header-title {
#             font-size: 24px;
#         }

#         .header-subtitle {
#             font-size: 14px;
#         }

#         .enhanced-chat-container {
#             margin: 0 15px 20px 15px;
#             padding: 25px 20px;
#             border-radius: 20px;
#             min-height: 400px;
#             max-height: 450px;
#         }

#         .quick-questions-grid {
#             grid-template-columns: 1fr;
#             gap: 12px;
#         }

#         .user-bubble, .bot-bubble {
#             max-width: 85%;
#             font-size: 14px;
#             padding: 14px 18px;
#         }

#         .welcome-icon {
#             font-size: 60px;
#         }

#         .welcome-title {
#             font-size: 22px;
#         }

#         .welcome-description {
#             font-size: 15px;
#         }

#         .enhanced-trust-section {
#             gap: 12px;
#             margin: 20px 15px;
#         }

#         .trust-badge {
#             font-size: 12px;
#             padding: 10px 14px;
#         }

#         .enhanced-footer {
#             margin: 25px 15px 15px 15px;
#             padding: 20px;
#         }

#         .footer-tip {
#             font-size: 13px;
#         }

#         .enhanced-input-section {
#             margin: 0 15px;
#             padding: 18px;
#         }
#     }

#     /* SCROLLBAR STYLING */
#     .enhanced-chat-container::-webkit-scrollbar {
#         width: 8px;
#     }

#     .enhanced-chat-container::-webkit-scrollbar-track {
#         background: rgba(255,255,255,0.3);
#         border-radius: 10px;
#     }

#     .enhanced-chat-container::-webkit-scrollbar-thumb {
#         background: linear-gradient(135deg, #4ddbb7, #42c9a7);
#         border-radius: 10px;
#         border: 2px solid rgba(255,255,255,0.3);
#     }

#     .enhanced-chat-container::-webkit-scrollbar-thumb:hover {
#         background: linear-gradient(135deg, #42c9a7, #39b89c);
#     }
# </style>
# """, unsafe_allow_html=True)

# # ═══════════════════════════════════════════════════════════════════════════════════
# # HELPER FUNCTIONS FOR BETTER CODE ORGANIZATION
# # ═══════════════════════════════════════════════════════════════════════════════════

# def add_message_to_chat(role: str, content: str):
#     """Add a message to chat history"""
#     st.session_state.chat_history.append({"role": role, "content": content})

# def get_bot_response(user_question: str) -> str:
#     """Get response from Jupiter chatbot with error handling"""
#     try:
#         response = query_jupiter(user_question, session_id=st.session_state.session_id)
#         return response.get("answer", "❌ Something went wrong. Please try again!")
#     except Exception as e:
#         return "🚨 Sorry, I'm experiencing some technical difficulties. Please try again!"

# def handle_quick_question(question: str):
#     """Handle quick question button clicks"""
#     st.session_state.show_welcome = False
#     add_message_to_chat("user", question)

#     # Show loading state
#     st.session_state.is_loading = True

#     # Get response
#     response = get_bot_response(question)
#     add_message_to_chat("bot", response)

#     # Clear loading state
#     st.session_state.is_loading = False

# def display_loading_bubble():
#     """Display loading animation in chat"""
#     return """
#     <div class="bot-message-container">
#         <div class="enhanced-bot-avatar">🤖</div>
#         <div class="loading-bubble">
#             <div class="typing-animation">
#                 <div class="typing-dot"></div>
#                 <div class="typing-dot"></div>
#                 <div class="typing-dot"></div>
#             </div>
#             <span>Jupiter AI is thinking...</span>
#         </div>
#     </div>
#     """

# # ═══════════════════════════════════════════════════════════════════════════════════
# # MAIN UI COMPONENTS
# # ═══════════════════════════════════════════════════════════════════════════════════

# # Enhanced Header with Icon
# st.markdown("""
# <div class="enhanced-header">
#     <div class="header-content">
#         <div class="header-icon">🚀</div>
#         <div class="header-text">
#             <div class="header-title">Jupiter FAQ Assistant</div>
#             <div class="header-subtitle">Ask about accounts, cards, Jewels, KYC & more!</div>
#         </div>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Main Chat Container
# with st.container():
#     st.markdown('<div class="enhanced-chat-container">', unsafe_allow_html=True)

#     # Welcome Screen or Chat History
#     if not st.session_state.chat_history and st.session_state.show_welcome:
#         # Enhanced Welcome Screen
#         st.markdown("""
#         <div class="welcome-area">
#             <div class="welcome-icon">🚀</div>
#             <div class="welcome-title">Welcome to Jupiter Support!</div>
#             <div class="welcome-description">
#                 I'm your AI assistant, ready to help with all Jupiter Money questions.
#                 Pick a topic below or ask me anything!
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#         # Enhanced Quick Questions with Better Layout
#         st.markdown("### 💡 Popular Questions")

#         # Use columns for better button layout
#         col1, col2 = st.columns(2, gap="medium")

#         with col1:
#             if st.button("💳 Credit Card Application", key="q1", help="Learn how to apply for Jupiter credit card"):
#                 handle_quick_question("How do I apply for a Jupiter credit card?")
#                 st.rerun()

#             if st.button("✅ KYC Verification", key="q3", help="Complete your KYC process"):
#                 handle_quick_question("How do I complete my KYC verification?")
#                 st.rerun()

#         with col2:
#             if st.button("💎 Jupiter Jewels", key="q2", help="Learn about earning Jewels"):
#                 handle_quick_question("What are Jupiter Jewels and how do I earn them?")
#                 st.rerun()

#             if st.button("⭐ Jupiter Pro Benefits", key="q4", help="Discover Pro membership perks"):
#                 handle_quick_question("What are the benefits of Jupiter Pro?")
#                 st.rerun()

#     else:
#         # Display Enhanced Chat History
#         for i, msg in enumerate(st.session_state.chat_history):
#             if msg["role"] == "user":
#                 st.markdown(f"""
#                 <div class="message-wrapper">
#                     <div class="user-message-container">
#                         <div class="user-bubble">{msg['content']}</div>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
#             else:
#                 st.markdown(f"""
#                 <div class="message-wrapper">
#                     <div class="bot-message-container">
#                         <div class="enhanced-bot-avatar">🤖</div>
#                         <div class="bot-bubble">{msg['content']}</div>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)

#         # Show loading animation if processing
#         if st.session_state.is_loading:
#             st.markdown(display_loading_bubble(), unsafe_allow_html=True)

#     st.markdown('</div>', unsafe_allow_html=True)

# # Enhanced Input Section
# st.markdown('<div class="enhanced-input-section">', unsafe_allow_html=True)

# # Input Form with Better UX
# with st.form("enhanced_chat_form", clear_on_submit=True):
#     col1, col2 = st.columns([4, 1], gap="medium")

#     with col1:
#         user_input = st.text_input(
#             "",
#             placeholder="Ask me anything about Jupiter Money...",
#             label_visibility="collapsed",
#             help="Type your question and press Enter or click Send"
#         )

#     with col2:
#         st.markdown('<div class="send-button">', unsafe_allow_html=True)
#         send_button = st.form_submit_button("Send", use_container_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)

# # Handle Form Submission with Better UX
# if send_button and user_input:
#     # Hide welcome screen
#     st.session_state.show_welcome = False

#     # Add user message
#     add_message_to_chat("user", user_input)

#     # Set loading state
#     st.session_state.is_loading = True

#     # Rerun to show user message and loading animation
#     st.rerun()

# # Process bot response if loading
# if st.session_state.is_loading and st.session_state.chat_history:
#     # Simulate thinking time for better UX
#     time.sleep(0.3)

#     # Get the last user message
#     last_message = st.session_state.chat_history[-1]["content"]

#     # Get bot response
#     with st.spinner(""):  # Hidden spinner since we show loading in chat
#         response = get_bot_response(last_message)
#         add_message_to_chat("bot", response)

#     # Clear loading state
#     st.session_state.is_loading = False

#     # Rerun to show bot response
#     st.rerun()

# # Enhanced Trust Indicators
# st.markdown("""
# <div class="enhanced-trust-section">
#     <div class="trust-badge">
#         <i class="fas fa-lock trust-icon"></i>
#         <span>Secure & Encrypted</span>
#     </div>
#     <div class="trust-badge">
#         <i class="fas fa-bolt trust-icon"></i>
#         <span>Instant Responses</span>
#     </div>
#     <div class="trust-badge">
#         <i class="fas fa-shield-alt trust-icon"></i>
#         <span>RBI Regulated</span>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Enhanced Footer
# st.markdown("""
# <div class="enhanced-footer">
#     <div class="footer-tip">
#         <i class="fas fa-lightbulb" style="color: #f1843b;"></i>
#         <strong>Tip:</strong> Try asking about account features, card benefits, or transaction queries!
#     </div>
#     <div class="footer-links">
#         Made with ❤️ for Jupiter Money users |
#         <a href="https://jupiter.money" target="_blank">Visit Jupiter.money</a>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Auto-scroll JavaScript
# st.markdown("""
# <script>
#     const chatContainer = document.querySelector('.chat-container');
#     chatContainer.scrollTop = chatContainer.scrollHeight;
# </script>
# """, unsafe_allow_html=True)
# CSS to style the submit button as circular




# import streamlit as st
# import uuid
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

# init_session_state()

# # ═══════════════════════════════════════════════════════════════════════════════════
# # ENHANCED CSS STYLING WITH CHATGPT-STYLE INPUT
# # ═══════════════════════════════════════════════════════════════════════════════════

# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

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

#     /* Header with icon */
#     .chat-header {
#         background: linear-gradient(135deg, #1e3a5c 0%, #4a8cb5 100%);
#         color: white;
#         padding: 20px;
#         border-radius: 0 0 20px 20px;
#         text-align: center;
#         margin-bottom: 20px;
#         box-shadow: 0 4px 20px rgba(30, 58, 92, 0.3);
#         position: relative;
#     }

#     .header-content {
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         gap: 12px;
#     }

#     .header-icon {
#         font-size: 24px;
#         animation: pulse 2s ease-in-out infinite alternate;
#     }

#     @keyframes pulse {
#         0% { transform: scale(1); }
#         100% { transform: scale(1.05); }
#     }

#     .header-title {
#         font-size: 22px;
#         font-weight: 700;
#         margin: 0;
#     }

#     .header-subtitle {
#         font-size: 13px;
#         opacity: 0.9;
#         color: #4ddbb7;
#         margin-top: 4px;
#     }

#     /* Chat content - NO CONTAINER */
#     .chat-content {
#         margin: 0 16px 16px 16px;
#         min-height: 300px;
#         max-height: 400px;
#         overflow-y: auto;
#         scroll-behavior: smooth;
#     }

#     /* Welcome screen */
#     .welcome-screen {
#         text-align: center;
#         padding: 24px 16px;
#         color: #1e3a5c;
#         background: white;
#         border-radius: 16px;
#         box-shadow: 0 6px 24px rgba(0,0,0,0.08);
#         margin-bottom: 20px;
#     }

#     .welcome-icon {
#         font-size: 48px;
#         margin-bottom: 12px;
#         animation: float 3s ease-in-out infinite;
#     }

#     @keyframes float {
#         0%, 100% { transform: translateY(0px); }
#         50% { transform: translateY(-6px); }
#     }

#     .welcome-title {
#         font-size: 20px;
#         font-weight: 700;
#         margin-bottom: 6px;
#         color: #1e3a5c;
#     }

#     .welcome-text {
#         font-size: 14px;
#         opacity: 0.8;
#         margin-bottom: 20px;
#         line-height: 1.4;
#     }

#     /* Quick question buttons */
#     .quick-buttons {
#         display: grid;
#         grid-template-columns: 1fr 1fr;
#         gap: 10px;
#         margin-top: 20px;
#     }

#     .stButton > button {
#         background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
#         color: #1e3a5c !important;
#         border: 2px solid #f1843b !important;
#         border-radius: 16px !important;
#         padding: 10px 14px !important;
#         font-weight: 600 !important;
#         font-size: 13px !important;
#         transition: all 0.3s ease !important;
#         box-shadow: 0 3px 10px rgba(241, 132, 59, 0.15) !important;
#         width: 100% !important;
#         min-height: 42px !important;
#     }

#     .stButton > button:hover {
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%) !important;
#         color: white !important;
#         transform: translateY(-1px) scale(1.02) !important;
#         box-shadow: 0 5px 16px rgba(241, 132, 59, 0.3) !important;
#     }

#     /* Message bubbles */
#     .message-wrapper {
#         margin-bottom: 12px;
#         animation: slideIn 0.3s ease-out;
#     }

#     @keyframes slideIn {
#         from { opacity: 0; transform: translateY(8px); }
#         to { opacity: 1; transform: translateY(0); }
#     }

#     .user-message {
#         display: flex;
#         justify-content: flex-end;
#         margin-bottom: 12px;
#     }

#     .bot-message {
#         display: flex;
#         justify-content: flex-start;
#         align-items: flex-start;
#         gap: 10px;
#         margin-bottom: 12px;
#     }

#     .user-bubble {
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%);
#         color: white;
#         padding: 10px 14px;
#         border-radius: 18px 18px 4px 18px;
#         max-width: 80%;
#         font-size: 14px;
#         line-height: 1.4;
#         box-shadow: 0 2px 6px rgba(241, 132, 59, 0.25);
#     }

#     .bot-bubble {
#         background: linear-gradient(135deg, #4ddbb7 0%, #42c9a7 100%);
#         color: white;
#         padding: 10px 14px;
#         border-radius: 18px 18px 18px 4px;
#         max-width: 80%;
#         font-size: 14px;
#         line-height: 1.4;
#         box-shadow: 0 2px 6px rgba(77, 219, 183, 0.25);
#     }

#     .bot-avatar {
#         width: 32px;
#         height: 32px;
#         background: linear-gradient(135deg, #1e3a5c 0%, #4a8cb5 100%);
#         border-radius: 50%;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 14px;
#         color: white;
#         flex-shrink: 0;
#         box-shadow: 0 2px 6px rgba(30, 58, 92, 0.25);
#     }

#     /* Loading animation */
#     .loading-message {
#         background: #f8f9fa;
#         color: #6c757d;
#         padding: 10px 14px;
#         border-radius: 18px 18px 18px 4px;
#         display: flex;
#         align-items: center;
#         gap: 8px;
#         font-size: 13px;
#         font-style: italic;
#     }

#     .typing-dots {
#         display: flex;
#         gap: 3px;
#     }

#     .dot {
#         width: 5px;
#         height: 5px;
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

#     /* CHATGPT-STYLE INPUT SECTION */
#     .input-section {
#         padding: 12px 16px;
#         margin: 0 16px 16px 16px;
#         background: white;
#         border-radius: 24px;
#         box-shadow: 0 4px 16px rgba(0,0,0,0.08);
#         border: 1px solid rgba(241, 132, 59, 0.1);
#         position: relative;
#     }

#     /* Hide default streamlit form styling */
#     .stForm {
#         border: none !important;
#         background: transparent !important;
#         padding: 0 !important;
#     }

#     /* CHATGPT-STYLE CONTENTEDITABLE INPUT */
#     .chatgpt-input-container {
#         position: relative;
#         display: flex;
#         align-items: end;
#         gap: 8px;
#         min-height: 48px;
#     }

#     .chatgpt-input {
#         flex: 1;
#         min-height: 24px;
#         max-height: 200px;
#         padding: 12px 16px;
#         border: 2px solid #e9ecef;
#         border-radius: 24px;
#         font-size: 15px;
#         font-family: 'Inter', sans-serif;
#         background: #f8f9fa;
#         color: #1e3a5c;
#         outline: none;
#         resize: none;
#         overflow-y: auto;
#         line-height: 1.4;
#         transition: all 0.3s ease;
#         word-wrap: break-word;
#         white-space: pre-wrap;
#     }

#     .chatgpt-input:focus {
#         border-color: #f1843b;
#         box-shadow: 0 0 0 3px rgba(241, 132, 59, 0.1);
#         background: white;
#     }

#     .chatgpt-input:empty::before {
#         content: "Ask me anything about Jupiter Money...";
#         color: #9ca3af;
#         pointer-events: none;
#         position: absolute;
#     }

#     .chatgpt-input:focus::before {
#         display: none;
#     }

#     /* CIRCULAR SEND BUTTON */
#     .send-button {
#         width: 48px;
#         height: 48px;
#         border-radius: 50%;
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%);
#         border: none;
#         color: white;
#         font-size: 18px;
#         font-weight: bold;
#         cursor: pointer;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         transition: all 0.2s ease;
#         box-shadow: 0 2px 8px rgba(241, 132, 59, 0.3);
#         flex-shrink: 0;
#     }

#     .send-button:hover {
#         transform: scale(1.05);
#         box-shadow: 0 4px 12px rgba(241, 132, 59, 0.4);
#     }

#     .send-button:active {
#         transform: scale(0.95);
#     }

#     .send-button:disabled {
#         background: #e9ecef;
#         color: #9ca3af;
#         cursor: not-allowed;
#         transform: none;
#         box-shadow: none;
#     }

#     /* Hide streamlit input completely */
#     .stTextInput {
#         display: none !important;
#     }

#     .stFormSubmitButton {
#         display: none !important;
#     }

#     /* Trust indicators */
#     .trust-section {
#         display: flex;
#         justify-content: center;
#         gap: 12px;
#         margin: 12px;
#         flex-wrap: wrap;
#     }

#     .trust-badge {
#         background: rgba(255,255,255,0.9);
#         padding: 6px 10px;
#         border-radius: 10px;
#         font-size: 11px;
#         font-weight: 600;
#         color: #1e3a5c;
#         box-shadow: 0 2px 6px rgba(0,0,0,0.08);
#         display: flex;
#         align-items: center;
#         gap: 4px;
#     }

#     .trust-icon {
#         font-size: 11px;
#         color: #f1843b;
#     }

#     /* Footer */
#     .footer {
#         text-align: center;
#         margin: 20px 16px 16px 16px;
#         padding: 12px;
#         background: rgba(255,255,255,0.8);
#         border-radius: 12px;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#     }

#     .footer-text {
#         font-size: 13px;
#         color: #1e3a5c;
#         margin-bottom: 6px;
#     }

#     .footer-links {
#         font-size: 11px;
#         color: #6c757d;
#     }

#     .footer-links a {
#         color: #f1843b;
#         text-decoration: none;
#         font-weight: 600;
#     }

#     /* Mobile responsiveness */
#     @media (max-width: 768px) {
#         .chat-header {
#             margin: -8px -8px 16px -8px;
#             border-radius: 0 0 16px 16px;
#             padding: 16px;
#         }

#         .header-title {
#             font-size: 20px;
#         }

#         .chat-content {
#             margin: 0 8px 12px 8px;
#             max-height: 300px;
#             min-height: 250px;
#         }

#         .quick-buttons {
#             grid-template-columns: 1fr;
#         }

#         .user-bubble, .bot-bubble {
#             max-width: 90%;
#             font-size: 13px;
#         }

#         .input-section {
#             margin: 0 8px 8px 8px;
#         }

#         .chatgpt-input {
#             font-size: 14px;
#         }

#         .send-button {
#             width: 44px;
#             height: 44px;
#             font-size: 16px;
#         }
#     }

#     /* Scrollbar */
#     .chat-content::-webkit-scrollbar {
#         width: 4px;
#     }

#     .chat-content::-webkit-scrollbar-track {
#         background: #f1f1f1;
#         border-radius: 8px;
#     }

#     .chat-content::-webkit-scrollbar-thumb {
#         background: #4ddbb7;
#         border-radius: 8px;
#     }

#     .chatgpt-input::-webkit-scrollbar {
#         width: 4px;
#     }

#     .chatgpt-input::-webkit-scrollbar-track {
#         background: transparent;
#     }

#     .chatgpt-input::-webkit-scrollbar-thumb {
#         background: #ddd;
#         border-radius: 4px;
#     }

#     /* Remove default streamlit margins */
#     .element-container {
#         margin-bottom: 0 !important;
#     }

#     .stMarkdown {
#         margin-bottom: 0 !important;
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
#         return "🚨 Sorry, I'm having technical difficulties. Please try again!"

# def handle_quick_question(question: str):
#     """Handle quick question button clicks"""
#     add_message("user", question)
#     st.session_state.is_loading = True

# # ═══════════════════════════════════════════════════════════════════════════════════
# # JAVASCRIPT FOR CHATGPT-STYLE INPUT
# # ═══════════════════════════════════════════════════════════════════════════════════

# st.markdown("""
# <script>
# let inputText = '';

# function initChatInput() {
#     const inputDiv = document.getElementById('chatgpt-input');
#     const sendBtn = document.getElementById('send-button');

#     if (!inputDiv || !sendBtn) {
#         setTimeout(initChatInput, 100);
#         return;
#     }

#     // Handle input changes
#     inputDiv.addEventListener('input', function() {
#         inputText = this.innerText.trim();
#         updateSendButton();
#     });

#     // Handle paste
#     inputDiv.addEventListener('paste', function(e) {
#         e.preventDefault();
#         const text = (e.clipboardData || window.clipboardData).getData('text');
#         document.execCommand('insertText', false, text);
#     });

#     // Handle Enter key
#     inputDiv.addEventListener('keydown', function(e) {
#         if (e.key === 'Enter' && !e.shiftKey) {
#             e.preventDefault();
#             sendMessage();
#         }
#     });

#     // Handle send button click
#     sendBtn.addEventListener('click', sendMessage);

#     function updateSendButton() {
#         if (inputText.length > 0) {
#             sendBtn.disabled = false;
#             sendBtn.style.background = 'linear-gradient(135deg, #f1843b 0%, #ff6b35 100%)';
#         } else {
#             sendBtn.disabled = true;
#             sendBtn.style.background = '#e9ecef';
#         }
#     }

#     function sendMessage() {
#         if (inputText.trim()) {
#             // Set the hidden input value
#             const hiddenInput = document.querySelector('input[data-testid="textInput-input"]');
#             if (hiddenInput) {
#                 hiddenInput.value = inputText;
#                 hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
#             }

#             // Clear the contenteditable div
#             inputDiv.innerText = '';
#             inputText = '';
#             updateSendButton();

#             // Trigger form submission
#             const submitBtn = document.querySelector('button[data-testid="baseButton-secondary"]');
#             if (submitBtn) {
#                 submitBtn.click();
#             }
#         }
#     }

#     // Initial button state
#     updateSendButton();
# }

# // Initialize when page loads
# document.addEventListener('DOMContentLoaded', initChatInput);
# setTimeout(initChatInput, 500);
# </script>
# """, unsafe_allow_html=True)

# # ═══════════════════════════════════════════════════════════════════════════════════
# # MAIN UI COMPONENTS
# # ═══════════════════════════════════════════════════════════════════════════════════

# # Header
# st.markdown("""
# <div class="chat-header">
#     <div class="header-content">
#         <div class="header-icon">🚀</div>
#         <div>
#             <div class="header-title">Jupiter FAQ Assistant</div>
#             <div class="header-subtitle">Ask about accounts, cards, Jewels & more!</div>
#         </div>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Chat Content (NO CONTAINER)
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

#     # Quick question buttons
#     st.markdown("### 💡 Popular Questions")

#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("💳 Credit Card", key="card"):
#             handle_quick_question("How do I apply for a Jupiter credit card?")
#             st.rerun()

#         if st.button("✅ KYC Process", key="kyc"):
#             handle_quick_question("How do I complete KYC verification?")
#             st.rerun()

#     with col2:
#         if st.button("💎 Jupiter Jewels", key="jewels"):
#             handle_quick_question("What are Jupiter Jewels and how do I earn them?")
#             st.rerun()

#         if st.button("⭐ Pro Benefits", key="pro"):
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

# # CHATGPT-STYLE INPUT SECTION
# st.markdown('<div class="input-section">', unsafe_allow_html=True)

# # Custom ChatGPT-style input
# st.markdown("""
# <div class="chatgpt-input-container">
#     <div id="chatgpt-input" class="chatgpt-input" contenteditable="true" role="textbox" aria-label="Ask me anything about Jupiter Money..." data-placeholder="Ask me anything about Jupiter Money..."></div>
#     <button id="send-button" class="send-button" disabled>↑</button>
# </div>
# """, unsafe_allow_html=True)

# # Hidden Streamlit form for backend processing
# with st.form("hidden_chat_form", clear_on_submit=True):
#     user_input = st.text_input("", key="hidden_input", label_visibility="collapsed")
#     send_clicked = st.form_submit_button("Send", use_container_width=False)

# st.markdown('</div>', unsafe_allow_html=True)

# # Handle form submission
# if send_clicked and user_input:
#     add_message("user", user_input)
#     st.session_state.is_loading = True
#     st.rerun()

# # Process bot response
# if st.session_state.is_loading and st.session_state.chat_history:
#     last_message = st.session_state.chat_history[-1]["content"]

#     with st.spinner(""):
#         response = get_bot_response(last_message)
#         add_message("bot", response)

#     st.session_state.is_loading = False
#     st.rerun()

# # Trust indicators
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

# # Footer
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


# import streamlit as st
# import uuid
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
# # ENHANCED CSS STYLING WITH CHATGPT-STYLE INPUT
# # ═══════════════════════════════════════════════════════════════════════════════════

# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

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

#     /* Header with icon */
#     .chat-header {
#         background: linear-gradient(135deg, #1e3a5c 0%, #4a8cb5 100%);
#         color: white;
#         padding: 20px;
#         border-radius: 0 0 20px 20px;
#         text-align: center;
#         margin-bottom: 20px;
#         box-shadow: 0 4px 20px rgba(30, 58, 92, 0.3);
#         position: relative;
#     }

#     .header-content {
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         gap: 12px;
#     }

#     .header-icon {
#         font-size: 24px;
#         animation: pulse 2s ease-in-out infinite alternate;
#     }

#     @keyframes pulse {
#         0% { transform: scale(1); }
#         100% { transform: scale(1.05); }
#     }

#     .header-title {
#         font-size: 22px;
#         font-weight: 700;
#         margin: 0;
#     }

#     .header-subtitle {
#         font-size: 13px;
#         opacity: 0.9;
#         color: #4ddbb7;
#         margin-top: 4px;
#     }

#     /* Chat content - NO CONTAINER */
#     .chat-content {
#         margin: 0 16px 16px 16px;
#         min-height: 300px;
#         max-height: 400px;
#         overflow-y: auto;
#         scroll-behavior: smooth;
#     }

#     /* Welcome screen */
#     .welcome-screen {
#         text-align: center;
#         padding: 24px 16px;
#         color: #1e3a5c;
#         background: white;
#         border-radius: 16px;
#         box-shadow: 0 6px 24px rgba(0,0,0,0.08);
#         margin-bottom: 20px;
#     }

#     .welcome-icon {
#         font-size: 48px;
#         margin-bottom: 12px;
#         animation: float 3s ease-in-out infinite;
#     }

#     @keyframes float {
#         0%, 100% { transform: translateY(0px); }
#         50% { transform: translateY(-6px); }
#     }

#     .welcome-title {
#         font-size: 20px;
#         font-weight: 700;
#         margin-bottom: 6px;
#         color: #1e3a5c;
#     }

#     .welcome-text {
#         font-size: 14px;
#         opacity: 0.8;
#         margin-bottom: 20px;
#         line-height: 1.4;
#     }

#     /* Quick question buttons */
#     .quick-buttons {
#         display: grid;
#         grid-template-columns: 1fr 1fr;
#         gap: 10px;
#         margin-top: 20px;
#     }

#     .stButton > button {
#         background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
#         color: #1e3a5c !important;
#         border: 2px solid #f1843b !important;
#         border-radius: 16px !important;
#         padding: 10px 14px !important;
#         font-weight: 600 !important;
#         font-size: 13px !important;
#         transition: all 0.3s ease !important;
#         box-shadow: 0 3px 10px rgba(241, 132, 59, 0.15) !important;
#         width: 100% !important;
#         min-height: 42px !important;
#     }

#     .stButton > button:hover {
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%) !important;
#         color: white !important;
#         transform: translateY(-1px) scale(1.02) !important;
#         box-shadow: 0 5px 16px rgba(241, 132, 59, 0.3) !important;
#     }

#     /* Message bubbles */
#     .message-wrapper {
#         margin-bottom: 12px;
#         animation: slideIn 0.3s ease-out;
#     }

#     @keyframes slideIn {
#         from { opacity: 0; transform: translateY(8px); }
#         to { opacity: 1; transform: translateY(0); }
#     }

#     .user-message {
#         display: flex;
#         justify-content: flex-end;
#         margin-bottom: 12px;
#     }

#     .bot-message {
#         display: flex;
#         justify-content: flex-start;
#         align-items: flex-start;
#         gap: 10px;
#         margin-bottom: 12px;
#     }

#     .user-bubble {
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%);
#         color: white;
#         padding: 10px 14px;
#         border-radius: 18px 18px 4px 18px;
#         max-width: 80%;
#         font-size: 14px;
#         line-height: 1.4;
#         box-shadow: 0 2px 6px rgba(241, 132, 59, 0.25);
#     }

#     .bot-bubble {
#         background: linear-gradient(135deg, #4ddbb7 0%, #42c9a7 100%);
#         color: white;
#         padding: 10px 14px;
#         border-radius: 18px 18px 18px 4px;
#         max-width: 80%;
#         font-size: 14px;
#         line-height: 1.4;
#         box-shadow: 0 2px 6px rgba(77, 219, 183, 0.25);
#     }

#     .bot-avatar {
#         width: 32px;
#         height: 32px;
#         background: linear-gradient(135deg, #1e3a5c 0%, #4a8cb5 100%);
#         border-radius: 50%;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 14px;
#         color: white;
#         flex-shrink: 0;
#         box-shadow: 0 2px 6px rgba(30, 58, 92, 0.25);
#     }

#     /* Loading animation */
#     .loading-message {
#         background: #f8f9fa;
#         color: #6c757d;
#         padding: 10px 14px;
#         border-radius: 18px 18px 18px 4px;
#         display: flex;
#         align-items: center;
#         gap: 8px;
#         font-size: 13px;
#         font-style: italic;
#     }

#     .typing-dots {
#         display: flex;
#         gap: 3px;
#     }

#     .dot {
#         width: 5px;
#         height: 5px;
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

#     /* CHATGPT-STYLE INPUT SECTION */
#     .input-section {
#         padding: 12px 16px;
#         margin: 0 16px 16px 16px;
#         background: white;
#         border-radius: 24px;
#         box-shadow: 0 4px 16px rgba(0,0,0,0.08);
#         border: 1px solid rgba(241, 132, 59, 0.1);
#         position: relative;
#     }

#     /* Hide default streamlit form styling */
#     .stForm {
#         border: none !important;
#         background: transparent !important;
#         padding: 0 !important;
#     }

#     /* Input field styling */
#     .stTextInput > div > div > input {
#         border: 2px solid #e9ecef !important;
#         border-radius: 24px !important;
#         padding: 12px 16px !important;
#         font-size: 15px !important;
#         background: #f8f9fa !important;
#         color: #1e3a5c !important;
#         transition: all 0.3s ease !important;
#         box-shadow: none !important;
#     }

#     .stTextInput > div > div > input:focus {
#         border-color: #f1843b !important;
#         box-shadow: 0 0 0 3px rgba(241, 132, 59, 0.1) !important;
#         outline: none !important;
#         background: white !important;
#     }

#     .stTextInput > div > div > input::placeholder {
#         color: #9ca3af !important;
#         font-size: 14px !important;
#     }

#     /* CIRCULAR SEND BUTTON STYLING */
#     .stFormSubmitButton > button {
#         background: linear-gradient(135deg, #f1843b 0%, #ff6b35 100%) !important;
#         color: white !important;
#         border: none !important;
#         border-radius: 50% !important;
#         width: 45px !important;
#         height: 45px !important;
#         min-width: 45px !important;
#         min-height: 45px !important;
#         padding: 0 !important;
#         display: flex !important;
#         align-items: center !important;
#         justify-content: center !important;
#         font-size: 18px !important;
#         font-weight: bold !important;
#         transition: all 0.2s ease !important;
#         box-shadow: 0 2px 8px rgba(241, 132, 59, 0.3) !important;
#         position: relative !important;
#     }

#     .stFormSubmitButton > button:hover {
#         transform: scale(1.05) !important;
#         box-shadow: 0 4px 12px rgba(241, 132, 59, 0.4) !important;
#     }

#     .stFormSubmitButton > button:active {
#         transform: scale(0.95) !important;
#     }

#     /* Hide button text and add arrow */
#     .stFormSubmitButton > button::before {
#         content: "↑" !important;
#         font-size: 18px !important;
#         font-weight: bold !important;
#         color: white !important;
#     }

#     .stFormSubmitButton > button > div {
#         display: none !important;
#     }

#     /* Trust indicators */
#     .trust-section {
#         display: flex;
#         justify-content: center;
#         gap: 12px;
#         margin: 12px;
#         flex-wrap: wrap;
#     }

#     .trust-badge {
#         background: rgba(255,255,255,0.9);
#         padding: 6px 10px;
#         border-radius: 10px;
#         font-size: 11px;
#         font-weight: 600;
#         color: #1e3a5c;
#         box-shadow: 0 2px 6px rgba(0,0,0,0.08);
#         display: flex;
#         align-items: center;
#         gap: 4px;
#     }

#     .trust-icon {
#         font-size: 11px;
#         color: #f1843b;
#     }

#     /* Footer */
#     .footer {
#         text-align: center;
#         margin: 20px 16px 16px 16px;
#         padding: 12px;
#         background: rgba(255,255,255,0.8);
#         border-radius: 12px;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#     }

#     .footer-text {
#         font-size: 13px;
#         color: #1e3a5c;
#         margin-bottom: 6px;
#     }

#     .footer-links {
#         font-size: 11px;
#         color: #6c757d;
#     }

#     .footer-links a {
#         color: #f1843b;
#         text-decoration: none;
#         font-weight: 600;
#     }

#     /* Mobile responsiveness */
#     @media (max-width: 768px) {
#         .chat-header {
#             margin: -8px -8px 16px -8px;
#             border-radius: 0 0 16px 16px;
#             padding: 16px;
#         }

#         .header-title {
#             font-size: 20px;
#         }

#         .chat-content {
#             margin: 0 8px 12px 8px;
#             max-height: 300px;
#             min-height: 250px;
#         }

#         .quick-buttons {
#             grid-template-columns: 1fr;
#         }

#         .user-bubble, .bot-bubble {
#             max-width: 90%;
#             font-size: 13px;
#         }

#         .input-section {
#             margin: 0 8px 8px 8px;
#         }
#     }

#     /* Scrollbar */
#     .chat-content::-webkit-scrollbar {
#         width: 4px;
#     }

#     .chat-content::-webkit-scrollbar-track {
#         background: #f1f1f1;
#         border-radius: 8px;
#     }

#     .chat-content::-webkit-scrollbar-thumb {
#         background: #4ddbb7;
#         border-radius: 8px;
#     }

#     /* Remove default streamlit margins */
#     .element-container {
#         margin-bottom: 0 !important;
#     }

#     .stMarkdown {
#         margin-bottom: 0 !important;
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

# # Check for query parameters (FIXED: Using new API)
# try:
#     # Use new query_params API instead of deprecated experimental version
#     query_params = dict(st.query_params)
#     if "msg" in query_params:
#         if query_params["msg"] and query_params["msg"] != st.session_state.pending_message:
#             st.session_state.pending_message = query_params["msg"]
#             # Clear the query parameter
#             del st.query_params["msg"]
# except Exception as e:
#     # Fallback for older versions
#     pass

# # ═══════════════════════════════════════════════════════════════════════════════════
# # MAIN UI COMPONENTS
# # ═══════════════════════════════════════════════════════════════════════════════════

# # Header
# st.markdown("""
# <div class="chat-header">
#     <div class="header-content">
#         <div class="header-icon">🚀</div>
#         <div>
#             <div class="header-title">Jupiter FAQ Assistant</div>
#             <div class="header-subtitle">Ask about accounts, cards, Jewels & more!</div>
#         </div>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Chat Content (NO CONTAINER)
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

#     # Quick question buttons
#     #st.markdown("### 💡 Popular Questions")

#     st.markdown("""
#         <style>
#             #popular-questions {
#                 color: #FF6347;  # This is an example color (Tomato). You can change it to any color you want.
#         }
#         </style>
#         """, unsafe_allow_html=True)

#     # Add the header with the styled id
#     st.markdown('<h3 id="popular-questions">💡 Popular Questions</h3>', unsafe_allow_html=True)

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

# # HORIZONTAL INPUT SECTION (SIMPLIFIED AND FIXED)
# st.markdown('<div class="input-section">', unsafe_allow_html=True)

# # Use native Streamlit form with proper error handling
# with st.form("chat_form", clear_on_submit=True, border=False):
#     # Horizontal layout: input field + send button
#     col1, col2 = st.columns([6, 1])

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

# # Trust indicators
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

# # Footer
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

import uuid,streamlit as st
import time
from chatbot import query_jupiter_enhanced

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
        print('sai  ',response)
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
