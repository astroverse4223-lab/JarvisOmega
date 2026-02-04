"""
Quick test script to verify interrupt key detection works
Run this to test if Ctrl key is being detected properly
"""

import keyboard
import time

print("=" * 50)
print("INTERRUPT KEY DETECTION TEST")
print("=" * 50)
print("\nTesting all possible Ctrl key variations...")
print("Press and HOLD Ctrl (any side) to test")
print("Press ESC to quit")
print("-" * 50)

test_keys = ['ctrl', 'left ctrl', 'right ctrl', 'control', 'left control', 'right control']
check_count = 0

while True:
    # Test ESC to quit
    if keyboard.is_pressed('esc'):
        print("\n✓ ESC pressed - exiting")
        break
    
    # Check all possible Ctrl variations
    detected = []
    for key_name in test_keys:
        try:
            if keyboard.is_pressed(key_name):
                detected.append(key_name)
        except Exception as e:
            pass  # Ignore invalid key names
    
    if detected:
        print(f"✓ DETECTED: {', '.join(detected)}")
        time.sleep(0.3)  # Debounce
    
    # Show we're checking
    check_count += 1
    if check_count % 100 == 0:
        print(f"  ... still checking (cycle {check_count}) ...")
    
    time.sleep(0.05)

print("\nTest complete!")
print("\nIf you saw 'DETECTED' messages when pressing Ctrl,")
print("then keyboard detection is working!")
