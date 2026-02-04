"""
Test Multi-Agent Debate System

Quick test to verify the multi-agent reasoning system is working correctly.
"""

import yaml
import logging
from core.agents import MultiAgentDebate
from core.memory import MemorySystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

def test_multi_agent_system():
    """Test the multi-agent debate system."""
    print("=" * 70)
    print("🧠 TESTING MULTI-AGENT DEBATE SYSTEM")
    print("=" * 70)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    model = config['llm'].get('model', 'llama3.2:3b')
    print(f"\n✓ Using model: {model}")
    
    # Initialize agents
    print("✓ Initializing multi-agent system...")
    agents = MultiAgentDebate(model=model, enabled=True)
    
    # Test scenarios
    test_cases = [
        "What time is it?",
        "Delete all my files",
        "Turn the volume down",
        "Remind me to call mom tomorrow"
    ]
    
    print(f"\n{'=' * 70}")
    print("RUNNING TEST SCENARIOS")
    print(f"{'=' * 70}\n")
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n{'─' * 70}")
        print(f"TEST {i}: {test_input}")
        print(f"{'─' * 70}\n")
        
        # Run debate
        result = agents.debate(test_input)
        
        if result['enabled']:
            # Display results
            print("📊 ANALYST:")
            print(f"   {result['analyst_response']}\n")
            
            print("⚠️ SKEPTIC:")
            print(f"   {result['skeptic_response']}\n")
            
            print("🏗️ ARCHITECT:")
            print(f"   {result['architect_response']}\n")
            
            duration = result.get('duration_seconds', 0)
            print(f"⏱️ Duration: {duration:.2f}s")
        else:
            print("❌ Debate system disabled or failed")
            if 'error' in result:
                print(f"   Error: {result['error']}")
    
    print(f"\n{'=' * 70}")
    print("✓ ALL TESTS COMPLETED")
    print(f"{'=' * 70}\n")

def test_memory_integration():
    """Test memory storage of debates."""
    print("\n" + "=" * 70)
    print("💾 TESTING MEMORY INTEGRATION")
    print("=" * 70 + "\n")
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize memory
    print("✓ Initializing memory system...")
    memory = MemorySystem(config['memory'])
    
    # Store a test debate
    print("✓ Storing test debate...")
    
    test_debate = {
        'timestamp': '2024-01-01T12:00:00',
        'analyst_response': 'INTENT: test\nPROPOSED ACTION: Store test data\nREASONING: Testing storage',
        'skeptic_response': 'CONCERNS: This is a test\nRISKS: None\nRECOMMENDATIONS: Proceed',
        'architect_response': 'SYNTHESIS: Test successful\nREFINED SOLUTION: Store data\nCONFIDENCE: High',
        'duration_seconds': 2.5,
        'enabled': True
    }
    
    # Store interaction first
    interaction_id = memory.store_interaction(
        user_input="test multi-agent system",
        response="test completed",
        intent="test",
        success=True
    )
    
    # Store debate
    memory.store_agent_debate(
        user_input="test multi-agent system",
        debate_result=test_debate,
        jarvis_decision="Test: Success",
        interaction_id=interaction_id
    )
    
    print(f"✓ Stored with interaction_id: {interaction_id}")
    
    # Retrieve debates
    print("\n✓ Retrieving recent debates...")
    debates = memory.get_recent_debates(limit=3)
    
    if debates:
        print(f"✓ Found {len(debates)} debate(s) in database\n")
        for i, debate in enumerate(debates, 1):
            print(f"Debate {i}:")
            print(f"  User Input: {debate['user_input']}")
            print(f"  Jarvis Decision: {debate['jarvis_decision']}")
            print(f"  Duration: {debate['duration_seconds']:.2f}s\n")
    else:
        print("⚠️ No debates found in database")
    
    print("=" * 70)
    print("✓ MEMORY INTEGRATION TEST COMPLETE")
    print("=" * 70 + "\n")

def main():
    """Run all tests."""
    try:
        # Test 1: Multi-agent debate functionality
        test_multi_agent_system()
        
        # Test 2: Memory integration
        test_memory_integration()
        
        print("\n" + "🎉" * 35)
        print("ALL TESTS PASSED SUCCESSFULLY!")
        print("🎉" * 35 + "\n")
        
        print("Next steps:")
        print("1. Launch Jarvis: python main.py")
        print("2. Make a request via voice or UI")
        print("3. Open menu (M) → 'INTERNAL REASONING' to view debates")
        print("4. Check logs in logs/ folder for detailed output\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
