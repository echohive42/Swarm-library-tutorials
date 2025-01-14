"""
# Error Handling Example - Robust Task Executor
# This example demonstrates advanced error handling and recovery strategies
# Shows how to handle various types of errors and provide fallback options
# Implements a system that can recover from failures and adapt its approach
"""

import os
import time
import random
from termcolor import colored
from swarm import Swarm, Agent, Result

# Constants
MODEL = "gpt-4o"
HISTORY = []
MAX_RETRIES = 3
TASKS = {
    "process_data": {"success_rate": 0.7, "retry_delay": 1},
    "validate_input": {"success_rate": 0.9, "retry_delay": 0.5},
    "generate_report": {"success_rate": 0.8, "retry_delay": 1.5}
}

class TaskError(Exception):
    """Custom error for task execution failures."""
    pass

def simulate_task_execution(task_name: str) -> bool:
    """Simulate task execution with controlled failure rate."""
    if task_name not in TASKS:
        return False
    return random.random() < TASKS[task_name]["success_rate"]

def with_retry(func):
    """Decorator to add retry logic to functions."""
    def wrapper(*args, **kwargs):
        retries = 0
        while retries < MAX_RETRIES:
            try:
                return func(*args, **kwargs)
            except TaskError as e:
                retries += 1
                if retries == MAX_RETRIES:
                    return f"Failed after {MAX_RETRIES} retries: {str(e)}"
                delay = TASKS.get(args[0], {}).get("retry_delay", 1)
                time.sleep(delay)
                print(colored(f"Retry {retries}/{MAX_RETRIES} after {delay}s delay...", "yellow"))
        return "Maximum retries exceeded"
    return wrapper

@with_retry
def process_data(task_name: str, data: str) -> str:
    """Process some data with error simulation.
    
    Args:
        task_name: Name of the task
        data: Data to process
    """
    print(colored(f"\n🔄 Processing data: {data}...", "magenta"))
    if not simulate_task_execution(task_name):
        raise TaskError(f"Failed to process data: {data}")
    return f"Successfully processed data: {data}"

@with_retry
def validate_input(task_name: str, input_data: str) -> str:
    """Validate input data with error simulation.
    
    Args:
        task_name: Name of the task
        input_data: Data to validate
    """
    print(colored(f"\n✅ Validating input: {input_data}...", "magenta"))
    if not simulate_task_execution(task_name):
        raise TaskError(f"Failed to validate input: {input_data}")
    return f"Input validated successfully: {input_data}"

@with_retry
def generate_report(task_name: str, report_type: str) -> str:
    """Generate a report with error simulation.
    
    Args:
        task_name: Name of the task
        report_type: Type of report to generate
    """
    print(colored(f"\n📄 Generating {report_type} report...", "magenta"))
    if not simulate_task_execution(task_name):
        raise TaskError(f"Failed to generate {report_type} report")
    return f"Generated {report_type} report successfully"

def list_available_tasks() -> str:
    """List all available tasks and their success rates."""
    print(colored("\n📋 Listing available tasks...", "magenta"))
    tasks = []
    for task, info in TASKS.items():
        success_rate = info["success_rate"] * 100
        tasks.append(f"{task}: {success_rate}% success rate")
    return "Available tasks:\n" + "\n".join(tasks)

# Initialize Swarm client
print(colored("Initializing Swarm client...", "cyan"))
client = Swarm()

# Create error-handling agent
error_handler = Agent(
    name="Error Handler",
    model=MODEL,
    instructions="""You are a robust task execution agent.
    You handle tasks that may fail and implement retry strategies.
    When a task fails:
    1. Inform the user about the failure
    2. Explain the retry strategy
    3. Suggest alternatives if available
    
    Always monitor task success rates and adapt your approach accordingly.
    Use simpler tasks when multiple failures occur.""",
    functions=[process_data, validate_input, generate_report, list_available_tasks]
)

def chat_loop():
    global HISTORY
    
    print(colored("\nRobust Task Executor started! Type 'exit' to end.", "green"))
    print(colored("Try:\n- Processing data\n- Validating input\n- Generating reports", "cyan"))
    print(colored("Note: Tasks may fail randomly to demonstrate error handling", "yellow"))
    
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
            print(colored("\nExecuting task...", "cyan"))
            response = client.run(
                agent=error_handler,
                messages=HISTORY
            )

            # Update history with agent's response
            HISTORY.extend(response.messages)
            
            # Print agent's response
            print(colored(f"\nAgent: {response.messages[-1]['content']}", "green"))

        except Exception as e:
            print(colored(f"\nSystem Error: {str(e)}", "red"))
            print(colored("This error was handled by the system, not the agent", "yellow"))

if __name__ == "__main__":
    try:
        chat_loop()
    except KeyboardInterrupt:
        print(colored("\nSession ended by user.", "yellow"))
    except Exception as e:
        print(colored(f"\nUnexpected error: {str(e)}", "red")) 