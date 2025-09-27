"""
Exercise 0: Hello Agent - Your First AI Agent
=============================================

Learning Objectives:
- Understand basic agent initialization
- Learn how to interact with an LLM via Groq
- See the simplest possible agent in action

This is the most basic agent possible - just a conversation with an LLM.
No tools, no memory, just pure conversation.
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq

# Load environment variables from .env file
load_dotenv()

def main():
    print("🤖 Exercise 0: Hello Agent")
    print("=" * 40)
    print("This is the simplest possible agent - just an LLM conversation.")
    print("Type 'exit' to quit.\n")

    # Create the simplest agent
    agent = Agent(
        model=Groq(
            id="llama-3.3-70b-versatile",  # Fast and capable model
            max_tokens=500                  # Limit response length
        ),
        description="You are a helpful and friendly AI assistant.",
        markdown=True  # Format responses nicely
    )

    # Simple conversation loop
    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye! 👋")
                break

            print("\nAgent:")
            agent.print_response(user_input, stream=False)
            print()  # Add spacing

        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key.")
        exit(1)

    main()

"""
🎯 Try these prompts:
1. "Hello! What can you do?"
2. "Tell me a joke"
3. "Explain quantum computing in simple terms"
4. "What's 2+2?" (Notice: no calculator tool yet!)

🧠 Key Concepts:
- Agent() creates an AI agent
- Groq() provides the LLM model
- agent.print_response() generates and displays responses
- No tools = no external actions, just conversation

📝 Next: In 01_agent_with_tools.py, we'll add web search capabilities!
"""