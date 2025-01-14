"""
# Streaming Example - Interactive Storyteller
# This example demonstrates how to use streaming responses
# Shows how to handle streaming chunks and display them in real-time
# Implements an interactive storytelling system with dynamic choices
"""

import os
import sys
import time
from termcolor import colored
from swarm import Swarm, Agent
from swarm.types import Result

# Constants
MODEL = "gpt-4o"
HISTORY = []
STORY_CONTEXT = {
    "current_chapter": 1,
    "character_name": "",
    "character_class": "",
    "health": 100,
    "inventory": []
}

def create_character(context_variables: dict, name: str, character_class: str) -> Result:
    """Create a new character for the story.
    
    Args:
        name: Character name
        character_class: Type of character (warrior, mage, rogue)
    """
    print(colored(f"\n✨ Creating new character: {name} the {character_class}...", "magenta"))
    classes = {
        "warrior": {"health": 120, "inventory": ["sword", "shield"]},
        "mage": {"health": 80, "inventory": ["staff", "spellbook"]},
        "rogue": {"health": 100, "inventory": ["dagger", "lockpicks"]}
    }
    
    if character_class.lower() not in classes:
        return Result(value=f"Invalid class. Choose from: {', '.join(classes.keys())}")
    
    class_info = classes[character_class.lower()]
    context = {
        "character_name": name,
        "character_class": character_class.lower(),
        "health": class_info["health"],
        "inventory": class_info["inventory"]
    }
    
    return Result(
        value=f"Character created: {name} the {character_class}\nHealth: {class_info['health']}\nInventory: {', '.join(class_info['inventory'])}",
        context_variables=context
    )

def make_choice(choice: str) -> str:
    """Make a choice in the story.
    
    Args:
        choice: The choice made (A, B, or C)
    """
    print(colored(f"\n🎲 Processing choice {choice}...", "magenta"))
    return f"You chose option {choice}."

def get_character_status(context_variables: dict) -> str:
    """Get the current status of the character."""
    print(colored("\n📊 Checking character status...", "magenta"))
    return f"""
Character Status:
Name: {context_variables.get('character_name', 'Not created')}
Class: {context_variables.get('character_class', 'Not created')}
Health: {context_variables.get('health', 0)}
Inventory: {', '.join(context_variables.get('inventory', []))}
"""

# Initialize Swarm client
print(colored("Initializing Swarm client...", "cyan"))
client = Swarm()

# Create storyteller agent
storyteller = Agent(
    name="Storyteller",
    model=MODEL,
    instructions="""You are an interactive storyteller.
    Create an engaging fantasy adventure story based on the user's character.
    After each story segment, provide 3 choices (A, B, C) for the user to choose from.
    Use the character's stats and inventory in the story.
    Make the story adapt to the user's choices.
    Keep each story segment concise but engaging.""",
    functions=[create_character, make_choice, get_character_status]
)

def print_streaming(text: str, color: str = "white", delay: float = 0.02):
    """Print text with a typewriter effect."""
    for char in text:
        sys.stdout.write(colored(char, color))
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")

def chat_loop():
    global HISTORY
    context = STORY_CONTEXT.copy()
    
    print_streaming("\nInteractive Storyteller started! Type 'exit' to end.", "green")
    print_streaming("First, create your character with: create character [name] [class]", "cyan")
    print_streaming("Available classes: warrior, mage, rogue", "cyan")
    
    while True:
        # Get user input
        user_input = input(colored("\nYou: ", "yellow"))
        
        if user_input.lower() == 'exit':
            print_streaming("\nEnding story...", "red")
            break

        # Add user message to history
        HISTORY.append({"role": "user", "content": user_input})

        try:
            # Get streaming response from agent
            print_streaming("\nStoryteller is weaving the tale...", "cyan", 0.05)
            stream = client.run(
                agent=storyteller,
                messages=HISTORY,
                context_variables=context,
                stream=True
            )

            # Process streaming response
            for chunk in stream:
                if "delim" in chunk:
                    continue
                elif "response" in chunk:
                    # Final response object
                    response = chunk["response"]
                    context.update(response.context_variables)
                    HISTORY.extend(response.messages)
                else:
                    # Content chunk
                    if "content" in chunk:
                        print_streaming(chunk["content"], "green", 0.02)

        except Exception as e:
            print_streaming(f"\nError: {str(e)}", "red")

if __name__ == "__main__":
    try:
        chat_loop()
    except KeyboardInterrupt:
        print_streaming("\nStory ended by user.", "yellow")
    except Exception as e:
        print_streaming(f"\nUnexpected error: {str(e)}", "red") 