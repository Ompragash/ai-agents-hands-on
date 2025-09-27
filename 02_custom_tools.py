"""
Exercise 2: Custom Tools - Building Your Own Agent Capabilities
===============================================================

Learning Objectives:
- Learn how to create custom tools for agents
- Understand tool interfaces and function signatures
- See how to combine multiple tools in one agent

This exercise shows how to build custom tools that extend agent capabilities
beyond pre-built options like web search.
"""

import os
import random
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.toolkit import Toolkit

# Load environment variables
load_dotenv()

class MathToolkit(Toolkit):
    """Custom toolkit for mathematical operations"""

    def __init__(self):
        super().__init__(name="math_toolkit")
        self.register(self.calculator)
        self.register(self.random_number)

    def calculator(self, expression: str) -> str:
        """
        Evaluate mathematical expressions safely.

        Args:
            expression (str): Mathematical expression to evaluate (e.g., "2+2", "10*5+3")

        Returns:
            str: Result of the calculation
        """
        try:
            # Safe evaluation - only allow basic math operations
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return "Error: Only basic math operations (+, -, *, /, parentheses) are allowed"

            result = eval(expression)
            return f"The result of '{expression}' is: {result}"

        except Exception as e:
            return f"Error calculating '{expression}': {str(e)}"

    def random_number(self, min_val: int = 1, max_val: int = 100) -> str:
        """
        Generate a random number within a specified range.

        Args:
            min_val (int): Minimum value (default: 1)
            max_val (int): Maximum value (default: 100)

        Returns:
            str: Random number and range information
        """
        if min_val >= max_val:
            return "Error: min_val must be less than max_val"

        number = random.randint(min_val, max_val)
        return f"Random number between {min_val} and {max_val}: {number}"


class UtilityToolkit(Toolkit):
    """Custom toolkit for utility functions"""

    def __init__(self):
        super().__init__(name="utility_toolkit")
        self.register(self.current_time)
        self.register(self.text_stats)

    def current_time(self, timezone: str = "UTC") -> str:
        """
        Get the current date and time.

        Args:
            timezone (str): Timezone (currently only supports UTC)

        Returns:
            str: Current date and time
        """
        now = datetime.now()
        return f"Current time ({timezone}): {now.strftime('%Y-%m-%d %H:%M:%S')}"

    def text_stats(self, text: str) -> str:
        """
        Analyze text and provide statistics.

        Args:
            text (str): Text to analyze

        Returns:
            str: Text statistics
        """
        words = text.split()
        characters = len(text)
        characters_no_spaces = len(text.replace(' ', ''))
        sentences = len([s for s in text.split('.') if s.strip()])

        return f"""Text Analysis:
        - Characters: {characters}
        - Characters (no spaces): {characters_no_spaces}
        - Words: {len(words)}
        - Sentences: {sentences}
        - Average word length: {characters_no_spaces / len(words):.1f} characters"""


def main():
    print("🔧 Exercise 2: Custom Tools")
    print("=" * 40)
    print("This agent has custom math and utility tools!")
    print("Try calculations, random numbers, time, or text analysis.")
    print("Type 'exit' to quit.\n")

    # Create agent with multiple custom toolkits
    agent = Agent(
        model=Groq(
            id="llama-3.3-70b-versatile",
            max_tokens=600
        ),
        description="""You are a helpful assistant with mathematical and utility tools.
        You can perform calculations, generate random numbers, tell time, and analyze text.
        When users ask for calculations or utilities, use your available tools.""",

        # 🔧 Multiple custom toolkits
        tools=[
            MathToolkit(),    # Math operations
            UtilityToolkit()  # Utility functions
        ],

        markdown=True
    )

    print("💡 Available capabilities:")
    print("  📊 Math: calculations, random numbers")
    print("  🛠️  Utilities: current time, text analysis")
    print()

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
🎯 Try these prompts to test custom tools:

Math Tools:
1. "What's 15 * 23 + 7?"
2. "Calculate (100 - 25) / 3"
3. "Give me a random number between 1 and 1000"
4. "Generate a random number between 50 and 75"

Utility Tools:
5. "What time is it?"
6. "Analyze this text: 'The quick brown fox jumps over the lazy dog'"
7. "Give me stats for this paragraph: [paste any text]"

Mixed:
8. "Generate 3 random numbers and calculate their sum"
9. "What time is it and what's 24 * 60 * 60?" (seconds in a day)

🧠 Key Concepts:
- Toolkit class lets you group related functions
- self.register() adds functions as tools
- Docstrings become tool descriptions for the LLM
- Type hints help the LLM understand parameters
- Error handling prevents crashes from bad inputs

🎨 DIY Challenge:
Add a weather tool that returns mock weather data for different cities!

📝 Next: In 03_agent_with_memory.py, we'll add conversation memory!
"""