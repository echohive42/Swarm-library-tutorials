# Swarm Examples - Customer Service Edition

This collection of examples demonstrates how to build customer service applications using the Swarm library. Each example progressively introduces more complex concepts and features.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Examples

### 1. Basic Chat (01_basic_chat.py)
- Simple customer service chat bot
- Basic conversation handling
- Error handling and graceful exits

### 2. Function Calling (02_function_calling.py)
- Order status checking
- Shipment tracking
- Basic customer service functions

### 3. Context Variables (03_context_variables.py)
- Customer preference management
- Interaction history tracking
- Personalized responses

### 4. Agent Handoff (04_agent_handoff.py)
- Multiple specialized departments
- Seamless conversation transfers
- Department-specific functions

### 5. Streaming (05_streaming.py)
- Real-time response streaming
- Product information system
- Enhanced user experience

### 6. Parallel Tools (06_parallel_tools.py)
- Travel booking system
- Concurrent service checks
- Multi-service coordination

### 7. Model Override (07_model_override.py)
- Support ticket system
- Different models for different tasks
- Advanced error handling

### 8. Advanced Context (08_advanced_context.py)
- Shopping assistant
- Complex preference management
- Cart and purchase history

### 9. Complex Multi-Agent (09_complex_multi_agent.py)
- Restaurant ordering system
- Kitchen and delivery coordination
- Multi-step workflows

### 10. Complete Platform (10_complete_platform.py)
- Comprehensive support system
- Knowledge base integration
- Ticket management
- Live chat support

## Running the Examples

Each example can be run independently:

```bash
python example_name.py
```

For example:
```bash
python 01_basic_chat.py
```

## Features Demonstrated

- Conversation Management
- Function Calling
- Context Variables
- Agent Handoff
- Streaming Responses
- Parallel Tool Execution
- Model Overrides
- Error Handling
- Multi-Agent Systems
- Complex Workflows

## Best Practices Implemented

- Descriptive error messages
- Proper exception handling
- Clean code organization
- Separation of concerns
- Maintainable code structure
- User-friendly interfaces
- Informative status messages
- Graceful error recovery

## Notes

- These examples use mock data for demonstration
- Replace mock functions with actual implementations for production use
- Add proper authentication and security measures
- Implement proper data persistence
- Add logging and monitoring for production deployments 