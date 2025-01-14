"""
# Complete customer service platform example
# Shows how to build a comprehensive support system
# Demonstrates integration of multiple support channels
# Includes knowledge base, ticket system, and live chat
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
import random

# Constants
DEFAULT_MODEL = "gpt-4o"
FAST_MODEL = "gpt-4o-mini"

# Mock knowledge base
KNOWLEDGE_BASE = {
    "account": {
        "password_reset": {
            "title": "How to Reset Your Password",
            "content": """1. Go to the login page
2. Click 'Forgot Password'
3. Enter your email
4. Follow the instructions in the email""",
            "tags": ["account", "password", "login"]
        },
        "account_deletion": {
            "title": "How to Delete Your Account",
            "content": """1. Go to Account Settings
2. Scroll to bottom
3. Click 'Delete Account'
4. Confirm deletion""",
            "tags": ["account", "deletion", "privacy"]
        }
    },
    "billing": {
        "refund_policy": {
            "title": "Refund Policy",
            "content": """- 30-day money-back guarantee
- Full refund for unused services
- Contact billing support for processing""",
            "tags": ["billing", "refund", "payment"]
        },
        "payment_methods": {
            "title": "Accepted Payment Methods",
            "content": """We accept:
- Credit/Debit Cards
- PayPal
- Bank Transfer""",
            "tags": ["billing", "payment", "methods"]
        }
    },
    "technical": {
        "system_requirements": {
            "title": "System Requirements",
            "content": """Minimum Requirements:
- 4GB RAM
- 2GHz Processor
- 10GB Free Space""",
            "tags": ["technical", "requirements", "specs"]
        },
        "api_documentation": {
            "title": "API Documentation",
            "content": """API Base URL: api.example.com
Authentication: Bearer token
Rate Limit: 100 requests/minute""",
            "tags": ["technical", "api", "development"]
        }
    }
}

# Mock ticket database
TICKETS = {}
TICKET_COUNTER = 0

# Knowledge Base Functions
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for articles
    
    Args:
        query: Search query
    """
    print(colored(f"\n🔍 Searching knowledge base for: {query}", "magenta"))
    try:
        results = []
        for category, articles in KNOWLEDGE_BASE.items():
            for article_id, article in articles.items():
                if any(term.lower() in article['content'].lower() or 
                      term.lower() in article['title'].lower() or
                      term.lower() in ' '.join(article['tags']).lower() 
                      for term in query.split()):
                    results.append(f"[{category.upper()}] {article['title']}")
        
        if results:
            return "Found relevant articles:\n" + "\n".join(results)
        return "No relevant articles found."
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"

def get_article(category: str, article_id: str) -> str:
    """Get a specific knowledge base article
    
    Args:
        category: Article category
        article_id: Article ID
    """
    print(colored(f"\n📖 Retrieving article: {category}/{article_id}", "magenta"))
    try:
        if category in KNOWLEDGE_BASE and article_id in KNOWLEDGE_BASE[category]:
            article = KNOWLEDGE_BASE[category][article_id]
            return f"""Title: {article['title']}
            
Content:
{article['content']}

Tags: {', '.join(article['tags'])}"""
        return "Article not found."
    except Exception as e:
        return f"Error retrieving article: {str(e)}"

# Ticket Management Functions
def create_ticket(
    context_variables: Dict,
    customer_email: str,
    subject: str,
    description: str,
    priority: str = "medium"
) -> str:
    """Create a support ticket
    
    Args:
        context_variables: Current context
        customer_email: Customer's email
        subject: Ticket subject
        description: Ticket description
        priority: Ticket priority
    """
    try:
        global TICKET_COUNTER
        TICKET_COUNTER += 1
        ticket_id = f"TICK{TICKET_COUNTER:04d}"
        
        TICKETS[ticket_id] = {
            "ticket_id": ticket_id,
            "customer_email": customer_email,
            "subject": subject,
            "description": description,
            "priority": priority,
            "status": "open",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updates": []
        }
        
        context_variables["current_ticket_id"] = ticket_id
        
        return f"Created ticket {ticket_id}"
    except Exception as e:
        return f"Error creating ticket: {str(e)}"

def update_ticket(
    ticket_id: str,
    update_text: str,
    new_status: str = None
) -> str:
    """Update a support ticket
    
    Args:
        ticket_id: Ticket to update
        update_text: Update message
        new_status: Optional new status
    """
    try:
        if ticket_id not in TICKETS:
            return f"Ticket {ticket_id} not found"
            
        ticket = TICKETS[ticket_id]
        
        # Add update
        ticket["updates"].append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "message": update_text
        })
        
        # Update status if provided
        if new_status:
            valid_statuses = ["open", "in_progress", "pending", "resolved", "closed"]
            if new_status not in valid_statuses:
                return f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            ticket["status"] = new_status
            
        return f"Updated ticket {ticket_id}"
    except Exception as e:
        return f"Error updating ticket: {str(e)}"

def get_ticket_details(ticket_id: str) -> str:
    """Get detailed ticket information
    
    Args:
        ticket_id: Ticket to view
    """
    try:
        if ticket_id not in TICKETS:
            return f"Ticket {ticket_id} not found"
            
        ticket = TICKETS[ticket_id]
        
        details = [
            f"Ticket {ticket_id}:",
            f"Subject: {ticket['subject']}",
            f"Status: {ticket['status']}",
            f"Priority: {ticket['priority']}",
            f"Created: {ticket['created_at']}",
            f"\nDescription:",
            ticket['description'],
            "\nUpdates:"
        ]
        
        for update in ticket["updates"]:
            details.append(
                f"[{update['timestamp']}] {update['message']}"
            )
            
        return "\n".join(details)
    except Exception as e:
        return f"Error getting ticket details: {str(e)}"

# Live Chat Functions
def start_chat_session(
    context_variables: Dict,
    customer_name: str,
    initial_message: str
) -> str:
    """Start a live chat session
    
    Args:
        context_variables: Current context
        customer_name: Customer's name
        initial_message: Initial chat message
    """
    try:
        context_variables["chat_session"] = {
            "customer_name": customer_name,
            "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "messages": []
        }
        
        # Add initial message
        context_variables["chat_session"]["messages"].append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sender": customer_name,
            "message": initial_message
        })
        
        return f"Started chat session with {customer_name}"
    except Exception as e:
        return f"Error starting chat session: {str(e)}"

def add_chat_message(
    context_variables: Dict,
    message: str,
    is_customer: bool = True
) -> str:
    """Add a message to the chat session
    
    Args:
        context_variables: Current context
        message: Chat message
        is_customer: Whether the message is from the customer
    """
    try:
        if "chat_session" not in context_variables:
            return "No active chat session"
            
        session = context_variables["chat_session"]
        sender = session["customer_name"] if is_customer else "Support Agent"
        
        session["messages"].append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sender": sender,
            "message": message
        })
        
        return f"Added message from {sender}"
    except Exception as e:
        return f"Error adding chat message: {str(e)}"

def end_chat_session(context_variables: Dict) -> str:
    """End the current chat session
    
    Args:
        context_variables: Current context
    """
    try:
        if "chat_session" not in context_variables:
            return "No active chat session"
            
        session = context_variables.pop("chat_session")
        return f"Ended chat session with {session['customer_name']}"
    except Exception as e:
        return f"Error ending chat session: {str(e)}"

# Create specialized agents
knowledge_agent = Agent(
    name="Knowledge Base Agent",
    model=FAST_MODEL,
    instructions="""You are a Knowledge Base Specialist.
Help customers find relevant articles and information.
Use the search and retrieval functions to find answers quickly.""",
    functions=[search_knowledge_base, get_article]
)

ticket_agent = Agent(
    name="Ticket Support Agent",
    model=DEFAULT_MODEL,
    instructions="""You are a Ticket Support Specialist.
Handle ticket creation, updates, and status changes.
Ensure proper documentation of all customer interactions.""",
    functions=[create_ticket, update_ticket, get_ticket_details]
)

chat_agent = Agent(
    name="Live Chat Agent",
    model=DEFAULT_MODEL,
    instructions="""You are a Live Chat Support Agent.
Provide real-time assistance to customers.
Maintain a friendly and helpful tone throughout the conversation.""",
    functions=[start_chat_session, add_chat_message, end_chat_session]
)

# Transfer functions
def transfer_to_knowledge_base() -> Result:
    """Transfer to knowledge base agent"""
    return Result(
        value="Transferring to knowledge base...",
        agent=knowledge_agent
    )

def transfer_to_ticket_support() -> Result:
    """Transfer to ticket support agent"""
    return Result(
        value="Transferring to ticket support...",
        agent=ticket_agent
    )

def transfer_to_live_chat() -> Result:
    """Transfer to live chat agent"""
    return Result(
        value="Transferring to live chat...",
        agent=chat_agent
    )

# Add transfer functions to each agent
knowledge_agent.functions.extend([transfer_to_ticket_support, transfer_to_live_chat])
ticket_agent.functions.extend([transfer_to_knowledge_base, transfer_to_live_chat])
chat_agent.functions.extend([transfer_to_knowledge_base, transfer_to_ticket_support])

try:
    # Initialize the client
    client = Swarm()
    
    # Initialize conversation and context
    conversation_history = []
    context = {}
    
    # Start with knowledge base agent
    current_agent = knowledge_agent
    
    print(colored("Customer Support Platform Initialized!", "green"))
    print(colored("Available services:", "yellow"))
    print(colored("1. Knowledge Base", "yellow"))
    print(colored("   - Search articles (e.g., 'Search for password reset')", "yellow"))
    print(colored("   - View article (e.g., 'Show me the refund policy')", "yellow"))
    print(colored("2. Ticket Support", "yellow"))
    print(colored("   - Create ticket (e.g., 'I need help with billing')", "yellow"))
    print(colored("   - Check status (e.g., 'What's the status of TICK0001?')", "yellow"))
    print(colored("3. Live Chat", "yellow"))
    print(colored("   - Start chat (e.g., 'I want to chat with support')", "yellow"))
    print(colored("Type 'exit' to end the session\n", "yellow"))
    
    while True:
        # Get user input
        user_input = input(colored("You: ", "cyan"))
        
        if user_input.lower() == 'exit':
            print(colored("\nThank you for using our support platform! Goodbye!", "green"))
            break
            
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Get response from current agent
            response = client.run(
                agent=current_agent,
                messages=conversation_history,
                context_variables=context
            )
            
            # Update context with any changes
            context.update(response.context_variables)
            
            # Handle agent transfer if it occurred
            if response.agent:
                current_agent = response.agent
                print(colored(f"\nTransferred to {current_agent.name}!", "yellow"))
            
            # Update conversation history
            conversation_history.extend(response.messages)
            
            # Print agent's response
            print(colored(f"\n{response.messages[-1]['sender']}: {response.messages[-1]['content']}\n", "green"))
            
        except Exception as e:
            print(colored(f"\nError: {str(e)}", "red"))
            print(colored("Please try again.\n", "yellow"))
            
except Exception as e:
    print(colored(f"Initialization Error: {str(e)}", "red")) 