#!/usr/bin/env python3
"""
Quick Codex Conversation - Simple command line interface for starting conversations.

This script provides a quick way to start conversations using command line arguments,
similar to the original codex.py format.

Usage examples:
  python quick_conversation.py "Project Name" "Initial prompt"
  python quick_conversation.py "Web App" "Design a modern interface" 3
  python quick_conversation.py "Business Plan" "Create a startup plan" 5 "creative" "analytical"
"""

import sys
import os

# Add the current directory to the path so we can import the orchestrator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conversation_orchestrator import CodexInstance, ConversationOrchestrator


def get_personality_by_type(personality_type: str) -> str:
    """
    Get a predefined personality based on type.
    
    Args:
        personality_type (str): Type of personality (creative, analytical, optimistic, etc.)
        
    Returns:
        str: Personality prompt
    """
    personalities = {
        "creative": "You are a creative and innovative AI assistant. Focus on generating new ideas, thinking outside the box, and exploring unconventional solutions.",
        "analytical": "You are a practical and analytical AI assistant. Focus on refining ideas, providing detailed implementation suggestions, and considering practical constraints.",
        "optimistic": "You are an optimistic and enthusiastic AI assistant. Focus on opportunities, positive outcomes, and what can go right rather than what can go wrong.",
        "realistic": "You are a practical and realistic AI assistant. Focus on practical constraints, potential issues, and real-world implementation challenges.",
        "strategic": "You are a strategic and high-level AI assistant. Focus on big-picture thinking, long-term planning, and overall vision.",
        "tactical": "You are a tactical and detail-oriented AI assistant. Focus on specific implementation details, step-by-step planning, and execution strategies.",
        "user-focused": "You are a user-focused AI assistant. Focus on user experience, customer needs, and how solutions benefit end users.",
        "technical": "You are a technical and implementation-focused AI assistant. Focus on technical feasibility, architecture, and engineering considerations."
    }
    
    return personalities.get(personality_type.lower(), personalities["creative"])


def main():
    """
    Main function for quick conversation setup.
    """
    # Check command line arguments
    if len(sys.argv) < 3:
        print("Quick Codex Conversation")
        print("=" * 30)
        print("Usage: python quick_conversation.py <project_name> <initial_prompt> [rounds] [personality1] [personality2]")
        print()
        print("Arguments:")
        print("  project_name    - Name for the project (used in file naming)")
        print("  initial_prompt  - The starting prompt for the conversation")
        print("  rounds          - Number of conversation rounds (default: 5)")
        print("  personality1    - Personality type for first instance (default: creative)")
        print("  personality2    - Personality type for second instance (default: analytical)")
        print()
        print("Personality types: creative, analytical, optimistic, realistic, strategic, tactical, user-focused, technical")
        print()
        print("Examples:")
        print("  python quick_conversation.py 'Web App' 'Design a modern interface'")
        print("  python quick_conversation.py 'Business Plan' 'Create a startup plan' 3")
        print("  python quick_conversation.py 'Architecture' 'Design system' 5 'strategic' 'tactical'")
        sys.exit(1)
    
    # Parse arguments
    project_name = sys.argv[1]
    initial_prompt = sys.argv[2]
    
    # Get number of rounds (default: 5)
    rounds = 5
    if len(sys.argv) >= 4:
        try:
            rounds = int(sys.argv[3])
            if rounds < 1:
                print("Number of rounds must be at least 1. Using 5.")
                rounds = 5
        except ValueError:
            print("Invalid number of rounds. Using 5.")
            rounds = 5
    
    # Get personality types (default: creative, analytical)
    personality1_type = "creative"
    personality2_type = "analytical"
    
    if len(sys.argv) >= 5:
        personality1_type = sys.argv[4]
    if len(sys.argv) >= 6:
        personality2_type = sys.argv[5]
    
    # Get personality prompts
    personality1 = get_personality_by_type(personality1_type)
    personality2 = get_personality_by_type(personality2_type)
    
    # Create instances
    instance1 = CodexInstance(name="Codex Alpha", personality=personality1)
    instance2 = CodexInstance(name="Codex Beta", personality=personality2)
    
    # Create and start the conversation
    orchestrator = ConversationOrchestrator(project_name, instance1, instance2)
    
    print(f"🚀 Quick Codex Conversation")
    print(f"Project: {project_name}")
    print(f"Initial prompt: {initial_prompt}")
    print(f"Rounds: {rounds}")
    print(f"Personalities: {personality1_type} vs {personality2_type}")
    print("=" * 60)
    
    try:
        orchestrator.start_conversation(initial_prompt, rounds)
        print(f"\n✅ Conversation completed! Saved to: {orchestrator.get_conversation_filename()}")
    except KeyboardInterrupt:
        print("\n\nConversation interrupted by user.")
        print("Saving partial conversation...")
        orchestrator.save_conversation()
        print(f"Partial conversation saved to: {orchestrator.get_conversation_filename()}")
    except Exception as e:
        print(f"\n❌ Error during conversation: {e}")
        print("This might be due to:")
        print("- codex command not being available")
        print("- Network connectivity issues")
        print("- API rate limits")


if __name__ == "__main__":
    main() 