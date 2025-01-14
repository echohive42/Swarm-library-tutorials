"""
# Streaming example with product knowledge base agent
# Shows how to implement streaming responses for better UX
# Demonstrates real-time response generation with progress indicators
# Includes detailed product information and search capabilities
"""

from swarm import Swarm, Agent
from swarm.types import Result
from termcolor import colored
import os
from openai import AsyncOpenAI
import asyncio
from typing import Dict, List
import time
import sys

# Constants
MODEL_NAME = "gpt-4o"
AGENT_NAME = "Product Specialist"

# Mock product database
PRODUCTS = {
    "laptop-pro": {
        "name": "LaptopPro X1",
        "price": 1299.99,
        "specs": {
            "cpu": "Intel i7 12th Gen",
            "ram": "16GB DDR4",
            "storage": "512GB SSD",
            "display": "15.6\" 4K OLED"
        },
        "features": [
            "Backlit Keyboard",
            "Fingerprint Reader",
            "Thunderbolt 4",
            "Wi-Fi 6E"
        ]
    },
    "smartphone-x": {
        "name": "SmartPhone X12",
        "price": 899.99,
        "specs": {
            "cpu": "Snapdragon 8 Gen 2",
            "ram": "8GB",
            "storage": "256GB",
            "display": "6.7\" AMOLED 120Hz"
        },
        "features": [
            "5G Compatible",
            "Wireless Charging",
            "IP68 Water Resistant",
            "Triple Camera System"
        ]
    }
}

def get_product_info(product_id: str) -> str:
    """Get detailed product information
    
    Args:
        product_id: ID of the product to look up
    """
    print(colored(f"\n📱 Retrieving product information for: {product_id}", "magenta"))
    try:
        if product_id in PRODUCTS:
            product = PRODUCTS[product_id]
            info = [
                f"Product: {product['name']}",
                f"Price: ${product['price']}",
                "\nSpecifications:",
                *[f"- {k.upper()}: {v}" for k, v in product['specs'].items()],
                "\nFeatures:",
                *[f"- {feature}" for feature in product['features']]
            ]
            return "\n".join(info)
        return f"Product {product_id} not found in our catalog."
    except Exception as e:
        return f"Error retrieving product information: {str(e)}"

def compare_products(product_id1: str, product_id2: str) -> str:
    """Compare two products
    
    Args:
        product_id1: First product ID
        product_id2: Second product ID
    """
    try:
        if product_id1 not in PRODUCTS or product_id2 not in PRODUCTS:
            return "One or both products not found."
            
        p1 = PRODUCTS[product_id1]
        p2 = PRODUCTS[product_id2]
        
        comparison = [
            f"Comparing {p1['name']} vs {p2['name']}",
            f"\nPrice:",
            f"{p1['name']}: ${p1['price']}",
            f"{p2['name']}: ${p2['price']}",
            f"\nSpecifications Comparison:"
        ]
        
        for spec in p1['specs'].keys():
            comparison.append(f"{spec.upper()}:")
            comparison.append(f"- {p1['name']}: {p1['specs'][spec]}")
            comparison.append(f"- {p2['name']}: {p2['specs'][spec]}")
            
        return "\n".join(comparison)
    except Exception as e:
        return f"Error comparing products: {str(e)}"

def search_products(query: str) -> str:
    """Search products by keyword
    
    Args:
        query: Search query
    """
    try:
        results = []
        query = query.lower()
        
        for pid, product in PRODUCTS.items():
            if (query in product['name'].lower() or
                query in str(product['specs']).lower() or
                query in str(product['features']).lower()):
                results.append(f"- {product['name']} (ID: {pid})")
                
        if results:
            return "Found products:\n" + "\n".join(results)
        return "No products found matching your query."
    except Exception as e:
        return f"Error searching products: {str(e)}"

try:
    # Initialize the client
    client = Swarm()
    
    # Create the product specialist agent
    agent = Agent(
        name=AGENT_NAME,
        model=MODEL_NAME,
        instructions="""You are a Product Specialist with deep knowledge of our product catalog.
Help customers find and compare products, and provide detailed information about specifications and features.
Use the available functions to search and retrieve product information.""",
        functions=[get_product_info, compare_products, search_products]
    )
    
    # Initialize conversation history
    conversation_history = []
    
    print(colored("Product Information System Initialized!", "green"))
    print(colored("Available commands:", "yellow"))
    print(colored("- Get product info (e.g., 'Tell me about laptop-pro')", "yellow"))
    print(colored("- Compare products (e.g., 'Compare laptop-pro and smartphone-x')", "yellow"))
    print(colored("- Search products (e.g., 'Search for laptops')", "yellow"))
    print(colored("Type 'exit' to end the conversation\n", "yellow"))
    
    while True:
        # Get user input
        user_input = input(colored("You: ", "cyan"))
        
        if user_input.lower() == 'exit':
            print(colored("\nThank you for using our Product Information System! Goodbye!", "green"))
            break
            
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Get streaming response from agent
            stream = client.run(
                agent=agent,
                messages=conversation_history,
                stream=True
            )
            
            # Process the stream
            current_message = ""
            print(colored(f"\n{AGENT_NAME}: ", "green"), end="", flush=True)
            
            for chunk in stream:
                if "delim" in chunk:
                    continue
                elif "response" in chunk:
                    # Final response object
                    conversation_history.extend(chunk["response"].messages)
                    print("\n")
                else:
                    # Content chunk
                    if "content" in chunk:
                        content = chunk["content"]
                        current_message += content
                        print(content, end="", flush=True)
                        
        except Exception as e:
            print(colored(f"\nError: {str(e)}", "red"))
            print(colored("Please try again.\n", "yellow"))
            
except Exception as e:
    print(colored(f"Initialization Error: {str(e)}", "red")) 