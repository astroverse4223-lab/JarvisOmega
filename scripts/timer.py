"""
Timer - Countdown timer with Windows notification
"""
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

def show_notification(title, message):
    """Show Windows toast notification"""
    try:
        # Try using PowerShell for notification
        ps_command = f"""
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
        [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
        
        $template = @"
        <toast>
            <visual>
                <binding template="ToastText02">
                    <text id="1">{title}</text>
                    <text id="2">{message}</text>
                </binding>
            </visual>
            <audio src="ms-winsoundevent:Notification.Looping.Alarm" loop="false"/>
        </toast>
"@
        
        $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
        $xml.LoadXml($template)
        $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Jarvis Timer").Show($toast)
        """
        
        subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            check=False
        )
        
        # Also play a beep sound
        subprocess.run(
            ["powershell", "-Command", "[System.Media.SystemSounds]::Beep.Play()"],
            capture_output=True,
            check=False
        )
        
        # Fallback to msg command for visibility
        subprocess.run(
            ["msg", "*", f"{title}: {message}"],
            capture_output=True,
            check=False
        )
    except Exception as e:
        print(f"Notification error: {e}")

def countdown(minutes, message="Timer Complete"):
    """Countdown timer with notification"""
    seconds = minutes * 60
    end_time = datetime.now() + timedelta(seconds=seconds)
    
    print(f"⏰ Timer set for {minutes} minute(s)")
    print(f"Will complete at {end_time.strftime('%I:%M %p')}")
    
    # Run in background using threading
    import threading
    
    def timer_thread():
        try:
            time.sleep(seconds)
            
            # Show notification
            if minutes == 1:
                time_str = "1 minute"
            else:
                time_str = f"{minutes} minutes"
            show_notification(
                "Timer Complete! ⏰",
                f"{time_str} timer finished - {message}"
            )
        except KeyboardInterrupt:
            pass
    
    # Start timer in background thread
    thread = threading.Thread(target=timer_thread, daemon=True)
    thread.start()
    
    return f"Timer started for {minutes} minute(s)"

def main():
    """Parse arguments and start timer"""
    # Check for command line arguments
    if len(sys.argv) > 1:
        try:
            minutes = int(sys.argv[1])
            message = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Timer Complete"
        except ValueError:
            print("Usage: timer.py <minutes> [message]")
            return
    else:
        # Default 5-minute timer
        minutes = 5
        message = "5-minute timer complete"
    
    countdown(minutes, message)

if __name__ == "__main__":
    main()
