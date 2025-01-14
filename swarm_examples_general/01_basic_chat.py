"""
# Basic Swarm Example - Simple Chat Agent
# This example demonstrates the most basic usage of Swarm
# Shows how to create a simple agent and maintain conversation history
# Perfect starting point for understanding Swarm's core functionality
"""

import os
from termcolor import colored
from openai import AsyncOpenAI
from swarm import Swarm, Agent

# Constants
MODEL = "gpt-4o"
HISTORY = []

# Initialize Swarm client
print(colored("Initializing Swarm client...", "cyan"))
client = Swarm()

# Create a basic agent
basic_agent = Agent(
    name="Basic Helper",
    model=MODEL,
    instructions="You are a helpful and friendly AI assistant. Keep your responses concise and clear."
)

def chat_loop():
    global HISTORY
    print(colored("\nChat started! Type 'exit' to end the conversation.", "green"))
    
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
                agent=basic_agent,
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
