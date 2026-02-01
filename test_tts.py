"""
Test Script - Text-to-Speech

Quick test to verify TTS is working.
"""

import yaml
from core.tts import VoiceSynthesizer


def main():
    print("=" * 60)
    print("Testing Text-to-Speech")
    print("=" * 60)
    print()
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize TTS
    print("Initializing TTS engine...")
    tts = VoiceSynthesizer(config['tts'])
    
    # List available voices
    print("\nAvailable voices:")
    voices = tts.list_voices()
    for voice in voices:
        print(f"  [{voice['index']}] {voice['name']}")
    
    print()
    
    # Test speech
    test_phrases = [
        "Jarvis Mark 3 systems online.",
        "How may I assist you today, sir?",
        "All systems operational."
    ]
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"Speaking test phrase {i}: {phrase}")
        tts.speak(phrase)
        print("✓ Complete")
        print()
    
    print("=" * 60)
    print("TTS test complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
