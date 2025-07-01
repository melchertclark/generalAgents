#!/usr/bin/env python3
"""
Example Codex Conversation - Demonstrates how to use the conversation orchestrator programmatically.

This script shows how to:
1. Create custom codex instances with specific personalities
2. Start a conversation programmatically
3. Handle the conversation flow
4. Access the saved conversation file

Usage: python example_conversation.py
"""

import sys
import os

# Add the current directory to the path so we can import the orchestrator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conversation_orchestrator import CodexInstance, ConversationOrchestrator


def main():
    """
    Example conversation demonstrating different personality types.
    """
    print("🎭 Example Codex Conversation")
    print("=" * 40)
    print("This example creates two instances with contrasting personalities:")
    print("- Optimist: Focuses on opportunities and positive outcomes")
    print("- Realist: Considers practical constraints and potential issues")
    print()
    
    # Create instances with contrasting personalities
    optimist = CodexInstance(
        name="The Optimist",
        personality="""You are an optimistic and enthusiastic AI assistant. You focus on:
- Opportunities and positive outcomes
- Creative solutions and possibilities
- What can go right rather than what can go wrong
- Inspiring and motivating language
- Thinking big and dreaming large"""
    )
    
    realist = CodexInstance(
        name="The Realist", 
        personality="""You are a practical and realistic AI assistant. You focus on:
- Practical constraints and limitations
- Potential issues and risks
- What needs to be considered for success
- Measurable and achievable goals
- Real-world implementation challenges"""
    )
    
    # Create the orchestrator
    project_name = "Startup Business Plan"
    orchestrator = ConversationOrchestrator(project_name, optimist, realist)
    
    # Define the initial prompt
    initial_prompt = """Let's create a business plan for a new tech startup. 
    The startup aims to create an AI-powered personal productivity assistant 
    that helps people manage their time, tasks, and goals more effectively.
    
    What are the key opportunities and potential for this business idea?"""
    
    print(f"Starting conversation: {project_name}")
    print(f"Initial prompt: {initial_prompt}")
    print(f"Rounds: 3")
    print("=" * 60)
    
    try:
        # Start the conversation
        orchestrator.start_conversation(initial_prompt, rounds=3)
        
        # Get the filename of the saved conversation
        conversation_file = orchestrator.get_conversation_filename()
        
        print(f"\n✅ Example conversation completed!")
        print(f"📄 Conversation saved to: {conversation_file}")
        print(f"\n💡 You can now:")
        print(f"   - Read the full conversation in the markdown file")
        print(f"   - Use this as a template for your own conversations")
        print(f"   - Modify the personalities for different types of discussions")
        
    except Exception as e:
        print(f"❌ Error during conversation: {e}")
        print("This might be due to:")
        print("- codex command not being available")
        print("- Network connectivity issues")
        print("- API rate limits")


if __name__ == "__main__":
    main() 