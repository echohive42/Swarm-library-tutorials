"""
# Model Override Example - Multi-Model Task Handler
# This example demonstrates how to use different models for different tasks
# Shows how to override models based on task complexity
# Implements a system that uses appropriate models for different types of processing
"""

import os
from termcolor import colored
from swarm import Swarm, Agent
from swarm.types import Result

# Constants
DEFAULT_MODEL = "gpt-4o"
FAST_MODEL = "gpt-4o-mini"  # For simple tasks
HISTORY = []

def summarize_text(text: str) -> str:
    """Summarize a piece of text.
    
    Args:
        text: The text to summarize
    """
    print(colored("\n📝 Summarizing text...", "magenta"))
    return "This function will be handled by the model."

def analyze_sentiment(text: str) -> str:
    """Analyze the sentiment of a text.
    
    Args:
        text: The text to analyze
    """
    print(colored("\n😊 Analyzing sentiment...", "magenta"))
    return "This function will be handled by the model."

def extract_keywords(text: str) -> str:
    """Extract key words from a text.
    
    Args:
        text: The text to analyze
    """
    print(colored("\n🔑 Extracting keywords...", "magenta"))
    return "This function will be handled by the model."

def translate_text(text: str, target_language: str) -> str:
    """Translate text to another language.
    
    Args:
        text: The text to translate
        target_language: The target language
    """
    print(colored(f"\n🌐 Translating text to {target_language}...", "magenta"))
    return "This function will be handled by the model."

# Initialize Swarm client
print(colored("Initializing Swarm client...", "cyan"))
client = Swarm()

# Create specialized agents for different tasks
basic_agent = Agent(
    name="Basic Processor",
    model=FAST_MODEL,  # Use faster model for simple tasks
    instructions="""You are a basic text processor.
    You handle simple tasks like keyword extraction and sentiment analysis.
    Keep responses brief and to the point.""",
    functions=[extract_keywords, analyze_sentiment]
)

advanced_agent = Agent(
    name="Advanced Processor",
    model=DEFAULT_MODEL,  # Use more capable model for complex tasks
    instructions="""You are an advanced text processor.
    You handle complex tasks like summarization and translation.
    Provide detailed and accurate responses.""",
    functions=[summarize_text, translate_text]
)

def transfer_to_advanced() -> Result:
    """Transfer to the advanced agent for complex tasks."""
    print(colored("\n🔄 Transferring to advanced processor...", "yellow"))
    return Result(
        value="Transferring to advanced processor for complex task...",
        agent=advanced_agent
    )

def transfer_to_basic() -> Result:
    """Transfer to the basic agent for simple tasks."""
    print(colored("\n🔄 Transferring to basic processor...", "yellow"))
    return Result(
        value="Transferring to basic processor for simple task...",
        agent=basic_agent
    )

# Add transfer functions to each agent
basic_agent.functions.append(transfer_to_advanced)
advanced_agent.functions.append(transfer_to_basic)

def chat_loop():
    global HISTORY
    current_agent = basic_agent  # Start with basic agent
    
    print(colored("\nMulti-Model Processing System started! Type 'exit' to end.", "green"))
    print(colored("Available tasks:", "cyan"))
    print(colored("Basic tasks (fast model):\n- Keyword extraction\n- Sentiment analysis", "cyan"))
    print(colored("Advanced tasks (powerful model):\n- Text summarization\n- Translation", "cyan"))
    
    while True:
        # Get user input
        user_input = input(colored("\nYou: ", "yellow"))
        
        if user_input.lower() == 'exit':
            print(colored("\nEnding session...", "red"))
            break

        # Add user message to history
        HISTORY.append({"role": "user", "content": user_input})

        try:
            # Get response from current agent
            print(colored(f"\n{current_agent.name} ({current_agent.model}) is processing...", "cyan"))
            response = client.run(
                agent=current_agent,
                messages=HISTORY
            )

            # Update history with agent's response
            HISTORY.extend(response.messages)
            
            # Check if agent changed
            if response.agent and response.agent != current_agent:
                current_agent = response.agent
                print(colored(f"\nSwitched to {current_agent.name} ({current_agent.model})", "yellow"))
            
            # Print agent's response
            print(colored(f"\nAgent: {response.messages[-1]['content']}", "green"))

        except Exception as e:
            print(colored(f"\nError: {str(e)}", "red"))

if __name__ == "__main__":
    try:
        chat_loop()
    except KeyboardInterrupt:
        print(colored("\nSession ended by user.", "yellow"))
    except Exception as e:
        print(colored(f"\nUnexpected error: {str(e)}", "red")) 