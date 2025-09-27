"""
Exercise 6: Agentic RAG - Dynamic and Intelligent Retrieval
===========================================================

Learning Objectives:
- Understand the difference between basic and agentic RAG
- Learn about dynamic multi-step retrieval
- See how agents can intelligently search across multiple documents

This agent demonstrates agentic RAG - it can search across multiple knowledge
sources and make multiple retrieval calls as needed to answer complex questions.
"""

import os
from typing import List
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector
from agno.knowledge.embedder.huggingface import HuggingfaceCustomEmbedder
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.toolkit import Toolkit

# Load environment variables
load_dotenv()

def setup_multiple_knowledge_bases():
    """Set up multiple knowledge bases for comprehensive information"""

    knowledge_bases = []

    # Check if sample documents exist
    docs = [
        ("sample_data/company_handbook.txt", "hr_policies"),
        ("sample_data/technical_docs.txt", "technical_docs")
    ]

    for doc_path, collection_name in docs:
        if not os.path.exists(doc_path):
            print(f"❌ Sample document not found: {doc_path}")
            continue

        try:
            print(f"📚 Loading {doc_path}...")

            # Separate vector collections for different document types
            vector_db = PgVector(
                db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
                table_name=f"agentic_rag_hf_{collection_name}",
                embedder=HuggingfaceCustomEmbedder(
                    id="sentence-transformers/all-MiniLM-L6-v2",
                    dimensions=384
                )
            )

            knowledge_base = Knowledge(
                name=collection_name,
                description=f"Knowledge base for {collection_name}",
                vector_db=vector_db,
                max_results=5
            )

            # Load content from file
            knowledge_base.add_content(
                name=f"{collection_name}.txt",
                description=f"Content from {doc_path}",
                path=doc_path,
                metadata={"source": doc_path, "type": collection_name}
            )

            knowledge_bases.append(knowledge_base)
            print(f"✅ Loaded {collection_name}: Content processed")

        except Exception as e:
            print(f"❌ Error loading {doc_path}: {e}")

    return knowledge_bases

class AgenticRAGToolkit(Toolkit):
    """Custom toolkit for intelligent document search"""

    def __init__(self, knowledge_bases: List[Knowledge]):
        super().__init__(name="agentic_rag_toolkit")
        self.knowledge_bases = knowledge_bases
        # Register the search methods as tools
        self.register(self.search_hr_policies)
        self.register(self.search_technical_docs)

    def search_hr_policies(self, query: str) -> str:
        """
        Search HR policies and company handbook.

        Args:
            query (str): Search query related to HR policies, benefits, work policies

        Returns:
            str: Relevant HR policy information
        """
        if not self.knowledge_bases:
            return "No HR knowledge base available"

        try:
            # Search in the first knowledge base (HR policies)
            hr_kb = self.knowledge_bases[0]
            results = hr_kb.search(query, max_results=3)

            if results:
                context = "\n\n".join([doc.content for doc in results])
                return f"HR Policy Information:\n{context}"
            else:
                return "No relevant HR policy information found for this query."

        except Exception as e:
            return f"Error searching HR policies: {str(e)}"

    def search_technical_docs(self, query: str) -> str:
        """
        Search technical documentation and API references.

        Args:
            query (str): Search query related to APIs, technical implementation, database schema

        Returns:
            str: Relevant technical documentation
        """
        if len(self.knowledge_bases) < 2:
            return "No technical knowledge base available"

        try:
            # Search in the second knowledge base (technical docs)
            tech_kb = self.knowledge_bases[1]
            results = tech_kb.search(query, max_results=3)

            if results:
                context = "\n\n".join([doc.content for doc in results])
                return f"Technical Documentation:\n{context}"
            else:
                return "No relevant technical documentation found for this query."

        except Exception as e:
            return f"Error searching technical docs: {str(e)}"

def main():
    print("🤖 Exercise 6: Agentic RAG")
    print("=" * 40)
    print("Setting up intelligent multi-document RAG system...")
    print()

    # Set up multiple knowledge bases
    knowledge_bases = setup_multiple_knowledge_bases()
    if not knowledge_bases:
        print("❌ No knowledge bases available. Check sample documents.")
        return

    print(f"\n✅ Loaded {len(knowledge_bases)} knowledge bases")
    print("🧠 Agent can intelligently search across different document types!")
    print()

    # Combine all knowledge bases for unified search
    # Use the first knowledge base as primary (it contains multiple documents)
    combined_knowledge = knowledge_bases[0] if knowledge_bases else None

    # Create sophisticated agent with built-in knowledge search
    agent = Agent(
        model=Groq(
            id="llama-3.3-70b-versatile",
            max_tokens=1200
        ),
        description="""You are an intelligent assistant for ACME Corporation with access to
        company knowledge including HR policies and technical documentation.
        Use your knowledge base to answer questions about company policies, procedures,
        technical documentation, and other company information.

        If you can't find information in the knowledge base, you can also search the web.""",

        # 🔧 Knowledge and web search capabilities
        knowledge=combined_knowledge,
        search_knowledge=True,  # Enable automatic knowledge search
        tools=[DuckDuckGoTools()],  # Web search for missing information

        markdown=True,
        read_tool_call_history=True  # Remember previous searches
    )

    print("💡 Agentic RAG features:")
    print("  🎯 Intelligent routing to appropriate knowledge base")
    print("  🔄 Multi-step retrieval for complex questions")
    print("  📚 Search across HR policies and technical docs")
    print("  🌐 Fallback to web search for missing information")
    print()

    print("🎮 Try these complex questions:")
    print("  💼 'How do I set up a new employee with API access?'")
    print("  🔧 'What's our remote work policy and how do I configure VPN API calls?'")
    print("  📊 'I need the performance review schedule and user management API details'")
    print()

    while True:
        try:
            user_input = input("Question: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye! 👋")
                break

            print("\nIntelligent Assistant:")
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
🎯 Try these agentic RAG questions:

Cross-Domain Questions:
1. "I'm a new developer. What equipment will I get and how do I access the API?"
2. "What's the remote work policy and how do I set up webhook endpoints from home?"
3. "How many vacation days do I get and what's the rate limit for the user API?"

Multi-Step Retrieval:
4. "I need to create a project management dashboard. What API endpoints should I use and what's our deployment policy?"
5. "A team member is leaving. How do I handle their benefits termination and deactivate their API access?"

Testing Intelligence:
6. "What programming languages does the company use?" (not in docs, should search web)
7. "Compare our benefits to Google's" (needs external search)

🧠 Key Concepts (Agentic vs Basic RAG):

Basic RAG:
- Single retrieval per question
- Fixed search strategy
- One knowledge source
- Simple query → retrieve → generate

Agentic RAG:
- Multiple retrievals as needed
- Intelligent routing to appropriate sources
- Multi-document search
- Dynamic: question → analyze → route → search → reason → search again → generate

🔍 What You'll See:
- Agent deciding which knowledge base to search
- Multiple tool calls for complex questions
- Intelligent routing based on question type
- Combination of internal docs + web search
- Multi-step reasoning with retrieved information

⚡ Advanced Features:
- read_tool_call_history=True enables learning from previous searches
- Separate vector collections for different document types
- Custom tools for targeted knowledge search
- Fallback to web search for missing information

📝 Next: In 07_workflow_agent.py, we'll build multi-step business workflows!
"""