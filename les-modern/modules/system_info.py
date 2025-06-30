#!/usr/bin/env python3
"""
System Information Collector
=============================
Linux sistemlerden kapsamlı bilgi toplama modülü
"""

import os
import json
import subprocess
import platform
import psutil
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn

console = Console()

class SystemInfoCollector:
    def __init__(self, verbose=False):
        self.verbose = verbose
        
    def _run_command(self, command, shell=True):
        """Güvenli komut çalıştırma"""
        try:
            if self.verbose:
                console.print(f"[dim]Running: {command}[/dim]")
            
            result = subprocess.run(
                command, 
                shell=shell, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            return result.stdout.strip() if result.returncode == 0 else ""
        except subprocess.TimeoutExpired:
            if self.verbose:
                console.print(f"[yellow]Timeout: {command}[/yellow]")
            return ""
        except Exception as e:
            if self.verbose:
                console.print(f"[red]Error: {command} - {str(e)}[/red]")
            return ""
    
    def collect_kernel_info(self, manual_kernel=None):
        """Kernel bilgilerini topla"""
        kernel_info = {}
        
        if manual_kernel:
            kernel_info['release'] = manual_kernel
            kernel_info['source'] = 'manual'
        else:
            kernel_info['release'] = self._run_command('uname -r')
            kernel_info['source'] = 'uname'
        
        kernel_info['version'] = self._run_command('uname -v')
        kernel_info['machine'] = self._run_command('uname -m')
        kernel_info['platform'] = platform.platform()
        kernel_info['architecture'] = platform.architecture()[0]
        
        return kernel_info
    
    def collect_distro_info(self):
        """Dağıtım bilgilerini topla"""
        distro_info = {}
        
        # /etc/os-release
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        distro_info[key.lower()] = value.strip('"')
        except FileNotFoundError:
            pass
        
        # lsb_release
        lsb_info = self._run_command('lsb_release -a 2>/dev/null')
        if lsb_info:
            distro_info['lsb_release'] = lsb_info
        
        # Fallback
        if not distro_info:
            distro_info['name'] = platform.system()
            distro_info['version'] = platform.release()
        
        return distro_info
    
    def collect_package_info(self):
        """Paket bilgilerini topla"""
        packages = {}
        
        # Debian/Ubuntu - dpkg
        dpkg_output = self._run_command('dpkg -l 2>/dev/null | grep ^ii')
        if dpkg_output:
            packages['dpkg'] = self._parse_dpkg_output(dpkg_output)
        
        # RedHat/CentOS - rpm
        rpm_output = self._run_command('rpm -qa 2>/dev/null')
        if rpm_output:
            packages['rpm'] = self._parse_rpm_output(rpm_output)
        
        # Snap packages
        snap_output = self._run_command('snap list 2>/dev/null')
        if snap_output:
            packages['snap'] = self._parse_snap_output(snap_output)
        
        return packages
    
    def _parse_dpkg_output(self, output):
        """dpkg -l çıktısını parse et"""
        packages = []
        for line in output.split('\n'):
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    packages.append({
                        'name': parts[1],
                        'version': parts[2],
                        'description': ' '.join(parts[3:]) if len(parts) > 3 else ''
                    })
        return packages
    
    def _parse_rpm_output(self, output):
        """rpm -qa çıktısını parse et"""
        packages = []
        for line in output.split('\n'):
            if line.strip():
                # rpm paket formatı: name-version-release.arch
                parts = line.rsplit('-', 2)
                if len(parts) >= 2:
                    packages.append({
                        'name': parts[0],
                        'version': f"{parts[1]}-{parts[2]}" if len(parts) == 3 else parts[1],
                        'full_name': line
                    })
        return packages
    
    def _parse_snap_output(self, output):
        """snap list çıktısını parse et"""
        packages = []
        lines = output.split('\n')[1:]  # Header'ı atla
        for line in lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    packages.append({
                        'name': parts[0],
                        'version': parts[1],
                        'rev': parts[2] if len(parts) > 2 else '',
                        'tracking': parts[3] if len(parts) > 3 else ''
                    })
        return packages
    
    def collect_security_info(self):
        """Güvenlik ile ilgili bilgileri topla"""
        security_info = {}
        
        # Kullanıcı bilgileri
        security_info['user'] = {
            'username': self._run_command('whoami'),
            'uid': os.getuid() if hasattr(os, 'getuid') else 'N/A',
            'gid': os.getgid() if hasattr(os, 'getgid') else 'N/A',
            'groups': self._run_command('groups'),
            'id_output': self._run_command('id')
        }
        
        # Sudo bilgileri
        security_info['sudo'] = self._run_command('sudo -l 2>/dev/null || echo "sudo erişimi yok"')
        
        # SUID dosyalar (sadece bazıları)
        security_info['suid_files'] = self._run_command('find /usr/bin /bin /usr/sbin /sbin -perm -4000 -type f 2>/dev/null | head -20')
        
        # Çevre değişkenleri (önemli olanlar)
        important_envs = ['PATH', 'HOME', 'USER', 'SHELL', 'TERM']
        security_info['environment'] = {env: os.environ.get(env, '') for env in important_envs}
        
        return security_info
    
    def collect_system_status(self):
        """Sistem durumu bilgileri"""
        status_info = {}
        
        # CPU ve Memory
        status_info['cpu'] = {
            'count': psutil.cpu_count(),
            'usage_percent': psutil.cpu_percent(interval=1)
        }
        
        memory = psutil.virtual_memory()
        status_info['memory'] = {
            'total': memory.total,
            'available': memory.available,
            'percent_used': memory.percent
        }
        
        # Disk bilgileri
        disk = psutil.disk_usage('/')
        status_info['disk'] = {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent_used': (disk.used / disk.total) * 100
        }
        
        # Mount points
        status_info['mounts'] = self._run_command('mount | grep -E "^/dev" | head -10')
        
        # Aktif servisler (systemd)
        status_info['services'] = self._run_command('systemctl list-units --type=service --state=active --no-pager --no-legend | head -15')
        
        return status_info
    
    def collect_all_info(self, manual_kernel=None):
        """Tüm sistem bilgilerini topla"""
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            task = progress.add_task("System analysis...", total=6)
            
            system_info = {
                'timestamp': datetime.now().isoformat(),
                'les_modern_version': '3.0.0-beta'
            }
            
            # Kernel information
            progress.update(task, advance=1, description="Collecting kernel information...")
            system_info['kernel'] = self.collect_kernel_info(manual_kernel)
            
            # Distribution information
            progress.update(task, advance=1, description="Collecting distribution information...")
            system_info['distro'] = self.collect_distro_info()
            
            # Package information
            progress.update(task, advance=1, description="Collecting package list...")
            system_info['packages'] = self.collect_package_info()
            
            # Security information
            progress.update(task, advance=1, description="Collecting security information...")
            system_info['security'] = self.collect_security_info()
            
            # System status
            progress.update(task, advance=1, description="Collecting system status...")
            system_info['system_status'] = self.collect_system_status()
            
            progress.update(task, advance=1, description="Analysis completed!")
        
        return system_info
    
    def save_to_json(self, system_info, filename):
        """Sistem bilgilerini JSON dosyasına kaydet"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(system_info, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            console.print(f"[red]JSON save error: {str(e)}[/red]")
            return False 