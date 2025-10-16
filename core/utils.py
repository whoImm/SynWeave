import time
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.text import Text

console = Console()

def clear_screen():
    console.clear()

def print_slow(text, delay=0.015, color="white"):
    if hasattr(text, 'plain'):
        for char in text.plain:
            console.print(f"[{color}]{char}[/{color}]", end="", highlight=False)
            sys.stdout.flush()
            time.sleep(delay)
        console.print()
    else:
        for char in text:
            console.print(f"[{color}]{char}[/{color}]", end="", highlight=False)
            sys.stdout.flush()
            time.sleep(delay)
        console.print()

def print_fast(text, color="white"):
    console.print(f"[{color}]{text}[/{color}]")

def animate_loading(text="Loading", duration=2):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start_time = time.time()
    frame_count = 0
    
    while time.time() - start_time < duration:
        frame = frames[frame_count % len(frames)]
        console.print(f"[yellow]{frame}[/yellow] [cyan]{text}[/cyan]", end="\r")
        frame_count += 1
        time.sleep(0.1)
    
    console.print(f"[green]✓ {text} Complete![/green]")

def get_choice(prompt_text, choices):
    return Prompt.ask(f"[cyan]{prompt_text}[/cyan]", choices=choices)

def press_enter_to_continue():
    console.print()
    Prompt.ask("[yellow]Press Enter to continue[/yellow]", default="")