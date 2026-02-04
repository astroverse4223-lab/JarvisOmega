"""
Code Viewer - Display generated code in a GUI window
"""
import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox
from pathlib import Path
import requests

def generate_code(description):
    """Generate code using Ollama LLM."""
    try:
        # Prepare the prompt for code generation
        prompt = f"""You are an expert programmer. Write complete, working code based on this description:

{description}

Requirements:
1. Write clean, well-commented code
2. Include comprehensive error handling
3. Add a docstring explaining what the code does
4. Make it production-ready and robust
5. Use modern, reliable libraries
6. ONLY output the code, no explanations or markdown code blocks

Code:"""

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
            elif code.startswith('```javascript'):
                code = code.split('```javascript', 1)[1]
            elif code.startswith('```'):
                code = code.split('```', 1)[1]
            
            if '```' in code:
                code = code.split('```')[0]
            
            return code.strip()
        else:
            return None
            
    except Exception as e:
        return f"Error generating code: {e}"

def save_code_to_file(code, description):
    """Save code to JarvisScripts folder."""
    try:
        # Get desktop path
        onedrive_desktop = Path.home() / "OneDrive" / "Desktop"
        desktop = onedrive_desktop if onedrive_desktop.exists() else Path.home() / "Desktop"
        
        scripts_dir = desktop / "JarvisScripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        filename = description.lower()
        filename = ''.join(c if c.isalnum() or c.isspace() else '' for c in filename)
        filename = '_'.join(filename.split())[:50]
        
        # Detect language from code content
        if 'import' in code.lower() or 'def ' in code or 'class ' in code:
            ext = '.py'
        elif 'function' in code or 'const' in code or 'let' in code or 'var' in code:
            ext = '.js'
        elif '<html' in code.lower() or '<!doctype' in code.lower():
            ext = '.html'
        else:
            ext = '.txt'
        
        filename = f"{filename}{ext}"
        
        # Make unique
        filepath = scripts_dir / filename
        counter = 1
        while filepath.exists():
            name_without_ext = filename.rsplit('.', 1)[0]
            filepath = scripts_dir / f"{name_without_ext}_{counter}{ext}"
            counter += 1
        
        # Save
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        
        return str(filepath)
    except Exception as e:
        return None

class CodeViewerWindow:
    def __init__(self, description):
        self.description = description
        self.code = None
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Jarvis Code Generator")
        self.root.geometry("900x700")
        self.root.configure(bg='#0a0e1a')
        
        # Title
        title = tk.Label(
            self.root,
            text="🤖 GENERATED CODE",
            font=("Consolas", 16, "bold"),
            bg='#0a0e1a',
            fg='#00ffff'
        )
        title.pack(pady=10)
        
        # Description
        desc_label = tk.Label(
            self.root,
            text=f"Request: {description}",
            font=("Consolas", 10),
            bg='#0a0e1a',
            fg='#00d4cc',
            wraplength=850
        )
        desc_label.pack(pady=5)
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="⏳ Generating code... Please wait...",
            font=("Consolas", 10),
            bg='#0a0e1a',
            fg='#ffdd00'
        )
        self.status_label.pack(pady=5)
        
        # Text editor frame
        editor_frame = tk.Frame(self.root, bg='#00d4cc', bd=2)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Code text widget
        self.text_editor = scrolledtext.ScrolledText(
            editor_frame,
            font=("Consolas", 10),
            bg='#1a1f2e',
            fg='#e0e6ed',
            insertbackground='#00ffff',
            selectbackground='#00d4cc',
            bd=0,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#0a0e1a')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Save button
        self.save_btn = tk.Button(
            button_frame,
            text="💾 SAVE TO FILE",
            font=("Consolas", 11, "bold"),
            bg='#00d4cc',
            fg='#000000',
            activebackground='#00ffff',
            relief=tk.FLAT,
            bd=0,
            pady=10,
            command=self.save_code,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Copy button
        self.copy_btn = tk.Button(
            button_frame,
            text="📋 COPY TO CLIPBOARD",
            font=("Consolas", 11, "bold"),
            bg='#00d4cc',
            fg='#000000',
            activebackground='#00ffff',
            relief=tk.FLAT,
            bd=0,
            pady=10,
            command=self.copy_code,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.copy_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Close button
        close_btn = tk.Button(
            button_frame,
            text="✖ CLOSE",
            font=("Consolas", 11),
            bg='#1a1f2e',
            fg='#e0e6ed',
            activebackground='#333333',
            relief=tk.FLAT,
            bd=0,
            pady=10,
            command=self.root.destroy,
            cursor="hand2"
        )
        close_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Start generation in background
        self.root.after(100, self.generate_and_display)
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def generate_and_display(self):
        """Generate code and display it."""
        self.code = generate_code(self.description)
        
        if self.code and not self.code.startswith("Error"):
            self.text_editor.delete('1.0', tk.END)
            self.text_editor.insert('1.0', self.code)
            self.status_label.config(text="✅ Code generated successfully!", fg='#00ff00')
            self.save_btn.config(state=tk.NORMAL)
            self.copy_btn.config(state=tk.NORMAL)
        else:
            error_msg = self.code if self.code else "Failed to generate code"
            self.text_editor.delete('1.0', tk.END)
            self.text_editor.insert('1.0', f"❌ {error_msg}\n\nMake sure Ollama is running.")
            self.status_label.config(text="❌ Generation failed", fg='#ff4444')
    
    def save_code(self):
        """Save code to file."""
        if self.code:
            filepath = save_code_to_file(self.code, self.description)
            if filepath:
                messagebox.showinfo("Saved", f"Code saved to:\n{Path(filepath).name}")
            else:
                messagebox.showerror("Error", "Failed to save code")
    
    def copy_code(self):
        """Copy code to clipboard."""
        if self.code:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.code)
            self.status_label.config(text="✅ Code copied to clipboard!", fg='#00ff00')
            self.root.after(2000, lambda: self.status_label.config(
                text="✅ Code generated successfully!", fg='#00ff00'
            ))
    
    def run(self):
        """Start the GUI."""
        self.root.mainloop()

def main():
    """Show code viewer window."""
    if len(sys.argv) < 2:
        print("Usage: code_viewer.py <description>")
        return
    
    description = ' '.join(sys.argv[1:])
    
    # Just print confirmation for Jarvis
    print("Here is the code you asked for")
    
    # Show GUI window
    viewer = CodeViewerWindow(description)
    viewer.run()

if __name__ == "__main__":
    main()
