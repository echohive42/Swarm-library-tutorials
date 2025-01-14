"""
# Parallel Tool Calls Example - Data Processing Agent
# This example demonstrates how to use parallel tool calls for efficient processing
# Shows how to handle multiple function calls simultaneously
# Implements a data processing system that can analyze multiple metrics in parallel
"""

import os
import time
import random
from termcolor import colored
from swarm import Swarm, Agent

# Constants
MODEL = "gpt-4o"
HISTORY = []
SAMPLE_DATA = {
    "temperature": [20, 22, 21, 23, 22, 24, 23, 25, 24, 26],
    "humidity": [45, 48, 47, 46, 45, 44, 46, 47, 48, 49],
    "pressure": [1013, 1014, 1012, 1011, 1013, 1015, 1014, 1012, 1011, 1010]
}

def calculate_average(metric: str) -> str:
    """Calculate the average value for a metric.
    
    Args:
        metric: The metric to analyze (temperature, humidity, pressure)
    """
    print(colored(f"\n📊 Calculating average for {metric}...", "magenta"))
    if metric not in SAMPLE_DATA:
        return f"Error: Metric '{metric}' not found"
    
    time.sleep(1)  # Simulate processing time
    avg = sum(SAMPLE_DATA[metric]) / len(SAMPLE_DATA[metric])
    return f"Average {metric}: {avg:.2f}"

def find_peak_value(metric: str) -> str:
    """Find the peak value for a metric.
    
    Args:
        metric: The metric to analyze (temperature, humidity, pressure)
    """
    print(colored(f"\n📈 Finding peak value for {metric}...", "magenta"))
    if metric not in SAMPLE_DATA:
        return f"Error: Metric '{metric}' not found"
    
    time.sleep(1)  # Simulate processing time
    peak = max(SAMPLE_DATA[metric])
    return f"Peak {metric}: {peak}"

def calculate_trend(metric: str) -> str:
    """Calculate the trend for a metric.
    
    Args:
        metric: The metric to analyze (temperature, humidity, pressure)
    """
    print(colored(f"\n📉 Calculating trend for {metric}...", "magenta"))
    if metric not in SAMPLE_DATA:
        return f"Error: Metric '{metric}' not found"
    
    time.sleep(1)  # Simulate processing time
    first_half = sum(SAMPLE_DATA[metric][:5]) / 5
    second_half = sum(SAMPLE_DATA[metric][5:]) / 5
    
    if second_half > first_half:
        trend = "increasing"
    elif second_half < first_half:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return f"{metric.title()} trend: {trend}"

def get_available_metrics() -> str:
    """List all available metrics."""
    print(colored("\n📋 Listing available metrics...", "magenta"))
    return "Available metrics: " + ", ".join(SAMPLE_DATA.keys())

# Initialize Swarm client
print(colored("Initializing Swarm client...", "cyan"))
client = Swarm()

# Create data processing agent
data_agent = Agent(
    name="Data Processor",
    model=MODEL,
    instructions="""You are a data processing assistant.
    You can analyze multiple metrics in parallel using the available functions.
    When asked about multiple metrics, use parallel tool calls for efficiency.
    Always explain the results in a clear and concise way.
    Use get_available_metrics() if user needs to know what metrics are available.""",
    functions=[calculate_average, find_peak_value, calculate_trend, get_available_metrics],
    parallel_tool_calls=True  # Enable parallel tool calls
)

def chat_loop():
    global HISTORY
    
    print(colored("\nData Processing System started! Type 'exit' to end.", "green"))
    print(colored("Try asking about:\n- Average values\n- Peak values\n- Trends\nFor multiple metrics at once!", "cyan"))
    
    while True:
        # Get user input
        user_input = input(colored("\nYou: ", "yellow"))
        
        if user_input.lower() == 'exit':
            print(colored("\nEnding session...", "red"))
            break

        # Add user message to history
        HISTORY.append({"role": "user", "content": user_input})

        try:
            # Get response from agent
            print(colored("\nProcessing data...", "cyan"))
            start_time = time.time()
            
            response = client.run(
                agent=data_agent,
                messages=HISTORY
            )

            # Update history with agent's response
            HISTORY.extend(response.messages)
            
            # Print agent's response and processing time
            print(colored(f"\nAgent: {response.messages[-1]['content']}", "green"))
            print(colored(f"Processing time: {time.time() - start_time:.2f} seconds", "yellow"))

        except Exception as e:
            print(colored(f"\nError: {str(e)}", "red"))

if __name__ == "__main__":
    try:
        chat_loop()
    except KeyboardInterrupt:
        print(colored("\nSession ended by user.", "yellow"))
    except Exception as e:
        print(colored(f"\nUnexpected error: {str(e)}", "red")) 