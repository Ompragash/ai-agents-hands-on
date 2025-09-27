"""
Exercise 3: Agent with Memory - Short-term Conversation Memory
==============================================================

Learning Objectives:
- Understand how agents can remember conversation history
- Learn about context windows and memory management
- See how memory improves user experience

This agent remembers your conversation within the session, making it feel
more natural and contextual.
"""

import os
from uuid import uuid4
from dotenv import load_dotenv
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools

# Load environment variables
load_dotenv()

# Database configuration - matches the setup in agent-course
DB_URL = "postgresql+psycopg://ai:ai@localhost:5532/ai"

def main():
    print("🧠 Exercise 3: Agent with Memory")
    print("=" * 40)
    print("This agent remembers our conversation!")
    print("Try referring to things you mentioned earlier.")
    print("Type 'exit' to quit.\n")

    # Initialize database connection
    try:
        db = PostgresDb(db_url=DB_URL)
        print("✅ Database connected successfully!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Memory features will be limited without database.")
        db = None

    # Generate a unique session ID for this conversation
    session_id = str(uuid4())
    user_id = "workshop_student"  # In real apps, this would be the actual user ID

    # Create an agent with memory capabilities
    agent = Agent(
        model=Groq(
            id="llama-3.3-70b-versatile",
            max_tokens=800
        ),
        description="""You are a helpful assistant with a good memory.
        You remember what users tell you during our conversation and can
        refer back to previous topics, preferences, and information.""",

        tools=[DuckDuckGoTools()],  # Keep web search for comprehensive responses

        # 🧠 Memory configuration
        db=db,                        # Database for persistent memory
        add_history_to_context=True,  # Include conversation history in context
        num_history_runs=5,           # Remember last 5 exchanges

        markdown=True
    )

    print("💡 Memory features:")
    print("  🔄 Remembers last 5 conversation exchanges")
    print("  📝 Can refer to things you mentioned earlier")
    print("  🎯 Maintains context throughout the session")
    print()

    print("🎮 Try this:")
    print("1. Tell the agent your name and favorite hobby")
    print("2. Ask about something unrelated")
    print("3. Later, ask 'What's my name?' or 'What do I like?'")
    print()

    exchange_count = 0

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye! 👋")
                break

            exchange_count += 1
            print(f"\nAgent (Exchange #{exchange_count}):")

            # The session_id and user_id help maintain conversation continuity
            agent.print_response(
                user_input,
                stream=False,
                session_id=session_id,
                user_id=user_id
            )
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
🎯 Try these conversation flows to test memory:

Flow 1 - Personal Information:
1. "Hi! My name is [your name] and I love [hobby]"
2. "What's the weather like today?" (different topic)
3. "What's my name again?" (should remember)
4. "What do I enjoy doing?" (should remember hobby)

Flow 2 - Building Context:
1. "I'm planning a trip to Japan"
2. "What's the currency there?"
3. "Should I visit in spring or fall?" (remembers you're going to Japan)
4. "Any food recommendations for my trip?" (still remembers the context)

Flow 3 - Problem Solving:
1. "I'm learning Python programming"
2. "What's a good first project?"
3. "How do I handle errors in Python?" (knows you're learning Python)
4. "Any good resources for someone like me?" (remembers you're a beginner)

🧠 Key Concepts:
- add_history_to_context=True includes past messages in LLM context
- num_history_runs=5 limits memory to prevent context overflow
- session_id groups related conversations
- user_id identifies the specific user (for multi-user systems)
- Memory improves user experience but uses more tokens

⚠️ Limitations:
- Memory is temporary (lost when script ends)
- Limited to recent exchanges (5 in this example)
- Uses more tokens = higher API costs
- No long-term user preferences stored

📝 Next: In 04_persistent_memory.py, we'll add permanent memory with a database!
"""