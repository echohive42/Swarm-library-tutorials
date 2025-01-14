"""
# Parallel tools example with travel booking agent
# Shows how to execute multiple tools in parallel for faster responses
# Demonstrates checking multiple services simultaneously
# Includes flight, hotel, and car rental availability checks
"""

from swarm import Swarm, Agent
from swarm.types import Result
from termcolor import colored
import os
from openai import AsyncOpenAI
import asyncio
from typing import Dict, List
import random
from datetime import datetime, timedelta

# Constants
MODEL_NAME = "gpt-4o"
AGENT_NAME = "Travel Advisor"

# Mock travel data
FLIGHTS = {
    "NYC-LAX": [
        {"airline": "SkyHigh", "price": 299.99, "duration": "5h 30m"},
        {"airline": "CoastAir", "price": 349.99, "duration": "5h 45m"}
    ],
    "LAX-NYC": [
        {"airline": "SkyHigh", "price": 319.99, "duration": "5h 45m"},
        {"airline": "CoastAir", "price": 329.99, "duration": "6h"}
    ]
}

HOTELS = {
    "NYC": [
        {"name": "Grand Plaza", "price": 199.99, "rating": 4.5},
        {"name": "City View", "price": 149.99, "rating": 4.0}
    ],
    "LAX": [
        {"name": "Beach Resort", "price": 249.99, "rating": 4.7},
        {"name": "Sunset Hotel", "price": 179.99, "rating": 4.2}
    ]
}

CARS = {
    "NYC": [
        {"type": "Economy", "price": 45.99, "company": "SpeedRent"},
        {"type": "SUV", "price": 89.99, "company": "LuxDrive"}
    ],
    "LAX": [
        {"type": "Economy", "price": 49.99, "company": "SpeedRent"},
        {"type": "SUV", "price": 94.99, "company": "LuxDrive"}
    ]
}

def check_flights(from_city: str, to_city: str) -> str:
    """Check flight availability
    
    Args:
        from_city: Departure city
        to_city: Arrival city
    """
    print(colored(f"\n✈️ Checking flights from {from_city} to {to_city}", "magenta"))
    try:
        route = f"{from_city}-{to_city}"
        if route in FLIGHTS:
            flights = FLIGHTS[route]
            result = [f"Found {len(flights)} flights from {from_city} to {to_city}:"]
            for flight in flights:
                result.append(
                    f"- {flight['airline']}: ${flight['price']} ({flight['duration']})"
                )
            return "\n".join(result)
        return f"No flights found for route {from_city} to {to_city}"
    except Exception as e:
        return f"Error checking flights: {str(e)}"

def check_hotels(city: str, max_price: float = 1000.0) -> str:
    """Check hotel availability
    
    Args:
        city: City to search in
        max_price: Maximum price per night
    """
    try:
        if city in HOTELS:
            hotels = [h for h in HOTELS[city] if h['price'] <= max_price]
            result = [f"Found {len(hotels)} hotels in {city}:"]
            for hotel in hotels:
                result.append(
                    f"- {hotel['name']}: ${hotel['price']}/night ({hotel['rating']}★)"
                )
            return "\n".join(result)
        return f"No hotels found in {city}"
    except Exception as e:
        return f"Error checking hotels: {str(e)}"

def check_car_rentals(city: str, car_type: str = "all") -> str:
    """Check car rental availability
    
    Args:
        city: City to search in
        car_type: Type of car (Economy, SUV, or all)
    """
    try:
        if city in CARS:
            cars = CARS[city]
            if car_type.lower() != "all":
                cars = [c for c in cars if c['type'].lower() == car_type.lower()]
            
            result = [f"Found {len(cars)} car rentals in {city}:"]
            for car in cars:
                result.append(
                    f"- {car['company']} {car['type']}: ${car['price']}/day"
                )
            return "\n".join(result)
        return f"No car rentals found in {city}"
    except Exception as e:
        return f"Error checking car rentals: {str(e)}"

def get_travel_package(from_city: str, to_city: str) -> str:
    """Get complete travel package information
    
    Args:
        from_city: Departure city
        to_city: Destination city
    """
    try:
        flight_info = check_flights(from_city, to_city)
        hotel_info = check_hotels(to_city)
        car_info = check_car_rentals(to_city)
        
        package = [
            "Complete Travel Package Information:",
            "\nFLIGHTS:",
            flight_info,
            "\nHOTELS:",
            hotel_info,
            "\nCAR RENTALS:",
            car_info
        ]
        
        return "\n".join(package)
    except Exception as e:
        return f"Error getting travel package: {str(e)}"

try:
    # Initialize the client
    client = Swarm()
    
    # Create the travel advisor agent
    agent = Agent(
        name=AGENT_NAME,
        model=MODEL_NAME,
        instructions="""You are a Travel Advisor helping customers plan their trips.
Use the available functions to check flights, hotels, and car rentals.
You can check multiple services in parallel for faster responses.
For complete trip planning, use get_travel_package to check everything at once.""",
        functions=[check_flights, check_hotels, check_car_rentals, get_travel_package],
        parallel_tool_calls=True  # Enable parallel function execution
    )
    
    # Initialize conversation history
    conversation_history = []
    
    print(colored("Travel Planning System Initialized!", "green"))
    print(colored("Available services:", "yellow"))
    print(colored("- Check flights (NYC-LAX, LAX-NYC)", "yellow"))
    print(colored("- Check hotels (NYC, LAX)", "yellow"))
    print(colored("- Check car rentals (NYC, LAX)", "yellow"))
    print(colored("- Get complete travel packages", "yellow"))
    print(colored("Type 'exit' to end the conversation\n", "yellow"))
    
    while True:
        # Get user input
        user_input = input(colored("You: ", "cyan"))
        
        if user_input.lower() == 'exit':
            print(colored("\nThank you for using our Travel Planning System! Goodbye!", "green"))
            break
            
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Get response from agent
            response = client.run(
                agent=agent,
                messages=conversation_history
            )
            
            # Update conversation history
            conversation_history.extend(response.messages)
            
            # Print agent's response
            print(colored(f"\n{AGENT_NAME}: {response.messages[-1]['content']}\n", "green"))
            
        except Exception as e:
            print(colored(f"\nError: {str(e)}", "red"))
            print(colored("Please try again.\n", "yellow"))
            
except Exception as e:
    print(colored(f"Initialization Error: {str(e)}", "red")) 