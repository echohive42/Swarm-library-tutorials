"""
# Agent Handoff Example - Customer Service System
# This example shows how to implement agent handoffs between different departments
# Demonstrates how to transfer conversations between specialized agents
# Implements a customer service system with support, sales, and technical departments
"""

import os
from termcolor import colored
from swarm import Swarm, Agent
from swarm.types import Result

# Constants
MODEL = "gpt-4o"
HISTORY = []

def check_order_status(order_id: str) -> str:
    """Check the status of an order.
    
    Args:
        order_id: The order ID to check
    """
    print(colored(f"\n🔍 Checking status for Order #{order_id}...", "magenta"))
    # Simulate order status check
    import random
    statuses = ["Processing", "Shipped", "Delivered", "Pending"]
    return f"Order {order_id} status: {random.choice(statuses)}"

def get_product_info(product_name: str) -> str:
    """Get information about a product.
    
    Args:
        product_name: Name of the product
    """
    print(colored(f"\n📦 Fetching information for product: {product_name}...", "magenta"))
    products = {
        "laptop": "High-performance laptop with 16GB RAM, 512GB SSD",
        "phone": "Latest smartphone with 5G capability",
        "tablet": "10-inch tablet with retina display",
    }
    return products.get(product_name.lower(), f"Product '{product_name}' not found.")

def technical_faq(issue: str) -> str:
    """Get technical support for common issues.
    
    Args:
        issue: The technical issue description
    """
    print(colored(f"\n🔧 Looking up solution for issue: {issue}...", "magenta"))
    faqs = {
        "wifi": "1. Restart your device\n2. Check WiFi settings\n3. Reset network settings",
        "battery": "1. Check power settings\n2. Update firmware\n3. Contact support if issue persists",
        "update": "1. Go to Settings\n2. Check for Updates\n3. Install available updates"
    }
    
    for keyword, solution in faqs.items():
        if keyword in issue.lower():
            return f"Solution for {issue}:\n{solution}"
    return "No specific solution found. Please contact technical support."

# Create specialized agents
support_agent = Agent(
    name="Support Agent",
    model=MODEL,
    instructions="""You are a customer support agent.
    You handle general inquiries and can check order status.
    If the query is about sales or technical issues, transfer to the appropriate agent.""",
    functions=[check_order_status]
)

sales_agent = Agent(
    name="Sales Agent",
    model=MODEL,
    instructions="""You are a sales agent.
    You provide product information and handle sales inquiries.
    If the query is about support or technical issues, transfer to the appropriate agent.""",
    functions=[get_product_info]
)

tech_agent = Agent(
    name="Technical Agent",
    model=MODEL,
    instructions="""You are a technical support agent.
    You handle technical issues and provide troubleshooting steps.
    If the query is about sales or general support, transfer to the appropriate agent.""",
    functions=[technical_faq]
)

def transfer_to_support() -> Result:
    """Transfer the conversation to the support agent."""
    print(colored("\n🔄 Transferring to support team...", "yellow"))
    return Result(
        value="Transferring you to our support team...",
        agent=support_agent
    )

def transfer_to_sales() -> Result:
    """Transfer the conversation to the sales agent."""
    print(colored("\n🔄 Transferring to sales team...", "yellow"))
    return Result(
        value="Transferring you to our sales team...",
        agent=sales_agent
    )

def transfer_to_tech() -> Result:
    """Transfer the conversation to the technical support agent."""
    print(colored("\n🔄 Transferring to technical support team...", "yellow"))
    return Result(
        value="Transferring you to our technical support team...",
        agent=tech_agent
    )

# Add transfer functions to each agent
support_agent.functions.extend([transfer_to_sales, transfer_to_tech])
sales_agent.functions.extend([transfer_to_support, transfer_to_tech])
tech_agent.functions.extend([transfer_to_support, transfer_to_sales])

# Initialize Swarm client
print(colored("Initializing Swarm client...", "cyan"))
client = Swarm()

def chat_loop():
    global HISTORY
    current_agent = support_agent  # Start with support agent
    
    print(colored("\nCustomer Service System started! Type 'exit' to end.", "green"))
    print(colored("You can ask about:\n- Order status\n- Product information\n- Technical support", "cyan"))
    
    while True:
        # Get user input
        user_input = input(colored("\nYou: ", "yellow"))
        
        if user_input.lower() == 'exit':
            print(colored("\nEnding chat...", "red"))
            break

        # Add user message to history
        HISTORY.append({"role": "user", "content": user_input})

        try:
            # Get response from current agent
            print(colored(f"\n{current_agent.name} is thinking...", "cyan"))
            response = client.run(
                agent=current_agent,
                messages=HISTORY
            )

            # Update history with agent's response
            HISTORY.extend(response.messages)
            
            # Check if agent changed
            if response.agent and response.agent != current_agent:
                current_agent = response.agent
                print(colored(f"\nTransferred to {current_agent.name}", "yellow"))
            
            # Print agent's response
            print(colored(f"\n{current_agent.name}: {response.messages[-1]['content']}", "green"))

        except Exception as e:
            print(colored(f"\nError: {str(e)}", "red"))

if __name__ == "__main__":
    try:
        chat_loop()
    except KeyboardInterrupt:
        print(colored("\nChat ended by user.", "yellow"))
    except Exception as e:
        print(colored(f"\nUnexpected error: {str(e)}", "red")) 