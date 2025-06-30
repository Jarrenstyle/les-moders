#!/usr/bin/env python3
"""
LES-Modern - Linux Exploit Suggester 2025
==========================================
Dynamic Internet-based CVE and Exploit Analysis System
"""

import os
import sys
import argparse
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.text import Text

# Modülleri import et
from modules.system_info import SystemInfoCollector
from modules.dynamic_exploit_checker import DynamicExploitChecker
from modules.report_generator import ReportGenerator

console = Console()

class LESModern:
    def __init__(self):
        self.version = "3.0"
        self.banner = self._create_banner()
        
    def _create_banner(self):
        """Professional banner oluştur"""
        banner_text = f"""
LES-Modern v{self.version} - Linux Exploit Suggester
Dynamic CVE and Exploit Analysis System
Real-time vulnerability assessment for Linux systems
        """
        return Panel(
            Text(banner_text.strip(), justify="center"),
            style="bold cyan",
            border_style="blue"
        )
    
    def display_security_warning(self):
        """Güvenlik uyarısını göster"""
        warning = """
IMPORTANT SECURITY AND LEGAL NOTICE

This tool is designed for authorized security testing and educational purposes only.

Usage Guidelines:
- Only use on systems you own or have explicit written permission to test
- Comply with all applicable laws and regulations in your jurisdiction
- Use responsibly and ethically for defensive security purposes
- Do not use for malicious activities or unauthorized access attempts

Legal Disclaimer:
- Users are solely responsible for their actions and compliance with laws
- This tool is provided "as is" without warranties
- Authors assume no liability for misuse or damage

By proceeding, you acknowledge understanding and agreement to these terms.
        """
        
        console.print(Panel(
            Text(warning.strip(), justify="left"),
            title="SECURITY WARNING",
            style="bold red",
            border_style="red"
        ))
        
        try:
            response = input("\nDo you understand and agree to these terms? (yes/no): ").lower().strip()
            if response not in ['yes', 'y']:
                console.print("[red]Exiting due to user disagreement with terms.[/red]")
                sys.exit(1)
        except KeyboardInterrupt:
            console.print("\n[red]Exiting...[/red]")
            sys.exit(1)
    
    def check_system_compatibility(self):
        """Sistem uyumluluğunu kontrol et"""
        if sys.platform != 'linux':
            console.print("[red]ERROR: This tool only works on Linux systems[/red]")
            console.print("[yellow]Detected platform: {sys.platform}[/yellow]")
            console.print("[cyan]This tool analyzes Linux kernel vulnerabilities and requires Linux to function properly.[/cyan]")
            sys.exit(1)
    
    def run_analysis(self, args):
        """Ana analiz sürecini çalıştır"""
        console.print(self.banner)
        console.print(f"\n[cyan]Starting analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/cyan]\n")
        
        try:
            # Sistem bilgilerini topla
            console.print("[bold]Step 1/3: Collecting system information[/bold]")
            system_collector = SystemInfoCollector(verbose=args.verbose)
            system_info = system_collector.collect_all()
            
            if not system_info:
                console.print("[red]Failed to collect system information[/red]")
                return False
            
            # Dinamik exploit analizi
            console.print("\n[bold]Step 2/3: Dynamic vulnerability analysis[/bold]")
            exploit_checker = DynamicExploitChecker(verbose=args.verbose)
            analysis_results = exploit_checker.analyze_system(system_info)
            
            if not analysis_results:
                console.print("[red]Failed to perform vulnerability analysis[/red]")
                return False
            
            # Sonuçları göster
            console.print("\n[bold]Step 3/3: Generating reports and displaying results[/bold]")
            exploit_checker.display_results(analysis_results)
            
            # Rapor oluştur
            if args.output:
                report_generator = ReportGenerator()
                
                # Birleşik veri hazırla
                combined_data = {
                    'system_info': system_info,
                    'vulnerability_analysis': analysis_results,
                    'scan_metadata': {
                        'scan_time': datetime.now().isoformat(),
                        'les_version': self.version,
                        'scan_type': 'dynamic_internet_based'
                    }
                }
                
                # Raporları oluştur
                success = report_generator.generate_all_reports(combined_data, args.output)
                if success:
                    console.print(f"\n[green]Reports generated successfully in: {args.output}[/green]")
                    
                    # CVE linklerini de kaydet
                    exploit_checker.export_cve_links(analysis_results, args.output)
            
            # Özet bilgi
            console.print(f"\n[bold green]Analysis completed successfully![/bold green]")
            
            if 'exploit_summary' in analysis_results:
                summary = analysis_results['exploit_summary']
                console.print(f"[cyan]Found {summary['total_cves']} CVEs for your kernel version[/cyan]")
                
                if summary['by_severity']['CRITICAL'] > 0:
                    console.print(f"[bold red]WARNING: {summary['by_severity']['CRITICAL']} CRITICAL vulnerabilities found![/bold red]")
                elif summary['by_severity']['HIGH'] > 0:
                    console.print(f"[orange1]CAUTION: {summary['by_severity']['HIGH']} HIGH severity vulnerabilities found[/orange1]")
                else:
                    console.print("[green]No critical vulnerabilities detected[/green]")
            
            return True
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Analysis interrupted by user[/yellow]")
            return False
        except Exception as e:
            console.print(f"[red]Analysis failed: {str(e)}[/red]")
            if args.verbose:
                import traceback
                console.print(f"[dim]{traceback.format_exc()}[/dim]")
            return False
    
    def run_test_mode(self, args):
        """Test modunu çalıştır"""
        console.print("[cyan]Running in test mode...[/cyan]")
        
        # Internet bağlantısını test et
        from modules.cve_fetcher import CVEFetcher
        cve_fetcher = CVEFetcher(verbose=True)
        
        console.print("\n[bold]Testing internet connectivity and API access:[/bold]")
        connection_ok = cve_fetcher.test_connection()
        
        if connection_ok:
            console.print("[green]All API endpoints are accessible[/green]")
            
            # Test kernel version ile CVE arama
            console.print("\n[bold]Testing CVE search with sample kernel version:[/bold]")
            test_cves = cve_fetcher.search_kernel_cves("5.15.0")
            
            if test_cves:
                console.print(f"[green]Successfully found {len(test_cves)} CVEs for test kernel[/green]")
                console.print("Sample CVE results:")
                for i, cve in enumerate(test_cves[:3], 1):
                    console.print(f"  {i}. {cve['cve_id']} - CVSS: {cve.get('cvss_score', 0):.1f}")
            else:
                console.print("[yellow]No CVEs found for test kernel (this might be normal)[/yellow]")
        else:
            console.print("[red]Internet connectivity or API access issues detected[/red]")
            console.print("[yellow]The tool will fall back to offline mode during analysis[/yellow]")
        
        console.print("\n[green]Test mode completed[/green]")
        return True

def main():
    parser = argparse.ArgumentParser(
        description="LES-Modern v3.0 - Dynamic Linux Exploit Suggester",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py                          # Basic system analysis
  python3 main.py -v                       # Verbose analysis
  python3 main.py -o /tmp/security_report  # Generate reports
  python3 main.py --test                   # Test internet connectivity
  python3 main.py --no-warning             # Skip security warning (for automation)

Report Formats:
  - JSON: machine-readable vulnerability data
  - HTML: professional web-based report with charts
  - Markdown: documentation-friendly format
  - TXT: CVE and exploit links for easy access
        """
    )
    
    parser.add_argument('-v', '--verbose', 
                       action='store_true',
                       help='Enable verbose output and debugging')
    
    parser.add_argument('-o', '--output',
                       type=str,
                       help='Output directory for reports (creates if not exists)')
    
    parser.add_argument('--test',
                       action='store_true',
                       help='Run connectivity and API tests')
    
    parser.add_argument('--no-warning',
                       action='store_true',
                       help='Skip security warning (for automation)')
    
    parser.add_argument('--version',
                       action='version',
                       version='LES-Modern v3.0')
    
    args = parser.parse_args()
    
    # LES-Modern instance oluştur
    les = LESModern()
    
    # Sistem uyumluluğunu kontrol et
    les.check_system_compatibility()
    
    # Test modu
    if args.test:
        return les.run_test_mode(args)
    
    # Güvenlik uyarısı göster
    if not args.no_warning:
        les.display_security_warning()
    
    # Ana analizi çalıştır
    success = les.run_analysis(args)
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Program interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Fatal error: {str(e)}[/red]")
        sys.exit(1) 