# 🤖 Jupiter FAQ Bot: AI-Powered Customer Support System

Transform static FAQ pages into intelligent, conversational AI support that understands context and delivers instant, accurate responses.

---

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![LLM-Driven](https://img.shields.io/badge/LLM-Powered-brightgreen?logo=openai)
![License](https://img.shields.io/badge/License-MIT-green?logo=opensourceinitiative)
![Status](https://img.shields.io/badge/Status-Beta-orange?logo=githubactions)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)  
[![Star](https://img.shields.io/github/stars/your-username/jupiter-faq-bot?style=social)](https://github.com/your-username/jupiter-faq-bot/stargazers)

---

## 🎯 **Problem Statement**

Traditional FAQ systems suffer from:
- **Poor User Experience**: Users struggle to find relevant answers in static lists
- **High Support Load**: 80%+ of customer queries are repetitive and could be automated
- **No Context Awareness**: Systems can't handle follow-up questions or maintain conversation flow
- **Scalability Issues**: Human agents required for basic query resolution

## 💡 **Our Solution**

An intelligent FAQ bot that combines advanced web scraping, semantic search, and conversational AI to deliver:
- **Instant Responses**: 0.4-second average query processing
- **Context Awareness**: Multi-turn conversations with memory
- **High Accuracy**: 80%+ success rate in query-category matching
- **24/7 Availability**: Automated support without human intervention

## 📊 **Live Demo Results**

### **Example Conversations**

**Query 1: Card Activation**
```
👤 User: "How can I activate my Jupiter card?"

🤖 Bot: "To activate your Jupiter card, you can simply swipe your debit card at any 
       pre-approved merchant using a card that has the debit card facility. The 
       activation process is automatic and instant upon first use."

📊 Metadata: Category: Cards | Response Time: 0.41s | Confidence: 95%
```

**Query 2: Rewards System**
```
👤 User: "What are Jewels?"

🤖 Bot: "Jewels are credits you earn when you make eligible payments with Jupiter. 
       You can redeem them for instant discounts on future bill payments. Think of 
       them as cashback rewards that you can use immediately!"

📊 Metadata: Category: Rewards & Jewels | Response Time: 0.36s | Confidence: 98%
```

**Query 3: Payment Issues**
```
👤 User: "My bill payment failed, what should I do?"

🤖 Bot: "Sorry to hear that your bill payment failed! If you're experiencing issues 
       with a failed transaction, please contact the app's customer support 
       immediately. They can help investigate the issue and process a refund if 
       necessary. You can also try the payment again after some time."

📊 Metadata: Category: Bills & Recharges | Response Time: 0.40s | Confidence: 92%
```

### **Performance Metrics**
- **📈 Data Processed**: 1,497 FAQ documents across 7 categories
- **🎯 Accuracy**: 80%+ category matching success rate
- **⚡ Speed**: Average 0.4 seconds response time
- **🔄 Conversations**: Multi-turn dialogue with context preservation

## 📁 **Project Structure**

```bash
Jupiter_FAQ_Bot/
├── Jupyter.ipynb              # Main notebook implementation
├── FAQ.json                   # Extracted FAQ data
├── requirements.txt           # Python dependencies
├── jupiter_vectordb_enhanced/ # ChromaDB storage
│   └── chroma.sqlite3
├── all_urls.txt              # Crawled URLs list
└── README.md                 # Project documentation
```

## 🚀 **Quick Start Guide**

### **Prerequisites**

```bash
# Required Software
- Python 3.8 or higher
- Git
- Groq API key (free tier available)
```

### **Installation**

```bash
# Clone the repository
git clone https://github.com/sAI-2025/Jupiter_FAQ_Bot.git
cd Jupiter_FAQ_Bot

# Install dependencies
pip install -r requirements.txt
```

### **Setup API Key**

```python
# Get your free Groq API key from: https://console.groq.com/keys
os.environ["GROQ_API_KEY"] = "your_groq_api_key_here"
```

### **Run the Notebook**

1. **Open Jupyter Notebook**
   ```bash
   jupyter notebook Jupyter.ipynb
   ```

2. **Or use Google Colab** (Recommended)
   ```
   🔗 Direct Link: https://colab.research.google.com/drive/1r6LuB3XVM_V4OWgakm90mKBLTTht2STp
   ```

3. **Execute all cells** to:
   - Load and process FAQ data
   - Create vector database
   - Start interactive chat session

## 🛠️ **How It Works**

### **System Architecture**

```
User Query → Memory Check → Query Enhancement → Dual Retrieval → LLM Response → Context Update
```

### **Key Components**

| **Component** | **Technology** | **Purpose** |
|---|---|---|
| **Web Scraping** | BeautifulSoup + Requests | FAQ data extraction |
| **Embeddings** | sentence-transformers | Semantic search |
| **Vector Store** | ChromaDB | Document storage |
| **LLM** | Groq Llama3-8b-8192 | Response generation |
| **Framework** | LangChain | AI orchestration |

### **Implementation Steps**

1. **Data Collection**: Crawl Jupiter's website for FAQ content
2. **Processing**: Extract and categorize Q&A pairs
3. **Vector Database**: Create embeddings for semantic search
4. **Retrieval**: Dual system (Similarity + MMR) for better accuracy
5. **Generation**: LLM-powered responses with conversation memory

## 🎯 **Key Features**

- **🧠 Smart Retrieval**: Combines similarity search with Maximum Marginal Relevance
- **💬 Conversational Memory**: Maintains context across multiple turns
- **⚡ Fast Processing**: Sub-second response times
- **🎯 High Accuracy**: 80%+ success rate in category matching
- **📊 Rich Metadata**: Includes confidence scores and response times

## 🧪 **Testing the System**

### **Basic Usage**

```python
# Load the system
vectorstore = main_enhanced_workflow("/content/FAQ.json")

# Test with sample queries
test_queries = [
    "How can I pay bills?",
    "What are Jewels?", 
    "How to activate card?",
    "KYC documents needed?"
]

# Run tests
for query in test_queries:
    response = enhanced_query_processing(query, primary_retriever, mmr_retriever)
    print(f"Query: {query}")
    print(f"Response: {response}")
```

### **Performance Benchmarks**

- **Simple Queries**: 0.26 - 0.45 seconds
- **Complex Queries**: 0.5 - 2.0 seconds
- **Multi-turn Conversations**: 0.4 - 1.5 seconds

## 🔧 **Configuration**

### **Environment Variables**

```bash
# Required
GROQ_API_KEY=your_groq_api_key

# Optional
VECTOR_STORE_PATH=./jupiter_vectordb_enhanced
LOG_LEVEL=INFO
MAX_CONVERSATION_HISTORY=10
```

### **Model Parameters**

```python
# Retrieval settings
SIMILARITY_TOP_K = 3
MMR_TOP_K = 3
MMR_DIVERSITY = 0.7

# LLM configuration
LLM_MODEL = "llama3-8b-8192"
MAX_TOKENS = 1000
TEMPERATURE = 0.1
```

## 🚀 **Business Impact**

| **Metric** | **Achievement** |
|---|---|
| **Support Automation** | 80%+ queries handled automatically |
| **Response Time** | 0.4 seconds average |
| **Availability** | 24/7 operation |
| **Scalability** | Unlimited concurrent users |
| **Cost Reduction** | Significant Tier-1 support savings |

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Open Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ **Support & Contact**

- **GitHub Issues**: [Report bugs or request features](https://github.com/sAI-2025/Jupiter_FAQ_Bot/issues)
- **Live Demo**: [Try it on Google Colab](https://colab.research.google.com/drive/1r6LuB3XVM_V4OWgakm90mKBLTTht2STp)

**Author**: Sai Krishna Chowdary Chundru  
**GitHub**: [github.com/sAI-2025](https://github.com/sAI-2025)

**Built with ❤️ for intelligent customer support automation**
