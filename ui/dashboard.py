"""
Jarvis Dashboard UI - Holographic Circular Interface

Borderless circular widget with concentric animated rings and teal holographic aesthetic
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import logging
from typing import TYPE_CHECKING
import math
import time
import sys
import os


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

if TYPE_CHECKING:
    from core.jarvis import Jarvis


class SplashScreen:
    """Animated splash screen shown during Jarvis initialization."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S. Omega")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        # Transparency
        try:
            self.root.attributes('-transparentcolor', '#000001')
        except:
            pass
        
        # Window size
        self.width = 700
        self.height = 700
        
        # Center on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        # Modern dark colors with vibrant accents
        self.bg_color = '#000001'
        self.primary_color = '#00d4ff'  # Bright cyan
        self.secondary_color = '#0099ff'  # Blue
        self.accent_color = '#00ffcc'  # Teal
        self.glow_color = '#6600ff'  # Purple
        
        self.root.configure(bg=self.bg_color)
        
        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Animation state
        self.frame = 0
        self.max_frames = 90  # 3 seconds at 30fps
        self.alpha = 0
        
        # Particle system for splash
        import random
        self.particles = []
        for _ in range(40):
            self.particles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'size': random.randint(1, 3)
            })
        
        # Start animation
        self._animate()
        
    def _animate(self):
        """Animate the splash screen."""
        self.canvas.delete("all")
        
        cx = self.width // 2
        cy = self.height // 2
        
        # Calculate animation progress (0 to 1)
        progress = self.frame / self.max_frames
        
        # Fade in effect
        if self.frame < 20:
            self.alpha = self.frame / 20
        elif self.frame > 70:
            self.alpha = (self.max_frames - self.frame) / 20
        else:
            self.alpha = 1.0
        
        # === PARTICLES BACKGROUND ===
        import random
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Wrap around
            if particle['x'] < 0: particle['x'] = self.width
            elif particle['x'] > self.width: particle['x'] = 0
            if particle['y'] < 0: particle['y'] = self.height
            elif particle['y'] > self.height: particle['y'] = 0
            
            # Draw particle
            x, y = int(particle['x']), int(particle['y'])
            size = particle['size']
            self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill=self.accent_color, outline=''
            )
        
        # === HEXAGONAL GRID PATTERN ===
        if self.frame > 10:
            hex_alpha = min(0.3, (self.frame - 10) / 30)
            hex_size = 30
            for row in range(-2, int(self.height / hex_size) + 2):
                for col in range(-2, int(self.width / hex_size) + 2):
                    x = col * hex_size * 1.5
                    y = row * hex_size * math.sqrt(3)
                    if col % 2:
                        y += hex_size * math.sqrt(3) / 2
                    
                    # Only draw hexagons near edges
                    dist_from_center = math.sqrt((x - cx)**2 + (y - cy)**2)
                    if dist_from_center > 180 and dist_from_center < 350:
                        # Draw hexagon
                        points = []
                        for i in range(6):
                            angle = math.radians(60 * i)
                            px = x + hex_size * 0.3 * math.cos(angle)
                            py = y + hex_size * 0.3 * math.sin(angle)
                            points.extend([px, py])
                        if len(points) > 0:
                            self.canvas.create_polygon(
                                points, outline=self.secondary_color, 
                                fill='', width=1
                            )
        
        # === MULTIPLE ROTATING RINGS ===
        for ring_idx in range(4):
            ring_radius = 100 + (ring_idx * 40)
            num_segments = 24 - (ring_idx * 4)
            rotation_speed = 2 + (ring_idx * 0.5)
            
            for i in range(num_segments):
                angle = (360 / num_segments) * i + (self.frame * rotation_speed * (1 if ring_idx % 2 == 0 else -1))
                angle_rad = math.radians(angle)
                
                # Segment length varies
                segment_length = 20 + (ring_idx * 3)
                
                x1 = cx + ring_radius * math.cos(angle_rad)
                y1 = cy + ring_radius * math.sin(angle_rad)
                x2 = cx + (ring_radius - segment_length) * math.cos(angle_rad)
                y2 = cy + (ring_radius - segment_length) * math.sin(angle_rad)
                
                # Color varies by ring
                if ring_idx == 0:
                    color = self.primary_color
                    width = 3
                elif ring_idx == 1:
                    color = self.accent_color
                    width = 2
                elif ring_idx == 2:
                    color = self.glow_color
                    width = 2
                else:
                    color = self.secondary_color
                    width = 1
                
                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=color, width=width
                )
        
        # === PULSING CENTER CORE ===
        pulse = math.sin(self.frame * 0.2) * 15 + 60
        
        # Outer glow rings
        for i in range(5):
            glow_r = pulse + (i * 8)
            glow_alpha = 1 - (i * 0.2)
            if glow_alpha > 0:
                color = self.primary_color if i % 2 == 0 else self.accent_color
                self.canvas.create_oval(
                    cx - glow_r, cy - glow_r,
                    cx + glow_r, cy + glow_r,
                    outline=color, width=2
                )
        
        # Core circle
        self.canvas.create_oval(
            cx - pulse, cy - pulse,
            cx + pulse, cy + pulse,
            outline=self.primary_color, width=4
        )
        
        # === SCAN LINES ===
        scan_y = (self.frame * 8) % self.height
        for offset in range(-3, 4):
            y = scan_y + offset * 3
            if 0 <= y < self.height:
                alpha = 1 - abs(offset) * 0.2
                color = self.accent_color if abs(offset) < 2 else self.secondary_color
                self.canvas.create_line(
                    0, y, self.width, y,
                    fill=color, width=1
                )
        
        # === HOLOGRAPHIC TEXT ===
        # "JARVIS" - main title with glitch effect
        if self.frame > 15:
            text_alpha = min(1.0, (self.frame - 15) / 20)
            
            # Glitch offset effect
            glitch_x = random.randint(-2, 2) if self.frame % 10 == 0 else 0
            glitch_y = random.randint(-1, 1) if self.frame % 10 == 0 else 0
            
            # Shadow/glow layers
            for i in range(3):
                self.canvas.create_text(
                    cx + i - 1, cy - 5 + i - 1,
                    text="J.A.R.V.I.S.",
                    font=('Consolas', 52, 'bold'),
                    fill=self.glow_color
                )
            
            # Main text
            self.canvas.create_text(
                cx + glitch_x, cy - 5 + glitch_y,
                text="J.A.R.V.I.S.",
                font=('Consolas', 52, 'bold'),
                fill=self.primary_color
            )
        
        # "OMEGA" with tech style
        if self.frame > 25:
            self.canvas.create_text(
                cx, cy + 55,
                text="[ OMEGA EDITION ]",
                font=('Consolas', 14, 'bold'),
                fill=self.accent_color
            )
        
        # "INITIALIZING..." with animated underscores
        if self.frame > 35:
            loading_chars = ['|', '/', '-', '\\']
            loading_char = loading_chars[(self.frame // 5) % 4]
            dots = '.' * ((self.frame // 10) % 4)
            
            self.canvas.create_text(
                cx, cy + 140,
                text=f"{loading_char} INITIALIZING{dots}",
                font=('Consolas', 13, 'bold'),
                fill=self.primary_color
            )
            
            # System status
            status_lines = [
                "NEURAL CORE",
                "VOICE MATRIX", 
                "SKILL ENGINE",
                "AI PROCESSOR"
            ]
            line_idx = min(3, self.frame // 15)
            for i in range(line_idx + 1):
                status_y = cy + 165 + (i * 18)
                self.canvas.create_text(
                    cx - 100, status_y,
                    text=f"[{'✓' if i < line_idx else '»'}] {status_lines[i]}",
                    font=('Consolas', 9),
                    fill=self.accent_color if i < line_idx else self.secondary_color,
                    anchor='w'
                )
        
        # === FUTURISTIC PROGRESS BAR ===
        if self.frame > 40:
            bar_width = 350
            bar_height = 6
            bar_progress = min(1.0, (self.frame - 40) / 40)
            
            # Background bar with segments
            segments = 20
            for i in range(segments):
                seg_x = cx - bar_width//2 + (i * bar_width // segments)
                seg_width = (bar_width // segments) - 2
                
                self.canvas.create_rectangle(
                    seg_x, cy + 250,
                    seg_x + seg_width, cy + 250 + bar_height,
                    outline=self.secondary_color, fill='', width=1
                )
                
                # Fill completed segments
                if i < int(bar_progress * segments):
                    self.canvas.create_rectangle(
                        seg_x + 1, cy + 250 + 1,
                        seg_x + seg_width - 1, cy + 250 + bar_height - 1,
                        fill=self.primary_color, outline=''
                    )
            
            # Progress percentage
            percentage = int(bar_progress * 100)
            self.canvas.create_text(
                cx, cy + 275,
                text=f"{percentage}%",
                font=('Consolas', 11, 'bold'),
                fill=self.primary_color
            )
        
        # === CORNER HUD ELEMENTS ===
        corner_size = 50
        corner_offset = 40
        
        # Top-left corner
        self.canvas.create_line(
            corner_offset, corner_offset,
            corner_offset + corner_size, corner_offset,
            fill=self.primary_color, width=3
        )
        self.canvas.create_line(
            corner_offset, corner_offset,
            corner_offset, corner_offset + corner_size,
            fill=self.primary_color, width=3
        )
        # Corner detail
        self.canvas.create_line(
            corner_offset + 10, corner_offset + 10,
            corner_offset + 20, corner_offset + 10,
            fill=self.accent_color, width=2
        )
        
        # Top-right corner
        self.canvas.create_line(
            self.width - corner_offset, corner_offset,
            self.width - corner_offset - corner_size, corner_offset,
            fill=self.primary_color, width=3
        )
        self.canvas.create_line(
            self.width - corner_offset, corner_offset,
            self.width - corner_offset, corner_offset + corner_size,
            fill=self.primary_color, width=3
        )
        self.canvas.create_line(
            self.width - corner_offset - 20, corner_offset + 10,
            self.width - corner_offset - 10, corner_offset + 10,
            fill=self.accent_color, width=2
        )
        
        # Bottom-left corner
        self.canvas.create_line(
            corner_offset, self.height - corner_offset,
            corner_offset + corner_size, self.height - corner_offset,
            fill=self.primary_color, width=3
        )
        self.canvas.create_line(
            corner_offset, self.height - corner_offset,
            corner_offset, self.height - corner_offset - corner_size,
            fill=self.primary_color, width=3
        )
        self.canvas.create_line(
            corner_offset + 10, self.height - corner_offset - 10,
            corner_offset + 20, self.height - corner_offset - 10,
            fill=self.accent_color, width=2
        )
        
        # Bottom-right corner
        self.canvas.create_line(
            self.width - corner_offset, self.height - corner_offset,
            self.width - corner_offset - corner_size, self.height - corner_offset,
            fill=self.primary_color, width=3
        )
        self.canvas.create_line(
            self.width - corner_offset, self.height - corner_offset,
            self.width - corner_offset, self.height - corner_offset - corner_size,
            fill=self.primary_color, width=3
        )
        self.canvas.create_line(
            self.width - corner_offset - 20, self.height - corner_offset - 10,
            self.width - corner_offset - 10, self.height - corner_offset - 10,
            fill=self.accent_color, width=2
        )
        
        # === VERSION TAG ===
        if self.frame > 30:
            self.canvas.create_text(
                self.width - 50, self.height - 15,
                text="v2.0",
                font=('Consolas', 8),
                fill=self.secondary_color,
                anchor='e'
            )
        
        # Continue animation
        self.frame += 1
        if self.frame < self.max_frames:
            self.root.after(33, self._animate)  # ~30fps
        else:
            self.root.after(500, self.close)  # Wait a bit then close
    
    def close(self):
        """Close the splash screen."""
        try:
            self.root.destroy()
        except:
            pass


class Dashboard:
    """
    Holographic circular interface for Jarvis - inspired by futuristic sci-fi design.
    
    Features:
    - Borderless transparent window (500x500 circular)
    - Concentric animated rings with teal/cyan glow
    - Central "JARVIS" branding
    - Hexagonal detail patterns
    - Rotating animated segments
    - Right-click menu for controls
    - Draggable interface
    """
    
    def __init__(self, config: dict, jarvis: 'Jarvis'):
        """
        Initialize dashboard.
        
        Args:
            config: UI configuration
            jarvis: Jarvis instance
        """
        self.config = config['ui']
        self.jarvis = jarvis
        self.logger = logging.getLogger("jarvis.ui")
        
        # Create borderless transparent window
        self.root = tk.Tk()
        self.root.title("J.A.R.V.I.S.")
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Always on top
        
        # Restore transparency
        try:
            self.root.attributes('-transparentcolor', '#000001')
        except:
            pass
        
        # Window size (circular holographic design)
        self.width = 500
        self.height = 500
        self.root.geometry(f"{self.width}x{self.height}")
        
        # Center on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        # Theme system
        self.current_theme = "holographic_teal"  # Default theme
        self.themes = {
            "holographic_teal": "Holographic Teal",
            "arc_reactor": "Arc Reactor",
            "iron_man": "Iron Man",
            "ultron": "Ultron",
            "matrix": "Matrix",
            "cyberpunk": "Cyberpunk",
            "stealth": "Stealth",
            "emerald": "Emerald",
            "gold": "Gold Rush"
        }
        
        # Theme voice command aliases
        self.theme_aliases = {
            "teal": "holographic_teal",
            "holographic": "holographic_teal",
            "arc": "arc_reactor",
            "reactor": "arc_reactor",
            "iron": "iron_man",
            "ultron": "ultron",
            "matrix": "matrix",
            "cyber": "cyberpunk",
            "punk": "cyberpunk",
            "stealth": "stealth",
            "emerald": "emerald",
            "green": "emerald",
            "gold": "gold",
            "yellow": "gold"
        }
        
        # Apply theme
        self._apply_theme()
        
        # Build UI
        self._build_ui()
        
        # State
        self.current_state = "idle"
        self.pulse_alpha = 0
        self.bar_width = 0
        
        # Audio visualization
        self.audio_level = 0  # 0.0 to 1.0
        self.audio_bars = [0] * 12  # 12 bars for equalizer
        
        # Particle effects
        self.particles = []
        self.max_particles = 50
        self._init_particles()
        
        # Holographic scan lines
        self.scan_line_y = 0
        self.scan_direction = 1
        
        # Floating data elements
        self.floating_elements = []
        self._init_floating_elements()
        
        # Quick actions
        self.favorite_commands = [
            "open browser",
            "what time is it",
            "system information",
            "close all windows"
        ]
        self.show_quick_actions = False
        self.quick_action_regions = []  # Store button click regions for detection
        
        # Settings
        self.settings_window = None
        
        # Menu state
        self.menu_open = False
        
        # Open mic mode
        self.open_mic_mode = False
        self.listening_thread = None
        self.stop_listening = False
        
        # Shutdown flag
        self.is_shutting_down = False
        
        # Dragging
        self.drag_x = 0
        self.drag_y = 0
        
        # Draw initial HUD
        self._draw_hud()
        
        # Start animations after a short delay
        self.root.after(100, self._animate)
        
        # Auto-enable open mic mode on startup
        self.root.after(500, self._enable_open_mic)
        
        self.logger.info("Modern Dashboard initialized - Open Mic Mode")
    
    def _apply_theme(self):
        """Apply HUD theme colors based on current theme."""
        # Transparent background
        self.bg_color = '#000001'
        
        if self.current_theme == "holographic_teal":
            # Dark Teal/Cyan Holographic (matching the image)
            self.primary_glow = '#00d4cc'
            self.secondary_glow = '#008b88'
            self.tertiary_glow = '#00ffee'
            self.accent_orange = '#00ccbb'
            self.accent_gold = '#44ddcc'
            self.accent_bright = '#00ffff'
            self.dark_overlay = '#001414'
            self.darker_overlay = '#000a0a'
            self.text_color = '#00d4cc'
            self.text_secondary = '#008b88'
            self.text_dim = '#005555'
            
        elif self.current_theme == "iron_man":
            # Red/Orange Iron Man
            self.primary_glow = '#ff3333'
            self.secondary_glow = '#cc2200'
            self.tertiary_glow = '#ff6633'
            self.accent_orange = '#ff8800'
            self.accent_gold = '#ffaa44'
            self.accent_bright = '#ff4444'
            self.dark_overlay = '#330000'
            self.darker_overlay = '#1a0000'
            self.text_color = '#ff6633'
            self.text_secondary = '#cc4422'
            self.text_dim = '#aa3311'
            
        elif self.current_theme == "arc_reactor":
            # Blue/Cyan Arc Reactor
            self.primary_glow = '#00d9ff'
            self.secondary_glow = '#0088cc'
            self.tertiary_glow = '#00bbff'
            self.accent_orange = '#00ffff'
            self.accent_gold = '#66ddff'
            self.accent_bright = '#33ccff'
            self.dark_overlay = '#001a33'
            self.darker_overlay = '#000d1a'
            self.text_color = '#00bbff'
            self.text_secondary = '#0088cc'
            self.text_dim = '#005577'
            
        elif self.current_theme == "ultron":
            # Purple/Red Ultron
            self.primary_glow = '#cc00ff'
            self.secondary_glow = '#8800aa'
            self.tertiary_glow = '#dd00ff'
            self.accent_orange = '#ff0088'
            self.accent_gold = '#ff00cc'
            self.accent_bright = '#ee00ff'
            self.dark_overlay = '#1a0033'
            self.darker_overlay = '#0d001a'
            self.text_color = '#dd00ff'
            self.text_secondary = '#aa00cc'
            self.text_dim = '#770099'
            
        elif self.current_theme == "matrix":
            # Green Matrix
            self.primary_glow = '#00ff00'
            self.secondary_glow = '#00cc00'
            self.tertiary_glow = '#00ff33'
            self.accent_orange = '#33ff00'
            self.accent_gold = '#66ff33'
            self.accent_bright = '#00ff66'
            self.dark_overlay = '#001a00'
            self.darker_overlay = '#000d00'
            self.text_color = '#00ff33'
            self.text_secondary = '#00cc22'
            self.text_dim = '#007700'
            
        elif self.current_theme == "cyberpunk":
            # Pink/Purple Cyberpunk
            self.primary_glow = '#ff00ff'
            self.secondary_glow = '#cc00cc'
            self.tertiary_glow = '#ff00cc'
            self.accent_orange = '#ff0088'
            self.accent_gold = '#ff44cc'
            self.accent_bright = '#ff33ff'
            self.dark_overlay = '#330033'
            self.darker_overlay = '#1a001a'
            self.text_color = '#ff00cc'
            self.text_secondary = '#cc0099'
            self.text_dim = '#880066'
            
        elif self.current_theme == "stealth":
            # Dark Gray Stealth
            self.primary_glow = '#aaaaaa'
            self.secondary_glow = '#777777'
            self.tertiary_glow = '#999999'
            self.accent_orange = '#cccccc'
            self.accent_gold = '#bbbbbb'
            self.accent_bright = '#dddddd'
            self.dark_overlay = '#1a1a1a'
            self.darker_overlay = '#0d0d0d'
            self.text_color = '#999999'
            self.text_secondary = '#777777'
            self.text_dim = '#555555'
            
        elif self.current_theme == "emerald":
            # Emerald Green
            self.primary_glow = '#00ff88'
            self.secondary_glow = '#00cc66'
            self.tertiary_glow = '#00dd77'
            self.accent_orange = '#00ffaa'
            self.accent_gold = '#44ffaa'
            self.accent_bright = '#00ffcc'
            self.dark_overlay = '#001a11'
            self.darker_overlay = '#000d08'
            self.text_color = '#00dd77'
            self.text_secondary = '#00aa55'
            self.text_dim = '#007744'
            
        elif self.current_theme == "gold":
            # Gold/Yellow
            self.primary_glow = '#ffcc00'
            self.secondary_glow = '#cc9900'
            self.tertiary_glow = '#ffaa00'
            self.accent_orange = '#ffdd00'
            self.accent_gold = '#ffee44'
            self.accent_bright = '#ffbb00'
            self.dark_overlay = '#332200'
            self.darker_overlay = '#1a1100'
            self.text_color = '#ffaa00'
            self.text_secondary = '#cc8800'
            self.text_dim = '#996600'
        
        self.root.configure(bg=self.bg_color)
    
    def _init_particles(self):
        """Initialize particle system for background effects."""
        import random
        for _ in range(self.max_particles):
            self.particles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-1, 0),  # Float upward
                'size': random.randint(1, 3),
                'alpha': random.uniform(0.3, 0.8),
                'life': random.randint(100, 200)
            })
    
    def _init_floating_elements(self):
        """Initialize floating holographic data elements."""
        import random
        elements = ['[NEURAL LINK]', '[AI CORE]', '[VOICE MODULE]', '[MEMORY BANK]', 
                    '[SKILL ENGINE]', '[NETWORK]', '[SENSORS]', '[PROTOCOLS]']
        for i, text in enumerate(elements):
            angle = (i / len(elements)) * 360
            self.floating_elements.append({
                'text': text,
                'angle': angle,
                'radius': 180,
                'alpha': 0.4,
                'pulse': 0
            })
    
    def _build_ui(self):
        """Build the circular holographic interface."""
        # Main canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Make window draggable
        self.canvas.bind('<Button-1>', self._start_drag)
        self.canvas.bind('<B1-Motion>', self._on_drag)
        
        # Click to toggle menu
        self.canvas.bind('<Button-3>', self._toggle_menu)
        self.canvas.bind('<Double-Button-1>', self._on_talk)
        
        # Keyboard shortcuts
        self.root.bind('<q>', lambda e: self._toggle_quick_actions())
        self.root.bind('<Q>', lambda e: self._toggle_quick_actions())
        self.root.bind('<s>', lambda e: self._open_settings())
        self.root.bind('<S>', lambda e: self._open_settings())
        self.root.bind('<t>', lambda e: self._cycle_theme())
        self.root.bind('<T>', lambda e: self._cycle_theme())
    
    def _start_drag(self, event):
        """Start dragging the window or handle quick action click."""
        # Check if clicking on quick action button first
        if self.show_quick_actions and self.quick_action_regions:
            self.logger.debug(f"Click at ({event.x}, {event.y}), checking {len(self.quick_action_regions)} regions")
            for i, (x1, y1, x2, y2) in enumerate(self.quick_action_regions):
                self.logger.debug(f"  Region {i}: ({x1}, {y1}) to ({x2}, {y2})")
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    # Clicked on a quick action button
                    self.logger.info(f"Quick action button {i} clicked!")
                    if i < len(self.favorite_commands):
                        cmd = self.favorite_commands[i]
                        self.logger.info(f"Executing: {cmd}")
                        self._execute_quick_action(cmd)
                    return  # Don't start drag
        
        # Only drag if not clicking on menu area
        if not self.menu_open:
            self.drag_x = event.x
            self.drag_y = event.y
    
    def _on_drag(self, event):
        """Handle window dragging."""
        if not self.menu_open:
            x = self.root.winfo_x() + event.x - self.drag_x
            y = self.root.winfo_y() + event.y - self.drag_y
            self.root.geometry(f"+{x}+{y}")
    
    def _toggle_menu(self, event):
        """Toggle the menu window."""
        self.menu_open = not self.menu_open
        if self.menu_open:
            self._draw_menu()
        else:
            if hasattr(self, 'menu_window') and self.menu_window and self.menu_window.winfo_exists():
                self.menu_window.destroy()
            self._draw_hud()
    
    def _exit_app(self):
        """Exit the application with goodbye message."""
        self.stop_listening = True
        
        # Speak goodbye message and wait for it to complete
        try:
            import time
            goodbye_text = "Goodbye sir. System shutting down."
            
            # Speak and wait
            self.jarvis.tts.speak(goodbye_text, wait=True)
            
            # Additional safety wait to ensure audio buffer is fully played
            time.sleep(1.0)
            
            self.logger.info("Goodbye message completed")
        except Exception as e:
            self.logger.error(f"Error speaking goodbye: {e}")
            # Still wait a bit in case of error
            import time
            time.sleep(1.0)
        
        self.root.quit()
    
    def _cycle_theme(self):
        """Cycle to the next theme."""
        theme_list = list(self.themes.keys())
        current_index = theme_list.index(self.current_theme)
        next_index = (current_index + 1) % len(theme_list)
        self.current_theme = theme_list[next_index]
        self._apply_theme()
        self._draw_hud()
        
        # Show theme name briefly
        theme_name = self.themes[self.current_theme]
        self.logger.info(f"Theme changed to: {theme_name}")
    
    def change_theme_by_voice(self, theme_keyword):
        """Change theme via voice command."""
        theme_keyword = theme_keyword.lower().strip()
        
        # Check aliases
        if theme_keyword in self.theme_aliases:
            new_theme = self.theme_aliases[theme_keyword]
            self.current_theme = new_theme
            self._apply_theme()
            self._draw_hud()
            
            theme_name = self.themes[self.current_theme]
            self.logger.info(f"Theme changed to: {theme_name}")
            self.jarvis.tts.speak(f"Theme changed to {theme_name}")
            return True
        return False
    
    def _toggle_quick_actions(self):
        """Toggle quick actions panel visibility."""
        self.show_quick_actions = not self.show_quick_actions
        self._draw_hud()
    
    def _execute_quick_action(self, command):
        """Execute a quick action command."""
        self.logger.info(f"Quick action: {command}")
        
        # Temporarily pause open mic to prevent self-listening
        was_listening = self.open_mic_mode
        if was_listening:
            self.stop_listening = True
            self.logger.debug("Pausing open mic for quick action")
            # Give it a moment to stop listening
            import time
            time.sleep(0.3)
        
        try:
            # Simulate voice command
            response = self.jarvis.process_input(command)
            if response:
                self.logger.info(f"Quick Action Result: {response}")
                # Speak response
                self.jarvis.tts.speak(response)
        finally:
            # Resume open mic after speaking completes
            if was_listening:
                # Wait for speech to complete
                import time
                while self.jarvis.tts.is_speaking:
                    time.sleep(0.1)
                # Small delay before resuming
                time.sleep(0.5)
                self.stop_listening = False
                self.logger.debug("Resuming open mic after quick action")
    
    def _open_settings(self):
        """Open settings window."""
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return
        
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("J.A.R.V.I.S. Settings")
        self.settings_window.geometry("500x700")
        self.settings_window.configure(bg='#1a1a1a')
        
        # Center on screen
        sw = self.settings_window.winfo_screenwidth()
        sh = self.settings_window.winfo_screenheight()
        x = (sw - 500) // 2
        y = (sh - 700) // 2
        self.settings_window.geometry(f"500x700+{x}+{y}")
        
        # Title
        title = tk.Label(
            self.settings_window,
            text="⚙ SETTINGS",
            font=('Arial', 16, 'bold'),
            fg='#00d4cc',
            bg='#1a1a1a'
        )
        title.pack(pady=20)
        
        # === VOICE SELECTION ===
        voice_frame = tk.Frame(self.settings_window, bg='#1a1a1a')
        voice_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            voice_frame,
            text="Voice Selection:",
            font=('Courier', 11, 'bold'),
            fg='#00d4cc',
            bg='#1a1a1a'
        ).pack(anchor='w', pady=(0, 5))
        
        # Get available voices
        try:
            available_voices = self.jarvis.tts.list_voices()
            
            # Create scrollable frame for voices
            voice_canvas = tk.Canvas(voice_frame, bg='#2a2a2a', height=120, highlightthickness=1, highlightbackground='#00d4cc')
            voice_scrollbar = tk.Scrollbar(voice_frame, orient='vertical', command=voice_canvas.yview)
            voice_list_frame = tk.Frame(voice_canvas, bg='#2a2a2a')
            
            voice_list_frame.bind(
                "<Configure>",
                lambda e: voice_canvas.configure(scrollregion=voice_canvas.bbox("all"))
            )
            
            voice_canvas.create_window((0, 0), window=voice_list_frame, anchor='nw')
            voice_canvas.configure(yscrollcommand=voice_scrollbar.set)
            
            voice_canvas.pack(side='left', fill='both', expand=True)
            voice_scrollbar.pack(side='right', fill='y')
            
            # Current voice index
            current_voice_idx = 0
            
            def change_voice(idx):
                """Change the TTS voice."""
                try:
                    if hasattr(self.jarvis.tts, 'use_pyttsx3') and self.jarvis.tts.use_pyttsx3:
                        voices = self.jarvis.tts.speaker.getProperty('voices')
                        if 0 <= idx < len(voices):
                            self.jarvis.tts.speaker.setProperty('voice', voices[idx].id)
                            self.logger.info(f"Voice changed to: {voices[idx].name}")
                    else:
                        # Windows SAPI
                        voices = self.jarvis.tts.speaker.GetVoices()
                        if 0 <= idx < voices.Count:
                            self.jarvis.tts.speaker.Voice = voices.Item(idx)
                            self.logger.info(f"Voice changed to: {voices.Item(idx).GetDescription()}")
                except Exception as e:
                    self.logger.error(f"Failed to change voice: {e}")
            
            # Create radio buttons for each voice
            voice_var = tk.IntVar(value=current_voice_idx)
            for voice_info in available_voices:
                idx = voice_info['index']
                name = voice_info['name']
                
                rb = tk.Radiobutton(
                    voice_list_frame,
                    text=name,
                    variable=voice_var,
                    value=idx,
                    font=('Courier', 9),
                    fg='#e0e6ed',
                    bg='#2a2a2a',
                    selectcolor='#1a1a1a',
                    activebackground='#2a2a2a',
                    activeforeground='#00ffff',
                    command=lambda i=idx: change_voice(i)
                )
                rb.pack(anchor='w', padx=10, pady=2)
                
        except Exception as e:
            tk.Label(
                voice_frame,
                text=f"Voice selection unavailable: {e}",
                font=('Courier', 8),
                fg='#ff6666',
                bg='#1a1a1a'
            ).pack(anchor='w')
        
        # === GET MORE VOICES ===
        get_voices_frame = tk.Frame(self.settings_window, bg='#1a1a1a')
        get_voices_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(
            get_voices_frame,
            text="💡 Want JARVIS Movie Voice?",
            font=('Courier', 9, 'bold'),
            fg='#ffaa00',
            bg='#1a1a1a'
        ).pack(anchor='w')
        
        info_text = "Install premium voices like:\n• Ivona Brian (British, sounds like movie JARVIS)\n• CereProc voices (high quality)\n• Microsoft David Desktop (free, British)"
        tk.Label(
            get_voices_frame,
            text=info_text,
            font=('Courier', 8),
            fg='#aaaaaa',
            bg='#1a1a1a',
            justify='left'
        ).pack(anchor='w', padx=10)
        
        # Buttons for getting more voices
        btn_frame = tk.Frame(get_voices_frame, bg='#1a1a1a')
        btn_frame.pack(fill='x', pady=5)
        
        def open_windows_speech():
            """Open Windows Speech settings."""
            try:
                import subprocess
                # Use ms-settings URI for Windows 10/11
                subprocess.Popen(['cmd', '/c', 'start', 'ms-settings:speech'], shell=False)
                self.logger.info("Opened Windows Speech settings")
            except Exception as e:
                self.logger.error(f"Failed to open speech settings: {e}")
                # Fallback to control panel
                try:
                    subprocess.Popen(['control.exe', '/name', 'Microsoft.Speech'], shell=False)
                except:
                    pass
        
        def open_voice_store():
            """Open Microsoft Store for language packs."""
            try:
                import subprocess
                subprocess.Popen(['cmd', '/c', 'start', 'ms-settings:regionlanguage'], shell=False)
                self.logger.info("Opened Windows Language settings")
            except Exception as e:
                self.logger.error(f"Failed to open settings: {e}")
        
        def open_ivona_info():
            """Open info about Ivona voices (best JARVIS-like voice)."""
            try:
                import webbrowser
                webbrowser.open('https://www.cereproc.com/en/products/voices')
                self.logger.info("Opened voice vendor website")
            except Exception as e:
                self.logger.error(f"Failed to open browser: {e}")
        
        tk.Button(
            btn_frame,
            text="🔧 Windows Speech Settings",
            command=open_windows_speech,
            bg='#2a2a2a',
            fg='#00d4cc',
            font=('Courier', 8, 'bold'),
            relief='flat',
            padx=8,
            pady=3
        ).pack(side='left', padx=(0, 5))
        
        tk.Button(
            btn_frame,
            text="🛒 Get Premium Voices",
            command=open_ivona_info,
            bg='#2a2a2a',
            fg='#ffaa00',
            font=('Courier', 8, 'bold'),
            relief='flat',
            padx=8,
            pady=3
        ).pack(side='left')
        
        # === VOICE SPEED ===
        speed_frame = tk.Frame(self.settings_window, bg='#1a1a1a')
        speed_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            speed_frame,
            text="Voice Speed:",
            font=('Courier', 11, 'bold'),
            fg='#00d4cc',
            bg='#1a1a1a'
        ).pack(anchor='w')
        
        # Get current rate
        try:
            if hasattr(self.jarvis.tts, 'use_pyttsx3') and self.jarvis.tts.use_pyttsx3:
                current_rate = self.jarvis.tts.speaker.getProperty('rate')
            else:
                # SAPI uses -10 to 10, convert to WPM (150-200 range)
                sapi_rate = self.jarvis.tts.speaker.Rate
                current_rate = int(175 + (sapi_rate * 25))
        except:
            current_rate = 175
        
        speed_var = tk.IntVar(value=current_rate)
        
        def update_speed(val):
            """Update TTS speed."""
            try:
                rate = int(val)
                if hasattr(self.jarvis.tts, 'use_pyttsx3') and self.jarvis.tts.use_pyttsx3:
                    self.jarvis.tts.speaker.setProperty('rate', rate)
                else:
                    # Convert WPM to SAPI rate
                    sapi_rate = int((rate - 175) / 25)
                    self.jarvis.tts.speaker.Rate = max(-10, min(10, sapi_rate))
                self.logger.info(f"Voice speed changed to: {rate}")
            except Exception as e:
                self.logger.error(f"Failed to change speed: {e}")
        
        speed_scale = tk.Scale(
            speed_frame,
            from_=100,
            to=300,
            orient='horizontal',
            variable=speed_var,
            bg='#2a2a2a',
            fg='#00d4cc',
            highlightthickness=0,
            command=update_speed
        )
        speed_scale.pack(fill='x')
        
        tk.Label(
            speed_frame,
            text="(100 = Slow, 175 = Normal, 300 = Fast)",
            font=('Courier', 8),
            fg='#888',
            bg='#1a1a1a'
        ).pack(anchor='w')
        
        # Test voice button
        def test_voice():
            """Test the current voice settings."""
            try:
                self.jarvis.tts.speak("Voice test successful. This is how I sound now.", wait=False)
            except Exception as e:
                self.logger.error(f"Voice test failed: {e}")
        
        tk.Button(
            speed_frame,
            text="🎙 Test Voice",
            command=test_voice,
            bg='#00d4cc',
            fg='#000000',
            font=('Courier', 9, 'bold'),
            relief='flat',
            padx=15,
            pady=3
        ).pack(anchor='w', pady=5)
        
        # === THEME SELECTION ===
        theme_frame = tk.Frame(self.settings_window, bg='#1a1a1a')
        theme_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            theme_frame,
            text="Theme:",
            font=('Courier', 11, 'bold'),
            fg='#00d4cc',
            bg='#1a1a1a'
        ).pack(anchor='w')
        
        theme_var = tk.StringVar(value=self.themes[self.current_theme])
        for theme_key, theme_name in self.themes.items():
            rb = tk.Radiobutton(
                theme_frame,
                text=theme_name,
                variable=theme_var,
                value=theme_name,
                font=('Courier', 9),
                fg='#00d4cc',
                bg='#1a1a1a',
                selectcolor='#2a2a2a',
                activebackground='#1a1a1a',
                activeforeground='#00ffff',
                command=lambda k=theme_key: self._apply_theme_from_settings(k)
            )
            rb.pack(anchor='w', padx=10)
        
        # === QUICK ACTIONS MANAGEMENT ===
        qa_frame = tk.Frame(self.settings_window, bg='#1a1a1a')
        qa_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(
            qa_frame,
            text="Quick Actions:",
            font=('Courier', 11, 'bold'),
            fg='#00d4cc',
            bg='#1a1a1a'
        ).pack(anchor='w')
        
        qa_list = tk.Listbox(
            qa_frame,
            bg='#2a2a2a',
            fg='#00d4cc',
            font=('Courier', 9),
            selectbackground='#00d4cc',
            selectforeground='#1a1a1a',
            height=8
        )
        qa_list.pack(fill='both', expand=True, pady=5)
        
        for cmd in self.favorite_commands:
            qa_list.insert('end', cmd)
        
        # Close button
        tk.Button(
            self.settings_window,
            text="Close",
            command=self.settings_window.destroy,
            bg='#00d4cc',
            fg='#000000',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=5
        ).pack(pady=20)
    
    def _apply_theme_from_settings(self, theme_key):
        """Apply theme from settings window."""
        self.current_theme = theme_key
        self._apply_theme()
        self._draw_hud()
    
    def update_audio_level(self, level):
        """Update audio level for visualization (0.0 to 1.0)."""
        self.audio_level = max(0.0, min(1.0, level))
        
        # Update audio bars with some randomness for effect
        import random
        for i in range(len(self.audio_bars)):
            target = level * random.uniform(0.5, 1.0)
            self.audio_bars[i] = self.audio_bars[i] * 0.7 + target * 0.3
    
    def _draw_hud(self):
        """Draw the circular holographic interface with advanced visual effects."""
        self.canvas.delete("all")
        
        # Center coordinates
        cx = self.width // 2
        cy = self.height // 2
        
        # State-based colors
        if self.current_state == "listening":
            accent_color = '#00ff88'
            status_text = "LISTENING"
        elif self.current_state == "thinking":
            accent_color = '#ffaa00'
            status_text = "PROCESSING"
        elif self.current_state == "speaking":
            accent_color = '#ff3333'
            status_text = "SPEAKING"
        else:
            accent_color = self.primary_glow
            status_text = "ONLINE"
        
        # === DARK RADIAL GRADIENT BACKGROUND ===
        # Create multiple concentric circles for gradient effect
        max_radius = int(math.sqrt((self.width/2)**2 + (self.height/2)**2))
        for r in range(max_radius, 0, -15):
            alpha_val = int(255 * (1 - r / max_radius) * 0.3)
            gradient_color = f"#{alpha_val:02x}{alpha_val:02x}{alpha_val:02x}"
            self.canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill=gradient_color, outline=''
            )
        
        # === OUTER RING LAYERS (Large to Small) ===
        # Large outer ring with glow
        outer_radius = 220
        self.canvas.create_oval(
            cx - outer_radius, cy - outer_radius,
            cx + outer_radius, cy + outer_radius,
            outline=self.text_dim, width=1
        )
        self.canvas.create_oval(
            cx - outer_radius + 2, cy - outer_radius + 2,
            cx + outer_radius - 2, cy + outer_radius - 2,
            outline=self.secondary_glow, width=2
        )
        
        # Medium outer ring
        med_radius = 190
        self.canvas.create_oval(
            cx - med_radius, cy - med_radius,
            cx + med_radius, cy + med_radius,
            outline=self.text_dim, width=1
        )
        
        # Animated ring segments
        segment_radius = 200
        num_segments = 36
        segment_length = 8
        for i in range(num_segments):
            angle = (360 / num_segments) * i + (self.pulse_alpha * 2)
            angle_rad = math.radians(angle)
            
            # Calculate segment start and end
            x1 = cx + segment_radius * math.cos(angle_rad)
            y1 = cy + segment_radius * math.sin(angle_rad)
            x2 = cx + (segment_radius - segment_length) * math.cos(angle_rad)
            y2 = cy + (segment_radius - segment_length) * math.sin(angle_rad)
            
            # Fade segments based on rotation
            opacity = (math.sin(math.radians(i * 10 + self.pulse_alpha * 3)) + 1) / 2
            if opacity > 0.5:
                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=self.primary_glow, width=2
                )
        
        # === MIDDLE RING WITH HEXAGONAL PATTERN ===
        mid_radius = 140
        self.canvas.create_oval(
            cx - mid_radius, cy - mid_radius,
            cx + mid_radius, cy + mid_radius,
            outline=self.primary_glow, width=3
        )
        
        # Hexagonal detail points around middle ring
        for i in range(6):
            angle = math.radians(60 * i + self.pulse_alpha)
            x = cx + mid_radius * math.cos(angle)
            y = cy + mid_radius * math.sin(angle)
            
            # Small hexagon markers
            hex_size = 6
            hex_points = []
            for j in range(6):
                h_angle = math.radians(60 * j)
                hx = x + hex_size * math.cos(h_angle)
                hy = y + hex_size * math.sin(h_angle)
                hex_points.extend([hx, hy])
            
            self.canvas.create_polygon(
                hex_points, 
                fill='', 
                outline=accent_color, 
                width=2
            )
        
        # === INNER RINGS ===
        inner_radius1 = 100
        self.canvas.create_oval(
            cx - inner_radius1, cy - inner_radius1,
            cx + inner_radius1, cy + inner_radius1,
            outline=self.tertiary_glow, width=2
        )
        
        inner_radius2 = 80
        self.canvas.create_oval(
            cx - inner_radius2, cy - inner_radius2,
            cx + inner_radius2, cy + inner_radius2,
            outline=self.text_dim, width=1
        )
        
        # === CENTER JARVIS TEXT ===
        # Background circle for text
        text_bg_radius = 65
        self.canvas.create_oval(
            cx - text_bg_radius, cy - text_bg_radius,
            cx + text_bg_radius, cy + text_bg_radius,
            fill=self.darker_overlay, outline=self.primary_glow, width=2
        )
        
        # "JARVIS" text with glow effect
        self.canvas.create_text(
            cx, cy - 10,
            text="JARVIS",
            font=('Arial Black', 32, 'bold'),
            fill=self.text_dim
        )
        self.canvas.create_text(
            cx, cy - 10,
            text="JARVIS",
            font=('Arial Black', 32, 'bold'),
            fill=self.primary_glow
        )
        
        # Status text below
        self.canvas.create_text(
            cx, cy + 25,
            text=status_text,
            font=('Courier New', 10, 'bold'),
            fill=accent_color
        )
        
        # === RADIAL LINES FROM CENTER ===
        num_lines = 24
        for i in range(num_lines):
            angle = (360 / num_lines) * i
            angle_rad = math.radians(angle)
            
            # Start from inner circle, extend to middle circle
            start_r = 70
            end_r = 75 + (5 * math.sin(math.radians(i * 15 + self.pulse_alpha * 4)))
            
            x1 = cx + start_r * math.cos(angle_rad)
            y1 = cy + start_r * math.sin(angle_rad)
            x2 = cx + end_r * math.cos(angle_rad)
            y2 = cy + end_r * math.sin(angle_rad)
            
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill=self.text_dim, width=1
            )
        
        # === AUDIO VISUALIZER EQUALIZER ===
        if self.current_state == "listening" and self.audio_level > 0.01:
            eq_radius = 110
            eq_bar_count = len(self.audio_bars)
            eq_bar_width = 8
            
            for i in range(eq_bar_count):
                angle = (360 / eq_bar_count) * i
                angle_rad = math.radians(angle)
                
                # Bar height based on audio level
                bar_height = self.audio_bars[i] * 30
                
                # Calculate bar position
                inner_r = eq_radius
                outer_r = eq_radius + bar_height
                
                # Bar coordinates
                x1 = cx + inner_r * math.cos(angle_rad)
                y1 = cy + inner_r * math.sin(angle_rad)
                x2 = cx + outer_r * math.cos(angle_rad)
                y2 = cy + outer_r * math.sin(angle_rad)
                
                # Color gradient based on height
                intensity = int(self.audio_bars[i] * 255)
                bar_color = f"#{intensity:02x}{200:02x}{200:02x}"
                
                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=bar_color, width=eq_bar_width
                )
        
        # === PULSING EFFECT FOR SPEAKING ===
        if self.current_state == "speaking":
            pulse_radius = 65 + math.sin(self.pulse_alpha * 0.3) * 10
            pulse_alpha = (math.sin(self.pulse_alpha * 0.2) + 1) / 4
            pulse_intensity = int(pulse_alpha * 150)
            pulse_color = f"#{pulse_intensity:02x}{pulse_intensity + 100:02x}{pulse_intensity + 100:02x}"
            
            self.canvas.create_oval(
                cx - pulse_radius, cy - pulse_radius,
                cx + pulse_radius, cy + pulse_radius,
                outline=pulse_color, width=2
            )
        
        # === CORNER INDICATORS ===
        corner_offset = 30
        corner_size = 20
        
        # Top-left
        self.canvas.create_line(
            corner_offset, corner_offset,
            corner_offset + corner_size, corner_offset,
            fill=self.primary_glow, width=2
        )
        self.canvas.create_line(
            corner_offset, corner_offset,
            corner_offset, corner_offset + corner_size,
            fill=self.primary_glow, width=2
        )
        
        # Top-right
        self.canvas.create_line(
            self.width - corner_offset, corner_offset,
            self.width - corner_offset - corner_size, corner_offset,
            fill=self.primary_glow, width=2
        )
        self.canvas.create_line(
            self.width - corner_offset, corner_offset,
            self.width - corner_offset, corner_offset + corner_size,
            fill=self.primary_glow, width=2
        )
        
        # Bottom-left
        self.canvas.create_line(
            corner_offset, self.height - corner_offset,
            corner_offset + corner_size, self.height - corner_offset,
            fill=self.primary_glow, width=2
        )
        self.canvas.create_line(
            corner_offset, self.height - corner_offset,
            corner_offset, self.height - corner_offset - corner_size,
            fill=self.primary_glow, width=2
        )
        
        # Bottom-right
        self.canvas.create_line(
            self.width - corner_offset, self.height - corner_offset,
            self.width - corner_offset - corner_size, self.height - corner_offset,
            fill=self.primary_glow, width=2
        )
        self.canvas.create_line(
            self.width - corner_offset, self.height - corner_offset,
            self.width - corner_offset, self.height - corner_offset - corner_size,
            fill=self.primary_glow, width=2
        )
        
        # === TOP STATUS BAR ===
        self.canvas.create_text(
            cx, 20,
            text="J.A.R.V.I.S. OMEGA",
            font=('Courier New', 10, 'bold'),
            fill=self.text_color
        )
        
        # === BOTTOM HELP TEXT ===
        mode_text = "● OPEN MIC MODE - ALWAYS LISTENING"
        self.canvas.create_text(
            cx, self.height - 20,
            text=mode_text,
            font=('Courier New', 8),
            fill=self.text_secondary
        )
        
        help_text = "ALWAYS LISTENING • [RIGHT-CLICK] MENU • [Q] QUICK ACTIONS • [S] SETTINGS"
        self.canvas.create_text(
            cx, self.height - 35,
            text=help_text,
            font=('Courier New', 7),
            fill=self.text_dim
        )
        
        # === QUICK ACTIONS PANEL ===
        if self.show_quick_actions:
            # Clear previous button regions
            self.quick_action_regions = []
            
            # Background panel
            panel_width = 300
            panel_height = 150
            panel_x = cx - panel_width // 2
            panel_y = self.height - panel_height - 60
            
            self.canvas.create_rectangle(
                panel_x, panel_y,
                panel_x + panel_width, panel_y + panel_height,
                fill='#1a1a1a', outline=self.primary_glow, width=2
            )
            
            # Title
            self.canvas.create_text(
                cx, panel_y + 15,
                text="⚡ QUICK ACTIONS",
                font=('Courier New', 10, 'bold'),
                fill=self.primary_glow
            )
            
            # Command buttons
            btn_height = 25
            btn_spacing = 5
            for i, cmd in enumerate(self.favorite_commands[:4]):
                btn_y = panel_y + 40 + i * (btn_height + btn_spacing)
                btn_x1 = panel_x + 10
                btn_x2 = panel_x + panel_width - 10
                btn_y2 = btn_y + btn_height
                
                # Store button region for click detection
                self.quick_action_regions.append((btn_x1, btn_y, btn_x2, btn_y2))
                
                # Create button rectangle
                self.canvas.create_rectangle(
                    btn_x1, btn_y,
                    btn_x2, btn_y2,
                    fill='#2a2a2a', outline=self.text_secondary, width=1
                )
                
                # Create button text
                self.canvas.create_text(
                    cx, btn_y + btn_height // 2,
                    text=cmd.upper(),
                    font=('Courier New', 8, 'bold'),
                    fill=self.text_color
                )
        else:
            # Clear regions when panel is hidden
            self.quick_action_regions = []
        
        # === OVERLAY: PARTICLE EFFECTS (TOP LAYER) ===
        for particle in self.particles:
            x, y = int(particle['x']), int(particle['y'])
            size = particle['size']
            
            # Vary color based on alpha for intensity
            if particle['alpha'] > 0.6:
                particle_color = self.primary_glow
            elif particle['alpha'] > 0.4:
                particle_color = self.text_secondary
            else:
                particle_color = self.text_dim
            
            # Draw bright particle dot
            self.canvas.create_oval(
                x - size, y - size,
                x + size, y + size,
                fill=particle_color, outline=''
            )
        
        # === OVERLAY: HOLOGRAPHIC SCAN LINE (TOP LAYER) ===
        scan_y = int(self.scan_line_y)
        for offset in range(-2, 3):
            if abs(offset) == 0:
                scan_color = self.tertiary_glow
                width = 2
            elif abs(offset) == 1:
                scan_color = self.secondary_glow
                width = 1
            else:
                scan_color = self.text_dim
                width = 1
            
            self.canvas.create_line(
                0, scan_y + offset * 2, self.width, scan_y + offset * 2,
                fill=scan_color, width=width
            )
        
        # === OVERLAY: FLOATING DATA ELEMENTS (TOP LAYER) ===
        for elem in self.floating_elements:
            angle_rad = math.radians(elem['angle'])
            x = cx + elem['radius'] * math.cos(angle_rad)
            y = cy + elem['radius'] * math.sin(angle_rad)
            
            # Use varying colors based on pulse
            if elem['alpha'] > 0.5:
                text_color = self.text_secondary
            else:
                text_color = self.text_dim
            
            self.canvas.create_text(
                x, y,
                text=elem['text'],
                font=('Consolas', 7, 'bold'),
                fill=text_color
            )
    
    def _draw_menu(self):
        """Draw modern scrollable popup menu with enhanced styling."""
        if hasattr(self, 'menu_window') and self.menu_window and self.menu_window.winfo_exists():
            self.menu_window.destroy()
            return
        
        # Create popup window
        self.menu_window = tk.Toplevel(self.root)
        self.menu_window.title("Menu")
        self.menu_window.overrideredirect(True)
        
        # Position near the main window
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        menu_x = root_x + (self.width - 280) // 2
        menu_y = root_y + (self.height - 450) // 2
        
        self.menu_window.geometry(f"280x450+{menu_x}+{menu_y}")
        self.menu_window.configure(bg='#000000')
        
        # Make it stay on top
        self.menu_window.attributes('-topmost', True)
        
        # Outer border frame
        outer_frame = tk.Frame(self.menu_window, bg=self.primary_glow, bd=0)
        outer_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Inner border frame
        inner_frame = tk.Frame(outer_frame, bg=self.secondary_glow, bd=0)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        # Main container
        main_container = tk.Frame(inner_frame, bg=self.darker_overlay, bd=0)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # === TITLE BAR WITH ENHANCED DESIGN ===
        title_frame = tk.Frame(main_container, bg='#000000', height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        # Top accent line
        accent_line = tk.Frame(title_frame, bg=self.primary_glow, height=3)
        accent_line.pack(fill=tk.X)
        
        # Title with futuristic styling
        title_label = tk.Label(
            title_frame,
            text="◢◤ CONTROL PANEL ◥◣",
            font=("Courier New", 16, "bold"),
            bg='#000000',
            fg=self.primary_glow
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle line
        subtitle_frame = tk.Frame(title_frame, bg='#000000')
        subtitle_frame.pack(fill=tk.X, padx=20)
        
        tk.Frame(subtitle_frame, bg=self.text_dim, height=1).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Theme display with styling
        theme_name = self.themes[self.current_theme]
        theme_label = tk.Label(
            title_frame,
            text=f"▸ {theme_name.upper()} ◂",
            font=("Courier New", 9, "bold"),
            bg='#000000',
            fg=self.text_color
        )
        theme_label.pack(pady=(5, 5))
        
        # Bottom accent line
        accent_line2 = tk.Frame(title_frame, bg=self.tertiary_glow, height=2)
        accent_line2.pack(fill=tk.X)
        
        # === SCROLLABLE CONTENT AREA ===
        canvas_frame = tk.Frame(main_container, bg=self.darker_overlay)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        # Canvas with custom scrollbar
        menu_canvas = tk.Canvas(
            canvas_frame, 
            bg=self.darker_overlay, 
            highlightthickness=0,
            bd=0
        )
        
        # Custom styled scrollbar
        scrollbar = tk.Scrollbar(
            canvas_frame, 
            orient="vertical", 
            command=menu_canvas.yview,
            bg=self.dark_overlay,
            troughcolor=self.darker_overlay,
            activebackground=self.primary_glow,
            width=12
        )
        
        scrollable_frame = tk.Frame(menu_canvas, bg=self.darker_overlay)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: menu_canvas.configure(scrollregion=menu_canvas.bbox("all"))
        )
        
        menu_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        menu_canvas.configure(yscrollcommand=scrollbar.set)
        
        menu_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # === MENU ITEMS WITH ENHANCED DESIGN ===
        items = [
            ("CHANGE THEME", self._cycle_theme, self.accent_bright),
            ("COMMANDS LIST", self._open_commands_editor, self.accent_orange),
            ("Q&A EDITOR", self._open_qa_editor, self.accent_gold),
            ("TOGGLE MIC MODE", self._toggle_open_mic, self.primary_glow),
            ("HISTORY LOG", self._show_history, self.text_color),
            ("EXIT JARVIS", self._exit_app, '#ff0000')
        ]
        
        # Create enhanced menu buttons
        for idx, (text, command, color) in enumerate(items):
            # Button container with borders
            btn_container = tk.Frame(scrollable_frame, bg=self.darker_overlay)
            btn_container.pack(fill=tk.X, padx=8, pady=4)
            
            # Outer glow frame
            glow_frame = tk.Frame(btn_container, bg=self.dark_overlay, bd=0)
            glow_frame.pack(fill=tk.X, padx=1, pady=1)
            
            # Button frame
            btn_frame = tk.Frame(glow_frame, bg=self.darker_overlay, bd=0)
            btn_frame.pack(fill=tk.X)
            
            # Create button with enhanced styling
            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Courier New", 11, "bold"),
                bg=self.dark_overlay,
                fg=color,
                activebackground=color,
                activeforeground='#000000',
                relief=tk.FLAT,
                bd=0,
                pady=14,
                cursor="hand2",
                anchor='w',
                padx=15,
                command=lambda cmd=command: self._menu_click_window(cmd)
            )
            btn.pack(fill=tk.X)
            
            # Side indicator line
            indicator = tk.Frame(btn_frame, bg=color, width=4)
            indicator.place(relx=0, rely=0, relheight=1)
            
            # Enhanced hover effects with color changes
            def on_enter(e, b=btn, gf=glow_frame, c=color):
                b.config(bg=c, fg='#000000', font=("Courier New", 11, "bold"))
                gf.config(bg=c)
            
            def on_leave(e, b=btn, gf=glow_frame, c=color):
                b.config(bg=self.dark_overlay, fg=c, font=("Courier New", 11, "bold"))
                gf.config(bg=self.dark_overlay)
            
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
        
        # === FOOTER WITH CONTROLS INFO ===
        footer_frame = tk.Frame(main_container, bg='#000000', height=45)
        footer_frame.pack(fill=tk.X)
        footer_frame.pack_propagate(False)
        
        # Top accent line
        tk.Frame(footer_frame, bg=self.tertiary_glow, height=2).pack(fill=tk.X)
        
        # Controls hint
        controls_label = tk.Label(
            footer_frame,
            text="[ESC] CLOSE  •  [SCROLL] NAVIGATE",
            font=("Courier New", 8),
            bg='#000000',
            fg=self.text_dim
        )
        controls_label.pack(pady=8)
        
        # System status
        status_label = tk.Label(
            footer_frame,
            text="● SYSTEM OPERATIONAL",
            font=("Courier New", 7, "bold"),
            bg='#000000',
            fg='#00ff00'
        )
        status_label.pack()
        
        # Close on ESC key
        def on_escape(event):
            if self.menu_window and self.menu_window.winfo_exists():
                self.menu_window.destroy()
                self.menu_open = False
                self._draw_hud()
        
        self.menu_window.bind('<Escape>', on_escape)
        
        # Close on click outside
        def close_menu(event=None):
            if self.menu_window and self.menu_window.winfo_exists():
                self.menu_window.destroy()
                self.menu_open = False
                self._draw_hud()
        
        self.menu_window.bind('<FocusOut>', close_menu)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            try:
                if menu_canvas.winfo_exists():
                    menu_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except:
                pass
        
        menu_canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def _menu_click_window(self, command):
        """Handle menu item click from window menu."""
        if self.menu_window and self.menu_window.winfo_exists():
            self.menu_window.destroy()
        self.menu_open = False
        self._draw_hud()
        command()
    
    def _menu_click(self, command):
        """Handle menu item click."""
        self.menu_open = False
        self._draw_hud()
        command()
    
    def _draw_triangle(self, x, y, direction, color, size):
        """Draw a triangular direction marker."""
        if direction == 'up':
            points = [x, y - size, x - size, y + size, x + size, y + size]
        elif direction == 'down':
            points = [x, y + size, x - size, y - size, x + size, y - size]
        elif direction == 'left':
            points = [x - size, y, x + size, y - size, x + size, y + size]
        else:  # right
            points = [x + size, y, x - size, y - size, x - size, y + size]
        
        self.canvas.create_polygon(points, fill=color, outline='')
    
    def _draw_tick_ring(self, cx, cy, radius, count, length, color, rotation=0):
        """Draw a ring of tick marks."""
        angle_step = 360 / count
        for i in range(count):
            angle = i * angle_step + rotation
            rad = math.radians(angle)
            
            x1 = cx + radius * math.cos(rad)
            y1 = cy + radius * math.sin(rad)
            x2 = cx + (radius - length) * math.cos(rad)
            y2 = cy + (radius - length) * math.sin(rad)
            
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=1)
    
    def _draw_segmented_ring(self, cx, cy, inner_radius, outer_radius, color, 
                            segments=40, rotation=0, gap=0):
        """Draw a segmented ring with rotation."""
        angle_per_segment = 360 / segments
        
        for i in range(segments):
            start_angle = i * angle_per_segment + rotation
            end_angle = start_angle + angle_per_segment - gap
            
            points = []
            for angle in [start_angle, end_angle]:
                rad = math.radians(angle)
                x_outer = cx + outer_radius * math.cos(rad)
                y_outer = cy + outer_radius * math.sin(rad)
                points.append((x_outer, y_outer))
            
            for angle in [end_angle, start_angle]:
                rad = math.radians(angle)
                x_inner = cx + inner_radius * math.cos(rad)
                y_inner = cy + inner_radius * math.sin(rad)
                points.append((x_inner, y_inner))
            
            flat_points = [coord for point in points for coord in point]
            self.canvas.create_polygon(flat_points, fill=color, outline='')
    
    def _draw_notched_ring(self, cx, cy, inner_radius, outer_radius, color, notches=40, rotation=0):
        """Draw a ring with notched segments."""
        angle_per_notch = 360 / notches
        
        for i in range(notches):
            if i % 2 == 0:  # Only draw every other segment for notched effect
                start_angle = i * angle_per_notch + rotation
                end_angle = start_angle + angle_per_notch * 0.8
                
                points = []
                for angle in [start_angle, end_angle]:
                    rad = math.radians(angle)
                    x_outer = cx + outer_radius * math.cos(rad)
                    y_outer = cy + outer_radius * math.sin(rad)
                    points.append((x_outer, y_outer))
                
                for angle in [end_angle, start_angle]:
                    rad = math.radians(angle)
                    x_inner = cx + inner_radius * math.cos(rad)
                    y_inner = cy + inner_radius * math.sin(rad)
                    points.append((x_inner, y_inner))
                
                flat_points = [coord for point in points for coord in point]
                self.canvas.create_polygon(flat_points, fill=color, outline='')
    
    def _draw_arc_segment(self, cx, cy, inner_radius, outer_radius, color, 
                         start_angle=0, extent=40):
        """Draw a colored arc segment (for accents)."""
        points = []
        
        for angle in range(int(start_angle), int(start_angle + extent), 2):
            rad = math.radians(angle)
            x = cx + outer_radius * math.cos(rad)
            y = cy + outer_radius * math.sin(rad)
            points.append((x, y))
        
        for angle in range(int(start_angle + extent), int(start_angle), -2):
            rad = math.radians(angle)
            x = cx + inner_radius * math.cos(rad)
            y = cy + inner_radius * math.sin(rad)
            points.append((x, y))
        
        if points:
            flat_points = [coord for point in points for coord in point]
            self.canvas.create_polygon(flat_points, fill=color, outline='')
    
    def _animate(self):
        """Animate the modern dashboard with particle effects and scan lines."""
        # Pulse alpha for smooth animations
        self.pulse_alpha += 0.05
        
        # Animate bar width for progress animations
        if self.current_state in ["listening", "thinking", "speaking"]:
            self.bar_width = (math.sin(self.pulse_alpha) * 0.5 + 0.5)
        
        # Update particles
        self._update_particles()
        
        # Update scan line position
        self.scan_line_y += 2 * self.scan_direction
        if self.scan_line_y > self.height:
            self.scan_line_y = 0
        
        # Update floating elements
        for elem in self.floating_elements:
            elem['angle'] += 0.3
            elem['pulse'] = (elem['pulse'] + 0.1) % (2 * 3.14159)
            elem['alpha'] = 0.3 + 0.3 * math.sin(elem['pulse'])
        
        self._draw_hud()
        
        # Schedule next frame
        self.root.after(50, self._animate)
    
    def _update_particles(self):
        """Update particle positions and create new ones."""
        import random
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            # Wrap around screen
            if particle['x'] < 0:
                particle['x'] = self.width
            elif particle['x'] > self.width:
                particle['x'] = 0
            
            # Reset if dead or out of bounds
            if particle['life'] <= 0 or particle['y'] < -10:
                particle['x'] = random.randint(0, self.width)
                particle['y'] = self.height
                particle['vx'] = random.uniform(-0.5, 0.5)
                particle['vy'] = random.uniform(-1, -0.3)
                particle['life'] = random.randint(100, 200)
                particle['alpha'] = random.uniform(0.3, 0.8)
    
    def set_state(self, state: str):
        """
        Update HUD state.
        
        Args:
            state: One of 'idle', 'listening', 'thinking', 'speaking'
        """
        self.current_state = state
        # Schedule drawing on main thread to avoid tkinter threading issues
        try:
            self.root.after(0, self._draw_hud)
        except:
            # If root is destroyed or not available, just update state
            pass
    
    def _on_talk(self):
        """Handle talk command from menu."""
        import threading
        thread = threading.Thread(target=self.jarvis.listen_and_respond)
        thread.daemon = True
        thread.start()
    
    def _start_voice_command(self):
        """Alias for _on_talk - used by menu buttons."""
        self._on_talk()
    
    def _show_history(self):
        """Show conversation history in a separate window."""
        history_window = tk.Toplevel(self.root)
        history_window.title("Conversation History")
        history_window.geometry("700x500")
        history_window.configure(bg='#0a0e1a')
        
        # Title
        title = tk.Label(
            history_window,
            text="📜 CONVERSATION HISTORY",
            font=("Consolas", 14, "bold"),
            bg='#0a0e1a',
            fg=self.text_color
        )
        title.pack(pady=10)
        
        # Text widget
        text_frame = tk.Frame(history_window, bg=self.secondary_glow, bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        history_text = scrolledtext.ScrolledText(
            text_frame,
            font=("Consolas", 10),
            bg='#1a1f2e',
            fg='#e0e6ed',
            wrap=tk.WORD,
            bd=0,
            padx=10,
            pady=10
        )
        history_text.pack(fill=tk.BOTH, expand=True)
        
        # Load history from memory if available
        if self.jarvis.memory:
            try:
                recent = self.jarvis.memory.get_recent_interactions(50)
                for interaction in recent:
                    timestamp = interaction.get('timestamp', '')
                    user_input = interaction.get('user_input', '')
                    response = interaction.get('response', '')
                    history_text.insert(tk.END, f"[{timestamp}]\n")
                    history_text.insert(tk.END, f"You: {user_input}\n")
                    history_text.insert(tk.END, f"Jarvis: {response}\n\n")
            except:
                history_text.insert(tk.END, "No conversation history available.\n")
        else:
            history_text.insert(tk.END, "Memory system not enabled.\n")
        
        history_text.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(
            history_window,
            text="✖ CLOSE",
            font=("Consolas", 11),
            bg='#1a1f2e',
            fg=self.text_color,
            activebackground='#333333',
            relief=tk.FLAT,
            bd=0,
            pady=10,
            command=history_window.destroy,
            cursor="hand2"
        )
        close_btn.pack(fill=tk.X, padx=20, pady=(0, 20))
    
    def _open_commands_editor(self):
        """Open custom commands editor dialog."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Custom Commands Editor")
        settings_window.geometry("800x600")
        settings_window.configure(bg='#0a0e1a')
        
        # Title
        title = tk.Label(
            settings_window,
            text="⚙ CUSTOM COMMANDS EDITOR",
            font=("Consolas", 16, "bold"),
            bg='#0a0e1a',
            fg=self.text_color
        )
        title.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(
            settings_window,
            text="Edit custom_commands.yaml to add your own voice commands.\nRestart Jarvis to load changes.",
            font=("Consolas", 9),
            bg='#0a0e1a',
            fg='#e0e6ed',
            justify=tk.LEFT
        )
        instructions.pack(pady=5)
        
        # Text editor
        editor_frame = tk.Frame(settings_window, bg=self.secondary_glow, bd=2)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        text_editor = scrolledtext.ScrolledText(
            editor_frame,
            font=("Consolas", 10),
            bg='#1a1f2e',
            fg='#e0e6ed',
            insertbackground=self.text_color,
            selectbackground=self.secondary_glow,
            bd=0,
            padx=10,
            pady=10
        )
        text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Load current config
        try:
            config_path = get_resource_path('custom_commands.yaml')
            if not os.path.exists(config_path):
                # Fallback to current directory
                config_path = 'custom_commands.yaml'
            
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
                text_editor.insert('1.0', content)
        except Exception as e:
            text_editor.insert('1.0', f"# Error loading custom_commands.yaml: {e}\n# Create the file manually or restart Jarvis")
        
        # Save button
        def save_commands():
            try:
                content = text_editor.get('1.0', tk.END)
                config_path = get_resource_path('custom_commands.yaml')
                if not os.path.exists(config_path):
                    # Save to current directory if bundled path not writable
                    config_path = 'custom_commands.yaml'
                
                with open(config_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.logger.info("Custom commands saved")
                settings_window.destroy()
            except Exception as e:
                self.logger.error(f"Error saving: {str(e)}")
        
        button_frame = tk.Frame(settings_window, bg='#0a0e1a')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        save_btn = tk.Button(
            button_frame,
            text="💾 SAVE CHANGES",
            font=("Consolas", 11, "bold"),
            bg=self.secondary_glow,
            fg='#ffffff',
            activebackground=self.primary_glow,
            relief=tk.FLAT,
            bd=0,
            pady=10,
            command=save_commands,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="✖ CANCEL",
            font=("Consolas", 11),
            bg='#1a1f2e',
            fg='#e0e6ed',
            activebackground='#333333',
            relief=tk.FLAT,
            bd=0,
            pady=10,
            command=settings_window.destroy,
            cursor="hand2"
        )
        cancel_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    def _open_qa_editor(self):
        """Open Q&A database editor dialog."""
        qa_window = tk.Toplevel(self.root)
        qa_window.title("Q&A Database Editor")
        qa_window.geometry("900x700")
        qa_window.configure(bg='#0a0e1a')
        
        # Title
        title = tk.Label(
            qa_window,
            text="💬 Q&A DATABASE EDITOR",
            font=("Consolas", 16, "bold"),
            bg='#0a0e1a',
            fg=self.text_color
        )
        title.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(
            qa_window,
            text="Add your own questions and answers for Jarvis to respond with.\nJarvis checks this database FIRST, before processing other commands.\nRestart Jarvis to load changes.",
            font=("Consolas", 9),
            bg='#0a0e1a',
            fg='#e0e6ed',
            justify=tk.LEFT
        )
        instructions.pack(pady=5)
        
        # Text editor
        editor_frame = tk.Frame(qa_window, bg=self.secondary_glow, bd=2)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        text_editor = scrolledtext.ScrolledText(
            editor_frame,
            font=("Consolas", 10),
            bg='#1a1f2e',
            fg='#e0e6ed',
            insertbackground=self.text_color,
            selectbackground=self.secondary_glow,
            bd=0,
            padx=10,
            pady=10
        )
        text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Load current Q&A database
        try:
            qa_path = get_resource_path('custom_qa.yaml')
            if not os.path.exists(qa_path):
                # Fallback to current directory
                qa_path = 'custom_qa.yaml'
            
            with open(qa_path, 'r', encoding='utf-8') as f:
                content = f.read()
                text_editor.insert('1.0', content)
        except Exception as e:
            text_editor.insert('1.0', f"# Error loading custom_qa.yaml: {e}\n# Create the file manually or restart Jarvis")
        
        # Save button
        def save_qa():
            try:
                content = text_editor.get('1.0', tk.END)
                qa_path = get_resource_path('custom_qa.yaml')
                if not os.path.exists(qa_path):
                    # Save to current directory if bundled path not writable
                    qa_path = 'custom_qa.yaml'
                
                with open(qa_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.logger.info("Q&A database saved")
                qa_window.destroy()
            except Exception as e:
                self.logger.error(f"Error saving Q&A: {str(e)}")
        
        button_frame = tk.Frame(qa_window, bg='#0a0e1a')
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        save_btn = tk.Button(
            button_frame,
            text="💾 SAVE Q&A DATABASE",
            font=("Consolas", 11, "bold"),
            bg=self.secondary_glow,
            fg='#ffffff',
            activebackground=self.primary_glow,
            relief=tk.FLAT,
            bd=0,
            pady=10,
            command=save_qa,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="✖ CANCEL",
            font=("Consolas", 11),
            bg='#1a1f2e',
            fg='#e0e6ed',
            activebackground='#333333',
            relief=tk.FLAT,
            bd=0,
            pady=10,
            command=qa_window.destroy,
            cursor="hand2"
        )
        cancel_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    
    def _enable_open_mic(self):
        """Enable open mic mode permanently."""
        if not self.open_mic_mode:
            self.open_mic_mode = True
            self.logger.info("Open Mic Mode ENABLED")
            
            # Start continuous listening
            self.stop_listening = False
            import threading
            self.listening_thread = threading.Thread(target=self._continuous_listening)
            self.listening_thread.daemon = True
            self.listening_thread.start()
    
    def _toggle_open_mic(self):
        """Toggle between open mic and push-to-talk mode."""
        self.open_mic_mode = not self.open_mic_mode
        
        if self.open_mic_mode:
            # Enable open mic mode
            self.logger.info("Open Mic Mode ENABLED")
            
            # Start continuous listening
            self.stop_listening = False
            import threading
            self.listening_thread = threading.Thread(target=self._continuous_listening)
            self.listening_thread.daemon = True
            self.listening_thread.start()
        else:
            # Disable open mic mode
            self._stop_open_mic()
    
    def _stop_open_mic(self):
        """Stop open mic mode and enter dormant state (still listens for wake word)."""
        self.stop_listening = True
        self.logger.info("Open Mic Mode PAUSED - Say 'jarvis' to resume")
        self.set_state("idle")
        # Don't disable open_mic_mode completely - just pause it
        # The listening loop will continue but only respond to wake word
    
    def _continuous_listening(self):
        """Continuously listen for voice input in open mic mode."""
        import time
        
        while self.open_mic_mode and not self.is_shutting_down:
            try:
                # If in dormant/stopped state, only listen for wake word
                if self.stop_listening:
                    self.set_state("idle")
                    
                    # Listen for wake word to resume
                    try:
                        # Record audio
                        text = self.jarvis.stt.recognize(bypass_activation=True)
                        
                        # Check if wake word detected
                        if text:
                            text_lower = text.lower()
                            wake_word = self.jarvis.stt.wake_word.lower()
                            
                            self.logger.debug(f"Dormant mode heard: '{text}'")
                            
                            # Check if wake word is in the text
                            if wake_word in text_lower:
                                # Wake word detected! Resume listening
                                self.stop_listening = False
                                self.logger.info("Wake word detected - Resuming listening")
                                self.add_to_history("[JARVIS is now listening...]")
                                
                                # Small delay before continuing
                                time.sleep(0.5)
                                continue
                        
                        # No wake word, continue in dormant mode
                        time.sleep(0.3)
                        
                    except Exception as e:
                        self.logger.debug(f"Wake word detection error: {e}")
                        time.sleep(0.5)
                    continue
                
                # Normal listening mode (not dormant)
                # Check if already processing or speaking
                if self.current_state in ['thinking', 'speaking']:
                    time.sleep(0.1)
                    continue
                
                # Skip listening if TTS is currently speaking (prevent audio feedback)
                if self.jarvis.tts.is_speaking:
                    time.sleep(0.1)
                    continue
                
                # Listen for input
                self.set_state("listening")
                
                # Use try-except for STT in case it fails
                try:
                    # Pass bypass_activation=True to skip key press in open mic mode
                    text = self.jarvis.stt.recognize(bypass_activation=True)
                except Exception as e:
                    self.logger.error(f"STT error: {e}")
                    time.sleep(0.5)
                    continue
                
                # Check if we got actual speech (not just silence or noise)
                # Filter out very short or nonsensical transcriptions
                if text and len(text.strip()) > 0:
                    # Additional validation: ignore single words or very short phrases
                    word_count = len(text.strip().split())
                    if word_count < 2 or len(text.strip()) < 5:
                        # Too short - likely background noise
                        self.logger.debug(f"Ignoring short transcription: {text}")
                        self.set_state("idle")
                        time.sleep(0.3)
                        continue
                    
                    self.logger.info(f"You: {text}")
                    self.set_state("thinking")
                    
                    try:
                        response = self.jarvis.process_input(text)
                        
                        self.logger.info(f"Jarvis: {response}")
                        self.set_state("speaking")
                        
                        # Speak the response with interrupt capability
                        self.jarvis._speak_with_interrupt(response)
                        
                        # Check if shutdown was triggered
                        if self.is_shutting_down:
                            self.logger.info("Shutdown detected - exiting listening loop")
                            self.open_mic_mode = False
                            break
                        
                        # IMPORTANT: Wait for TTS to fully complete before continuing
                        # This prevents the mic from picking up Jarvis's own voice
                        time.sleep(1)  # Extra buffer after speaking
                        
                        # Reset state to idle after speaking completes
                        self.set_state("idle")
                    except Exception as e:
                        self.logger.error(f"Processing error: {e}")
                        self.set_state("idle")
                        time.sleep(1)
                        continue
                    
                    # Brief pause before listening again
                    time.sleep(0.5)
                else:
                    # No speech detected or empty text, return to idle and try again
                    self.set_state("idle")
                    time.sleep(0.3)
                    
            except Exception as e:
                self.logger.error(f"Error in continuous listening: {e}", exc_info=True)
                self.set_state("idle")
                time.sleep(1)
        
        # Cleanup when stopping
        self.set_state("idle")
    
    def run(self):
        """Start the UI main loop."""
        self.logger.info("Starting HUD interface")
        
        # Run main loop
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.logger.info("HUD closed by user")
        except Exception as e:
            self.logger.error(f"UI error: {e}", exc_info=True)
        finally:
            # Stop open mic if active
            if self.open_mic_mode:
                self.stop_listening = True
                if self.listening_thread and self.listening_thread.is_alive():
                    self.listening_thread.join(timeout=2)
            # Shutdown Jarvis
            try:
                self.jarvis.shutdown()
            except Exception as e:
                self.logger.error(f"Shutdown error: {e}")
