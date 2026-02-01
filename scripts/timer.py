"""
Timer - Countdown timer with notification
"""
import time
from datetime import datetime, timedelta

def countdown(minutes):
    """Countdown timer"""
    seconds = minutes * 60
    end_time = datetime.now() + timedelta(seconds=seconds)
    
    print(f"Timer started for {minutes} minute(s)")
    print(f"Will complete at {end_time.strftime('%I:%M %p')}")
    
    try:
        time.sleep(seconds)
        print(f"\nTimer complete! {minutes} minute(s) elapsed")
    except KeyboardInterrupt:
        print("\nTimer cancelled")

def main():
    """Set a default 5-minute timer"""
    default_minutes = 5
    
    print(f"Starting {default_minutes}-minute timer")
    countdown(default_minutes)

if __name__ == "__main__":
    main()
