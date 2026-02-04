"""
Script Generator - Use Jarvis LLM to write Python scripts
"""
import sys
import os
from pathlib import Path
import json

def generate_script(description):
    """Generate a Python script based on description using Ollama LLM."""
    try:
        import requests
        
        # Prepare the prompt for code generation
        prompt = f"""You are an expert Python programmer. Write a complete, working Python script based on this description:

{description}

Requirements:
1. Write clean, well-commented Python code
2. Include comprehensive error handling with try-except blocks
3. Add a docstring explaining what the script does
4. Make it executable with proper if __name__ == "__main__" block
5. Follow PEP 8 style guidelines
6. Use modern, reliable libraries (e.g., for YouTube downloads use yt-dlp instead of pytube)
7. Add user-friendly error messages
8. Include input validation
9. ONLY output the Python code, no explanations or markdown code blocks
10. Make the code production-ready and robust

Python script:"""

        # Call Ollama API
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama3.2:3b',
                'prompt': prompt,
                'stream': False,
                'options': {
                    'temperature': 0.7,
                    'top_p': 0.9
                }
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            code = result.get('response', '').strip()
            
            # Clean up code - remove markdown code blocks if present
            if code.startswith('```python'):
                code = code.split('```python', 1)[1]
            if code.startswith('```'):
                code = code.split('```', 1)[1]
            if '```' in code:
                code = code.split('```')[0]
            
            code = code.strip()
            
            return code
        else:
            return None
            
    except Exception as e:
        print(f"Error generating script: {e}")
        return None

def get_desktop_path():
    """Get the correct desktop path for the current user."""
    # Try OneDrive Desktop first (most common on Windows 10/11)
    onedrive_desktop = Path.home() / "OneDrive" / "Desktop"
    if onedrive_desktop.exists():
        return onedrive_desktop
    
    # Standard Windows Desktop
    standard_desktop = Path.home() / "Desktop"
    if standard_desktop.exists():
        return standard_desktop
    
    # Fallback
    return Path.home() / "Desktop"

def save_script(code, description):
    """Save the generated script to a file."""
    try:
        # Create scripts folder if it doesn't exist
        desktop = get_desktop_path()
        scripts_dir = desktop / "JarvisScripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename from description
        filename = description.lower()
        # Remove special characters
        filename = ''.join(c if c.isalnum() or c.isspace() else '' for c in filename)
        # Replace spaces with underscores
        filename = '_'.join(filename.split())
        # Limit length
        filename = filename[:50]
        filename = f"{filename}.py"
        
        # Make sure filename is unique
        filepath = scripts_dir / filename
        counter = 1
        while filepath.exists():
            name_without_ext = filename.rsplit('.', 1)[0]
            filepath = scripts_dir / f"{name_without_ext}_{counter}.py"
            counter += 1
        
        # Save the script
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        
        return str(filepath)
        
    except Exception as e:
        print(f"Error saving script: {e}")
        return None

def main():
    """Generate and save a Python script based on user description."""
    if len(sys.argv) < 2:
        print("Usage: script_generator.py <description>")
        print("Example: script_generator.py 'a script that renames files in a folder'")
        return
    
    # Get description from command line arguments
    description = ' '.join(sys.argv[1:])
    
    # Clean up description - remove common filler words
    description = description.strip()
    if not description:
        print("Please provide a description of the script you want")
        return
    
    print(f"Generating script: {description[:50]}...")
    
    # Generate the script
    code = generate_script(description)
    
    if not code:
        print("Failed to generate script. Make sure Ollama is running.")
        return
    
    # Save the script
    filepath = save_script(code, description)
    
    if filepath:
        filename = Path(filepath).name
        print(f"Script saved: {filename}")
    else:
        print("Failed to save script")

if __name__ == "__main__":
    main()
