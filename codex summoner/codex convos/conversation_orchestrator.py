#!/usr/bin/env python3
"""
Codex Conversation Orchestrator - Manages two codex instances conversing back and forth on a project.

This script creates two separate codex instances that can iterate on a project by:
1. Starting with an initial prompt
2. Having each instance respond to the other's output
3. Continuing the conversation for a specified number of rounds
4. Saving the conversation history to a file

Usage: python conversation_orchestrator.py [project_name] [initial_prompt] [rounds]
"""

import subprocess
import sys
import shlex
import json
import re
import os
import time
from datetime import datetime
from typing import List, Dict, Tuple


class CodexInstance:
    """
    Represents a single codex instance that can send prompts and receive responses.
    """
    
    def __init__(self, name: str, personality: str = ""):
        """
        Initialize a codex instance with a name and optional personality.
        
        Args:
            name (str): Name/identifier for this instance
            personality (str): Optional personality prompt to prepend to all messages
        """
        self.name = name
        self.personality = personality
        self.conversation_history = []  # Track conversation history for this instance
    
    def send_prompt(self, prompt: str) -> str:
        """
        Send a prompt to this codex instance and return the response.
        
        Args:
            prompt (str): The prompt to send
            
        Returns:
            str: The response from the codex instance
        """
        # Construct the full prompt with personality if specified
        full_prompt = prompt
        if self.personality:
            full_prompt = f"{self.personality}\n\n{prompt}"
        
        # Execute the codex command using the same format as the original codex.py
        command = f'codex --full-auto -q -m o3 "{full_prompt}"'
        
        try:
            # Execute the command using subprocess
            result = subprocess.run(
                shlex.split(command),  # Split command safely for shell execution
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout for longer conversations
            )
            
            # Check if command executed successfully
            if result.returncode == 0:
                # Parse the output to extract clean text
                raw_output = result.stdout.strip()
                clean_output = self._parse_codex_output(raw_output)
                
                # Add to conversation history
                self.conversation_history.append({
                    'prompt': prompt,
                    'response': clean_output,
                    'timestamp': datetime.now().isoformat()
                })
                
                return clean_output
            else:
                # If command failed, return the error message
                error_msg = result.stderr.strip() if result.stderr else "Unknown error occurred"
                return f"Error: {error_msg}"
                
        except subprocess.TimeoutExpired:
            return "Error: Command timed out after 120 seconds"
        except FileNotFoundError:
            return "Error: 'codex' command not found. Please ensure codex is installed and in your PATH."
        except Exception as e:
            return f"Error executing command: {str(e)}"
    
    def _parse_codex_output(self, raw_output: str) -> str:
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


class ConversationOrchestrator:
    """
    Manages a conversation between two codex instances.
    """
    
    def __init__(self, project_name: str, instance1: CodexInstance, instance2: CodexInstance):
        """
        Initialize the conversation orchestrator.
        
        Args:
            project_name (str): Name of the project for file naming
            instance1 (CodexInstance): First codex instance
            instance2 (CodexInstance): Second codex instance
        """
        self.project_name = project_name
        self.instance1 = instance1
        self.instance2 = instance2
        self.conversation_log = []
        self.output_dir = "conversations"
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def start_conversation(self, initial_prompt: str, rounds: int = 5) -> None:
        """
        Start a conversation between the two instances.
        
        Args:
            initial_prompt (str): The initial prompt to start the conversation
            rounds (int): Number of back-and-forth rounds to conduct
        """
        print(f"Starting conversation on project: {self.project_name}")
        print(f"Initial prompt: {initial_prompt}")
        print(f"Rounds: {rounds}")
        print("=" * 60)
        
        # Start with instance1 responding to the initial prompt
        current_prompt = initial_prompt
        current_instance = self.instance1
        responding_instance = self.instance2
        
        for round_num in range(1, rounds + 1):
            print(f"\n--- Round {round_num} ---")
            print(f"{current_instance.name} is responding...")
            
            # Get response from current instance
            response = current_instance.send_prompt(current_prompt)
            
            print(f"\n{current_instance.name}'s response:")
            print("-" * 40)
            print(response)
            print("-" * 40)
            
            # Log this exchange
            self.conversation_log.append({
                'round': round_num,
                'speaker': current_instance.name,
                'prompt': current_prompt,
                'response': response,
                'timestamp': datetime.now().isoformat()
            })
            
            # Switch instances for next round
            current_prompt = response
            current_instance, responding_instance = responding_instance, current_instance
            
            # Add a small delay between rounds to avoid overwhelming the API
            if round_num < rounds:
                print("\nWaiting 3 seconds before next round...")
                time.sleep(3)
        
        # Save the conversation
        self.save_conversation()
        
        print(f"\nConversation completed! Saved to: {self.get_conversation_filename()}")
    
    def save_conversation(self) -> None:
        """
        Save the conversation to a file in markdown format.
        """
        filename = self.get_conversation_filename()
        
        with open(filename, 'w') as f:
            f.write(f"# Codex Conversation: {self.project_name}\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Participants:** {self.instance1.name}, {self.instance2.name}\n\n")
            
            if self.instance1.personality:
                f.write(f"**{self.instance1.name} Personality:** {self.instance1.personality}\n\n")
            if self.instance2.personality:
                f.write(f"**{self.instance2.name} Personality:** {self.instance2.personality}\n\n")
            
            f.write("---\n\n")
            
            for exchange in self.conversation_log:
                f.write(f"## Round {exchange['round']}: {exchange['speaker']}\n\n")
                f.write(f"**Prompt:**\n{exchange['prompt']}\n\n")
                f.write(f"**Response:**\n{exchange['response']}\n\n")
                f.write("---\n\n")
    
    def get_conversation_filename(self) -> str:
        """
        Generate the filename for the conversation log.
        
        Returns:
            str: The filename for the conversation
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_project_name = re.sub(r'[^a-zA-Z0-9_-]', '_', self.project_name)
        return os.path.join(self.output_dir, f"{safe_project_name}_{timestamp}.md")


def main():
    """
    Main function to run the conversation orchestrator.
    """
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python conversation_orchestrator.py <project_name> [initial_prompt] [rounds]")
        print("\nExample: python conversation_orchestrator.py 'Web App Design' 'Design a modern web app' 5")
        sys.exit(1)
    
    project_name = sys.argv[1]
    
    # Get initial prompt (default or from command line)
    if len(sys.argv) >= 3:
        initial_prompt = sys.argv[2]
    else:
        initial_prompt = input("Enter the initial prompt for the conversation: ").strip()
        if not initial_prompt:
            print("No initial prompt provided. Exiting.")
            sys.exit(1)
    
    # Get number of rounds (default or from command line)
    if len(sys.argv) >= 4:
        try:
            rounds = int(sys.argv[3])
        except ValueError:
            print("Invalid number of rounds. Using default of 5.")
            rounds = 5
    else:
        rounds_input = input("Enter number of conversation rounds (default 5): ").strip()
        rounds = int(rounds_input) if rounds_input.isdigit() else 5
    
    # Create two codex instances with different personalities
    instance1 = CodexInstance(
        name="Codex Alpha",
        personality="You are a creative and innovative AI assistant. Focus on generating new ideas and thinking outside the box."
    )
    
    instance2 = CodexInstance(
        name="Codex Beta", 
        personality="You are a practical and analytical AI assistant. Focus on refining ideas and providing detailed implementation suggestions."
    )
    
    # Create and run the conversation
    orchestrator = ConversationOrchestrator(project_name, instance1, instance2)
    
    try:
        orchestrator.start_conversation(initial_prompt, rounds)
    except KeyboardInterrupt:
        print("\n\nConversation interrupted by user.")
        print("Saving partial conversation...")
        orchestrator.save_conversation()
        print(f"Partial conversation saved to: {orchestrator.get_conversation_filename()}")


if __name__ == "__main__":
    main() 