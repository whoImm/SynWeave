import os
import time
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from core.pattern_detector import AdvancedPatternDetector

console = Console()

class NumberPasswordAnalyzer:
    def __init__(self):
        self.pattern_detector = AdvancedPatternDetector()
        
    def calculate_password_score(self, password):
        if not password.isdigit():
            return 0
            
        length = len(password)
        if not 3 <= length <= 8:
            return 0

        analysis = self.pattern_detector.analyze_password(password)
        return analysis['total_score']
    
    def _detect_pattern_type(self, password):
        if not password.isdigit() or not 3 <= len(password) <= 8:
            return "Invalid"
            
        breakdown = self.pattern_detector.get_detailed_breakdown(password)
        return breakdown['risk_level']
    
    def analyze_wordlist(self, input_file_path):
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"Dosya bulunamadı: {input_file_path}")
        
        console.print(f"[cyan]📁 Analyzing: {os.path.basename(input_file_path)}[/cyan]")
        console.print(f"[yellow]🔍 Using Advanced Pattern Detection System (50-point scale)[/yellow]")
        console.print()

        try:
            with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as file:
                passwords = [line.strip() for line in file if line.strip()]
        except UnicodeDecodeError:
            with open(input_file_path, 'r', encoding='latin-1', errors='ignore') as file:
                passwords = [line.strip() for line in file if line.strip()]
        
        if not passwords:
            raise ValueError("File is empty!")
        
        valid_passwords = [pwd for pwd in passwords if pwd.isdigit() and 3 <= len(pwd) <= 8]
        invalid_count = len(passwords) - len(valid_passwords)
        
        if invalid_count > 0:
            console.print(f"[yellow]⚠️  Skipped {invalid_count} invalid passwords[/yellow]")
        
        total_passwords = len(valid_passwords)
        
        if total_passwords == 0:
            raise ValueError("No valid 3-8 digit passwords found!")
        
        console.print(f"[green]✅ Total valid passwords: {total_passwords}[/green]")
        console.print()
        scored_passwords = []
        
        with Progress() as progress:
            task = progress.add_task("[green]🔬 Advanced pattern analysis...", total=total_passwords)
            
            for i, password in enumerate(valid_passwords, 1):
                score = self.calculate_password_score(password)
                pattern_type = self._detect_pattern_type(password)
                scored_passwords.append((password, score, pattern_type))
                progress.update(task, advance=1)

                if i % 100 == 0:
                    progress.update(task, description=f"[green]Analyzed {i}/{total_passwords}")

        scored_passwords.sort(key=lambda x: x[1], reverse=True)
        
        return scored_passwords
    
    def display_analysis_results(self, scored_passwords, original_count):
        console.print()
        console.print(Panel.fit(
            Text("✅ ADVANCED ANALYSIS COMPLETE!", style="bold green"),
            style="green"
        ))
        
        if not scored_passwords:
            console.print("[red]No passwords to analyze![/red]")
            return

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Metric", style="white", width=25)
        table.add_column("Value", style="yellow", width=25)
        
        total_scored = len(scored_passwords)
        avg_score = sum(score for _, score, _ in scored_passwords) / total_scored
        max_score = scored_passwords[0][1] if scored_passwords else 0
        min_score = scored_passwords[-1][1] if scored_passwords else 0

        risk_levels = {
            "🚨 ÇOK YÜKSEK RİSK (40-50)": 0,
            "⚠️ YÜKSEK RİSK (30-39)": 0,
            "🎯 ORTA RİSK (20-29)": 0,
            "✅ DÜŞÜK RİSK (10-19)": 0,
            "🛡️  GÜVENLİ (0-9)": 0
        }
        
        for _, score, risk in scored_passwords:
            if score >= 40:
                risk_levels["🚨 ÇOK YÜKSEK RİSK (40-50)"] += 1
            elif score >= 30:
                risk_levels["⚠️ YÜKSEK RİSK (30-39)"] += 1
            elif score >= 20:
                risk_levels["🎯 ORTA RİSK (20-29)"] += 1
            elif score >= 10:
                risk_levels["✅ DÜŞÜK RİSK (10-19)"] += 1
            else:
                risk_levels["🛡️  GÜVENLİ (0-9)"] += 1

        
        table.add_row("Total Valid Passwords", str(total_scored))
        table.add_row("Average Risk Score", f"{avg_score:.1f}/50")
        table.add_row("Highest Risk Score", f"{max_score}/50")
        table.add_row("Lowest Risk Score", f"{min_score}/50")
        table.add_row("Analysis System", "Advanced Pattern Detection")
        
        console.print(table)
        
        console.print("\n[bold cyan]📊 RISK DISTRIBUTION:[/bold cyan]")
        risk_table = Table(show_header=True, header_style="bold green")
        risk_table.add_column("Risk Level", style="white", width=30)
        risk_table.add_column("Count", style="yellow", width=10)
        risk_table.add_column("Percentage", style="cyan", width=15)
        risk_table.add_column("Status", style="magenta", width=20)
        
        for level, count in risk_levels.items():
            percentage = (count / total_scored) * 100 if total_scored > 0 else 0
            status = "🟥 CRITICAL" if "ÇOK YÜKSEK" in level else \
                    "🟧 HIGH" if "YÜKSEK" in level else \
                    "🟨 MEDIUM" if "ORTA" in level else \
                    "🟩 LOW" if "DÜŞÜK" in level else "🟦 SAFE"
            
            risk_table.add_row(level, str(count), f"{percentage:.1f}%", status)
        
        console.print(risk_table)

        console.print("\n[bold red]🔥 TOP 20 HIGHEST RISK PASSWORDS:[/bold red]")
        top_table = Table(show_header=True, header_style="bold red")
        top_table.add_column("Rank", style="cyan", width=6)
        top_table.add_column("Password", style="white", width=12)
        top_table.add_column("Risk Score", style="red", width=12)
        top_table.add_column("Risk Level", style="yellow", width=20)
        top_table.add_column("Pattern Analysis", style="magenta", width=30)
        
        for i, (password, score, risk_level) in enumerate(scored_passwords[:20], 1):
            breakdown = self.pattern_detector.get_detailed_breakdown(password)
            pattern_details = self._get_pattern_summary(breakdown)
            
            top_table.add_row(
                str(i), 
                password, 
                f"{score}/50", 
                risk_level,
                pattern_details
            )
        
        console.print(top_table)
        console.print("\n[bold cyan]🔍 SAMPLE PATTERN ANALYSIS:[/bold cyan]")
        self._show_sample_analysis(scored_passwords)
    
    def _get_pattern_summary(self, breakdown):
        details = breakdown['details']
        high_risk_factors = []
        
        for key, value in details.items():
            score = float(value.split('/')[0])
            if score >= 3:
                factor_name = key.replace('_analysis', '').replace('_', ' ').title()
                high_risk_factors.append(factor_name)
        
        if high_risk_factors:
            return ", ".join(high_risk_factors[:2])
        else:
            return "Low risk factors"
    
    def _show_sample_analysis(self, scored_passwords):
        if len(scored_passwords) < 3:
            return
            
        samples = [
            scored_passwords[0],
            scored_passwords[len(scored_passwords)//2],
            scored_passwords[-1]
        ]
        
        for i, (password, score, risk_level) in enumerate(samples):
            if i == 0:
                title = "🎯 HIGHEST RISK EXAMPLE"
                style = "red"
            elif i == 1:
                title = "📊 AVERAGE RISK EXAMPLE" 
                style = "yellow"
            else:
                title = "🛡️  LOWEST RISK EXAMPLE"
                style = "green"
            
            console.print(f"\n[bold {style}]{title}:[/bold {style}]")
            breakdown = self.pattern_detector.get_detailed_breakdown(password)
            
            sample_table = Table(show_header=True, header_style=f"bold {style}")
            sample_table.add_column("Password", style="white")
            sample_table.add_column("Total Score", style=style)
            sample_table.add_column("Risk Level", style=style)
            
            sample_table.add_row(password, f"{score}/50", risk_level)
            console.print(sample_table)

            detail_table = Table(show_header=True, header_style=f"bold {style}")
            detail_table.add_column("Factor", style="white", width=20)
            detail_table.add_column("Score", style=style, width=15)
            detail_table.add_column("Analysis", style="cyan", width=35)
            
            for factor, analysis in breakdown['details'].items():
                factor_name = factor.replace('_analysis', '').replace('_', ' ').title()
                score_part, desc = analysis.split(' - ', 1)
                detail_table.add_row(factor_name, score_part, desc)
            
            console.print(detail_table)
    
    def save_optimized_list(self, scored_passwords, original_filename):
        output_dir = "wordlists/output"
        os.makedirs(output_dir, exist_ok=True)
        
        base_name = os.path.splitext(original_filename)[0]
        output_filename = f"{base_name}_optimized_v2.txt"
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(f"# Optimized by SynWeave Advanced Pattern Detection\n")
            file.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"# Total passwords: {len(scored_passwords)}\n")
            file.write(f"# Sorting: Highest to Lowest Risk\n")
            file.write("# Format: password | risk_score | risk_level\n")
            file.write("\n")
            
            for password, score, risk_level in scored_passwords:
                file.write(f"{password} | {score}/50 | {risk_level}\n")

        clean_filename = f"{base_name}_clean_optimized.txt"
        clean_path = os.path.join(output_dir, clean_filename)
        
        with open(clean_path, 'w', encoding='utf-8') as file:
            for password, score, risk_level in scored_passwords:
                file.write(password + '\n')
        
        return output_path, clean_path
    
    def quick_analyze(self, password):
        if not password.isdigit() or not 3 <= len(password) <= 8:
            return {"error": "Geçersiz şifre. 3-8 haneli rakam olmalı."}
        
        breakdown = self.pattern_detector.get_detailed_breakdown(password)
        console.print(f"\n[bold cyan]🔍 QUICK ANALYSIS: {password}[/bold cyan]")
        result_table = Table(show_header=True, header_style="bold green")
        result_table.add_column("Metric", style="white")
        result_table.add_column("Value", style="yellow")
        result_table.add_row("Password", password)
        result_table.add_row("Total Risk Score", f"{breakdown['total_score']}/50")
        result_table.add_row("Risk Level", breakdown['risk_level'])
        result_table.add_row("Length", str(len(password)))
        console.print(result_table)
        console.print("\n[bold cyan]📊 DETAILED BREAKDOWN:[/bold cyan]")
        detail_table = Table(show_header=True, header_style="bold blue")
        detail_table.add_column("Risk Factor", style="white", width=25)
        detail_table.add_column("Score", style="yellow", width=10)
        detail_table.add_column("Description", style="cyan", width=35)
        
        for factor, analysis in breakdown['details'].items():
            factor_name = factor.replace('_analysis', '').replace('_', ' ').title()
            score_part, desc = analysis.split(' - ', 1)
            detail_table.add_row(factor_name, score_part, desc)
        
        console.print(detail_table)
        
        return breakdown