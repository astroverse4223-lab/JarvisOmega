"""Quick test to inspect Ollama API structure."""
import ollama

print("Testing Ollama API...")
print("=" * 60)

# Get models
models = ollama.list()

print(f"\n1. Type of ollama.list() return: {type(models)}")
print(f"2. Value: {models}")
print(f"3. Dir: {dir(models)}")

if hasattr(models, '__dict__'):
    print(f"4. __dict__: {models.__dict__}")

if hasattr(models, 'models'):
    print(f"\n5. Has .models attribute!")
    print(f"   Type: {type(models.models)}")
    print(f"   Value: {models.models}")
    
    if models.models:
        first_model = models.models[0]
        print(f"\n6. First model type: {type(first_model)}")
        print(f"   Dir: {dir(first_model)}")
        if hasattr(first_model, '__dict__'):
            print(f"   __dict__: {first_model.__dict__}")
        
        # Try different access methods
        print(f"\n7. Trying different accessors:")
        print(f"   hasattr 'model': {hasattr(first_model, 'model')}")
        print(f"   hasattr 'name': {hasattr(first_model, 'name')}")
        
        if hasattr(first_model, 'model'):
            print(f"   first_model.model = {first_model.model}")
        if hasattr(first_model, 'name'):
            print(f"   first_model.name = {first_model.name}")

if isinstance(models, dict):
    print(f"\n8. It's a dict with keys: {models.keys()}")
    if 'models' in models:
        print(f"   models['models'] type: {type(models['models'])}")

print("\n" + "=" * 60)
