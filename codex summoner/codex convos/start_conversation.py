#!/usr/bin/env python3
"""
Interactive Codex Conversation Starter - A simple script to start conversations between two codex instances.

This script provides an interactive interface to:
1. Set up a project name
2. Define the initial prompt
3. Choose the number of conversation rounds
4. Optionally customize the personalities of the two instances
5. Start the conversation

Usage: python start_conversation.py
"""

import sys
import os

# Add the parent directory to the path so we can import the orchestrator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conversation_orchestrator import CodexInstance, ConversationOrchestrator


def get_user_input(prompt: str, default: str = "") -> str:
    """
    Get user input with an optional default value.
    
    Args:
        prompt (str): The prompt to show the user
        default (str): Default value if user just presses Enter
        
    Returns:
        str: User input or default value
    """
    if default:
        user_input = input(f"{prompt} (default: {default}): ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()


def main():
    """
    Main interactive function to start a codex conversation.
    """
    print("🤖 Codex Conversation Starter")
    print("=" * 40)
    print("This will start a conversation between two codex instances.")
    print("Each instance will respond to the other's output in turn.\n")
    
    # Get project details
    project_name = get_user_input("Enter project name")
    if not project_name:
        print("Project name is required. Exiting.")
        return
    
    initial_prompt = get_user_input("Enter initial prompt")
    if not initial_prompt:
        print("Initial prompt is required. Exiting.")
        return
    
    # Get number of rounds
    rounds_input = get_user_input("Enter number of conversation rounds", "5")
    try:
        rounds = int(rounds_input)
        if rounds < 1:
            print("Number of rounds must be at least 1. Using 5.")
            rounds = 5
    except ValueError:
        print("Invalid number. Using 5 rounds.")
        rounds = 5
    
    # Ask if user wants to customize personalities
    customize = get_user_input("Customize instance personalities? (y/n)", "n").lower()
    
    if customize in ['y', 'yes']:
        print("\n--- Customizing Personalities ---")
        personality1 = get_user_input(
            "Enter personality for Codex Alpha (creative/innovative)", 
            "You are a creative and innovative AI assistant. Focus on generating new ideas and thinking outside the box."
        )
        personality2 = get_user_input(
            "Enter personality for Codex Beta (practical/analytical)", 
            "You are a practical and analytical AI assistant. Focus on refining ideas and providing detailed implementation suggestions."
        )
    else:
        # Use default personalities
        personality1 = "You are a creative and innovative AI assistant. Focus on generating new ideas and thinking outside the box."
        personality2 = "You are a practical and analytical AI assistant. Focus on refining ideas and providing detailed implementation suggestions."
    
    # Create the instances
    instance1 = CodexInstance(name="Codex Alpha", personality=personality1)
    instance2 = CodexInstance(name="Codex Beta", personality=personality2)
    
    # Create and start the conversation
    orchestrator = ConversationOrchestrator(project_name, instance1, instance2)
    
    print(f"\n🎯 Starting conversation:")
    print(f"   Project: {project_name}")
    print(f"   Initial prompt: {initial_prompt}")
    print(f"   Rounds: {rounds}")
    print(f"   Participants: {instance1.name}, {instance2.name}")
    print("\n" + "=" * 60)
    
    try:
        orchestrator.start_conversation(initial_prompt, rounds)
    except KeyboardInterrupt:
        print("\n\nConversation interrupted by user.")
        print("Saving partial conversation...")
        orchestrator.save_conversation()
        print(f"Partial conversation saved to: {orchestrator.get_conversation_filename()}")
    except Exception as e:
        print(f"\nError during conversation: {e}")
        print("Saving partial conversation...")
        try:
            orchestrator.save_conversation()
            print(f"Partial conversation saved to: {orchestrator.get_conversation_filename()}")
        except:
            print("Could not save conversation.")


if __name__ == "__main__":
    main() 