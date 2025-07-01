# Codex Conversations

A powerful tool for creating conversations between two codex instances that can iterate back and forth on projects, ideas, and problems.

## Overview

This module allows you to create two separate codex instances with different personalities and have them engage in a structured conversation. Each instance responds to the other's output, creating an iterative process that can help develop ideas, solve problems, or explore concepts from multiple perspectives.

## Features

- **Dual Instance Conversations**: Two codex instances with different personalities
- **Configurable Personalities**: Customize how each instance thinks and responds
- **Structured Rounds**: Control the number of back-and-forth exchanges
- **Automatic Logging**: All conversations are saved to markdown files
- **Interactive Interface**: Easy-to-use prompts for setup
- **Command Line Support**: Direct command line usage for automation

## Files

- `conversation_orchestrator.py` - Core functionality for managing conversations
- `start_conversation.py` - Interactive script for easy setup
- `quick_conversation.py` - Command line interface with arguments (recommended)
- `example_conversation.py` - Example demonstrating different personality types
- `requirements.txt` - Dependencies (minimal, uses standard library)
- `README.md` - This documentation

## Quick Start

### Quick Start with Arguments (Recommended)

1. Navigate to the codex convos directory:
   ```bash
   cd "codex summoner/codex convos"
   ```

2. Use the quick conversation script with arguments:
   ```bash
   python quick_conversation.py "Project Name" "Initial prompt"
   ```

3. Optional arguments:
   ```bash
   python quick_conversation.py "Project Name" "Initial prompt" [rounds] [personality1] [personality2]
   ```

Arguments:
- `Project Name`: Name for the project (used in file naming)
- `Initial prompt`: The starting prompt for the conversation
- `rounds`: Number of conversation rounds (optional, default: 5)
- `personality1`: Personality type for first instance (optional, default: creative)
- `personality2`: Personality type for second instance (optional, default: analytical)

Personality types: `creative`, `analytical`, `optimistic`, `realistic`, `strategic`, `tactical`, `user-focused`, `technical`

### Interactive Mode

For guided setup:

```bash
python start_conversation.py
```

Follow the prompts to:
- Enter a project name
- Provide an initial prompt
- Choose the number of conversation rounds
- Optionally customize personalities

### Direct Command Line Mode

For programmatic usage:

```bash
python conversation_orchestrator.py "Project Name" "Initial prompt" 5
```

## How It Works

1. **Setup**: Two codex instances are created with different personalities:
   - **Codex Alpha**: Creative and innovative, focuses on new ideas
   - **Codex Beta**: Practical and analytical, focuses on refinement

2. **Conversation Flow**:
   - Instance 1 responds to the initial prompt
   - Instance 2 responds to Instance 1's output
   - Instance 1 responds to Instance 2's output
   - This continues for the specified number of rounds

3. **Output**: Each exchange is logged and the full conversation is saved to a markdown file in the `conversations/` directory.

## Example Usage

### Quick Start Examples

```bash
# Basic usage with defaults
python quick_conversation.py "Web App Design" "Design a modern task management app"

# Specify number of rounds
python quick_conversation.py "Business Plan" "Create a startup plan" 3

# Customize personalities
python quick_conversation.py "Architecture" "Design a scalable system" 5 "strategic" "tactical"

# Creative vs analytical discussion
python quick_conversation.py "Product Ideas" "Brainstorm new app features" 4 "creative" "analytical"

# User-focused vs technical discussion
python quick_conversation.py "UX Design" "Improve user experience" 3 "user-focused" "technical"
```

### Interactive Mode Example

```bash
python start_conversation.py
```

Example interaction:
```
🤖 Codex Conversation Starter
========================================
This will start a conversation between two codex instances.
Each instance will respond to the other's output in turn.

Enter project name: Web App Design
Enter initial prompt: Design a modern task management web application
Enter number of conversation rounds (default: 5): 3
Customize instance personalities? (y/n) (default: n): n

🎯 Starting conversation:
   Project: Web App Design
   Initial prompt: Design a modern task management web application
   Rounds: 3
   Participants: Codex Alpha, Codex Beta

============================================================

--- Round 1 ---
Codex Alpha is responding...

Codex Alpha's response:
----------------------------------------
[Creative response about modern UI/UX design]
----------------------------------------

Waiting 3 seconds before next round...

--- Round 2 ---
Codex Beta is responding...

Codex Beta's response:
----------------------------------------
[Practical implementation suggestions]
----------------------------------------

Waiting 3 seconds before next round...

--- Round 3 ---
Codex Alpha is responding...

Codex Alpha's response:
----------------------------------------
[Refined creative ideas based on practical feedback]
----------------------------------------

Conversation completed! Saved to: conversations/Web_App_Design_20241201_143022.md
```

### Customizing Personalities

You can customize the personalities of each instance to create different types of conversations:

- **Creative vs Analytical**: One instance generates ideas, the other critiques them
- **Optimistic vs Pessimistic**: One sees opportunities, the other identifies risks
- **High-level vs Detailed**: One thinks strategically, the other focuses on implementation
- **User-focused vs Technical**: One considers user experience, the other technical feasibility

## Output Files

Conversations are automatically saved to the `conversations/` directory with the naming format:
```
{project_name}_{timestamp}.md
```

Example: `Web_App_Design_20241201_143022.md`

The markdown files include:
- Project metadata (date, participants, personalities)
- Each round with prompts and responses
- Clear formatting for easy reading

## Use Cases

### Project Development
- **Brainstorming**: Generate and refine ideas
- **Problem Solving**: Approach problems from different angles
- **Architecture Design**: Creative design vs practical implementation
- **Feature Planning**: User needs vs technical constraints

### Learning and Exploration
- **Concept Development**: Explore complex topics from multiple perspectives
- **Research Planning**: Creative research questions vs methodological rigor
- **Content Creation**: Creative ideas vs structured organization

### Decision Making
- **Pros and Cons**: Optimistic vs cautious viewpoints
- **Risk Assessment**: Opportunity identification vs risk analysis
- **Strategy Development**: Vision vs execution planning

## Tips for Effective Conversations

1. **Clear Initial Prompts**: Start with specific, well-defined questions or problems
2. **Appropriate Round Count**: 3-7 rounds usually work well for most topics
3. **Complementary Personalities**: Choose personalities that complement each other
4. **Project-Specific Names**: Use descriptive project names for easy file organization
5. **Review Output**: Check the saved markdown files for insights and next steps

## Troubleshooting

### Common Issues

**"codex command not found"**
- Ensure the codex CLI tool is installed and in your PATH
- Check that you can run `codex --help` from the command line

**Conversation stops unexpectedly**
- Check your internet connection
- Verify codex API access and rate limits
- Try reducing the number of rounds

**Timeout errors**
- The script has a 2-minute timeout per response
- For complex topics, consider breaking them into smaller conversations

### Interrupting Conversations

You can interrupt a conversation at any time with `Ctrl+C`. The script will:
- Save the partial conversation to a file
- Display the filename where it was saved
- Exit gracefully

## Requirements

- Python 3.6 or higher
- codex CLI tool installed and accessible
- Internet connection for codex API access

## Dependencies

This script uses only Python standard library modules:
- `subprocess`: Execute codex commands
- `sys`: Command line argument handling
- `shlex`: Safe command parsing
- `json`: Parse codex output
- `re`: Regular expressions for file naming
- `os`: File and directory operations
- `time`: Delays between rounds
- `datetime`: Timestamps and file naming
- `typing`: Type hints for better code documentation

No additional Python packages need to be installed. 