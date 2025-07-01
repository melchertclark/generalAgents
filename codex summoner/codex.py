#!/usr/bin/env python3
"""
Codex Summoner - An interactive Python script that prompts for user input,
then executes the terminal command 'codex -m o3 "input"' and returns the output.

Usage: python codex.py
Then enter your prompt when asked.
"""

import subprocess
import sys
import shlex
import json
import re


def parse_codex_output(raw_output: str) -> str:
    """
    Parse the JSON output from codex command and extract clean text response.
    
    Args:
        raw_output (str): Raw output from codex command
        
    Returns:
        str: Clean text response without JSON metadata
    """
    lines = raw_output.strip().split('\n')
    clean_responses = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        try:
            # Try to parse as JSON
            data = json.loads(line)
            
            # Look for assistant message with output_text content
            if (data.get('type') == 'message' and 
                data.get('role') == 'assistant' and 
                data.get('status') == 'completed' and
                'content' in data):
                
                for content_item in data['content']:
                    if (isinstance(content_item, dict) and 
                        content_item.get('type') == 'output_text' and
                        'text' in content_item):
                        clean_responses.append(content_item['text'].strip())
                        
        except json.JSONDecodeError:
            # If it's not JSON, it might be plain text output
            # Only include if it doesn't look like JSON
            if not line.startswith('{') and not line.startswith('['):
                clean_responses.append(line)
    
    # Join all clean responses
    if clean_responses:
        return '\n'.join(clean_responses)
    else:
        # If no clean responses found, return the original output
        return raw_output


def run_codex_command(prompt: str) -> str:
    """
    Execute the terminal command 'codex -m o3 "prompt"' and return the output.
    
    Args:
        prompt (str): The user's prompt/question to send to o3
        
    Returns:
        str: The output from the codex command
    """
    # Construct the command: codex -m o3 "user_prompt"
    command = f'codex --full-auto -q -m o3 "{prompt}"'
    
    try:
        # Execute the command using subprocess
        # capture_output=True captures both stdout and stderr
        # text=True returns strings instead of bytes
        result = subprocess.run(
            shlex.split(command),  # Split command safely for shell execution
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )
        
        # Check if command executed successfully
        if result.returncode == 0:
            # Parse the output to extract clean text
            raw_output = result.stdout.strip()
            clean_output = parse_codex_output(raw_output)
            return clean_output
        else:
            # If command failed, return the error message
            error_msg = result.stderr.strip() if result.stderr else "Unknown error occurred"
            return f"Error: {error_msg}"
            
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 60 seconds"
    except FileNotFoundError:
        return "Error: 'codex' command not found. Please ensure codex is installed and in your PATH."
    except Exception as e:
        return f"Error executing command: {str(e)}"


def main():
    """
    Main function that prompts for user input and executes the codex command.
    """
    print("Codex Summoner - Interactive Mode")
    print("=" * 40)
    print("Enter your prompt (or 'quit' to exit):")
    
    while True:
        try:
            # Get user input with a prompt
            user_prompt = input("\n> ").strip()
            
            # Check if user wants to quit
            if user_prompt.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            # Check if input is empty
            if not user_prompt:
                print("Please enter a prompt.")
                continue
            
            # Execute the codex command with the user's prompt
            print("\nExecuting: codex -m o3 \"" + user_prompt + "\"")
            print("-" * 50)
            
            output = run_codex_command(user_prompt)
            print(output)
            print("-" * 50)
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n\nGoodbye!")
            break
        except EOFError:
            # Handle Ctrl+D gracefully
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main() 