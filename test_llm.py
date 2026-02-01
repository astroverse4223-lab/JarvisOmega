"""
Test Script - LLM Integration

Quick test to verify Ollama connection and LLM responses.
"""

import yaml
from core.llm import AIBrain


def main():
    print("=" * 60)
    print("Testing LLM Integration (Ollama)")
    print("=" * 60)
    print()
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    print(f"Model: {config['llm']['model']}")
    print(f"Host: {config['llm']['host']}")
    print()
    
    # Initialize AI Brain
    print("Initializing AI Brain...")
    try:
        brain = AIBrain(config['llm'])
        print("✓ LLM connected")
        print()
    except Exception as e:
        print(f"✗ Failed to connect: {e}")
        print("\nMake sure:")
        print("1. Ollama is installed and running")
        print("2. Model is pulled: ollama pull llama3.2:3b")
        return
    
    # Test intent classification
    print("=" * 60)
    print("Testing Intent Classification")
    print("=" * 60)
    print()
    
    test_inputs = [
        ("open notepad", "command"),
        ("what's the weather like?", "conversation"),
        ("search for python tutorials", "command"),
        ("tell me a joke", "conversation"),
        ("increase the volume", "command")
    ]
    
    for text, expected_type in test_inputs:
        result = brain.classify_intent(text)
        status = "✓" if result['type'] == expected_type else "✗"
        print(f"{status} Input: {text}")
        print(f"   Type: {result['type']} (expected: {expected_type})")
        
        if result['type'] == 'command':
            details = brain.extract_command_details(text)
            print(f"   Intent: {details['intent']}")
            print(f"   Entities: {details['entities']}")
        print()
    
    # Test conversation generation
    print("=" * 60)
    print("Testing Conversation Generation")
    print("=" * 60)
    print()
    
    conversation_tests = [
        "Hello, how are you?",
        "What can you help me with?",
        "Tell me about artificial intelligence"
    ]
    
    for text in conversation_tests:
        print(f"User: {text}")
        response = brain.generate_response(text, [])
        print(f"Jarvis: {response}")
        print()
    
    print("=" * 60)
    print("LLM test complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
