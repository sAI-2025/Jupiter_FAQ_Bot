
````markdown
# 🤖 Jupiter FAQ Bot

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Colab Demo](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1r6LuB3XVM_V4OWgakm90mKBLTTht2STp)

> **AI-Powered Customer Support System** that transforms static FAQ pages into intelligent, conversational support powered by Groq, LangChain, and ChromaDB.

---

## 🚀 Overview

**Jupiter FAQ Bot** is a conversational AI system that:
- 💬 Answers user questions instantly with high accuracy
- 🧠 Understands multi-turn queries with memory
- ⚙️ Uses advanced retrieval (similarity + MMR) and LLMs
- 🔍 Trains on real FAQs using semantic search and vector databases

This project is ideal for startups, fintechs, or any product team looking to automate customer support using AI.

---

## 🎯 Why This Project?

Most customer support tools:
- Are **static** and hard to navigate
- Waste time with **repetitive queries**
- Can’t handle **follow-up questions**

**Jupiter FAQ Bot** fixes that with:
- ✅ Contextual AI conversations
- ✅ Real-time query matching
- ✅ 80%+ accuracy with <0.5s response time

---

## 🧩 Features

| Feature               | Description |
|----------------------|-------------|
| **Dual Retriever**   | Combines Similarity & MMR search for better accuracy |
| **Groq LLM**         | Superfast Llama3-8b-8192 for blazing response |
| **LangChain**        | Modular orchestration of memory, retrieval, and generation |
| **ChromaDB**         | Efficient vector store for FAQs |
| **Web Crawler**      | Automatically extracts content from Jupiter’s site |
| **Colab Support**    | One-click demo via Google Colab |

---

## 📁 Project Structure

```bash
jupiter-faq-bot/
├── app.py                     # FastAPI app (if using API)
├── all_urls.txt               # Raw URL crawl list
├── FAQ.json                   # Raw FAQ data
├── jupiter_vectordb_enhanced/ # ChromaDB storage
│   └── chroma.sqlite3
├── Jupyter.ipynb              # Notebook demo
├── requirements.txt           # Python dependencies
````

---

## ⚙️ Quick Start

### ✅ Option 1: One-click Google Colab Demo (Recommended)

[🔗 Open in Colab](https://colab.research.google.com/drive/1r6LuB3XVM_V4OWgakm90mKBLTTht2STp)

```python
# Install dependencies
!pip install langchain chromadb sentence-transformers groq beautifulsoup4 requests pandas numpy

# Set API key
import os
os.environ["GROQ_API_KEY"] = "your_groq_api_key_here"

# Run the full workflow
from main import main_enhanced_workflow
vectorstore = main_enhanced_workflow("/path/to/FAQ.json")

# Start chatting
from chat_system import start_chat_session
start_chat_session(vectorstore)
```

---

### 💻 Option 2: Local Setup (For Developers)

#### 1. Clone the Repository

```bash
git clone https://github.com/sAI-2025/Jupiter_FAQ_Bot.git
cd Jupiter_FAQ_Bot
```

#### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Add Your Groq API Key

```bash
echo "GROQ_API_KEY=your_key_here" > .env
```

#### 5. Run the App (API Mode)

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 💬 Example Chat

```plaintext
👤 User: How can I activate my Jupiter card?

🤖 Bot: To activate your Jupiter card, you can simply swipe your debit card at any 
       pre-approved merchant. Activation is automatic and instant upon first use.
```

---

## 🧠 How It Works (Under the Hood)

1. **Web Crawler** pulls FAQ data from Jupiter’s site
2. **Text Preprocessing** cleans and structures the content
3. **Embeddings** are generated using `all-MiniLM-L6-v2`
4. **Vector DB** stores questions and answers in ChromaDB
5. **Dual Retriever** fetches similar and diverse results
6. **LLM (Groq)** generates human-like responses with memory

---

## 🔧 Configuration

```env
# .env file
GROQ_API_KEY=your_groq_key
VECTOR_STORE_PATH=./jupiter_vectordb_enhanced
LLM_MODEL=llama3-8b-8192
SIMILARITY_TOP_K=3
MMR_DIVERSITY=0.7
```

---

## 🧪 Testing

```bash
# Run all test cases
python -m pytest tests/ -v
```

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🙋‍♂️ Contact & Support

* 📂 GitHub Issues: [Open a Bug Report](https://github.com/sAI-2025/Jupiter_FAQ_Bot/issues)
* 📘 Documentation: [View Wiki](https://github.com/sAI-2025/Jupiter_FAQ_Bot/wiki)
* 💬 Chat: [Try it on Colab](https://colab.research.google.com/drive/1r6LuB3XVM_V4OWgakm90mKBLTTht2STp)

---

> Built with ❤️ using LangChain, Groq, and ChromaDB to automate support.

```

---

## 📌 Next Steps (for You)

If you're happy with the above:

✅ Let me know and I can generate the actual `README.md` file content  
✅ I can also help split your code into `/src`, `/tests`, etc.  
✅ Or convert this into a **GitHub Pages site** for better documentation

Would you like me to generate the actual updated README code file now?
```
