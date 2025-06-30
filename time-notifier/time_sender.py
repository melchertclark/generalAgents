#!/usr/bin/env python3
"""
Time Notifier Script

Sends the current time to an ntfy endpoint every 30 seconds.
"""

import requests
import time
from datetime import datetime
import sys
import signal

# Configuration
NTFY_ENDPOINT = "https://ntfy.sh/clark-m-random"  # Using the random topic from the screenshot
INTERVAL_SECONDS = 30

def send_time_notification():
    """Send current time to ntfy endpoint."""
    try:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Current time: {current_time}"
        
        response = requests.post(
            NTFY_ENDPOINT,
            data=message,
            headers={
                "Title": "Time Update",
                "Priority": "default",
                "Tags": "clock,time"
            }
        )
        
        if response.status_code == 200:
            print(f"✓ Sent: {message}")
        else:
            print(f"✗ Failed to send notification. Status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Network error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print("\n\nStopping time notifier...")
    sys.exit(0)

def main():
    """Main loop to send time notifications every 30 seconds."""
    print(f"Starting time notifier...")
    print(f"Sending to: {NTFY_ENDPOINT}")
    print(f"Interval: {INTERVAL_SECONDS} seconds")
    print("Press Ctrl+C to stop\n")
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        while True:
            send_time_notification()
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n\nStopping time notifier...")
        sys.exit(0)

if __name__ == "__main__":
    main()