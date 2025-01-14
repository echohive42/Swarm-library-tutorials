# Swarm Examples Collection

A comprehensive collection of examples demonstrating the capabilities of the Swarm library, ranging from basic usage to complex multi-agent systems.

## 🚀 Getting Started

### Prerequisites

```bash
pip install -r requirements.txt
```

Required packages:

- openai
- termcolor
- swarm

### Running Examples

Each example can be run independently:

```bash
python swarm_examples/XX_example_name.py
```

## 📚 Examples Overview

### 1. Basic Chat (01_basic_chat.py)

- Simple chat interaction with a single agent
- Demonstrates basic conversation handling
- Shows how to maintain chat history
- Perfect starting point for understanding Swarm

### 2. Function Calling (02_function_calling.py)

- Shows how to create an agent with utility functions
- Implements time, calculator, and weather functions
- Demonstrates function parameter handling
- Shows practical usage in conversation context

### 3. Context Variables (03_context_variables.py)

- Implements a shopping cart system
- Shows state management between function calls
- Demonstrates how to maintain and update context
- Features cart operations (add, remove, view)

### 4. Agent Handoff (04_agent_handoff.py)

- Customer service system with multiple departments
- Shows how to transfer conversations between agents
- Implements support, sales, and technical departments
- Demonstrates intelligent routing based on queries

### 5. Streaming (05_streaming.py)

- Interactive storytelling system
- Shows real-time streaming responses
- Implements typewriter-style output
- Features dynamic story choices

### 6. Parallel Tools (06_parallel_tools.py)

- Data processing system with parallel operations
- Shows how to handle multiple function calls simultaneously
- Demonstrates efficient processing of multiple metrics
- Features timing and performance tracking

### 7. Model Override (07_model_override.py)

- Text processing system with different models
- Shows how to use different models for different tasks
- Demonstrates model selection based on task complexity
- Features basic and advanced processors

### 8. Error Handling (08_error_handling.py)

- Robust task execution system
- Shows advanced error handling strategies
- Implements retry mechanisms
- Demonstrates graceful failure recovery

### 9. Advanced Context (09_advanced_context.py)

- RPG game system with complex state
- Shows advanced context management
- Features inventory, stats, and quest tracking
- Demonstrates complex state updates

### 10. Complex Multi-Agent (10_complex_multi_agent.py)

- Virtual company system with multiple departments
- Shows sophisticated multi-agent orchestration
- Implements complete business workflow
- Features tickets, orders, and department management

## 🎨 Features Across Examples

### Beautiful Terminal Output

- Colorful output using termcolor
- Emoji indicators for different operations
- Progress and status indicators
- Clear visual separation of different operations

### Error Handling

- Try-except blocks in all critical operations
- Informative error messages
- Graceful error recovery
- User-friendly error reporting

### Code Structure

- Clear separation of concerns
- Well-documented functions
- Consistent coding style
- Type hints and docstrings

### Agent Design

- Clear agent instructions
- Specialized agent roles
- Efficient function distribution
- Smart handoff mechanisms

## 🛠️ Common Patterns

### Function Structure

```python
def some_function(context_variables: dict, param: str) -> Result:
    """Function description.
  
    Args:
        context_variables: State dictionary
        param: Parameter description
    """
    print(colored(f"\n🔍 Operation description...", "magenta"))
    # Function logic
    return Result(
        value="Operation result",
        context_variables={"updated": "state"}
    )
```

### Agent Creation

```python
agent = Agent(
    name="Agent Name",
    model=MODEL,
    instructions="""Clear instructions about:
    1. Agent's role
    2. Available functions
    3. When to transfer to other agents""",
    functions=[function1, function2]
)
```

### Chat Loop

```python
while True:
    user_input = input(colored("\nYou: ", "yellow"))
    if user_input.lower() == 'exit':
        break
  
    try:
        response = client.run(
            agent=current_agent,
            messages=HISTORY,
            context_variables=context
        )
        # Handle response
    except Exception as e:
        print(colored(f"\nError: {str(e)}", "red"))
```

## 🎯 Best Practices Demonstrated

1. **State Management**

   - Clear context variable structure
   - Proper state updates
   - State isolation between agents
2. **User Experience**

   - Clear prompts and instructions
   - Visual feedback for operations
   - Consistent interaction patterns
3. **Error Handling**

   - Comprehensive error catching
   - Informative error messages
   - Graceful degradation
4. **Code Organization**

   - Constants at the top
   - Clear function grouping
   - Logical file structure
5. **Documentation**

   - Clear docstrings
   - Function parameter documentation
   - Usage examples
