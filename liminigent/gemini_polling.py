#!/usr/bin/env python3
"""
Gemini-Triggered Polling Script

Lean polling script that monitors for "Gemini" triggers and uses gemini-cli
to analyze context and provide intelligent responses via NTFY notifications.

Context Management Strategy:
- Limits context to last 96000 characters to prevent token overflow
- Prioritizes recent transcript entries over older ones
- Includes timestamp information for context understanding
"""

import asyncio
import requests
import time
import json
import os
import re
import pytz
import difflib
import subprocess
from datetime import datetime
from pathlib import Path
import sys

# Remove the poll_agent1 import since we're using gemini-cli now
# sys.path.append(str(Path(__file__).parent.parent))
# from poll_agent1 import analyze_transcript_with_agent

class TranscriptManager:
    """
    Manages daily transcript files with organized folder structure.
    
    Creates and maintains one transcript file per day in a hierarchical
    year/month/date folder structure for easy organization and retrieval.
    (Replicates enhanced_polling.py functionality)
    """
    
    def __init__(self, base_path):
        """Initialize the transcript management system."""
        self.base_path = Path(base_path)
        self.est = pytz.timezone('US/Eastern')
    
    def get_daily_transcript_path(self, date_str=None):
        """Get the file path for a daily transcript."""
        if date_str is None:
            date_str = datetime.now(self.est).strftime('%Y-%m-%d')
        
        # Parse date components
        year, month, day = date_str.split('-')
        
        # Create nested folder structure: logs/YYYY/MM/DD/
        folder_path = self.base_path / year / month / day
        folder_path.mkdir(parents=True, exist_ok=True)
        
        return folder_path / "transcript.txt"
    
    def initialize_daily_transcript(self, date_str=None):
        """Initialize a daily transcript file with header information."""
        transcript_path = self.get_daily_transcript_path(date_str)
        
        if not transcript_path.exists():
            # Create new transcript with header
            with open(transcript_path, 'w') as f:
                f.write(f"# Daily Limitless Transcript - {date_str or 'Today'}\n")
                f.write(f"# Generated: {datetime.now(self.est).strftime('%Y-%m-%d %H:%M:%S %Z')}\n")
                f.write(f"# Gemini triggers will be highlighted in **bold**\n")
                f.write("\n---\n\n")
            
            print(f"Created new daily transcript: {transcript_path}")
    
    def append_to_transcript(self, content, timestamp, title="Limitless Update", date_str=None):
        """Append new content to the daily transcript."""
        transcript_path = self.get_daily_transcript_path(date_str)
        self.initialize_daily_transcript(date_str)
        
        # Format the entry
        entry_time = datetime.now(self.est).strftime('%H:%M:%S')
        entry = f"\n## {title} - {entry_time}\n"
        entry += f"*Content timestamp: {timestamp}*\n\n"
        entry += f"{content}\n\n---\n"
        
        # Append to transcript
        with open(transcript_path, 'a') as f:
            f.write(entry)
    
    def log_difference(self, prev_content, new_content, timestamp, title="Limitless Update", date_str=None):
        """Log the differences between previous and new content."""
        # Generate diff for debugging (not shown in main transcript)
        diff = list(difflib.unified_diff(
            prev_content.splitlines(),
            new_content.splitlines(),
            lineterm="",
            fromfile="previous",
            tofile="updated"
        ))
        
        # Log the update to transcript
        self.append_to_transcript(new_content, timestamp, title, date_str)
        
        # Optionally log detailed diff to a separate debug file
        if diff:
            debug_path = self.get_daily_transcript_path(date_str).parent / "debug_diffs.txt"
            with open(debug_path, 'a') as f:
                f.write(f"\n--- Diff at {datetime.now(self.est).isoformat()} ---\n")
                f.write(f"Title: {title}\n")
                f.write(f"Content timestamp: {timestamp}\n")
                f.write("\n".join(diff))
                f.write("\n\n")

class GeminiPollingEngine:
    """
    Lean polling engine that triggers gemini-cli analysis on Gemini mentions.
    
    Uses the same polling and transcript writing logic as enhanced_polling.py
    but focuses specifically on Gemini trigger detection and gemini-cli integration.
    """
    
    def __init__(self):
        # API Configuration - same as enhanced_polling.py for compatibility
        self.api_key = "9c45d7ac-f7cb-4007-8fde-8e61c8f31886"
        self.api_url = "https://api.limitless.ai/v1/lifelogs"
        self.headers = {"X-API-Key": self.api_key, "Accept": "application/json"}
        
        # NTFY Configuration for agent responses
        self.ntfy_url = "https://ntfy.sh/clark-m-gemini-agent"
        
        # Context management - limit to 96000 chars to prevent token overflow
        self.max_context_chars = 96000
        
        # Polling Configuration (same as enhanced_polling.py)
        self.backoff_initial = 5
        self.backoff_max = 300
        self.stable_polls_required = 3
        
        # Timezone and paths - reuse enhanced_polling.py structure
        self.est = pytz.timezone('US/Eastern')
        self.base_path = Path(__file__).parent / "logs"
        
        # Initialize transcript manager
        self.transcript_manager = TranscriptManager(self.base_path)
        
        # Track Gemini triggers that have already been processed to avoid duplicates
        self.processed_gemini_triggers = set()
        
        # Check if gemini-cli is available
        self.check_gemini_cli_availability()
        
        print("Gemini Polling Engine initialized - monitoring for Gemini triggers")
    
    def check_gemini_cli_availability(self):
        """Check if gemini-cli is available and properly configured."""
        try:
            # Test if gemini-cli is available
            result = subprocess.run(
                ["gemini", "--help"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                print("✅ gemini-cli is available")
            else:
                print("❌ gemini-cli is not working properly")
                print(f"Error: {result.stderr}")
        except FileNotFoundError:
            print("❌ gemini-cli not found. Please install it with: npm i -g @google/gemini-cli")
            print("Or set GEMINI_API_KEY environment variable for headless operation")
        except subprocess.TimeoutExpired:
            print("❌ gemini-cli command timed out")
        except Exception as e:
            print(f"❌ Error checking gemini-cli: {e}")
    
    def today_est_date(self):
        """Get today's date in EST timezone."""
        return datetime.now(self.est).strftime('%Y-%m-%d')
    
    def fetch_lifelogs(self, date=None, start=None):
        """Fetch lifelogs from Limitless API (same as enhanced_polling.py)."""
        params = {
            "timezone": "US/Eastern",
            "includeMarkdown": "true", 
            "includeHeadings": "true",
            "direction": "desc",
            "limit": 1000
        }
        if date: params["date"] = date
        if start: params["start"] = start
        
        response = requests.get(self.api_url, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()
        return list(reversed(data.get("data", {}).get("lifelogs", [])))
    
    def detect_gemini_trigger(self, text):
        """
        Detect 'Gemini' mentions in text (case-insensitive, whole words only).
        
        Returns True if Gemini is mentioned, False otherwise.
        """
        if not text:
            return False
        # Use word boundaries to match only complete words "Gemini"
        return bool(re.search(r'\bgemini\b', text, re.IGNORECASE))
    
    def highlight_gemini_content(self, content):
        """
        Highlight Gemini mentions in content using markdown bold syntax.
        
        Args:
            content (str): Text content to process
            
        Returns:
            str: Content with Gemini mentions highlighted in **bold**
        """
        if not content:
            return content
        
        # Case-insensitive search with word boundaries
        pattern = r'\b(gemini)\b'
        
        def replace_match(match):
            """Replace function to bold the match."""
            return f"**{match.group(1)}**"
        
        # Replace all instances with bold markdown
        return re.sub(pattern, replace_match, content, flags=re.IGNORECASE)
    
    def get_current_transcript_context(self):
        """
        Get the current day's transcript with smart context limiting.
        
        Strategy: Get the most recent transcript content, limited to max_context_chars
        to prevent overwhelming the agent while maintaining relevant context.
        """
        date_str = self.today_est_date()
        year, month, day = date_str.split('-')
        
        # Use same path structure as enhanced_polling.py
        transcript_path = self.base_path / year / month / day / "transcript.txt"
        
        if not transcript_path.exists():
            return f"No transcript found for {date_str}"
        
        try:
            with open(transcript_path, 'r') as f:
                full_content = f.read()
            
            # If content is within limit, return as-is
            if len(full_content) <= self.max_context_chars:
                return full_content
            
            # Otherwise, take the most recent content (end of file) with buffer
            # Use slightly smaller limit to ensure we stay under after line adjustment
            safe_limit = self.max_context_chars - 100  # 100 char safety buffer
            truncated = full_content[-safe_limit:]
            
            # Find the first complete line to avoid cutting mid-sentence
            first_newline = truncated.find('\n')
            if first_newline > 0:
                truncated = truncated[first_newline + 1:]
            
            return f"[CONTEXT TRUNCATED - SHOWING MOST RECENT {len(truncated)} CHARS]\n\n{truncated}"
            
        except Exception as e:
            return f"Error reading transcript: {e}"
    
    async def process_gemini_trigger(self, lifelog, processed_content):
        """
        Process a Gemini trigger by sending context to gemini-cli and getting response.
        
        Args:
            lifelog: The lifelog entry that contained the Gemini trigger
            processed_content: Content with Gemini highlighted
        """
        print("🔍 Gemini trigger detected - gathering context for gemini-cli analysis...")
        
        # Get current transcript context
        context = self.get_current_transcript_context()
        
        # Prepare the gemini-cli query with context and current trigger
        trigger_content = processed_content
        trigger_title = lifelog.get("title", "Limitless Update")
        trigger_time = lifelog.get("endTime", "")
        
        # Construct the query for gemini-cli with brevity instruction
        gemini_query = f"""TRANSCRIPT ANALYSIS REQUEST - RESPOND VERY BRIEFLY (MAX 500 WORDS)

Current Trigger Entry:
Title: {trigger_title}
Time: {trigger_time}
Content: {trigger_content}

Full Context (Today's Transcript):
{context}

Please provide a VERY BRIEF analysis (max 500 words) addressing any questions or requests in the transcript, particularly focusing on the Gemini-related content. Keep responses short and actionable for mobile notifications."""
        
        try:
            print("🤖 Sending context to gemini-cli for analysis...")
            
            # Use gemini-cli with our constructed query
            response = await self.run_gemini_cli_query(gemini_query)
            
            if response:
                print("✅ gemini-cli analysis complete - sending notification...")
                await self.send_agent_response_notification(response, trigger_title)
            else:
                print("❌ No response from gemini-cli")
                
        except Exception as e:
            print(f"❌ Error processing Gemini trigger: {e}")
            await self.send_error_notification(str(e))
    
    async def run_gemini_cli_query(self, query):
        """
        Run gemini-cli with a custom query using subprocess.
        
        This replaces the previous poll agent integration with direct gemini-cli calls.
        """
        try:
            # Run gemini-cli in headless mode with the query
            # gemini-cli automatically detects non-TTY input and runs headless
            result = subprocess.run(
                ["gemini"],
                input=query,
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout for gemini-cli response
            )
            
            if result.returncode == 0:
                # Return the stdout (gemini-cli response)
                return result.stdout.strip()
            else:
                print(f"❌ gemini-cli error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ gemini-cli command timed out")
            return None
        except FileNotFoundError:
            print("❌ gemini-cli not found. Please install with: npm i -g @google/gemini-cli")
            return None
        except Exception as e:
            print(f"❌ Error running gemini-cli: {e}")
            return None
    
    async def send_agent_response_notification(self, response, trigger_title):
        """Send the gemini-cli response as a clean text NTFY notification."""
        # Keep it simple - just send clean text without complex formatting
        # This avoids NTFY attachment issues
        message = f"🤖 Gemini AI Analysis\n\nTrigger: {trigger_title}\n\n{response}\n\n---\nGenerated by Gemini Polling Agent"
        
        headers = {
            "Title": "Gemini AI Agent Response",
            "Priority": "high",
            "Tags": "ai,gemini,agent"
            # Removed Markdown header to avoid attachment issues
        }
        
        try:
            # Ensure message is not too long for NTFY
            if len(message) > 4000:  # NTFY limit safety
                # Truncate response but keep structure
                max_response_len = 4000 - 200  # Leave room for headers/footers
                truncated_response = response[:max_response_len] + "...\n[Response truncated for mobile notification]"
                message = f"🤖 Gemini AI Analysis\n\nTrigger: {trigger_title}\n\n{truncated_response}\n\n---\nGenerated by Gemini Polling Agent"
            
            response_req = requests.post(self.ntfy_url, data=message.encode("utf-8"), headers=headers)
            response_req.raise_for_status()
            print("📱 gemini-cli response notification sent successfully")
        except Exception as e:
            print(f"❌ Failed to send gemini-cli response notification: {e}")
    
    async def send_error_notification(self, error_msg):
        """Send error notification if gemini-cli processing fails."""
        message = f"❌ Gemini Agent Error: {error_msg}"
        headers = {
            "Title": "Gemini Agent Error", 
            "Priority": "high",
            "Tags": "error,gemini"
        }
        
        try:
            requests.post(self.ntfy_url, data=message.encode("utf-8"), headers=headers)
        except Exception as e:
            print(f"Failed to send error notification: {e}")
    
    async def run(self):
        """
        Main polling loop - monitors for Gemini triggers and processes them.
        
        Reuses the same polling logic as enhanced_polling.py but focuses
        specifically on Gemini detection and gemini-cli integration.
        """
        # State tracking (same as enhanced_polling.py)
        last_lifelogs = {}  # lifelog_id -> {content, endTime, stable_count}
        last_stable_end_time = None
        backoff = self.backoff_initial
        
        print("🚀 Starting Gemini polling loop...")
        
        while True:
            try:
                # Fetch current lifelogs for today
                date = self.today_est_date()
                start = last_stable_end_time
                lifelogs = self.fetch_lifelogs(date=date, start=start)
                
                # Track updates
                updated_ids = set()
                most_recent_update = None  # (lifelog, prev_content, processed_content, has_gemini_trigger)
                
                # Process each lifelog (same logic as enhanced_polling.py)
                for lifelog in lifelogs:
                    lifelog_id = lifelog.get("id")
                    raw_content = lifelog.get("markdown") or ""
                    end_time = lifelog.get("endTime")
                    title = lifelog.get("title") or "Limitless Update"
                    prev = last_lifelogs.get(lifelog_id)
                    
                    # Process content for Gemini highlighting
                    processed_content = self.highlight_gemini_content(raw_content)
                    has_gemini_trigger = self.detect_gemini_trigger(raw_content)
                    
                    if not prev:
                        # New lifelog discovered
                        most_recent_update = (lifelog, "", processed_content, has_gemini_trigger)
                        last_lifelogs[lifelog_id] = {
                            "content": raw_content, 
                            "endTime": end_time, 
                            "stable_count": 1
                        }
                    else:
                        if raw_content != prev["content"] or end_time != prev["endTime"]:
                            # Lifelog was updated
                            if (most_recent_update is None or end_time > most_recent_update[0]["endTime"]):
                                most_recent_update = (lifelog, prev["content"], processed_content, has_gemini_trigger)
                            last_lifelogs[lifelog_id] = {
                                "content": raw_content, 
                                "endTime": end_time, 
                                "stable_count": 1
                            }
                        else:
                            # Lifelog unchanged, increment stability counter
                            last_lifelogs[lifelog_id]["stable_count"] += 1
                    
                    updated_ids.add(lifelog_id)
                
                # Clean up tracking for removed lifelogs
                for lifelog_id in list(last_lifelogs.keys()):
                    if lifelog_id not in updated_ids:
                        del last_lifelogs[lifelog_id]
                
                # Process most recent update
                if most_recent_update:
                    lifelog, prev_content, processed_content, has_gemini_trigger = most_recent_update
                    end_time = lifelog.get("endTime")
                    title = lifelog.get("title") or "Limitless Update"
                    lifelog_id = lifelog.get("id")
                    
                    # Create unique trigger identifier for this content
                    trigger_id = f"{lifelog_id}:{end_time}:{has_gemini_trigger}"
                    
                    # Only process Gemini trigger if it's new content with Gemini AND we haven't processed this exact trigger
                    if has_gemini_trigger and trigger_id not in self.processed_gemini_triggers:
                        print(f"🎯 NEW Gemini trigger found in lifelog: {title}")
                        self.processed_gemini_triggers.add(trigger_id)
                        await self.process_gemini_trigger(lifelog, processed_content)
                    
                    # Always log to daily transcript (like enhanced_polling.py)
                    self.transcript_manager.log_difference(
                        prev_content, processed_content, end_time, title, date
                    )
                    
                    print(f"Updated transcript for {date} - Gemini trigger: {'Yes (NEW)' if has_gemini_trigger and trigger_id not in self.processed_gemini_triggers else 'No'}")
                
                # Update stable endTime tracking (same as enhanced_polling.py)
                stable_lifelogs = [
                    (lid, info) for lid, info in last_lifelogs.items()
                    if info["stable_count"] >= self.stable_polls_required
                ]
                if stable_lifelogs:
                    # Find the latest stable endTime
                    latest_stable = max(stable_lifelogs, key=lambda x: x[1]["endTime"])
                    if last_stable_end_time != latest_stable[1]["endTime"]:
                        print(f"Stable up to endTime: {latest_stable[1]['endTime']}")
                    last_stable_end_time = latest_stable[1]["endTime"]
                
                await asyncio.sleep(backoff)
                backoff = self.backoff_initial  # Reset backoff on success
                
            except Exception as e:
                print(f"❌ Polling error: {e}")
                print(f"⏱️  Retrying in {backoff} seconds...")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, self.backoff_max)  # Exponential backoff up to 5 minutes


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test mode - check current transcript context
        engine = GeminiPollingEngine()
        context = engine.get_current_transcript_context()
        print("Current transcript context preview:")
        print("=" * 50)
        print(context[:500] + "..." if len(context) > 500 else context)
        print("=" * 50)
        print(f"Total context length: {len(context)} characters")
    else:
        # Normal operation - start polling
        engine = GeminiPollingEngine()
        asyncio.run(engine.run())