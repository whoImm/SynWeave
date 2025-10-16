import time
import random
from rich.console import Console
from rich.text import Text

console = Console()

class Animations:
    def __init__(self, console):
        self.console = console
    
    def typewriter_effect(self, text, delay=0.03, color="white"):
        for char in text:
            self.console.print(f"[{color}]{char}[/{color}]", end="", highlight=False)
            time.sleep(delay)
        self.console.print()
    
    def monochrome_ascii_art(self, art, base_delay=0.002):
        gray_colors = ["bright_white", "white", "bright_black", "dim white"]
        
        lines = art.split('\n')
        for i, line in enumerate(lines):
            if line.strip():
                color = gray_colors[i % len(gray_colors)]
                for char in line:
                    self.console.print(f"[{color}]{char}[/{color}]", end="", highlight=False)
                    time.sleep(base_delay)
                self.console.print()
            else:
                self.console.print()
    
    def gradient_gray_art(self, art, base_delay=0.0016):
        lines = art.split('\n')
        total_lines = len([line for line in lines if line.strip()])
        
        line_count = 0
        for line in lines:
            if line.strip():
                intensity = line_count / total_lines
                if intensity < 0.33:
                    color = "bright_white"
                elif intensity < 0.66:
                    color = "white"
                else:
                    color = "bright_black"
                
                for char in line:
                    self.console.print(f"[{color}]{char}[/{color}]", end="", highlight=False)
                    time.sleep(base_delay)
                self.console.print()
                line_count += 1
            else:
                self.console.print()
    
    def matrix_ascii_art(self, art, base_delay=0.0012):
        lines = art.split('\n')
        for line in lines:
            if line.strip():
                for char in line:
                    green_shades = ["bright_green", "green", "dim green"]
                    color = random.choice(green_shades) if char != ' ' else "black"
                    self.console.print(f"[{color}]{char}[/{color}]", end="", highlight=False)
                    time.sleep(base_delay)
                self.console.print()
            else:
                self.console.print()
    
    def ultra_fast_ascii_art(self, art, base_delay=0.0005):
        lines = art.split('\n')
        for line in lines:
            if line.strip():
                color = "bright_white"
                self.console.print(f"[{color}]{line}[/{color}]")
                time.sleep(base_delay * 10)
            else:
                self.console.print()
    
    def random_dark_art(self, arts_list):
        art = random.choice(arts_list)

        dark_styles = [self.monochrome_ascii_art, self.gradient_gray_art, self.matrix_ascii_art, self.ultra_fast_ascii_art]
        style = random.choice(dark_styles)
        style(art)
        
        return art
    
    def loading_animation(self, frames, delay=0.2):
        for frame in frames:
            self.console.print(f"[bright_white]{frame}[/bright_white]", end="\r")
            time.sleep(delay)
        self.console.print()
    
    def matrix_rain(self, duration=2):
        width = 50
        height = 10
        chars = "01█▓▒░║╬╔╗╝╚╣╠"
        
        start_time = time.time()
        while time.time() - start_time < duration:
            self.console.clear()
            for i in range(height):
                line = "".join(random.choice(chars) for _ in range(width))
                colored_line = ""
                for j, char in enumerate(line):
                    green_intensity = ["bright_green", "green", "dim green"]
                    color = random.choice(green_intensity)
                    colored_line += f"[{color}]{char}[/{color}]"
                self.console.print(colored_line)
            time.sleep(0.1)
    
    def dark_banner(self, text, delay=0.002):
        colors = ["bright_white", "white", "bright_black"]
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            self.console.print(f"[{color}]{char}[/{color}]", end="", highlight=False)
            time.sleep(delay)
        self.console.print()
    
    def instant_ascii_art(self, art):
        colors = ["bright_white", "white", "bright_black"]
        lines = art.split('\n')
        for i, line in enumerate(lines):
            if line.strip():
                color = colors[i % len(colors)]
                self.console.print(f"[{color}]{line}[/{color}]")
            else:
                self.console.print()