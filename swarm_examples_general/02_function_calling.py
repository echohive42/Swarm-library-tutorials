"""
# Function Calling Example - Weather and Calculator Agent
# This example shows how to create an agent with multiple utility functions
# Demonstrates how to structure functions, handle their returns, and use them in conversation
# Shows practical usage of function calling in a chat context
"""

import os
from termcolor import colored
import json
from datetime import datetime
from swarm import Swarm, Agent

# Constants
MODEL = "gpt-4o"
HISTORY = []

def get_current_time() -> str:
    """Get the current time in a readable format."""
    print(colored("\n🕒 Getting current time...", "magenta"))
    current_time = datetime.now()
    return current_time.strftime("%I:%M %p")

def calculate(operation: str, x: float, y: float) -> str:
    """Perform basic mathematical operations.
    
    Args:
        operation: One of 'add', 'subtract', 'multiply', 'divide'
        x: First number
        y: Second number
    """
    print(colored(f"\n🔢 Calculating {operation} of {x} and {y}...", "magenta"))
    try:
        match operation.lower():
            case "add":
                result = x + y
            case "subtract":
                result = x - y
            case "multiply":
                result = x * y
            case "divide":
                if y == 0:
                    return "Error: Cannot divide by zero"
                result = x / y
            case _:
                return f"Error: Unknown operation '{operation}'"
        
        return f"Result of {operation}({x}, {y}) = {result}"
    except Exception as e:
        return f"Error performing calculation: {str(e)}"

def get_fake_weather(city: str) -> str:
    """Get simulated weather information for a city.
    
    Args:
        city: Name of the city
    """
    print(colored(f"\n🌤️ Checking weather for {city}...", "magenta"))
    import random
    conditions = ["Sunny", "Cloudy", "Rainy", "Windy"]
    temp = random.randint(0, 35)
    condition = random.choice(conditions)
    return f"Weather in {city}: {condition}, {temp}°C"

# Initialize Swarm client
print(colored("Initializing Swarm client...", "cyan"))
client = Swarm()

# Create utility agent with multiple functions
utility_agent = Agent(
    name="Utility Helper",
    model=MODEL,
    instructions="""You are a helpful assistant with access to various utility functions.
    You can:
    1. Tell the current time
    2. Perform basic calculations
    3. Check weather (simulated)
    
    Use these functions when appropriate in conversation.
    Always explain what you're doing before using a function.""",
    functions=[get_current_time, calculate, get_fake_weather]
)

def chat_loop():
    global HISTORY
    print(colored("\nUtility Agent Chat started! Type 'exit' to end.", "green"))
    print(colored("Try asking about:\n- Current time\n- Math calculations\n- Weather in any city", "cyan"))
    
    while True:
        # Get user input
        user_input = input(colored("\nYou: ", "yellow"))
        
        if user_input.lower() == 'exit':
            print(colored("\nEnding chat...", "red"))
            break

        # Add user message to history
        HISTORY.append({"role": "user", "content": user_input})

        try:
            # Get response from agent
            print(colored("\nAgent is thinking...", "cyan"))
            response = client.run(
                agent=utility_agent,
                messages=HISTORY
            )

            # Update history with agent's response
            HISTORY.extend(response.messages)
            
            # Print agent's response
            print(colored(f"\nAgent: {response.messages[-1]['content']}", "green"))

        except Exception as e:
            print(colored(f"\nError: {str(e)}", "red"))

if __name__ == "__main__":
    try:
        chat_loop()
    except KeyboardInterrupt:
        print(colored("\nChat ended by user.", "yellow"))
    except Exception as e:
        print(colored(f"\nUnexpected error: {str(e)}", "red")) 