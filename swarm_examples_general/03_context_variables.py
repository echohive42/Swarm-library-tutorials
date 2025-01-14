"""
# Context Variables Example - Shopping Cart Agent
# This example demonstrates how to use context variables to maintain state
# Shows how to pass and update context between function calls
# Implements a simple shopping cart system using context variables
"""

import os
from termcolor import colored
from swarm import Swarm, Agent
from swarm.types import Result

# Constants
MODEL = "gpt-4o"
HISTORY = []
PRODUCTS = {
    "laptop": 999.99,
    "phone": 599.99,
    "headphones": 99.99,
    "tablet": 299.99,
    "smartwatch": 199.99
}

def view_cart(context_variables: dict) -> str:
    """View the current items in the shopping cart."""
    print(colored("\n🛒 Viewing shopping cart contents...", "magenta"))
    cart = context_variables.get("cart", {})
    if not cart:
        return "Your cart is empty."
    
    total = sum(PRODUCTS[item] * qty for item, qty in cart.items())
    cart_items = [f"{item} (x{qty}) - ${PRODUCTS[item] * qty:.2f}" for item, qty in cart.items()]
    return "Cart Contents:\n" + "\n".join(cart_items) + f"\nTotal: ${total:.2f}"

def add_to_cart(context_variables: dict, item: str, quantity: int = 1) -> Result:
    """Add an item to the shopping cart.
    
    Args:
        item: Name of the product
        quantity: Number of items to add
    """
    print(colored(f"\n➕ Adding {quantity} {item}(s) to cart...", "magenta"))
    if item.lower() not in PRODUCTS:
        return Result(value=f"Error: Product '{item}' not found in our catalog.")
    
    cart = context_variables.get("cart", {})
    item = item.lower()
    cart[item] = cart.get(item, 0) + quantity
    
    return Result(
        value=f"Added {quantity} {item}(s) to cart.",
        context_variables={"cart": cart}
    )

def remove_from_cart(context_variables: dict, item: str, quantity: int = 1) -> Result:
    """Remove an item from the shopping cart.
    
    Args:
        item: Name of the product
        quantity: Number of items to remove
    """
    print(colored(f"\n➖ Removing {quantity} {item}(s) from cart...", "magenta"))
    cart = context_variables.get("cart", {})
    item = item.lower()
    
    if item not in cart:
        return Result(value=f"Error: '{item}' not found in your cart.")
    
    if quantity >= cart[item]:
        del cart[item]
        msg = f"Removed all {item}(s) from cart."
    else:
        cart[item] -= quantity
        msg = f"Removed {quantity} {item}(s) from cart."
    
    return Result(
        value=msg,
        context_variables={"cart": cart}
    )

def list_products() -> str:
    """List all available products and their prices."""
    print(colored("\n📋 Fetching product catalog...", "magenta"))
    return "Available Products:\n" + "\n".join(
        f"{item.title()}: ${price:.2f}" for item, price in PRODUCTS.items()
    )

# Initialize Swarm client
print(colored("Initializing Swarm client...", "cyan"))
client = Swarm()

# Create shopping cart agent
shopping_agent = Agent(
    name="Shopping Assistant",
    model=MODEL,
    instructions="""You are a helpful shopping assistant.
    You can help users:
    1. View available products
    2. Add items to their cart
    3. Remove items from their cart
    4. View their cart
    
    Always confirm actions and show the cart after modifications.
    Be helpful and suggest related items when appropriate.""",
    functions=[list_products, add_to_cart, remove_from_cart, view_cart]
)

def chat_loop():
    global HISTORY
    context = {"cart": {}}  # Initialize empty cart
    
    print(colored("\nShopping Assistant started! Type 'exit' to end.", "green"))
    print(colored("Try:\n- View products\n- Add items to cart\n- Remove items\n- View cart", "cyan"))
    
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
                agent=shopping_agent,
                messages=HISTORY,
                context_variables=context
            )

            # Update context with any changes
            context.update(response.context_variables)
            
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