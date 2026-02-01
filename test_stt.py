"""
Test Script - Speech-to-Text

Quick test to verify STT is working.
"""

import yaml
from core.stt import SpeechRecognizer


def main():
    print("=" * 60)
    print("Testing Speech-to-Text")
    print("=" * 60)
    print()
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    print(f"Mode: {config['stt']['mode']}")
    print(f"Activation: {config['stt']['activation']['mode']}")
    print()
    
    # Initialize STT
    print("Initializing STT...")
    stt = SpeechRecognizer(config['stt'])
    print("✓ STT ready")
    print()
    
    # Test recognition
    print("Press the activation key and speak a test phrase")
    print("Example: 'Hello Jarvis, this is a test'")
    print()
    
    for i in range(3):
        print(f"\n--- Test {i+1}/3 ---")
        text = stt.recognize()
        
        if text:
            print(f"✓ Recognized: {text}")
        else:
            print("✗ No speech detected")
    
    print()
    print("=" * 60)
    print("STT test complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
