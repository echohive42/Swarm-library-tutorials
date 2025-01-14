"""
# Model override and error handling example with support ticket system
# Shows how to use different models for different tasks
# Demonstrates advanced error handling and retry mechanisms
# Includes ticket priority assessment and routing
"""

from swarm import Swarm, Agent
from swarm.types import Result
from termcolor import colored
import os
from openai import AsyncOpenAI
import asyncio
from typing import Dict, List
import time
from datetime import datetime

# Constants
DEFAULT_MODEL = "gpt-4o"
FAST_MODEL = "gpt-4o-mini"  # For quick assessments
AGENT_NAME = "Support Coordinator"

# Mock ticket database
TICKETS = {}
TICKET_COUNTER = 0

class TicketPriorityError(Exception):
    """Custom error for invalid ticket priorities"""
    pass

class DepartmentRoutingError(Exception):
    """Custom error for invalid department routing"""
    pass

def create_ticket(
    description: str,
    customer_email: str,
    context_variables: Dict
) -> str:
    """Create a new support ticket
    
    Args:
        description: Ticket description
        customer_email: Customer's email
        context_variables: Context variables including agent assessment
    """
    print(colored(f"\n🎫 Creating ticket for customer: {customer_email}", "magenta"))
    try:
        global TICKET_COUNTER
        TICKET_COUNTER += 1
        ticket_id = f"TICK{TICKET_COUNTER:04d}"
        
        TICKETS[ticket_id] = {
            "description": description,
            "customer_email": customer_email,
            "status": "new",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "priority": context_variables.get("assessed_priority", "medium"),
            "department": context_variables.get("assigned_department", "general")
        }
        
        return f"Created ticket {ticket_id}"
    except Exception as e:
        return f"Error creating ticket: {str(e)}"

def assess_priority(description: str) -> str:
    """Assess ticket priority based on description
    
    Args:
        description: Ticket description
    """
    try:
        # Simulate priority assessment
        keywords = {
            "urgent": "high",
            "emergency": "high",
            "broken": "high",
            "bug": "medium",
            "question": "low",
            "help": "low"
        }
        
        description = description.lower()
        for keyword, priority in keywords.items():
            if keyword in description:
                return f"Assessed priority: {priority}"
        
        return "Assessed priority: medium"
    except Exception as e:
        return f"Error assessing priority: {str(e)}"

def route_to_department(description: str) -> str:
    """Route ticket to appropriate department
    
    Args:
        description: Ticket description
    """
    try:
        # Simulate department routing
        keywords = {
            "password": "security",
            "login": "security",
            "payment": "billing",
            "charge": "billing",
            "bug": "technical",
            "error": "technical"
        }
        
        description = description.lower()
        for keyword, dept in keywords.items():
            if keyword in description:
                return f"Routed to: {dept}"
        
        return "Routed to: general"
    except Exception as e:
        return f"Error routing ticket: {str(e)}"

def get_ticket_status(ticket_id: str) -> str:
    """Get ticket status
    
    Args:
        ticket_id: Ticket ID to check
    """
    try:
        if ticket_id in TICKETS:
            ticket = TICKETS[ticket_id]
            return (
                f"Ticket {ticket_id}:\n"
                f"Status: {ticket['status']}\n"
                f"Priority: {ticket['priority']}\n"
                f"Department: {ticket['department']}\n"
                f"Created: {ticket['created_at']}"
            )
        return f"Ticket {ticket_id} not found"
    except Exception as e:
        return f"Error checking ticket status: {str(e)}"

def update_ticket_status(ticket_id: str, new_status: str) -> str:
    """Update ticket status
    
    Args:
        ticket_id: Ticket ID to update
        new_status: New status value
    """
    try:
        if ticket_id not in TICKETS:
            raise ValueError(f"Ticket {ticket_id} not found")
            
        valid_statuses = ["new", "in_progress", "pending", "resolved", "closed"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
            
        TICKETS[ticket_id]["status"] = new_status
        return f"Updated ticket {ticket_id} status to: {new_status}"
    except Exception as e:
        return f"Error updating ticket status: {str(e)}"

try:
    # Initialize the client
    client = Swarm()
    
    # Create assessment agent with faster model
    assessment_agent = Agent(
        name="Priority Assessor",
        model=FAST_MODEL,
        instructions="""You are a Priority Assessment Specialist.
Quickly evaluate support tickets and determine their priority level.
Use the assess_priority function to evaluate ticket descriptions.""",
        functions=[assess_priority]
    )
    
    # Create routing agent with faster model
    routing_agent = Agent(
        name="Department Router",
        model=FAST_MODEL,
        instructions="""You are a Department Routing Specialist.
Quickly determine which department should handle each ticket.
Use the route_to_department function to evaluate ticket descriptions.""",
        functions=[route_to_department]
    )
    
    # Create main support agent
    support_agent = Agent(
        name=AGENT_NAME,
        model=DEFAULT_MODEL,
        instructions="""You are a Support Coordinator managing customer support tickets.
Handle ticket creation, status updates, and coordinate with assessment and routing specialists.
Use the available functions to manage tickets efficiently.""",
        functions=[create_ticket, get_ticket_status, update_ticket_status]
    )
    
    # Initialize conversation history
    conversation_history = []
    
    print(colored("Support Ticket System Initialized!", "green"))
    print(colored("Available commands:", "yellow"))
    print(colored("- Create ticket (e.g., 'I need help with login issues')", "yellow"))
    print(colored("- Check status (e.g., 'What's the status of TICK0001?')", "yellow"))
    print(colored("- Update status (e.g., 'Mark TICK0001 as resolved')", "yellow"))
    print(colored("Type 'exit' to end the conversation\n", "yellow"))
    
    while True:
        # Get user input
        user_input = input(colored("You: ", "cyan"))
        
        if user_input.lower() == 'exit':
            print(colored("\nThank you for using our Support System! Goodbye!", "green"))
            break
            
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Initialize context for new tickets
            context = {}
            
            # If it looks like a new ticket request, do priority assessment and routing
            if "help" in user_input.lower() or "issue" in user_input.lower():
                try:
                    # Get priority assessment
                    priority_response = client.run(
                        agent=assessment_agent,
                        messages=[{"role": "user", "content": user_input}]
                    )
                    priority = priority_response.messages[-1]["content"].split(": ")[1]
                    context["assessed_priority"] = priority
                    print(colored(f"Priority Assessment: {priority}", "yellow"))
                    
                    # Get department routing
                    routing_response = client.run(
                        agent=routing_agent,
                        messages=[{"role": "user", "content": user_input}]
                    )
                    department = routing_response.messages[-1]["content"].split(": ")[1]
                    context["assigned_department"] = department
                    print(colored(f"Department Assignment: {department}", "yellow"))
                    
                except Exception as e:
                    print(colored(f"Warning: Assessment error: {str(e)}", "yellow"))
                    print(colored("Proceeding with default values...\n", "yellow"))
            
            # Get response from support agent
            response = client.run(
                agent=support_agent,
                messages=conversation_history,
                context_variables=context
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