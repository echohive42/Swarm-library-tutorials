"""
# Context variables example with customer preferences and interaction history
# Shows how to maintain and update customer context throughout the conversation
# Demonstrates dynamic instruction modification based on context
# Includes preference tracking and personalized responses
"""

from swarm import Swarm, Agent, Result
from termcolor import colored
import os
from openai import AsyncOpenAI
import asyncio
from typing import Dict

# Constants
MODEL_NAME = "gpt-4o"
AGENT_NAME = "Personal Support Agent"

def get_instructions(context_variables: Dict) -> str:
    """Dynamic instructions based on context"""
    customer_name = context_variables.get("customer_name", "valued customer")
    preferred_language = context_variables.get("preferred_language", "English")
    previous_issues = context_variables.get("previous_issues", [])
    
    instructions = f"""You are a Personal Support Agent for {customer_name}.
Preferred Language: {preferred_language}
Previous Issues: {', '.join(previous_issues) if previous_issues else 'None'}

Tailor your responses based on the customer's preferences and history.
Be proactive in suggesting solutions based on previous interactions."""
    
    return instructions

def update_preferences(context_variables: Dict, preference_type: str, value: str) -> str:
    """Update customer preferences
    
    Args:
        context_variables: Current context variables
        preference_type: Type of preference to update
        value: New value for the preference
    """
    try:
        context_variables[preference_type] = value
        return f"Updated {preference_type} to: {value}"
    except Exception as e:
        return f"Error updating preferences: {str(e)}"

def add_issue(context_variables: Dict, issue: str) -> str:
    """Add a new issue to customer history
    
    Args:
        context_variables: Current context variables
        issue: New issue to add
    """
    try:
        if "previous_issues" not in context_variables:
            context_variables["previous_issues"] = []
        context_variables["previous_issues"].append(issue)
        return f"Added issue to history: {issue}"
    except Exception as e:
        return f"Error adding issue: {str(e)}"

def get_customer_profile(context_variables: Dict) -> str:
    """Get customer profile summary
    
    Args:
        context_variables: Current context variables
    """
    try:
        profile = [f"Customer Name: {context_variables.get('customer_name', 'Not set')}",
                  f"Preferred Language: {context_variables.get('preferred_language', 'Not set')}",
                  f"Previous Issues: {', '.join(context_variables.get('previous_issues', ['None']))}"]
        return "\n".join(profile)
    except Exception as e:
        return f"Error getting profile: {str(e)}"

try:
    # Initialize the client
    client = Swarm()
    
    # Initialize context variables
    context = {
        "customer_name": "Guest",
        "preferred_language": "English",
        "previous_issues": []
    }
    
    # Create the personal support agent
    agent = Agent(
        name=AGENT_NAME,
        model=MODEL_NAME,
        instructions=get_instructions,
        functions=[update_preferences, add_issue, get_customer_profile]
    )
    
    # Initialize conversation history
    conversation_history = []
    
    print(colored("Personal Support System Initialized!", "green"))
    print(colored("Available commands:", "yellow"))
    print(colored("- Update preferences (e.g., 'I prefer Spanish')", "yellow"))
    print(colored("- Report issue (e.g., 'I had a problem with login')", "yellow"))
    print(colored("- View profile (e.g., 'Show my profile')", "yellow"))
    print(colored("- Type 'exit' to end the conversation\n", "yellow"))
    
    while True:
        # Get user input
        user_input = input(colored("You: ", "cyan"))
        
        if user_input.lower() == 'exit':
            print(colored("\nThank you for using our Personal Support! Goodbye!", "green"))
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