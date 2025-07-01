#!/usr/bin/env python3
"""
Test script for gemini-cli integration with the polling engine.

This script tests the gemini-cli functionality without running the full polling loop.
"""

import asyncio
import subprocess
import os
from gemini_polling import GeminiPollingEngine

async def test_gemini_cli_basic():
    """Test basic gemini-cli functionality."""
    print("🧪 Testing basic gemini-cli functionality...")
    
    try:
        # Test if gemini-cli responds to a simple query
        test_query = "Hello! Please respond with 'gemini-cli is working' if you can see this message."
        
        result = subprocess.run(
            ["gemini"],
            input=test_query,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ gemini-cli responded successfully")
            print(f"Response: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ gemini-cli error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ gemini-cli not found. Please install with: npm i -g @google/gemini-cli")
        return False
    except subprocess.TimeoutExpired:
        print("❌ gemini-cli command timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing gemini-cli: {e}")
        return False

async def test_polling_engine_gemini_cli():
    """Test the polling engine's gemini-cli integration."""
    print("\n🧪 Testing polling engine gemini-cli integration...")
    
    try:
        # Create a test instance of the polling engine
        engine = GeminiPollingEngine()
        
        # Test the gemini-cli query method with a simple test
        test_query = """TRANSCRIPT ANALYSIS REQUEST - RESPOND VERY BRIEFLY (MAX 100 WORDS)

Current Trigger Entry:
Title: Test Entry
Time: 2024-01-01T12:00:00Z
Content: This is a test entry with **Gemini** mentioned.

Full Context (Today's Transcript):
# Test Transcript
This is a test transcript to verify gemini-cli integration is working properly.

Please provide a VERY BRIEF analysis (max 100 words) addressing any questions or requests in the transcript, particularly focusing on the Gemini-related content. Keep responses short and actionable for mobile notifications."""
        
        print("🤖 Sending test query to gemini-cli...")
        response = await engine.run_gemini_cli_query(test_query)
        
        if response:
            print("✅ gemini-cli integration test successful")
            print(f"Response: {response[:200]}..." if len(response) > 200 else f"Response: {response}")
            return True
        else:
            print("❌ No response from gemini-cli integration test")
            return False
            
    except Exception as e:
        print(f"❌ Error testing polling engine integration: {e}")
        return False

async def test_environment_setup():
    """Test if the environment is properly set up for gemini-cli."""
    print("\n🧪 Testing environment setup...")
    
    # Check if GEMINI_API_KEY is set
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key:
        print(f"✅ GEMINI_API_KEY is set (length: {len(api_key)})")
    else:
        print("⚠️  GEMINI_API_KEY not set - gemini-cli may prompt for authentication")
    
    # Check if gemini command is available
    try:
        result = subprocess.run(
            ["which", "gemini"], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            gemini_path = result.stdout.strip()
            print(f"✅ gemini-cli found at: {gemini_path}")
        else:
            print("❌ gemini-cli not found in PATH")
            return False
    except Exception as e:
        print(f"❌ Error checking gemini-cli availability: {e}")
        return False
    
    return True

async def main():
    """Run all tests."""
    print("🚀 Starting gemini-cli integration tests...\n")
    
    # Test environment setup
    env_ok = await test_environment_setup()
    if not env_ok:
        print("\n❌ Environment setup failed. Please install gemini-cli first.")
        return
    
    # Test basic gemini-cli functionality
    basic_ok = await test_gemini_cli_basic()
    if not basic_ok:
        print("\n❌ Basic gemini-cli test failed.")
        return
    
    # Test polling engine integration
    integration_ok = await test_polling_engine_gemini_cli()
    if not integration_ok:
        print("\n❌ Polling engine integration test failed.")
        return
    
    print("\n🎉 All tests passed! gemini-cli integration is working correctly.")
    print("\nYou can now run the polling engine with:")
    print("python gemini_polling.py")

if __name__ == "__main__":
    asyncio.run(main()) 