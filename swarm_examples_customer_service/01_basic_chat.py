"""
# Basic chat example demonstrating a simple customer service agent
# Shows how to set up a basic agent with instructions and maintain chat history
# Uses termcolor for better user experience
# Demonstrates basic error handling
"""

from swarm import Swarm, Agent
from termcolor import colored
import os
from openai import AsyncOpenAI
import asyncio

# Constants
MODEL_NAME = "gpt-4o"
AGENT_NAME = "Customer Service Rep"
SYSTEM_INSTRUCTIONS = """You are a friendly and professional customer service representative.
Your goal is to help customers with their inquiries in a polite and efficient manner.
Always maintain a positive tone and be solution-oriented."""

try:
    # Initialize the client
    client = Swarm()
    
    # Create the basic customer service agent
    agent = Agent(
        name=AGENT_NAME,
        model=MODEL_NAME,
        instructions=SYSTEM_INSTRUCTIONS
    )
    
    # Initialize conversation history
    conversation_history = []
    
    print(colored("Customer Service Chat Initialized!", "green"))
    print(colored("Type 'exit' to end the conversation\n", "yellow"))
    
    while True:
        # Get user input
        user_input = input(colored("You: ", "cyan"))
        
        if user_input.lower() == 'exit':
            print(colored("\nThank you for chatting! Goodbye!", "green"))
            break
            
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Get response from agent
            response = client.run(
                agent=agent,
                messages=conversation_history
            )
            
            # Update conversation history with agent's response
            conversation_history.extend(response.messages)
            
            # Print agent's response
            print(colored(f"\n{AGENT_NAME}: {response.messages[-1]['content']}\n", "green"))
            
        except Exception as e:
            print(colored(f"\nError: {str(e)}", "red"))
            print(colored("Please try again.\n", "yellow"))
            
except Exception as e:
    print(colored(f"Initialization Error: {str(e)}", "red")) 