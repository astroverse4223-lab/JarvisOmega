"""
Image Generator & Viewer - Generate and display AI images
"""
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
import io
import requests
import json

def generate_image(description, backend='stable-diffusion'):
    """Generate an image using AI backend."""
    try:
        if backend == 'stable-diffusion':
            # Stable Diffusion WebUI API (default: http://127.0.0.1:7860)
            response = requests.post(
                'http://127.0.0.1:7860/sdapi/v1/txt2img',
                json={
                    'prompt': description,
                    'negative_prompt': 'blurry, low quality, distorted, deformed',
                    'steps': 30,
                    'width': 512,
                    'height': 512,
                    'cfg_scale': 7,
                    'sampler_name': 'Euler a'
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                # Get base64 image data
                import base64
                image_data = base64.b64decode(result['images'][0])
                return image_data, None
            else:
                return None, f"API Error: {response.status_code}"
        
        elif backend == 'dalle':
            # OpenAI DALL-E API (requires API key in environment or config)
            api_key = get_api_key('openai')
            if not api_key:
                return None, "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
            
            response = requests.post(
                'https://api.openai.com/v1/images/generations',
                headers={'Authorization': f'Bearer {api_key}'},
                json={
                    'prompt': description,
                    'n': 1,
                    'size': '512x512'
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                image_response = requests.get(image_url)
                return image_response.content, None
            else:
                return None, f"DALL-E Error: {response.status_code}"
        
        else:
            return None, f"Unknown backend: {backend}"
            
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to image generation API. Make sure it's running."
    except requests.exceptions.Timeout:
        return None, "Request timed out. Image generation took too long."
    except Exception as e:
        return None, f"Error: {str(e)}"

def get_api_key(service):
    """Get API key from environment or config."""
    import os
    
    if service == 'openai':
        return os.environ.get('OPENAI_API_KEY')
    
    return None

def save_image(image_data, description):
    """Save image to JarvisImages folder."""
    try:
        # Get desktop path
        onedrive_desktop = Path.home() / "OneDrive" / "Desktop"
        desktop = onedrive_desktop if onedrive_desktop.exists() else Path.home() / "Desktop"
        
        images_dir = desktop / "JarvisImages"
        images_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        filename = description.lower()
        filename = ''.join(c if c.isalnum() or c.isspace() else '' for c in filename)
        filename = '_'.join(filename.split())[:50]
        filename = f"{filename}.png"
        
        # Make unique
        filepath = images_dir / filename
        counter = 1
        while filepath.exists():
            name_without_ext = filename.rsplit('.', 1)[0]
            filepath = images_dir / f"{name_without_ext}_{counter}.png"
            counter += 1
        
        # Save
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        return str(filepath)
    except Exception as e:
        return None

class ImageViewerWindow:
    def __init__(self, description, backend='stable-diffusion'):
        self.description = description
        self.backend = backend
        self.image_data = None
        self.pil_image = None
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Jarvis Image Generator")
        self.root.geometry("800x900")
        self.root.configure(bg='#0a0e1a')
        
        # Title
        title = tk.Label(
            self.root,
            text="🎨 GENERATED IMAGE",
            font=("Consolas", 16, "bold"),
            bg='#0a0e1a',
            fg='#00ffff'
        )
        title.pack(pady=10)
        
        # Description
        desc_label = tk.Label(
            self.root,
            text=f"Prompt: {description}",
            font=("Consolas", 10),
            bg='#0a0e1a',
            fg='#00d4cc',
            wraplength=750
        )
        desc_label.pack(pady=5)
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="⏳ Generating image... This may take 30-60 seconds...",
            font=("Consolas", 10),
            bg='#0a0e1a',
            fg='#ffdd00'
        )
        self.status_label.pack(pady=5)
        
        # Image display frame
        image_frame = tk.Frame(self.root, bg='#00d4cc', bd=2)
        image_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas for image
        self.canvas = tk.Canvas(
            image_frame,
            bg='#1a1f2e',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Placeholder text
        self.placeholder = self.canvas.create_text(
            400, 300,
            text="⏳ Generating...",
            font=("Consolas", 14),
            fill='#00ffff'
        )
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#0a0e1a')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Save button
        self.save_btn = tk.Button(
            button_frame,
            text="💾 SAVE IMAGE",
            font=("Consolas", 11, "bold"),
            bg='#00d4cc',
            fg='#000000',
            activebackground='#00ffff',
            relief=tk.FLAT,
            bd=0,
            pady=10,
            command=self.save_image,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Regenerate button
        self.regen_btn = tk.Button(
            button_frame,
            text="🔄 REGENERATE",
            font=("Consolas", 11, "bold"),
            bg='#00d4cc',
            fg='#000000',
            activebackground='#00ffff',
            relief=tk.FLAT,
            bd=0,
            pady=10,
            command=self.regenerate_image,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.regen_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
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
        
        # Backend info
        backend_label = tk.Label(
            self.root,
            text=f"Backend: {backend.upper()}",
            font=("Consolas", 8),
            bg='#0a0e1a',
            fg='#00aaaa'
        )
        backend_label.pack(pady=(0, 5))
        
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
        """Generate image and display it."""
        self.image_data, error = generate_image(self.description, self.backend)
        
        if self.image_data:
            try:
                # Load image from bytes
                self.pil_image = Image.open(io.BytesIO(self.image_data))
                
                # Resize to fit canvas while maintaining aspect ratio
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                
                if canvas_width < 100 or canvas_height < 100:
                    canvas_width, canvas_height = 760, 500
                
                img_width, img_height = self.pil_image.size
                ratio = min(canvas_width / img_width, canvas_height / img_height)
                new_width = int(img_width * ratio * 0.9)
                new_height = int(img_height * ratio * 0.9)
                
                resized_image = self.pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                self.photo = ImageTk.PhotoImage(resized_image)
                
                # Display on canvas
                self.canvas.delete('all')
                self.canvas.create_image(
                    canvas_width // 2, canvas_height // 2,
                    image=self.photo,
                    anchor=tk.CENTER
                )
                
                self.status_label.config(text="✅ Image generated successfully!", fg='#00ff00')
                self.save_btn.config(state=tk.NORMAL)
                self.regen_btn.config(state=tk.NORMAL)
            except Exception as e:
                self.show_error(f"Failed to display image: {str(e)}")
        else:
            self.show_error(error or "Unknown error occurred")
    
    def show_error(self, error_msg):
        """Show error message."""
        self.canvas.delete('all')
        
        # Word wrap error message
        words = error_msg.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > 60:
                lines.append(' '.join(current_line[:-1]))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        y_pos = 200
        for line in lines:
            self.canvas.create_text(
                400, y_pos,
                text=line,
                font=("Consolas", 10),
                fill='#ff4444',
                width=700
            )
            y_pos += 25
        
        # Add help text
        self.canvas.create_text(
            400, y_pos + 30,
            text="Troubleshooting:",
            font=("Consolas", 10, "bold"),
            fill='#00ffff'
        )
        
        help_lines = [
            "• Stable Diffusion: Install Automatic1111 WebUI",
            "• Start with: python launch.py --api",
            "• Default URL: http://127.0.0.1:7860",
            "• Or use --backend dalle with OpenAI API key"
        ]
        
        y_pos += 60
        for help_line in help_lines:
            self.canvas.create_text(
                400, y_pos,
                text=help_line,
                font=("Consolas", 9),
                fill='#00d4cc'
            )
            y_pos += 20
        
        self.status_label.config(text="❌ Generation failed", fg='#ff4444')
    
    def save_image(self):
        """Save image to file."""
        if self.image_data:
            filepath = save_image(self.image_data, self.description)
            if filepath:
                messagebox.showinfo("Saved", f"Image saved to:\n{Path(filepath).name}")
            else:
                messagebox.showerror("Error", "Failed to save image")
    
    def regenerate_image(self):
        """Regenerate the image."""
        self.status_label.config(text="⏳ Regenerating image...", fg='#ffdd00')
        self.save_btn.config(state=tk.DISABLED)
        self.regen_btn.config(state=tk.DISABLED)
        self.canvas.delete('all')
        self.placeholder = self.canvas.create_text(
            400, 300,
            text="⏳ Regenerating...",
            font=("Consolas", 14),
            fill='#00ffff'
        )
        self.root.after(100, self.generate_and_display)
    
    def run(self):
        """Start the GUI."""
        self.root.mainloop()

def main():
    """Show image viewer window."""
    if len(sys.argv) < 2:
        print("Usage: image_generator.py <description> [--backend stable-diffusion|dalle]")
        return
    
    # Parse arguments
    args = sys.argv[1:]
    backend = 'stable-diffusion'
    
    # Check for backend flag
    if '--backend' in args:
        idx = args.index('--backend')
        if idx + 1 < len(args):
            backend = args[idx + 1]
            args = args[:idx] + args[idx+2:]
    
    description = ' '.join(args)
    
    # Just print confirmation for Jarvis
    print("Here is the image you asked for")
    
    # Show GUI window
    viewer = ImageViewerWindow(description, backend)
    viewer.run()

if __name__ == "__main__":
    main()
