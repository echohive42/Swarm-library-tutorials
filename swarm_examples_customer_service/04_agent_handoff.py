"""
# Agent handoff example with specialized customer service departments
# Shows how to transfer conversations between different specialized agents
# Demonstrates context preservation during handoffs
# Includes department-specific functions and knowledge
"""

from swarm import Swarm, Agent
from swarm.types import Result
from termcolor import colored
import os
from openai import AsyncOpenAI
import asyncio
from typing import Dict, Optional

# Constants
MODEL_NAME = "gpt-4o"

# Technical Support Functions
def check_system_status() -> str:
    """Check the status of various systems"""
    print(colored("\n🔄 Checking system status...", "magenta"))
    return "All systems operational: Website (✓) | Database (✓) | API (✓)"

def troubleshoot_issue(issue_type: str) -> str:
    """Provide troubleshooting steps
    
    Args:
        issue_type: Type of issue to troubleshoot
    """
    print(colored(f"\n🛠️ Getting troubleshooting steps for: {issue_type}", "magenta"))
    solutions = {
        "login": "1. Clear browser cache\n2. Reset password\n3. Check email verification",
        "performance": "1. Check internet connection\n2. Clear browser cache\n3. Try incognito mode",
        "error": "1. Screenshot the error\n2. Note the error code\n3. Try again in 5 minutes"
    }
    return solutions.get(issue_type.lower(), "No specific steps available for this issue.")

# Billing Support Functions
def check_payment_status(invoice_id: str) -> str:
    """Check payment status
    
    Args:
        invoice_id: Invoice ID to check
    """
    print(colored(f"\n💳 Checking payment status for invoice: {invoice_id}", "magenta"))
    # Mock payment data
    payments = {
        "INV001": "Paid",
        "INV002": "Pending",
        "INV003": "Overdue"
    }
    return f"Invoice {invoice_id} status: {payments.get(invoice_id, 'Not Found')}"

def process_refund(order_id: str) -> str:
    """Process a refund request
    
    Args:
        order_id: Order ID to refund
    """
    print(colored(f"\n💰 Processing refund for order: {order_id}", "magenta"))
    return f"Refund initiated for order {order_id}. Please allow 3-5 business days for processing."

# Create specialized agents
tech_support = Agent(
    name="Tech Support",
    model=MODEL_NAME,
    instructions="""You are a Technical Support Specialist.
Focus on resolving technical issues and system-related problems.
Use the available diagnostic and troubleshooting tools.""",
    functions=[check_system_status, troubleshoot_issue]
)

billing_support = Agent(
    name="Billing Support",
    model=MODEL_NAME,
    instructions="""You are a Billing Support Specialist.
Handle all payment, invoice, and refund related queries.
Ensure accurate processing of financial transactions.""",
    functions=[check_payment_status, process_refund]
)

def transfer_to_tech_support() -> Result:
    """Transfer the conversation to technical support"""
    return Result(
        value="Transferring to Technical Support...",
        agent=tech_support
    )

def transfer_to_billing_support() -> Result:
    """Transfer the conversation to billing support"""
    return Result(
        value="Transferring to Billing Support...",
        agent=billing_support
    )

# Create main triage agent
triage_agent = Agent(
    name="Support Triage",
    model=MODEL_NAME,
    instructions="""You are the initial Support Triage Agent.
Determine if the customer needs technical or billing support.
Transfer to the appropriate department using the available functions.
For technical issues: transfer_to_tech_support()
For billing issues: transfer_to_billing_support()""",
    functions=[transfer_to_tech_support, transfer_to_billing_support]
)

try:
    # Initialize the client
    client = Swarm()
    
    # Initialize conversation history
    conversation_history = []
    
    print(colored("Customer Support System Initialized!", "green"))
    print(colored("Available departments:", "yellow"))
    print(colored("- Technical Support (system issues, troubleshooting)", "yellow"))
    print(colored("- Billing Support (payments, refunds, invoices)", "yellow"))
    print(colored("Type 'exit' to end the conversation\n", "yellow"))
    
    while True:
        # Get user input
        user_input = input(colored("You: ", "cyan"))
        
        if user_input.lower() == 'exit':
            print(colored("\nThank you for using our support system! Goodbye!", "green"))
            break
            
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Get response from current agent
            response = client.run(
                agent=triage_agent,  # Initial agent, may change during conversation
                messages=conversation_history
            )
            
            # Update conversation history
            conversation_history.extend(response.messages)
            
            # Handle agent transfer if it occurred
            if response.agent:
                triage_agent = response.agent
                print(colored(f"\nTransferred to {triage_agent.name}!", "yellow"))
            
            # Print agent's response
            print(colored(f"\n{response.messages[-1]['sender']}: {response.messages[-1]['content']}\n", "green"))
            
        except Exception as e:
            print(colored(f"\nError: {str(e)}", "red"))
            print(colored("Please try again.\n", "yellow"))
            
except Exception as e:
    print(colored(f"Initialization Error: {str(e)}", "red")) 