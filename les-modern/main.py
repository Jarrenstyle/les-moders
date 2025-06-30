#!/usr/bin/env python3
"""
LES-Modern - Linux Exploit Suggester 2025
==========================================
Modern Python versiyonu - CVE-2024/2025 uyumlu gelişmiş exploit suggester
"""

import click
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rich_print
from modules.system_info import SystemInfoCollector
from modules.exploit_checker import ExploitChecker
from modules.report_generator import ReportGenerator

VERSION = "3.0.0-beta"
console = Console()

def print_banner():
    """Professional banner display"""
    banner_text = f"""
LES-Modern v{VERSION}
Linux Exploit Suggester 2025
CVE-2024/2025 Compatible Version
    """
    console.print(Panel(banner_text, border_style="cyan", expand=False))

def show_security_warning():
    """Security warning display"""
    warning_text = """
[bold red]SECURITY WARNING[/bold red]

This tool is developed for [bold yellow]EDUCATIONAL PURPOSES ONLY[/bold yellow].
Exploit usage is permitted on:
- Your own systems
- Authorized penetration tests
- Educational laboratories

[bold red]ILLEGAL USE IS STRICTLY PROHIBITED![/bold red]
User accepts all legal responsibility.
    """
    console.print(Panel(warning_text, border_style="red", expand=False))
    
    if not click.confirm("\nDo you read and accept the legal warning?"):
        console.print("[bold red]Operation cancelled.[/bold red]")
        sys.exit(1)

@click.command()
@click.option('--kernel', '-k', help='Manual kernel version (e.g. 5.15.0)')
@click.option('--output-dir', '-o', default='output', help='Output directory')
@click.option('--json-report', is_flag=True, help='Generate JSON report')
@click.option('--html-report', is_flag=True, help='Generate HTML report')
@click.option('--markdown-report', is_flag=True, help='Generate Markdown report')
@click.option('--download', '-d', is_flag=True, help='Download exploit codes')
@click.option('--danger-mode', is_flag=True, help='POC test mode (DANGEROUS)')
@click.option('--no-warning', is_flag=True, help='Skip security warning')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def main(kernel, output_dir, json_report, html_report, markdown_report, 
         download, danger_mode, no_warning, verbose):
    """
    LES-Modern - 2025 Compatible Linux Exploit Suggester
    
    Modern Python-based exploit suggestion tool
    """
    
    print_banner()
    
    # Güvenlik uyarısı
    if not no_warning:
        show_security_warning()
    
    # Çıktı klasörünü oluştur
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Collect system information
        console.print("\n[bold cyan]Collecting system information...[/bold cyan]")
        system_collector = SystemInfoCollector(verbose=verbose)
        system_info = system_collector.collect_all_info(manual_kernel=kernel)
        
        # Save system information to JSON
        system_info_file = os.path.join(output_dir, "system_info.json")
        system_collector.save_to_json(system_info, system_info_file)
        console.print(f"System information saved: [green]{system_info_file}[/green]")
        
        # Display kernel information
        kernel_version = system_info.get('kernel', {}).get('release', 'Unknown')
        distro_name = system_info.get('distro', {}).get('name', 'Unknown')
        console.print(f"\n[bold yellow]Target System:[/bold yellow] {distro_name}")
        console.print(f"[bold yellow]Kernel Version:[/bold yellow] {kernel_version}")
        
        # Exploit checking
        console.print("\n[bold cyan]Scanning exploit database...[/bold cyan]")
        exploit_checker = ExploitChecker(verbose=verbose)
        exploits = exploit_checker.find_exploits(system_info)
        
        if not exploits:
            console.print("[bold red]No suitable exploits found for this system.[/bold red]")
            return
        
        # Display results
        console.print(f"\n[bold green]{len(exploits)} potential exploits found![/bold green]\n")
        exploit_checker.display_exploits(exploits)
        
        # Report generation
        if json_report or html_report or markdown_report:
            console.print("\n[bold cyan]Generating reports...[/bold cyan]")
            report_generator = ReportGenerator(output_dir)
            
            if json_report:
                json_file = report_generator.generate_json_report(system_info, exploits)
                console.print(f"JSON report: [green]{json_file}[/green]")
            
            if html_report:
                html_file = report_generator.generate_html_report(system_info, exploits)
                console.print(f"HTML report: [green]{html_file}[/green]")
            
            if markdown_report:
                md_file = report_generator.generate_markdown_report(system_info, exploits)
                console.print(f"Markdown report: [green]{md_file}[/green]")
        
        # Exploit download
        if download and exploits:
            console.print("\n[bold cyan]Exploit download menu...[/bold cyan]")
            exploit_checker.download_exploits(exploits, output_dir)
        
        # Danger mode warning
        if danger_mode:
            console.print("\n[bold red]DANGER MODE - POC tests active![/bold red]")
            console.print("[yellow]This feature is under development...[/yellow]")
        
        console.print("\n[bold green]Analysis completed![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[bold red]Operation cancelled by user.[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Error occurred: {str(e)}[/bold red]")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 