"""
Exercise 5: Basic RAG - Retrieval-Augmented Generation
=======================================================

Learning Objectives:
- Understand how RAG works with document knowledge
- Learn about embeddings and vector similarity
- See how agents can answer questions about specific documents

This agent can answer questions about documents by retrieving relevant
sections and using them to generate informed responses.
"""

import os
from typing import List
from dotenv import load_dotenv
from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.models.groq import Groq
from agno.vectordb.pgvector import PgVector
from agno.knowledge.embedder.huggingface import HuggingfaceCustomEmbedder

# Load environment variables
load_dotenv()

def setup_knowledge_base():
    """Set up the knowledge base with company handbook"""

    # Check if sample document exists
    doc_path = "sample_data/company_handbook.txt"
    if not os.path.exists(doc_path):
        print(f"❌ Sample document not found: {doc_path}")
        print("Make sure to run this from the hands-on directory")
        return None

    print("📚 Setting up knowledge base...")

    try:
        # Vector database for storing embeddings
        vector_db = PgVector(
            db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
            table_name="basic_rag_demo",
            embedder=HuggingfaceCustomEmbedder(
                id="sentence-transformers/all-MiniLM-L6-v2",
                dimensions=384
            )
        )

        # Create knowledge base using Knowledge
        knowledge_base = Knowledge(
            name="company_handbook",
            description="Company policies and procedures",
            vector_db=vector_db,
            max_results=5  # Number of relevant chunks to retrieve
        )

        # Load the text file directly into knowledge base
        knowledge_base.add_content(
            name="company_handbook.txt",
            description="Company handbook with policies and procedures",
            path=doc_path,
            metadata={"source": doc_path, "type": "handbook"}
        )

        print(f"✅ Loaded document: {doc_path}")
        print("📄 Document processed and added to knowledge base")

        return knowledge_base

    except Exception as e:
        print(f"❌ Error setting up knowledge base: {e}")
        print("Make sure PostgreSQL with pgvector is running (see Exercise 4)")
        return None

def main():
    print("📚 Exercise 5: Basic RAG")
    print("=" * 35)
    print("This agent can answer questions about the company handbook!")
    print("Loading document and creating embeddings...")
    print()

    # Set up knowledge base
    knowledge_base = setup_knowledge_base()
    if not knowledge_base:
        return

    print("\n🤖 Agent ready! Ask questions about ACME Corporation policies.")
    print("Type 'exit' to quit.\n")

    # Create RAG agent
    agent = Agent(
        model=Groq(
            id="llama-3.3-70b-versatile",
            max_tokens=1000
        ),
        description="""You are a helpful HR assistant for ACME Corporation.
        Use the company handbook information to answer employee questions accurately.
        If information isn't in the handbook, say so clearly.""",

        # 📚 Add knowledge base for RAG
        knowledge=knowledge_base,

        # RAG configuration
        search_knowledge=True,      # Enable knowledge search
        read_tool_call_history=True, # Read previous tool calls

        markdown=True
    )

    print("💡 Try asking about:")
    print("  🕐 Working hours and remote work policy")
    print("  🏥 Health insurance and benefits")
    print("  💻 IT equipment and security policies")
    print("  📈 Performance reviews and career development")
    print("  📞 Contact information")
    print()

    while True:
        try:
            user_input = input("Employee Question: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye! 👋")
                break

            print("\nHR Assistant:")
            agent.print_response(user_input, stream=False)
            print()

        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in environment variables.")
        exit(1)

    main()

"""
🎯 Try these questions to test RAG:

Basic Policy Questions:
1. "What are the standard working hours?"
2. "How many vacation days do I get?"
3. "What's the remote work policy?"
4. "How much is the health insurance coverage?"

Specific Details:
5. "What's the laptop refresh cycle?"
6. "How much is the annual learning budget?"
7. "What are the office locations?"
8. "When are performance reviews conducted?"

Testing Knowledge Boundaries:
9. "What's the CEO's name?" (not in document)
10. "What's the company stock price?" (not in document)
11. "How do I submit a vacation request?" (process not detailed)

🧠 Key Concepts:
- TextKnowledgeBase loads and processes documents
- PgVector stores embeddings for similarity search
- chunk_size and chunk_overlap control document segmentation
- search_knowledge=True enables automatic knowledge retrieval
- Agent retrieves relevant chunks before generating responses

🔍 How RAG Works:
1. Document is split into chunks (paragraphs/sections)
2. Each chunk is converted to embeddings (vectors)
3. User question is converted to embeddings
4. Most similar chunks are retrieved
5. LLM generates response using retrieved context

📊 What You'll See:
- Tool calls showing knowledge retrieval
- Relevant document sections being found
- Responses grounded in document content
- Clear indication when information isn't available

⚠️ Prerequisites:
- PostgreSQL with pgvector running (see Exercise 4)
- Sample document in sample_data/company_handbook.txt

📝 Next: In 06_agentic_rag.py, we'll make RAG more dynamic and intelligent!
"""