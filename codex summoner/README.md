# Codex Summoner

An interactive Python script that prompts for user input, then executes the terminal command `codex -m o3 "your input"` and returns the output.

## Setup

No dependencies required! The script uses only Python standard library modules.

## Usage

Simply run the script and enter your prompts interactively:

```bash
python codex.py
```

### Interactive Session Example

```
Codex Summoner - Interactive Mode
========================================
Enter your prompt (or 'quit' to exit):

> what is the capital of spain

Executing: codex -m o3 "what is the capital of spain"
--------------------------------------------------
Madrid
--------------------------------------------------

> explain quantum computing

Executing: codex -m o3 "explain quantum computing"
--------------------------------------------------
Quantum computing is a type of computation that harnesses...
--------------------------------------------------

> quit
Goodbye!
```

## Features

- **Interactive Mode**: Prompts for user input in a loop
- **Terminal Command Execution**: Executes `codex -m o3 "prompt"` and captures output
- **Error Handling**: Graceful handling of command failures and timeouts
- **Clean Output**: Shows the command being executed and returns clean results
- **Easy Exit**: Type 'quit', 'exit', or 'q' to exit, or use Ctrl+C

## Requirements

- Python 3.6+
- The `codex` command must be installed and available in your PATH
- The `codex` command must support the `-m o3` syntax

## Error Handling

The script handles various error conditions:
- Command not found (codex not in PATH)
- Command timeout (60 seconds)
- Command execution failures
- Keyboard interrupts (Ctrl+C)
- EOF (Ctrl+D)

## How It Works

1. Script starts and displays a welcome message
2. Prompts user for input with `>`
3. Constructs the command: `codex -m o3 "user_input"`
4. Executes the command using subprocess
5. Captures and displays the output
6. Repeats until user quits 