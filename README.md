# 🚀 Swarm Library Tutorial

## Overview

This repository contains two comprehensive tutorial sets for the [Swarm library](https://github.com/openai/swarm), a powerful tool for building AI-powered applications with multiple specialized agents. Each set demonstrates different aspects of the library through practical examples.

## 🎯 Purpose

The tutorials aim to help developers understand how to:

- Build AI applications using the Swarm library
- Work with different types of agents and conversation patterns
- Manage context and state in AI applications
- Handle errors and implement retry mechanisms
- Create production-ready AI systems with multiple agents

## 🎥 Watch How It's Built!

**[Watch the complete build process on Patreon](https://www.patreon.com/posts/how-to-build-119979655)** - This tutorial is part of the comprehensive 1000x Cursor Course!

See exactly how this automation system was created step by step, with detailed explanations and insights into the development process. Learn advanced techniques for building AI applications while mastering the Cursor Code Editor.

## ❤️ Support & Get 400+ AI Projects

This is one of 400+ fascinating projects in my collection! [Support me on Patreon](https://www.patreon.com/c/echohive42/membership) to get:

- 🎯 Access to 400+ AI projects (and growing daily!)
- 📥 Full source code & detailed explanations
- 📚 1000x Cursor Course (32 chapters, 21+ hours of comprehensive content for mastering the Cursor Code Editor)
- 🎓 Live coding sessions & AMAs
- 💬 1-on-1 consultations (higher tiers)
- 🎁 Exclusive discounts on AI tools & platforms (up to $180 value)

## 📦 Install Swarm Library

Requires Python 3.10+

```bash
pip install git+ssh://git@github.com/openai/swarm.git
```
or
```bash
pip install git+https://github.com/openai/swarm.git
```

## 📚 Tutorial Sets

### 💡 General Examples (`swarm_examples_general/`)

A broad collection of examples showcasing various Swarm features in different contexts:

1. **Basic Chat** - Simple chat agent with conversation history
2. **Function Calling** - Weather and calculator utilities
3. **Context Variables** - Shopping cart with state management
4. **Agent Handoff** - Department-based conversation transfers
5. **Streaming** - Interactive storytelling with real-time responses
6. **Parallel Tools** - Data processing with concurrent analysis
7. **Model Override** - Text processing with multiple models
8. **Error Handling** - Robust task execution with retries
9. **Advanced Context** - RPG game with complex state management
10. **Complex Multi-Agent** - Virtual company with department coordination

### 🎯 Customer Service Examples (`swarm_examples_customer_service/`)

Specialized examples focused on building customer service applications:

1. **Basic Chat** - Customer service chat fundamentals
2. **Function Calling** - Order tracking and support functions
3. **Context Variables** - Customer profile and interaction history
4. **Agent Handoff** - Support ticket routing between departments
5. **Streaming** - Real-time customer support responses
6. **Parallel Tools** - Concurrent customer request handling
7. **Model Override** - Priority-based support with different models
8. **Advanced Context** - Customer journey and preference tracking
9. **Complex Multi-Agent** - Full support system with multiple departments
10. **Complete Platform** - Integrated customer service platform

## 🔄 Key Differences Between Sets

### General Examples:

- Broader range of use cases
- Focus on demonstrating individual features
- More diverse implementations
- Suitable for learning core concepts

### Customer Service Examples:

- Focused on customer service scenarios
- Progressive building of a support system
- Interconnected examples
- Real-world customer service patterns

## 🛠️ Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key as an environment variable:

```bash
# Windows
set OPENAI_API_KEY=your_api_key_here

# Linux/Mac
export OPENAI_API_KEY=your_api_key_here
```

## 🎨 Common Features

- Beautiful terminal output with colored messages and emojis
- Comprehensive error handling with descriptive messages
- UTF-8 encoding for all file operations
- Separation of concerns in code organization
- Environment variable based configuration
- Async support for OpenAI operations

## 🌟 Best Practices Demonstrated

- Clear function documentation and type hints
- Consistent error handling patterns
- Clean code organization and modularity
- Effective use of constants and configuration
- Proper async/await usage
- Beautiful terminal UI with status indicators

## 📝 Notes

- Examples use mock data for demonstration purposes
- Each example can be run independently
- Code includes detailed comments and documentation
- Error handling follows best practices
- Terminal output is enhanced with colors and emojis

## 🚀 Getting Started

1. Clone this repository
2. Install dependencies from requirements.txt
3. Set up your OpenAI API key
4. Choose your learning path:

For general Swarm features:

```bash
python swarm_examples_general/01_basic_chat.py
```

For customer service focus:

```bash
python swarm_examples_customer_service/01_basic_chat.py
```

## 🎯 Learning Paths

### General Learning Path:

Start with the general examples if you're new to Swarm and want to understand core features in various contexts.

### Customer Service Path:

Choose the customer service examples if you're specifically building a customer service application or want to see a cohesive system built progressively.

## 🔧 Customization

Both sets of examples are well-documented and modular, making them easy to adapt for your specific use cases. Choose the set that best matches your needs and modify accordingly.
