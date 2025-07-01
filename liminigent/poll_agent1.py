import asyncio
from mcp_agent.core.fastagent import FastAgent
from mcp_agent.core.request_params import RequestParams

# Create the FastAgent application with enhanced configuration for transcript analysis
# FastAgent is the main class for creating AI agents with MCP (Model Context Protocol) support
fast = FastAgent("Transcript Analysis Poll Agent")

@fast.agent(
    instruction="""You are a transcript analysis agent specialized in processing daily transcript structures from Limitless AI (up to 96,000 characters). Your primary role is to:

1. **Identify the Gemini trigger**: Find the most recent mention of "Gemini" in the transcript
2. **Extract the key question**: Determine the specific question or request being made in the context around the most recent Gemini mention
3. **Analyze relevant context**: Review the surrounding conversation to understand the relevant details.
4. **Provide focused response**: Answer ONLY the specific question identified, ignoring unrelated content, previous questions, etc.
5. **Keep it brief**: Responses must be  concise (max 2-3 paragraphs) and directly address the core question

**IMPORTANT**: Do not summarize the whole transcript or provide general insights. Focus solely on answering the specific question that triggered the Gemini mention.

**Response format**:
Question: [short summary of the extracted question from Gemini context]
Answer: [Brief, focused response]""",
    request_params=RequestParams(maxTokens=32768)  # High token limit to process full context
)
async def test_agent():
    """
    Enhanced transcript analysis agent function.
    This runs asynchronously and can process both default queries and custom transcript analysis requests.
    The @fast.agent decorator creates an AI agent optimized for transcript analysis.
    """
    # Run the agent with a default test query for basic functionality testing
    # fast.run() creates a context manager that initializes the agent
    async with fast.run() as agent:
        # Send a default test query to verify agent functionality
        # agent.send() is the method to send messages to the agent
        response = await agent.send("Hello, can you tell me what a balloon is and how you can help with transcript analysis?")
        return response

async def analyze_transcript_with_agent(query):
    """
    Enhanced function to analyze transcript content with custom queries.
    
    This function is designed to be called by the Gemini polling script
    to process transcript content and provide intelligent responses.
    
    Args:
        query (str): The transcript content and analysis request to process
        
    Returns:
        str: The agent's analysis and response
    """
    try:
        # Create a new agent instance specifically for transcript analysis
        async with fast.run() as agent:
            # Send the custom transcript analysis query to the agent
            # The agent will process the transcript structure and provide intelligent responses
            response = await agent.send(query)
            return response
    except Exception as e:
        # Error handling for transcript analysis failures
        print(f"Error in transcript analysis: {e}")
        return f"Error analyzing transcript: {e}"

async def main():
    """
    Main function to run the agent asynchronously and demonstrate functionality.
    This function handles the execution flow and error handling for testing purposes.
    """
    try:
        # Execute the basic test agent and get the response
        # await is used because test_agent() is an async function
        result = await test_agent()
        print(f"Agent response: {result}")
        return result
    except Exception as e:
        # Error handling to catch and display any issues
        print(f"Error running agent: {e}")
        return None

if __name__ == "__main__":
    # Run the agent asynchronously and print the result
    # asyncio.run() is the entry point for async code in Python
    asyncio.run(main())