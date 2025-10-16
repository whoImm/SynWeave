import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm
from core.utils import clear_screen, print_slow, print_fast, animate_loading, get_choice, press_enter_to_continue
from ascii.arts import BANNER, SYNWEAVE_ARTS, LOADING_FRAMES
from ascii.animations import Animations
from core.analyzer import NumberPasswordAnalyzer
from core.protection import CodeProtection

console = Console()

class MenuSystem:
    def __init__(self):
        self.animations = Animations(console)
        self.analyzer = NumberPasswordAnalyzer()
        self.protection = CodeProtection()
    
    def show_welcome_screen(self):
        clear_screen()

        self.animations.random_dark_art(SYNWEAVE_ARTS)
        console.print()
        self.animations.dark_banner(BANNER)
        console.print()
        self.animations.loading_animation(LOADING_FRAMES)
        console.print()
    
    def show_test_screen(self):
        clear_screen()
        
        console.print(Panel.fit(
            Text("🧪 ADVANCED PASSWORD ANALYZER", style="bold bright_white"),
            style="white"
        ))
        console.print()
        
        try:
            input_dir = "wordlists/input"
            os.makedirs(input_dir, exist_ok=True)
            
            files = [f for f in os.listdir(input_dir) if f.lower().endswith('.txt')]
            
            if not files:
                console.print("[yellow]📁 No .txt files found in 'wordlists/input' folder[/yellow]")
                console.print()
                console.print(Text("Please add your wordlist files to the folder:", style="white"))
                console.print(Text(f"📂 {os.path.abspath(input_dir)}", style="cyan"))
                console.print()
                console.print(Text("Or enter a custom file path manually:", style="yellow"))
                custom_path = Prompt.ask("[bright_white]📁 Custom file path (or press Enter to go back)[/bright_white]")
                
                if not custom_path:
                    return
                    
                file_path = custom_path.strip('"\'')
            else:
                console.print(Text("📂 Available wordlist files:", style="bold bright_white"))
                console.print()
                
                file_table = Table(show_header=True, header_style="bold cyan")
                file_table.add_column("#", style="bright_white", width=6)
                file_table.add_column("File Name", style="white")
                file_table.add_column("Size", style="yellow")
                file_table.add_column("Modified", style="dim white")
                
                for i, filename in enumerate(files, 1):
                    file_path_full = os.path.join(input_dir, filename)
                    file_size = os.path.getsize(file_path_full)
                    mod_time = os.path.getmtime(file_path_full)
                    mod_date = time.strftime('%Y-%m-%d', time.localtime(mod_time))
                    

                    if file_size < 1024:
                        size_str = f"{file_size} B"
                    elif file_size < 1024*1024:
                        size_str = f"{file_size/1024:.1f} KB"
                    else:
                        size_str = f"{file_size/(1024*1024):.1f} MB"
                    
                    file_table.add_row(str(i), filename, size_str, mod_date)
                
                console.print(file_table)
                console.print()

                choices = [str(i) for i in range(1, len(files) + 1)] + ['c', 'b']
                console.print(Text("Select a file to analyze:", style="bright_white"))
                console.print(Text("1-" + str(len(files)) + " : Select file by number", style="white"))
                console.print(Text("c : Custom file path", style="cyan"))
                console.print(Text("b : Back to main menu", style="yellow"))
                console.print()
                
                selection = Prompt.ask("[bright_white]🎯 Your choice[/bright_white]", choices=choices)
                
                if selection == 'b':
                    return
                elif selection == 'c':
                    console.print()
                    console.print(Text("Enter custom file path:", style="white"))
                    custom_path = Prompt.ask("[bright_white]📁 File path[/bright_white]")
                    file_path = custom_path.strip('"\'')
                else:

                    selected_index = int(selection) - 1
                    selected_file = files[selected_index]
                    file_path = os.path.join(input_dir, selected_file)

            if not os.path.exists(file_path):
                console.print(f"[red]❌ File not found: {file_path}[/red]")
                press_enter_to_continue()
                return
            
            console.print()
            console.print(f"[green]✅ Selected: {os.path.basename(file_path)}[/green]")

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    total_lines = len(lines)
                    numeric_lines = sum(1 for line in lines if line.strip().isdigit() and 3 <= len(line.strip()) <= 8)
                
                console.print(f"[cyan]📊 File stats: {total_lines} total lines, {numeric_lines} valid passwords (3-8 digits)[/cyan]")
            except:
                console.print("[yellow]⚠️  Could not read file stats[/yellow]")
            
            console.print()
            if not Confirm.ask("[yellow]🚀 Start advanced analysis?[/yellow]"):
                return
            console.print()
            console.print("[cyan]🚀 Starting advanced pattern analysis...[/cyan]")
            console.print("[yellow]🔍 Using 50-point risk scoring system...[/yellow]")
            console.print()
            scored_passwords = self.analyzer.analyze_wordlist(file_path)
            self.analyzer.display_analysis_results(scored_passwords, len(scored_passwords))
            console.print()
            save_choice = Confirm.ask("[yellow]💾 Save optimized wordlist?[/yellow]")
            
            if save_choice:
                output_path, clean_path = self.analyzer.save_optimized_list(scored_passwords, os.path.basename(file_path))
                console.print(f"[green]✅ Detailed list saved to: {output_path}[/green]")
                console.print(f"[green]✅ Clean list saved to: {clean_path}[/green]")
                console.print()
                console.print("[cyan]📋 First 10 passwords in optimized list:[/cyan]")
                for i, (password, score, pattern) in enumerate(scored_passwords[:10], 1):
                    console.print(f"  {i:2d}. {password} (Risk: {score}/50) - {pattern}")
                    
            else:
                console.print("[yellow]⚠️  Optimized list not saved[/yellow]")
            
        except Exception as e:
            console.print(f"[red]❌ Error: {str(e)}[/red]")
            import traceback
            console.print(f"[red]Details: {traceback.format_exc()}[/red]")
        
        press_enter_to_continue()

    def show_info_screen(self):
        clear_screen()
        
        console.print(Panel.fit(
            Text("📚 ABOUT SYNWEAVE", style="bold bright_white"),
            style="white"
        ))
        console.print()

        dev_info = self.protection.get_developer_info()
        
        info_texts = [
            Text("🔥 SynWeave - Advanced Password Intelligence", style="bold bright_white"),
            "",
            Text("📖 Purpose:", style="bright_white"),
            "• Advanced numeric password pattern recognition",
            "• 50-point risk scoring system for optimal sorting", 
            "• Enhances efficiency of security testing tools",
            "• 8-factor comprehensive password analysis",
            "",
            Text("🎯 How it works:", style="bright_white"),
            "1. Upload your .txt wordlist file",
            "2. SynWeave performs deep pattern analysis",
            "3. Scores passwords 0-50 based on 8 risk factors",
            "4. Sorts from highest to lowest probability",
            "5. Export optimized wordlist with risk scores",
            "",
            Text("⚡ Advanced Scoring System (0-50 points):", style="bright_white"),
            "• Length Analysis (0-8p): Shorter = higher risk",
            "• Sequential Patterns (0-7p): 123456, 654321", 
            "• Repetition Analysis (0-6p): 111111, 112233, 121212",
            "• Keyboard Patterns (0-6p): 147258, 159357, QWERTY",
            "• Entropy Analysis (0-8p): Low randomness = high risk",
            "• Social Engineering (0-7p): Birth years, dates, common",
            "• Cultural References (0-5p): 777, 888, 666, 1313",
            "• Geographic Patterns (0-3p): Plate codes, area codes",
            "",
            Text("📊 Risk Levels:", style="bright_white"),
            "• 40-50: 🚨 VERY HIGH RISK - Immediate priority",
            "• 30-39: ⚠️ HIGH RISK - First wave attempts", 
            "• 20-29: 🎯 MEDIUM RISK - Secondary attempts",
            "• 10-19: ✅ LOW RISK - Tertiary attempts",
            "• 0-9:  🛡️ SAFE - Last resort attempts",
            "",
            Text("👨‍💻 Developer Information:", style="bright_white")
        ]

        for info in dev_info:
            info_texts.append(Text(f"• {info}", style="bright_white"))
        
        info_texts.extend([
            "",
            Text("🔒 Protected System: This software is secured against unauthorized modification.", style="yellow")
        ])
        
        for text in info_texts:
            if isinstance(text, Text):
                print_fast(text)
            else:
                print_slow(text, 0.015, "white")
            time.sleep(0.1)
        
        press_enter_to_continue()
    
    def show_guide_screen(self):
        clear_screen()
        
        console.print(Panel.fit(
            Text("📖 USER GUIDE", style="bold bright_white"),
            style="white"
        ))
        console.print()
        
        guide_steps = [
            Text("Step-by-Step Usage:", style="bold bright_white"),
            "",
            Text("1. Select 'Test' from main menu", style="white"),
            Text("2. Choose your wordlist file", style="white"), 
            Text("3. Wait for advanced analysis to complete", style="white"),
            Text("4. View optimization results with risk scores", style="white"),
            Text("5. Export sorted wordlist (high risk first)", style="white"),
            "",
            Text("Supported Formats:", style="bold bright_white"),
            "• .txt files",
            "• One word per line", 
            "• Only numeric passwords (0-9)",
            "• 3-8 characters long",
            "",
            Text("Output:", style="bold bright_white"),
            "• Optimized wordlist (highest risk first)",
            "• Detailed analysis report with 50-point scores", 
            "• Risk probability scores and pattern analysis",
            "• Two versions: Detailed and Clean"
        ]
        
        for step in guide_steps:
            if isinstance(step, Text):
                print_fast(step)
            else:
                print_slow(step, 0.015, "white")
            time.sleep(0.1)
        
        press_enter_to_continue()
    
    def show_results_screen(self):
        clear_screen()
        
        console.print(Panel.fit(
            Text("📊 PATTERN EXAMPLES & RISK SCORES", style="bold bright_white"),
            style="white"
        ))
        console.print()
        
        print_slow(Text("Common numeric password patterns and their risk scores (0-50):", style="white"), 0.015)
        console.print()

        examples = [
            ("111111", "Same digits", "46/50", "🚨 VERY HIGH"),
            ("123456", "Sequential", "44/50", "🚨 VERY HIGH"),
            ("19951995", "Birth year repeat", "38/50", "⚠️ HIGH"),
            ("000000", "All zeros", "45/50", "🚨 VERY HIGH"),
            ("147258", "Keyboard vertical", "32/50", "⚠️ HIGH"),
            ("112233", "Pair repetition", "40/50", "🚨 VERY HIGH"),
            ("777777", "Cultural lucky", "42/50", "🚨 VERY HIGH"),
            ("123123", "Pattern repeat", "39/50", "⚠️ HIGH"),
            ("34025", "Random medium", "18/50", "✅ LOW"),
            ("529384", "Random secure", "8/50", "🛡️ SAFE")
        ]
        
        table = Table(show_header=True, header_style="bold bright_white")
        table.add_column("Password", style="white", width=10)
        table.add_column("Pattern Type", style="cyan", width=20)
        table.add_column("Risk Score", style="red", width=10)
        table.add_column("Risk Level", style="yellow", width=15)
        
        for password, pattern, score, risk in examples:
            table.add_row(password, pattern, score, risk)
        
        console.print(table)
        console.print()
        
        console.print(Text("💡 Tip: Higher risk scores indicate passwords that should be tried first!", style="yellow"))
        console.print(Text("🔒 Security: System protected against unauthorized modification", style="green"))
        console.print()
        
        press_enter_to_continue()
    
    def show_main_menu(self):
        clear_screen()
        
        console.print(Panel.fit(
            Text("🏠 SYNWEAVE MAIN MENU", style="bold bright_white"),
            style="white"
        ))
        console.print()

        menu_options = [
            Text("1. 🧪 Test - Advanced wordlist analysis", style="white"),
            Text("2. 📚 Info - About SynWeave", style="white"),
            Text("3. 📖 Guide - How to use", style="white"), 
            Text("4. 📊 Results - View risk examples", style="white"),
            Text("5. 🚪 Exit - Close application", style="white")
        ]
        
        for option in menu_options:
            print_slow(option, 0.03)
            time.sleep(0.2)
        
        console.print()
        console.print(Text("🔒 Secured System | 50-Point Risk Analysis | Advanced Pattern Detection", style="dim cyan"))
        console.print()
    
    def quick_analyze_single(self):
        clear_screen()
        
        console.print(Panel.fit(
            Text("🔍 QUICK PASSWORD ANALYSIS", style="bold bright_white"),
            style="white"
        ))
        console.print()
        
        console.print(Text("Enter a numeric password to analyze (3-8 digits):", style="white"))
        password = Prompt.ask("[bright_white]🔢 Password[/bright_white]")
        
        if not password or not password.isdigit() or not 3 <= len(password) <= 8:
            console.print("[red]❌ Invalid password! Must be 3-8 digits.[/red]")
            press_enter_to_continue()
            return

        self.analyzer.quick_analyze(password)
        press_enter_to_continue()
    
    def exit_animation(self):
        clear_screen()
        
        print_slow(Text("Shutting down SynWeave Advanced...", style="red"))
        console.print()
        
        self.animations.matrix_rain(1.5)
        dev_info = self.protection.get_developer_info()
        dev_text = "\n".join([f"• {info}" for info in dev_info]) if dev_info else "• github: whoImm\n• discord: palyac0"
        
        console.print(Panel.fit(
            Text("Thank you for using SynWeave Advanced!", style="bold red") + "\n\n" +
            dev_text + "\n\n" +
            "🔒 Protected System v1.0",
            style="red"
        ))
        
        time.sleep(1)