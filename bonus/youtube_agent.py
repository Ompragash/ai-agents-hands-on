"""
Bonus Exercise: YouTube Agent - AI Assistant with Video Knowledge
================================================================

Learning Objectives:
- Learn how to extract knowledge from YouTube videos
- Understand video transcript processing and embeddings
- See how to build AI assistants with video-based knowledge

This agent can answer questions about the specific YouTube video content
by analyzing the video transcript and creating a searchable knowledge base.

Video: "Building AI Agents with Python" by Arjan Codes
URL: https://www.youtube.com/watch?v=D7_ipDqhtwk
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.knowledge import Knowledge
from agno.knowledge.reader.youtube_reader import YouTubeReader
from agno.vectordb.pgvector import PgVector
from agno.knowledge.embedder.huggingface import HuggingfaceCustomEmbedder
from agno.tools.duckduckgo import DuckDuckGoTools

# Load environment variables
load_dotenv()

# Database configuration
DB_URL = "postgresql+psycopg://ai:ai@localhost:5532/ai"

def setup_youtube_knowledge():
    """Set up YouTube video knowledge base"""

    print("🎥 Setting up YouTube knowledge base...")
    print("📺 Processing video: Building AI Agents with Python")
    print("🔗 https://www.youtube.com/watch?v=D7_ipDqhtwk")
    print()

    try:
        # Create vector database with HuggingFace embedder
        vector_db = PgVector(
            db_url=DB_URL,
            table_name="youtube_knowledge",
            embedder=HuggingfaceCustomEmbedder(
                id="sentence-transformers/all-MiniLM-L6-v2",
                dimensions=384
            )
        )

        # Create knowledge base
        knowledge = Knowledge(
            name="YouTube AI Agents Tutorial",
            description="Knowledge from Arjan Codes video about building AI agents with Python",
            vector_db=vector_db,
            max_results=5
        )

        # Add YouTube video content
        print("📥 Downloading and processing video transcript...")
        knowledge.add_content(
            name="ai_agents_tutorial",
            description="Tutorial video about building AI agents with Python by Arjan Codes",
            url="https://www.youtube.com/watch?v=D7_ipDqhtwk",
            reader=YouTubeReader(),
            metadata={
                "source": "youtube",
                "type": "tutorial",
                "author": "Arjan Codes",
                "topic": "AI Agents with Python"
            }
        )

        print("✅ YouTube knowledge base created successfully!")
        print("📄 Video transcript processed and embedded")
        return knowledge

    except Exception as e:
        print(f"❌ Error setting up YouTube knowledge: {e}")
        print("Make sure:")
        print("1. PostgreSQL with pgvector is running")
        print("2. HUGGINGFACE_API_KEY is set in .env file")
        print("3. Internet connection is available for video download")
        return None

def main():
    print("🎥 Bonus Exercise: YouTube Agent")
    print("=" * 45)
    print("This agent knows about AI agents from the Arjan Codes video!")
    print("Ask questions about the video content.")
    print("Type 'exit' to quit.\n")

    # Check database connection
    try:
        from agno.db.postgres import PostgresDb
        db = PostgresDb(db_url=DB_URL)
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please ensure PostgreSQL is running (see Exercise 4)")
        return

    # Setup YouTube knowledge base
    knowledge = setup_youtube_knowledge()
    if not knowledge:
        print("❌ Failed to setup YouTube knowledge base")
        return

    print("\n🤖 YouTube AI Agent ready!")
    print("Ask questions about building AI agents with Python.")
    print()

    # Create agent with YouTube knowledge
    agent = Agent(
        model=Groq(
            id="llama-3.3-70b-versatile",
            max_tokens=1000
        ),
        description="""You are an AI assistant with knowledge about building AI agents with Python,
        based on Arjan Codes' tutorial video. You can answer questions about:
        - AI agent architecture and design patterns
        - Python libraries and frameworks for AI agents
        - Best practices for building AI agents
        - Code examples and implementation details from the video

        Use your knowledge base to provide accurate information from the video content.
        If asked about topics not covered in the video, you can search the web for additional information.""",

        # 🎥 YouTube knowledge and web search
        knowledge=knowledge,
        search_knowledge=True,  # Enable automatic video knowledge search
        tools=[DuckDuckGoTools()],  # Web search for topics not in video

        markdown=True,
        read_tool_call_history=True
    )

    print("💡 Try asking about:")
    print("  🤖 'What are the main components of an AI agent?'")
    print("  🐍 'What Python libraries does Arjan recommend for AI agents?'")
    print("  🏗️  'How should I structure my AI agent code?'")
    print("  🔧 'What are some best practices for building AI agents?'")
    print("  📚 'Can you summarize the key points from the video?'")
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye! 👋")
                break

            print("\nYouTube AI Agent:")
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

    if not os.getenv("HUGGINGFACE_API_KEY"):
        print("❌ Error: HUGGINGFACE_API_KEY not found in environment variables.")
        print("Please add your HuggingFace API key to the .env file")
        exit(1)

    main()

"""
🎯 Try these questions to test YouTube knowledge:

Video Content Questions:
1. "What is the main topic of the video?"
2. "What Python libraries are mentioned for building AI agents?"
3. "What are the key components of an AI agent according to Arjan?"
4. "Can you explain the agent architecture shown in the video?"
5. "What are some best practices mentioned for AI agent development?"

Implementation Questions:
6. "How should I structure my AI agent project?"
7. "What design patterns are recommended for AI agents?"
8. "What are the common challenges in building AI agents?"
9. "Can you summarize the main takeaways from the video?"
10. "What tools and frameworks does Arjan recommend?"

🧠 Key Features:
- YouTubeReader automatically downloads and processes video transcripts
- HuggingFace embedder creates searchable video knowledge
- Agent can answer specific questions about video content
- Fallback web search for topics not covered in the video
- PostgreSQL storage for persistent video knowledge

🔧 Technical Notes:
- Requires active internet connection for video download
- Video transcript is chunked and embedded for efficient search
- Knowledge persists in database for future sessions
- Compatible with various video lengths and content types

📝 Next Steps:
Try building your own YouTube agents with different educational videos!
You can easily swap the URL to analyze other programming tutorials,
lectures, or educational content.
"""