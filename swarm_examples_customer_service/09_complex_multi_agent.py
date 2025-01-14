"""
# Complex multi-agent example with restaurant ordering system
# Shows how to coordinate multiple specialized agents
# Demonstrates complex workflows and state management
# Includes order processing, kitchen coordination, and delivery tracking
"""

from swarm import Swarm, Agent
from swarm.types import Result
from termcolor import colored
import os
from openai import AsyncOpenAI
import asyncio
from typing import Dict, List
from datetime import datetime
import json
import random

# Constants
DEFAULT_MODEL = "gpt-4o"
FAST_MODEL = "gpt-4o-mini"

# Mock restaurant data
MENU = {
    "appetizers": {
        "spring_rolls": {"name": "Spring Rolls", "price": 6.99, "prep_time": 10},
        "salad": {"name": "Garden Salad", "price": 7.99, "prep_time": 5},
        "soup": {"name": "Soup of the Day", "price": 5.99, "prep_time": 8}
    },
    "main_courses": {
        "pasta": {"name": "Fettuccine Alfredo", "price": 14.99, "prep_time": 20},
        "steak": {"name": "Grilled Ribeye", "price": 24.99, "prep_time": 25},
        "fish": {"name": "Grilled Salmon", "price": 19.99, "prep_time": 18}
    },
    "desserts": {
        "cake": {"name": "Chocolate Cake", "price": 6.99, "prep_time": 5},
        "ice_cream": {"name": "Ice Cream Sundae", "price": 5.99, "prep_time": 3},
        "pie": {"name": "Apple Pie", "price": 6.99, "prep_time": 5}
    }
}

# Mock order database
ORDERS = {}
ORDER_COUNTER = 0

# Order Taker Functions
def view_menu() -> str:
    """View the restaurant menu"""
    try:
        menu_text = ["Restaurant Menu:"]
        for category, items in MENU.items():
            menu_text.append(f"\n{category.upper()}:")
            for item_id, item in items.items():
                menu_text.append(
                    f"- {item['name']}: ${item['price']} ({item_id})"
                )
        return "\n".join(menu_text)
    except Exception as e:
        return f"Error viewing menu: {str(e)}"

def create_order(
    context_variables: Dict,
    customer_name: str,
    items: List[str],
    special_instructions: str = ""
) -> str:
    """Create a new order
    
    Args:
        context_variables: Current context
        customer_name: Name of the customer
        items: List of item IDs to order
        special_instructions: Special preparation instructions
    """
    try:
        global ORDER_COUNTER
        ORDER_COUNTER += 1
        order_id = f"ORD{ORDER_COUNTER:04d}"
        
        # Validate and collect items
        order_items = []
        total_prep_time = 0
        for item_id in items:
            item = None
            for category in MENU.values():
                if item_id in category:
                    item = category[item_id]
                    break
            
            if not item:
                return f"Item {item_id} not found in menu"
                
            order_items.append({
                "item_id": item_id,
                "name": item["name"],
                "price": item["price"]
            })
            total_prep_time += item["prep_time"]
            
        # Calculate total
        total = sum(item["price"] for item in order_items)
        
        # Create order
        ORDERS[order_id] = {
            "order_id": order_id,
            "customer_name": customer_name,
            "items": order_items,
            "special_instructions": special_instructions,
            "total": total,
            "status": "new",
            "estimated_prep_time": total_prep_time,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Store order ID in context for other agents
        context_variables["current_order_id"] = order_id
        
        return f"Created order {order_id} for {customer_name}. Total: ${total:.2f}"
    except Exception as e:
        return f"Error creating order: {str(e)}"

def check_order_status(order_id: str) -> str:
    """Check the status of an order
    
    Args:
        order_id: Order ID to check
    """
    try:
        if order_id not in ORDERS:
            return f"Order {order_id} not found"
            
        order = ORDERS[order_id]
        return (
            f"Order {order_id} Status:\n"
            f"Customer: {order['customer_name']}\n"
            f"Status: {order['status']}\n"
            f"Created: {order['created_at']}\n"
            f"Items: {', '.join(item['name'] for item in order['items'])}\n"
            f"Total: ${order['total']:.2f}"
        )
    except Exception as e:
        return f"Error checking order status: {str(e)}"

# Kitchen Functions
def start_preparation(context_variables: Dict) -> str:
    """Start preparing an order
    
    Args:
        context_variables: Current context including order ID
    """
    try:
        order_id = context_variables.get("current_order_id")
        if not order_id or order_id not in ORDERS:
            return "No valid order to prepare"
            
        order = ORDERS[order_id]
        if order["status"] != "new":
            return f"Order {order_id} is already {order['status']}"
            
        order["status"] = "preparing"
        return f"Started preparing order {order_id}. Estimated time: {order['estimated_prep_time']} minutes"
    except Exception as e:
        return f"Error starting preparation: {str(e)}"

def update_preparation_status(context_variables: Dict, status_update: str) -> str:
    """Update preparation status
    
    Args:
        context_variables: Current context including order ID
        status_update: Status update message
    """
    try:
        order_id = context_variables.get("current_order_id")
        if not order_id or order_id not in ORDERS:
            return "No valid order to update"
            
        order = ORDERS[order_id]
        if order["status"] not in ["preparing", "ready"]:
            return f"Order {order_id} is not being prepared"
            
        # Simulate progress
        progress = random.randint(0, 100)
        if progress >= 100:
            order["status"] = "ready"
            return f"Order {order_id} is ready for delivery!"
        
        return f"Order {order_id} preparation progress: {progress}% - {status_update}"
    except Exception as e:
        return f"Error updating status: {str(e)}"

# Delivery Functions
def assign_delivery(context_variables: Dict) -> str:
    """Assign order for delivery
    
    Args:
        context_variables: Current context including order ID
    """
    try:
        order_id = context_variables.get("current_order_id")
        if not order_id or order_id not in ORDERS:
            return "No valid order to deliver"
            
        order = ORDERS[order_id]
        if order["status"] != "ready":
            return f"Order {order_id} is not ready for delivery"
            
        # Simulate delivery assignment
        drivers = ["John", "Sarah", "Mike", "Lisa"]
        assigned_driver = random.choice(drivers)
        order["status"] = "out_for_delivery"
        order["driver"] = assigned_driver
        
        return f"Order {order_id} assigned to driver {assigned_driver}"
    except Exception as e:
        return f"Error assigning delivery: {str(e)}"

def track_delivery(context_variables: Dict) -> str:
    """Track delivery status
    
    Args:
        context_variables: Current context including order ID
    """
    try:
        order_id = context_variables.get("current_order_id")
        if not order_id or order_id not in ORDERS:
            return "No valid order to track"
            
        order = ORDERS[order_id]
        if order["status"] not in ["out_for_delivery", "delivered"]:
            return f"Order {order_id} is not out for delivery"
            
        # Simulate delivery progress
        progress = random.randint(0, 100)
        if progress >= 100:
            order["status"] = "delivered"
            return f"Order {order_id} has been delivered!"
            
        locations = ["Leaving restaurant", "On main street", "Near destination", "Arriving soon"]
        current_location = locations[progress // 25]
        
        return f"Order {order_id} - Driver {order['driver']} is {current_location}"
    except Exception as e:
        return f"Error tracking delivery: {str(e)}"

# Create specialized agents
order_taker = Agent(
    name="Order Taker",
    model=DEFAULT_MODEL,
    instructions="""You are a friendly Order Taker at our restaurant.
Help customers view the menu and place their orders.
Make sure to get all necessary details including special instructions.""",
    functions=[view_menu, create_order, check_order_status]
)

kitchen_manager = Agent(
    name="Kitchen Manager",
    model=FAST_MODEL,
    instructions="""You are the Kitchen Manager coordinating food preparation.
Monitor order preparation and update status regularly.
Ensure proper timing and coordination of all dishes.""",
    functions=[start_preparation, update_preparation_status]
)

delivery_coordinator = Agent(
    name="Delivery Coordinator",
    model=FAST_MODEL,
    instructions="""You are the Delivery Coordinator managing order deliveries.
Assign drivers and track delivery progress.
Keep customers informed about their delivery status.""",
    functions=[assign_delivery, track_delivery]
)

def transfer_to_kitchen() -> Result:
    """Transfer to kitchen manager"""
    return Result(
        value="Transferring to kitchen...",
        agent=kitchen_manager
    )

def transfer_to_delivery() -> Result:
    """Transfer to delivery coordinator"""
    return Result(
        value="Transferring to delivery...",
        agent=delivery_coordinator
    )

def transfer_to_order_taker() -> Result:
    """Transfer back to order taker"""
    return Result(
        value="Transferring to order taker...",
        agent=order_taker
    )

# Add transfer functions to each agent
order_taker.functions.append(transfer_to_kitchen)
kitchen_manager.functions.extend([transfer_to_delivery, transfer_to_order_taker])
delivery_coordinator.functions.append(transfer_to_order_taker)

try:
    # Initialize the client
    client = Swarm()
    
    # Initialize conversation and context
    conversation_history = []
    context = {}
    
    # Start with order taker
    current_agent = order_taker
    
    print(colored("Restaurant Ordering System Initialized!", "green"))
    print(colored("Available commands:", "yellow"))
    print(colored("- View menu (e.g., 'Show me the menu')", "yellow"))
    print(colored("- Place order (e.g., 'I want to order pasta and salad')", "yellow"))
    print(colored("- Check status (e.g., 'What's the status of my order?')", "yellow"))
    print(colored("Type 'exit' to end the conversation\n", "yellow"))
    
    while True:
        # Get user input
        user_input = input(colored("You: ", "cyan"))
        
        if user_input.lower() == 'exit':
            print(colored("\nThank you for dining with us! Goodbye!", "green"))
            break
            
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Get response from current agent
            response = client.run(
                agent=current_agent,
                messages=conversation_history,
                context_variables=context
            )
            
            # Update context with any changes
            context.update(response.context_variables)
            
            # Handle agent transfer if it occurred
            if response.agent:
                current_agent = response.agent
                print(colored(f"\nTransferred to {current_agent.name}!", "yellow"))
            
            # Update conversation history
            conversation_history.extend(response.messages)
            
            # Print agent's response
            print(colored(f"\n{response.messages[-1]['sender']}: {response.messages[-1]['content']}\n", "green"))
            
        except Exception as e:
            print(colored(f"\nError: {str(e)}", "red"))
            print(colored("Please try again.\n", "yellow"))
            
except Exception as e:
    print(colored(f"Initialization Error: {str(e)}", "red")) 