"""
Exercise 4: Persistent Memory - Long-term Memory with PostgreSQL
================================================================

Learning Objectives:
- Understand persistent memory storage
- Learn about user memories and session management
- See how database integration works with agents

This agent stores memories permanently in a PostgreSQL database,
remembering information across different conversation sessions.

Prerequisites:
- PostgreSQL with pgvector extension running
- See agent-course/podman_setup_commands.md for setup instructions
"""

import os
import argparse
from uuid import uuid4
from dotenv import load_dotenv
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from rich.pretty import pprint

# Load environment variables
load_dotenv()

# Database connection - matches the setup in agent-course
DB_URL = "postgresql+psycopg://ai:ai@localhost:5532/ai"

def check_database_connection():
    """Check if database is accessible"""
    try:
        db = PostgresDb(db_url=DB_URL)
        print("✅ Database connection successful!")
        return db
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n🔧 Setup required:")
        print("1. Make sure PostgreSQL with pgvector is running")
        print("2. Check agent-course/podman_setup_commands.md for setup")
        print("3. Verify database is accessible at localhost:5532")
        return None

def main(session_id: str = None):
    print("💾 Exercise 4: Persistent Memory")
    print("=" * 45)

    # Check database connection first
    db = check_database_connection()
    if not db:
        return

    print("This agent remembers you across different sessions!")
    print("Your memories are stored permanently in PostgreSQL.")
    print("Type 'mem' to see stored memories, 'exit' to quit.\n")

    # Use provided session or create new one
    if not session_id:
        session_id = str(uuid4())
        print(f"📝 New session: {session_id[:8]}...")
    else:
        print(f"📝 Continuing session: {session_id[:8]}...")

    user_id = "workshop_student"

    # Create agent with persistent memory
    agent = Agent(
        model=Groq(
            id="llama-3.3-70b-versatile",
            max_tokens=800
        ),
        description="""You are a helpful assistant with excellent long-term memory.
        You remember important information about users across different conversations
        and can build upon previous interactions.""",

        # 💾 Database and memory configuration
        db=db,                          # PostgreSQL database connection
        enable_user_memories=True,      # Store user-specific memories
        read_chat_history=True,         # Read previous conversations
        add_history_to_context=True,    # Include history in context
        num_history_runs=10,            # Remember more exchanges

        tools=[DuckDuckGoTools()],
        markdown=True
    )

    print("💡 Persistent memory features:")
    print("  💾 Memories stored permanently in database")
    print("  🔄 Continues conversations across sessions")
    print("  👤 Remembers user-specific information")
    print("  📜 Maintains chat history")
    print()

    print("🎮 Commands:")
    print("  'mem' or 'memories' - Show stored memories")
    print("  'exit', 'quit', 'q' - Exit the program")
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye! Your memories are saved. 👋")
                break

            # Special command to view memories
            if user_input.lower() in ['mem', 'memories']:
                try:
                    memories = agent.get_user_memories(user_id=user_id)
                    if memories:
                        print("\n🧠 Stored Memories:")
                        pprint(memories)
                    else:
                        print("\n🧠 No memories stored yet.")
                    print()
                    continue
                except Exception as e:
                    print(f"Error retrieving memories: {e}")
                    continue

            print("\nAgent:")
            agent.print_response(
                user_input,
                stream=False,
                user_id=user_id,
                session_id=session_id
            )
            print()

        except KeyboardInterrupt:
            print("\nGoodbye! Your memories are saved. 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in environment variables.")
        exit(1)

    # Command line argument for session continuation
    parser = argparse.ArgumentParser(description="Persistent Memory Agent")
    parser.add_argument(
        "--session-id",
        dest="session_id",
        help="Continue an existing session (use the session ID from previous run)"
    )
    args = parser.parse_args()

    main(session_id=args.session_id)

"""
🎯 Try these conversation flows:

First Session:
1. "Hi! My name is [your name] and I work as a [job title]"
2. "I'm interested in learning about machine learning"
3. "My favorite programming language is Python"
4. Type 'mem' to see what was stored
5. Exit and note your session ID

Second Session (use --session-id):
1. Run: python 04_persistent_memory.py --session-id YOUR_SESSION_ID
2. "Do you remember me?" (should remember your details)
3. "What was I interested in learning?" (should recall ML interest)
4. "Recommend some Python ML libraries" (contextual to your interests)

Testing Memory Persistence:
1. "I just bought a new car - it's a Tesla Model 3"
2. Exit and restart (new session)
3. "What kind of car do I drive?" (should remember Tesla)

🧠 Key Concepts:
- PostgresDb() provides persistent storage
- enable_user_memories=True stores user-specific information
- Memories survive across different conversation sessions
- session_id allows continuing specific conversations
- Database stores both memories and chat history

🔍 What's Stored:
- User memories (facts about the user)
- Chat history (conversation exchanges)
- Session information (conversation threads)
- Timestamps and metadata

⚙️ Database Setup Required:
If you get connection errors, you need to set up PostgreSQL:
1. See agent-course/podman_setup_commands.md
2. Ensure PostgreSQL is running on localhost:5532
3. Database should have pgvector extension installed

📝 Next: In 05_basic_rag.py, we'll add document knowledge with RAG!
"""