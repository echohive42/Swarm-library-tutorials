"""
# Function calling example with order status and shipment tracking
# Shows how to implement useful customer service functions
# Demonstrates how to handle function returns and maintain context
# Includes error handling and informative status messages
"""

from swarm import Swarm, Agent
from swarm.types import Result
from termcolor import colored
import os
from openai import AsyncOpenAI
import asyncio
from typing import Optional
import random
from datetime import datetime, timedelta

# Constants
MODEL_NAME = "gpt-4o"
AGENT_NAME = "Order Support Agent"
SYSTEM_INSTRUCTIONS = """You are an Order Support Agent who can help customers check their order status and track shipments.
Use the available functions to assist customers with their inquiries.
Always verify order numbers before checking status or tracking."""

# Mock database of orders
ORDERS = {
    "ORD123": {"status": "shipped", "tracking": "TRK789", "date": "2024-03-15"},
    "ORD456": {"status": "processing", "tracking": None, "date": "2024-03-18"},
    "ORD789": {"status": "delivered", "tracking": "TRK456", "date": "2024-03-10"}
}

def check_order_status(order_id: str) -> str:
    """Check the status of an order
    
    Args:
        order_id: The order ID to check
    """
    print(colored(f"\n🔍 Checking order status for: {order_id}", "magenta"))
    try:
        if order_id in ORDERS:
            order = ORDERS[order_id]
            return f"Order {order_id} is currently {order['status']}. Order date: {order['date']}"
        return f"Order {order_id} not found in our system."
    except Exception as e:
        return f"Error checking order status: {str(e)}"

def track_shipment(order_id: str) -> str:
    """Track a shipment for an order
    
    Args:
        order_id: The order ID to track
    """
    print(colored(f"\n📦 Tracking shipment for order: {order_id}", "magenta"))
    try:
        if order_id in ORDERS:
            order = ORDERS[order_id]
            if order['tracking']:
                # Simulate different tracking statuses
                locations = ["warehouse", "in transit", "local facility", "out for delivery", "delivered"]
                current_status = random.choice(locations)
                return f"Tracking number {order['tracking']} for order {order_id} - Status: {current_status}"
            return f"Order {order_id} doesn't have tracking information yet."
        return f"Order {order_id} not found in our system."
    except Exception as e:
        return f"Error tracking shipment: {str(e)}"

try:
    # Initialize the client
    client = Swarm()
    
    # Create the order support agent with functions
    agent = Agent(
        name=AGENT_NAME,
        model=MODEL_NAME,
        instructions=SYSTEM_INSTRUCTIONS,
        functions=[check_order_status, track_shipment]
    )
    
    # Initialize conversation history
    conversation_history = []
    
    print(colored("Order Support System Initialized!", "green"))
    print(colored("Available commands:", "yellow"))
    print(colored("- Check order status (e.g., 'What's the status of order ORD123?')", "yellow"))
    print(colored("- Track shipment (e.g., 'Track my order ORD123')", "yellow"))
    print(colored("- Type 'exit' to end the conversation\n", "yellow"))
    
    while True:
        # Get user input
        user_input = input(colored("You: ", "cyan"))
        
        if user_input.lower() == 'exit':
            print(colored("\nThank you for using our Order Support! Goodbye!", "green"))
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