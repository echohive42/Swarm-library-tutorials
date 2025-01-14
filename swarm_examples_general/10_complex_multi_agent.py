"""
# Complex Multi-Agent System Example - Virtual Company
# This example demonstrates a sophisticated multi-agent system
# Shows how multiple specialized agents can work together in a complex workflow
# Implements a virtual company with different departments and roles
"""

import os
import time
from termcolor import colored
from swarm import Swarm, Agent
from swarm.types import Result

# Constants
MODEL = "gpt-4o"
FAST_MODEL = "gpt-4o-mini"
HISTORY = []

# Company database simulation
PRODUCTS = {
    "laptop": {"price": 999.99, "stock": 50, "category": "electronics"},
    "smartphone": {"price": 599.99, "stock": 100, "category": "electronics"},
    "desk": {"price": 299.99, "stock": 30, "category": "furniture"},
    "chair": {"price": 199.99, "stock": 45, "category": "furniture"}
}

EMPLOYEES = {
    "sales": ["John", "Alice"],
    "support": ["Bob", "Carol"],
    "technical": ["Dave", "Eve"],
    "management": ["Frank"]
}

TICKETS = {}  # Will store support tickets
ORDERS = {}   # Will store orders

def check_product_info(product_name: str) -> str:
    """Get information about a product.
    
    Args:
        product_name: Name of the product
    """
    print(colored(f"\n📦 Checking product info: {product_name}...", "magenta"))
    if product_name not in PRODUCTS:
        return f"Product '{product_name}' not found."
    
    product = PRODUCTS[product_name]
    return f"""
Product: {product_name}
Price: ${product['price']}
Stock: {product['stock']} units
Category: {product['category']}
"""

def create_order(context_variables: dict, product_name: str, quantity: int) -> Result:
    """Create a new order.
    
    Args:
        product_name: Name of the product
        quantity: Quantity to order
    """
    print(colored(f"\n🛍️ Creating order: {quantity}x {product_name}...", "magenta"))
    if product_name not in PRODUCTS:
        return Result(value=f"Product '{product_name}' not found.")
    
    if quantity <= 0:
        return Result(value="Quantity must be positive.")
    
    product = PRODUCTS[product_name]
    if quantity > product["stock"]:
        return Result(value=f"Insufficient stock. Only {product['stock']} units available.")
    
    order_id = len(ORDERS) + 1
    total_price = product["price"] * quantity
    
    ORDERS[order_id] = {
        "product": product_name,
        "quantity": quantity,
        "total_price": total_price,
        "status": "pending",
        "customer_name": context_variables.get("customer_name", "Unknown")
    }
    
    # Update stock
    PRODUCTS[product_name]["stock"] -= quantity
    
    return Result(
        value=f"Order created successfully!\nOrder ID: {order_id}\nTotal: ${total_price:.2f}",
        context_variables={"last_order_id": order_id}
    )

def check_order_status(order_id: int) -> str:
    """Check the status of an order.
    
    Args:
        order_id: The order ID to check
    """
    print(colored(f"\n🔍 Checking order status #{order_id}...", "magenta"))
    if order_id not in ORDERS:
        return f"Order {order_id} not found."
    
    order = ORDERS[order_id]
    return f"""
Order ID: {order_id}
Product: {order['product']}
Quantity: {order['quantity']}
Total Price: ${order['total_price']:.2f}
Status: {order['status']}
Customer: {order['customer_name']}
"""

def create_support_ticket(context_variables: dict, issue: str, priority: str) -> Result:
    """Create a new support ticket.
    
    Args:
        issue: Description of the issue
        priority: Ticket priority (low, medium, high)
    """
    print(colored(f"\n🎫 Creating support ticket: {priority} priority...", "magenta"))
    if priority.lower() not in ["low", "medium", "high"]:
        return Result(value="Invalid priority. Use: low, medium, or high")
    
    ticket_id = len(TICKETS) + 1
    TICKETS[ticket_id] = {
        "issue": issue,
        "priority": priority.lower(),
        "status": "open",
        "customer_name": context_variables.get("customer_name", "Unknown"),
        "assigned_to": None
    }
    
    return Result(
        value=f"Support ticket created.\nTicket ID: {ticket_id}\nPriority: {priority}",
        context_variables={"last_ticket_id": ticket_id}
    )

def check_ticket_status(ticket_id: int) -> str:
    """Check the status of a support ticket.
    
    Args:
        ticket_id: The ticket ID to check
    """
    print(colored(f"\n🔍 Checking ticket status #{ticket_id}...", "magenta"))
    if ticket_id not in TICKETS:
        return f"Ticket {ticket_id} not found."
    
    ticket = TICKETS[ticket_id]
    return f"""
Ticket ID: {ticket_id}
Issue: {ticket['issue']}
Priority: {ticket['priority']}
Status: {ticket['status']}
Customer: {ticket['customer_name']}
Assigned to: {ticket['assigned_to'] or 'Unassigned'}
"""

def assign_ticket(ticket_id: int, department: str) -> Result:
    """Assign a ticket to a department.
    
    Args:
        ticket_id: The ticket ID to assign
        department: Department to assign to
    """
    print(colored(f"\n👥 Assigning ticket #{ticket_id} to {department} department...", "magenta"))
    if ticket_id not in TICKETS:
        return Result(value=f"Ticket {ticket_id} not found.")
    
    if department not in EMPLOYEES:
        return Result(value=f"Department '{department}' not found.")
    
    # Simple round-robin assignment
    assigned_to = EMPLOYEES[department][0]
    EMPLOYEES[department].append(EMPLOYEES[department].pop(0))
    
    TICKETS[ticket_id]["assigned_to"] = assigned_to
    
    return Result(
        value=f"Ticket {ticket_id} assigned to {assigned_to} from {department} department."
    )

def get_department_status(department: str) -> str:
    """Get the status of a department.
    
    Args:
        department: Name of the department
    """
    print(colored(f"\n📊 Checking {department} department status...", "magenta"))
    if department not in EMPLOYEES:
        return f"Department '{department}' not found."
    
    # Count assigned tickets
    assigned_tickets = sum(1 for t in TICKETS.values() if t["assigned_to"] in EMPLOYEES[department])
    
    return f"""
Department: {department}
Employees: {', '.join(EMPLOYEES[department])}
Active tickets: {assigned_tickets}
"""

# Initialize Swarm client
print(colored("Initializing Swarm client...", "cyan"))
client = Swarm()

# Create specialized agents
receptionist = Agent(
    name="Receptionist",
    model=FAST_MODEL,
    instructions="""You are the company receptionist.
    You handle initial customer contact and direct them to appropriate departments.
    For sales inquiries -> Sales Agent
    For support issues -> Support Agent
    For technical questions -> Technical Agent
    For management issues -> Management Agent
    
    Always be polite and professional."""
)

sales_agent = Agent(
    name="Sales Agent",
    model=MODEL,
    instructions="""You are a sales agent.
    Handle product inquiries and orders.
    Always check product availability before creating orders.
    Suggest related products when appropriate.""",
    functions=[check_product_info, create_order, check_order_status]
)

support_agent = Agent(
    name="Support Agent",
    model=MODEL,
    instructions="""You are a support agent.
    Handle customer issues and create support tickets.
    Prioritize tickets appropriately:
    - High: System down, critical features not working
    - Medium: Important issues affecting work
    - Low: Minor issues, cosmetic problems""",
    functions=[create_support_ticket, check_ticket_status]
)

technical_agent = Agent(
    name="Technical Agent",
    model=MODEL,
    instructions="""You are a technical support specialist.
    Handle complex technical issues and provide detailed solutions.
    Explain technical concepts in an understandable way.""",
    functions=[check_ticket_status, assign_ticket]
)

management_agent = Agent(
    name="Management Agent",
    model=MODEL,
    instructions="""You are a management representative.
    Handle escalated issues and department oversight.
    Monitor department performance and resource allocation.""",
    functions=[get_department_status, assign_ticket]
)

# Create transfer functions
def transfer_to_sales() -> Result:
    """Transfer to sales department."""
    print(colored("\n🔄 Transferring to sales department...", "yellow"))
    return Result(value="Transferring to sales...", agent=sales_agent)

def transfer_to_support() -> Result:
    """Transfer to support department."""
    print(colored("\n🔄 Transferring to support department...", "yellow"))
    return Result(value="Transferring to support...", agent=support_agent)

def transfer_to_technical() -> Result:
    """Transfer to technical department."""
    print(colored("\n🔄 Transferring to technical support...", "yellow"))
    return Result(value="Transferring to technical support...", agent=technical_agent)

def transfer_to_management() -> Result:
    """Transfer to management."""
    print(colored("\n🔄 Transferring to management...", "yellow"))
    return Result(value="Transferring to management...", agent=management_agent)

def transfer_to_receptionist() -> Result:
    """Transfer back to receptionist."""
    print(colored("\n🔄 Transferring back to reception...", "yellow"))
    return Result(value="Transferring back to reception...", agent=receptionist)

# Add transfer functions to each agent
receptionist.functions = [
    transfer_to_sales,
    transfer_to_support,
    transfer_to_technical,
    transfer_to_management
]

sales_agent.functions.extend([transfer_to_support, transfer_to_management, transfer_to_receptionist])
support_agent.functions.extend([transfer_to_technical, transfer_to_management, transfer_to_receptionist])
technical_agent.functions.extend([transfer_to_support, transfer_to_management, transfer_to_receptionist])
management_agent.functions.extend([
    transfer_to_sales,
    transfer_to_support,
    transfer_to_technical,
    transfer_to_receptionist
])

def chat_loop():
    global HISTORY
    current_agent = receptionist
    context = {"customer_name": ""}
    
    print(colored("\nVirtual Company System started! Type 'exit' to end.", "green"))
    print(colored("You're speaking with our receptionist.", "cyan"))
    print(colored("Available departments:\n- Sales\n- Support\n- Technical Support\n- Management", "cyan"))
    
    # Get customer name
    user_input = input(colored("\nReceptionist: Welcome! May I have your name? ", "green"))
    context["customer_name"] = user_input
    HISTORY.append({"role": "user", "content": user_input})
    
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
            print(colored(f"\n{current_agent.name} is responding...", "cyan"))
            response = client.run(
                agent=current_agent,
                messages=HISTORY,
                context_variables=context
            )

            # Update context with any changes
            context.update(response.context_variables)
            
            # Update history with agent's response
            HISTORY.extend(response.messages)
            
            # Check if agent changed
            if response.agent and response.agent != current_agent:
                current_agent = response.agent
                print(colored(f"\nTransferred to {current_agent.name}", "yellow"))
            
            # Print agent's response
            print(colored(f"\n{current_agent.name}: {response.messages[-1]['content']}", "green"))

        except Exception as e:
            print(colored(f"\nSystem Error: {str(e)}", "red"))

if __name__ == "__main__":
    try:
        chat_loop()
    except KeyboardInterrupt:
        print(colored("\nSession ended by user.", "yellow"))
    except Exception as e:
        print(colored(f"\nUnexpected error: {str(e)}", "red")) 