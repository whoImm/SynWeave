import time
from rich.console import Console
from core.menu import MenuSystem
from core.utils import get_choice

console = Console()

class SynWeaveInterface:
    def __init__(self):
        self.menu = MenuSystem()
    
    def run(self):
        try:
            self.menu.show_welcome_screen()
            time.sleep(1)
            
            while True:
                self.menu.show_main_menu()
                
                choice = get_choice("Select an option (1-5)", ["1", "2", "3", "4", "5"])
                
                if choice == "1":
                    self.menu.show_test_screen()
                elif choice == "2":
                    self.menu.show_info_screen()
                elif choice == "3":
                    self.menu.show_guide_screen()
                elif choice == "4":
                    self.menu.show_results_screen()
                elif choice == "5":
                    self.menu.exit_animation()
                    break
                else:
                    console.print("[red]Invalid option![/red]")
                    time.sleep(1)
        
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Interrupted by user...[/yellow]")
            self.menu.exit_animation()