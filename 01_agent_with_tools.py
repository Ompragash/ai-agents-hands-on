"""
Exercise 1: Agent with Tools - Adding Web Search Capabilities
=============================================================

Learning Objectives:
- Understand how tools extend agent capabilities
- Learn about function calling and tool use
- See how agents can access real-time information

This agent can search the web using DuckDuckGo, making it much more powerful
than the basic conversational agent from Exercise 0.
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools

# Load environment variables
load_dotenv()

def main():
    print("🔍 Exercise 1: Agent with Web Search Tools")
    print("=" * 50)
    print("This agent can search the web for current information!")
    print("Try asking about recent news, current events, or specific facts.")
    print("Type 'exit' to quit.\n")

    # Create an agent with web search capabilities
    agent = Agent(
        model=Groq(
            id="llama-3.3-70b-versatile",
            max_tokens=800  # Longer responses for detailed information
        ),
        description="""You are an enthusiastic research assistant with access to web search.
        When users ask for current information, recent news, or specific facts,
        use your search tools to find accurate, up-to-date information.""",

        # 🔧 This is the key addition - tools!
        tools=[DuckDuckGoTools()],  # Enables web search

        markdown=True
    )

    print("💡 Pro tip: The agent will automatically decide when to search the web!")
    print("Watch for tool calls when you ask for current information.\n")

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
🎯 Try these prompts to see tool usage:
1. "What's the latest news about AI?"
2. "What's the weather like in Tokyo today?"
3. "Tell me about the latest SpaceX launch"
4. "What are the current stock prices for Tesla?"
5. "What happened in the world today?"

Compare with these prompts that won't trigger tools:
1. "Tell me a joke" (no search needed)
2. "Explain how photosynthesis works" (general knowledge)
3. "What's 5 + 5?" (simple calculation)

🧠 Key Concepts:
- tools=[DuckDuckGoTools()] adds web search capability
- show_tool_calls=True lets you see when tools are used
- The agent automatically decides when to use tools
- Tools turn agents from chatbots into action-taking systems

📝 Next: In 02_custom_tools.py, we'll build our own custom tools!
"""