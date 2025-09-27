# Agentic AI Workshop - Hands-On Exercises

Welcome to the Agentic AI workshop! This directory contains progressive exercises that will teach you how to build AI agents from basic conversations to production-ready systems.

## 📁 Workshop Files

### Core Exercises (Progressive Learning Path)
- **`00_hello_agent.py`** - Your first AI agent (basic conversation)
- **`01_agent_with_tools.py`** - Adding web search capabilities
- **`02_custom_tools.py`** - Building custom business tools
- **`03_agent_with_memory.py`** - Short-term conversation memory
- **`04_persistent_memory.py`** - Long-term memory with PostgreSQL
- **`05_basic_rag.py`** - Simple document knowledge (RAG)
- **`06_agentic_rag.py`** - Dynamic multi-document RAG
- **`07_workflow_agent.py`** - Multi-step business workflows

### Bonus Examples
- **`bonus/youtube_agent.py`** - AI assistant with YouTube video knowledge
- **`bonus/README.md`** - Documentation for bonus examples

### Sample Data
- **`sample_data/company_handbook.txt`** - HR policies for RAG exercises
- **`sample_data/technical_docs.txt`** - API documentation for agentic RAG

## 🛠️ Setup Instructions

### Prerequisites
- **Python 3.10 or higher**
- **PostgreSQL with pgvector extension** (for memory and RAG exercises)
- **API Keys**: Groq and HuggingFace

### Step 1: Install Dependencies

#### Option A: Using UV (Recommended - Fast Package Manager)

**For Linux/Mac:**
```bash
# Install UV first
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to workshop directory
cd hands-on

# Install dependencies (8-10x faster than pip)
uv pip install -r requirements.txt
```

**For Windows:**
```cmd
# Install UV using pip (if UV installer fails on Windows)
pip install uv

# Navigate to workshop directory
cd hands-on

# Install dependencies
uv pip install -r requirements.txt
```

#### Option B: Using Regular pip

**For all platforms:**
```bash
cd hands-on
pip install -r requirements.txt
```

> **Note**: UV is significantly faster (8-10x) than pip and uses less memory, but pip works universally across all platforms if UV installation encounters issues.

### Step 2: Environment Variables

Create a `.env` file in the `hands-on` directory:

```bash
# Required API Keys
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

**Get your API keys:**
- **Groq**: https://console.groq.com/ (free tier available)
- **HuggingFace**: https://huggingface.co/settings/tokens (free tier available)

### Step 3: Database Setup (Required for Exercises 4-7 and Bonus)

You need PostgreSQL with pgvector extension for memory and RAG exercises.

#### Option A: Using Podman
```bash
# Start PostgreSQL with pgvector
podman run --name pgvector \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -p 5532:5432 \
  -d pgvector/pgvector:pg16

# Verify it's running
podman ps
```

#### Option B: Using Docker
```bash
# Start PostgreSQL with pgvector
docker run --name pgvector \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -p 5532:5432 \
  -d pgvector/pgvector:pg16

# Verify it's running
docker ps
```

> **Note**: Podman and Docker commands are interchangeable. Use whichever container runtime you prefer.

#### Cleanup Instructions (When Done)
```bash
# Stop and remove container
podman stop pgvector && podman rm pgvector
# OR
docker stop pgvector && docker rm pgvector
```

For more detailed database setup options, see `../agent-course/podman_setup_commands.md`.

## 🚀 Getting Started

### Run the Exercises

Start with Exercise 0 and work through progressively:

```bash
# Basic exercises (no database needed)
python 00_hello_agent.py
python 01_agent_with_tools.py
python 02_custom_tools.py

# Memory exercises (database required)
python 03_agent_with_memory.py
python 04_persistent_memory.py

# RAG exercises (database required)
python 05_basic_rag.py
python 06_agentic_rag.py

# Advanced workflows (database required)
python 07_workflow_agent.py

# Bonus: YouTube Agent (database required)
cd bonus
python youtube_agent.py
```

### Quick Test
Verify your setup works:
```bash
python 00_hello_agent.py
```
If this runs without errors, you're ready to go!

## 🎯 Learning Path

| Exercise | Core Concepts | Database Required |
|----------|---------------|-------------------|
| 0 | Basic agent, LLM integration | ❌ |
| 1 | Tools, function calling, web search | ❌ |
| 2 | Custom tools, toolkits, business logic | ❌ |
| 3 | Memory, conversation history, context | ✅ |
| 4 | Persistent storage, user memories, sessions | ✅ |
| 5 | RAG, embeddings, document knowledge | ✅ |
| 6 | Agentic RAG, multi-step retrieval | ✅ |
| 7 | Workflows, state management, business processes | ✅ |
| Bonus | YouTube knowledge extraction and Q&A | ✅ |

## 🔧 Framework: Agno

These exercises use the **Agno** framework (v2.0.10) because:
- **Simple and intuitive API** for building agents
- **Excellent tool integration** with web search, databases, and custom functions
- **Built-in memory and RAG support** for knowledge-aware agents
- **Production-ready features** like error handling and monitoring
- **Great for learning** agentic AI concepts progressively

## 🎮 Workshop Flow (2-3 hours)

1. **Setup & Verification** (15 min) - Environment and dependencies
2. **Basic Agents** (30 min) - Exercises 0-2
3. **Memory & Context** (30 min) - Exercises 3-4
4. **Knowledge & RAG** (45 min) - Exercises 5-6
5. **Advanced Workflows** (30 min) - Exercise 7
6. **Bonus: YouTube Agent** (15 min) - Video knowledge extraction
7. **Q&A & Experimentation** (15 min)

## 💡 Workshop Tips

### For Each Exercise:
1. **Read the docstring** - Detailed explanations and learning objectives
2. **Try the suggested prompts** - Test different scenarios in the comments
3. **Experiment** - Modify parameters and see what happens
4. **Build upon previous exercises** - Combine concepts from earlier lessons

### Troubleshooting:
- **Database connection errors**: Ensure PostgreSQL is running on port 5532
- **API errors**: Check your `.env` file has valid API keys (no quotes needed)
- **Import errors**: Make sure you're in the `hands-on` directory and dependencies are installed
- **UV installation issues on Windows**: Fall back to regular `pip install -r requirements.txt`

## 🎯 Key Features Demonstrated

### Bonus: YouTube Agent
The `bonus/youtube_agent.py` demonstrates:
- **Video knowledge extraction** from YouTube transcripts
- **Searchable video content** using HuggingFace embeddings
- **Question answering** about specific video content
- **Persistent knowledge storage** in PostgreSQL

**Example Video**: "Building AI Agents with Python" by Arjan Codes
- Ask questions like: "What are the main components of an AI agent?"
- Get answers based on the actual video content

## 🚀 After the Workshop

### Next Steps:
1. **Build your own agent** - Start with a specific use case
2. **Explore more tools** - Try different APIs and integrations
3. **Learn MCP (Model Context Protocol)** - Tool standardization
4. **Study production systems** - Look at real-world agent implementations

### Resources:
- [Agno Documentation](https://docs.agno.com)
- [Groq API Reference](https://console.groq.com/docs)
- [HuggingFace Models](https://huggingface.co/models)
- [YouTube Agent Example](https://docs.agno.com/examples/concepts/knowledge/readers/youtube/youtube-reader)

## 💡 Have Questions?

- Check the detailed docstrings in each exercise file
- Experiment with different prompts and parameters
- Ask during the workshop Q&A session
- Continue building after the workshop!

Happy learning! 🎉

---

**Technical Stack**: Python 3.10+, Agno Framework, Groq LLM, HuggingFace Embeddings, PostgreSQL + pgvector, UV/pip package management