import base64
import sys
from rich.console import Console

console = Console()

class CodeProtection:
    def __init__(self):
        self.required_data = self._load_protected_data()
        if not self.verify_integrity():
            self._show_tampering_message()
            sys.exit(1)
    
    def _load_protected_data(self):
        protected = {
            'dev_info': 'Z2l0aHViOiB3aG9JbW0=|ZGlzY29yZDogcGFseWFjMA==',
            'version': 'djIuMC1hZHZhbmNlZA==',
            'signature': 'c3lud2VhdmUtc2VjdXJpdHktc2lnbmF0dXJl'
        }
        
        decoded = {}
        for key, value in protected.items():
            parts = value.split('|')
            decoded_parts = []
            for part in parts:
                try:
                    decoded_parts.append(base64.b64decode(part).decode('utf-8'))
                except:
                    decoded_parts.append("")
            decoded[key] = decoded_parts
        
        return decoded
    
    def _show_tampering_message(self):
        console.print("\n" + "═" * 80)
        console.print("[bold red]🚫 SYSTEM SECURITY VIOLATION / SİSTEM GÜVENLİK İHLALİ[/bold red]")
        console.print("═" * 80)
        
        console.print("\n[yellow]⚠️  WARNING: This SynWeave copy has been modified![/yellow]")
        console.print("[yellow]⚠️  UYARI: Bu SynWeave kopyası değiştirilmiş![/yellow]")
        
        console.print("\n[white]• Developer information cannot be changed[/white]")
        console.print("[white]• Geliştirici bilgileri değiştirilemez[/white]")
        
        console.print("\n[white]• Banner names are protected[/white]")
        console.print("[white]• Banner'daki isimler korumalıdır[/white]")
        
        console.print("\n[white]• Code integrity has been violated[/white]") 
        console.print("[white]• Kod bütünlüğü ihlal edilmiş[/white]")
        
        console.print("\n[red]❌ Changing developer names is unethical and disrespectful![/red]")
        console.print("[red]❌ Geliştirici isimlerini değiştirmek etik değildir ve saygısızlıktır![/red]")
        
        console.print("\n[cyan]✅ Please use the original SynWeave version from official sources:[/cyan]")
        console.print("[cyan]✅ Lütfen orijinal SynWeave sürümünü resmi kaynaklardan kullanın:[/cyan]")
        
        console.print("\n[green]   github: whoImm[/green]")
        console.print("[green]   discord: palyac0[/green]")
        
        console.print("\n[red]❌ Application closing... / Uygulama kapatılıyor...[/red]")
        console.print("═" * 80)
    
    def verify_integrity(self):
        required_checks = [
            self._check_developer_info(),
            self._check_version(),
            self._check_signature(),
            self._check_banner_file()
        ]
        
        return all(required_checks)
    
    def _check_developer_info(self):
        dev_info = self.required_data.get('dev_info', [])
        return (len(dev_info) >= 2 and 
                "github: whoImm" in dev_info and 
                "discord: palyac0" in dev_info)
    
    def _check_banner_file(self):
        try:
            from ascii.arts import BANNER
            banner_ok = ("github: whoImm" in BANNER and 
                        "discord: palyac0" in BANNER and
                        "SYNWEAVE" in BANNER)
            return banner_ok
        except:
            return False
    
    def _check_version(self):
        version = self.required_data.get('version', [''])[0]
        return version.startswith('v2.0')
    
    def _check_signature(self):
        signature = self.required_data.get('signature', [''])[0]
        return "synweave-security" in signature
    
    def get_developer_info(self):
        return self.required_data.get('dev_info', [])