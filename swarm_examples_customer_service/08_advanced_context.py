"""
# Advanced context management example with personalized shopping assistant
# Shows how to maintain complex user preferences and shopping history
# Demonstrates dynamic recommendations based on context
# Includes personalized product suggestions and cart management
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

# Constants
MODEL_NAME = "gpt-4o"
AGENT_NAME = "Shopping Assistant"

# Mock product catalog
PRODUCTS = {
    "electronics": {
        "smartphone": {"name": "SmartPhone X12", "price": 899.99, "tags": ["mobile", "tech"]},
        "laptop": {"name": "LaptopPro X1", "price": 1299.99, "tags": ["computer", "tech"]},
        "headphones": {"name": "AudioMax Pro", "price": 199.99, "tags": ["audio", "accessories"]}
    },
    "clothing": {
        "jacket": {"name": "Winter Comfort Jacket", "price": 89.99, "tags": ["winter", "outerwear"]},
        "sneakers": {"name": "SportFlex Shoes", "price": 79.99, "tags": ["footwear", "sports"]},
        "jeans": {"name": "Classic Fit Jeans", "price": 59.99, "tags": ["pants", "casual"]}
    }
}

def get_instructions(context_variables: Dict) -> str:
    """Dynamic instructions based on user preferences and history"""
    print(colored("\n📋 Generating personalized shopping instructions", "magenta"))
    preferences = context_variables.get("preferences", {})
    cart = context_variables.get("shopping_cart", [])
    history = context_variables.get("purchase_history", [])
    
    instructions = f"""You are a Personalized Shopping Assistant.

Customer Preferences:
- Favorite Categories: {', '.join(preferences.get('favorite_categories', ['Not set']))}
- Size Preferences: {preferences.get('sizes', 'Not set')}
- Style Preferences: {preferences.get('style', 'Not set')}
- Budget Range: {preferences.get('budget_range', 'Not set')}

Current Cart: {len(cart)} items
Purchase History: {len(history)} previous purchases

Tailor your recommendations based on the customer's preferences and history.
Be mindful of their budget range when making suggestions."""
    
    return instructions

def update_preferences(
    context_variables: Dict,
    category: str = None,
    size: str = None,
    style: str = None,
    budget: str = None
) -> str:
    """Update customer preferences
    
    Args:
        context_variables: Current context
        category: Favorite category
        size: Size preference
        style: Style preference
        budget: Budget range
    """
    try:
        if "preferences" not in context_variables:
            context_variables["preferences"] = {}
            
        prefs = context_variables["preferences"]
        
        if category:
            if "favorite_categories" not in prefs:
                prefs["favorite_categories"] = []
            if category not in prefs["favorite_categories"]:
                prefs["favorite_categories"].append(category)
                
        if size:
            prefs["sizes"] = size
            
        if style:
            prefs["style"] = style
            
        if budget:
            prefs["budget_range"] = budget
            
        return "Updated preferences:\n" + json.dumps(prefs, indent=2)
    except Exception as e:
        return f"Error updating preferences: {str(e)}"

def add_to_cart(context_variables: Dict, product_id: str, quantity: int = 1) -> str:
    """Add product to shopping cart
    
    Args:
        context_variables: Current context
        product_id: Product to add
        quantity: Quantity to add
    """
    try:
        if "shopping_cart" not in context_variables:
            context_variables["shopping_cart"] = []
            
        # Find product in catalog
        product = None
        for category in PRODUCTS.values():
            if product_id in category:
                product = category[product_id]
                break
                
        if not product:
            return f"Product {product_id} not found"
            
        # Add to cart
        cart_item = {
            "product_id": product_id,
            "name": product["name"],
            "price": product["price"],
            "quantity": quantity,
            "total": product["price"] * quantity
        }
        
        context_variables["shopping_cart"].append(cart_item)
        
        return f"Added {quantity}x {product['name']} to cart"
    except Exception as e:
        return f"Error adding to cart: {str(e)}"

def view_cart(context_variables: Dict) -> str:
    """View current shopping cart
    
    Args:
        context_variables: Current context
    """
    try:
        cart = context_variables.get("shopping_cart", [])
        if not cart:
            return "Your cart is empty"
            
        total = sum(item["total"] for item in cart)
        
        cart_view = ["Your Shopping Cart:"]
        for item in cart:
            cart_view.append(
                f"- {item['quantity']}x {item['name']} (${item['price']} each)"
            )
        cart_view.append(f"\nTotal: ${total:.2f}")
        
        return "\n".join(cart_view)
    except Exception as e:
        return f"Error viewing cart: {str(e)}"

def get_recommendations(context_variables: Dict) -> str:
    """Get personalized product recommendations
    
    Args:
        context_variables: Current context
    """
    try:
        prefs = context_variables.get("preferences", {})
        history = context_variables.get("purchase_history", [])
        
        # Get favorite categories
        categories = prefs.get("favorite_categories", [])
        if not categories:
            categories = list(PRODUCTS.keys())
            
        # Get budget range
        budget = prefs.get("budget_range", "any")
        max_price = float('inf')
        if budget == "low":
            max_price = 100
        elif budget == "medium":
            max_price = 500
            
        # Find matching products
        recommendations = []
        for category in categories:
            if category in PRODUCTS:
                for pid, product in PRODUCTS[category].items():
                    if product["price"] <= max_price:
                        recommendations.append(
                            f"- {product['name']}: ${product['price']} ({pid})"
                        )
                        
        if recommendations:
            return "Recommended for you:\n" + "\n".join(recommendations)
        return "No recommendations found matching your preferences"
    except Exception as e:
        return f"Error getting recommendations: {str(e)}"

def checkout(context_variables: Dict) -> str:
    """Process checkout and update purchase history
    
    Args:
        context_variables: Current context
    """
    try:
        cart = context_variables.get("shopping_cart", [])
        if not cart:
            return "Cannot checkout with empty cart"
            
        # Calculate total
        total = sum(item["total"] for item in cart)
        
        # Add to purchase history
        if "purchase_history" not in context_variables:
            context_variables["purchase_history"] = []
            
        purchase = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": cart,
            "total": total
        }
        
        context_variables["purchase_history"].append(purchase)
        
        # Clear cart
        context_variables["shopping_cart"] = []
        
        return f"Checkout completed! Total paid: ${total:.2f}"
    except Exception as e:
        return f"Error processing checkout: {str(e)}"

try:
    # Initialize the client
    client = Swarm()
    
    # Create the shopping assistant agent
    agent = Agent(
        name=AGENT_NAME,
        model=MODEL_NAME,
        instructions=get_instructions,
        functions=[
            update_preferences,
            add_to_cart,
            view_cart,
            get_recommendations,
            checkout
        ]
    )
    
    # Initialize conversation and context
    conversation_history = []
    context = {
        "preferences": {},
        "shopping_cart": [],
        "purchase_history": []
    }
    
    print(colored("Shopping Assistant Initialized!", "green"))
    print(colored("Available commands:", "yellow"))
    print(colored("- Update preferences (e.g., 'I prefer casual style and medium budget')", "yellow"))
    print(colored("- View products (e.g., 'Show me recommendations')", "yellow"))
    print(colored("- Manage cart (e.g., 'Add laptop to cart', 'Show my cart')", "yellow"))
    print(colored("- Checkout (e.g., 'I want to checkout')", "yellow"))
    print(colored("Type 'exit' to end the conversation\n", "yellow"))
    
    while True:
        # Get user input
        user_input = input(colored("You: ", "cyan"))
        
        if user_input.lower() == 'exit':
            print(colored("\nThank you for shopping with us! Goodbye!", "green"))
            break
            
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Get response from agent with context
            response = client.run(
                agent=agent,
                messages=conversation_history,
                context_variables=context
            )
            
            # Update context with any changes
            context.update(response.context_variables)
            
            # Update conversation history
            conversation_history.extend(response.messages)
            
            # Print agent's response
            print(colored(f"\n{AGENT_NAME}: {response.messages[-1]['content']}\n", "green"))
            
        except Exception as e:
            print(colored(f"\nError: {str(e)}", "red"))
            print(colored("Please try again.\n", "yellow"))
            
except Exception as e:
    print(colored(f"Initialization Error: {str(e)}", "red")) 