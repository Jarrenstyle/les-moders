#!/usr/bin/env python3
"""
CVE Fetcher Module
==================
Internet-based CVE and exploit fetching system
"""

import requests
import json
import re
import time
from datetime import datetime, timedelta
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class CVEFetcher:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'LES-Modern/3.0 Security Scanner'
        })
        
        # API endpoints
        self.nvd_api = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.exploitdb_api = "https://www.exploit-db.com/search"
        self.vulners_api = "https://vulners.com/api/v3/search/lucene/"
        self.cve_details_base = "https://www.cvedetails.com"
    
    def search_kernel_cves(self, kernel_version):
        """Kernel versiyonu için CVE'leri ara"""
        console.print(f"[cyan]Searching CVEs for kernel {kernel_version}...[/cyan]")
        
        all_cves = []
        
        # NIST NVD'den ara
        nvd_cves = self._search_nvd_cves(kernel_version)
        if nvd_cves:
            all_cves.extend(nvd_cves)
        
        # Vulners API'dan ara
        vulners_cves = self._search_vulners_cves(kernel_version)
        if vulners_cves:
            all_cves.extend(vulners_cves)
        
        # Duplicate CVE'leri temizle
        unique_cves = self._remove_duplicate_cves(all_cves)
        
        # Exploit linklerini bul
        for cve in unique_cves:
            cve['exploits'] = self._find_exploits_for_cve(cve['cve_id'])
        
        return sorted(unique_cves, key=lambda x: x.get('cvss_score', 0), reverse=True)
    
    def _search_nvd_cves(self, kernel_version):
        """NIST NVD API'dan CVE ara"""
        try:
            major_minor = '.'.join(kernel_version.split('.')[:2])
            
            params = {
                'keywordSearch': f'linux kernel {major_minor}',
                'resultsPerPage': 50,
                'startIndex': 0
            }
            
            if self.verbose:
                console.print("[dim]Querying NIST NVD API...[/dim]")
            
            response = self._make_request(self.nvd_api, params=params)
            if not response:
                return []
            
            data = response.json()
            cves = []
            
            for item in data.get('vulnerabilities', []):
                cve_data = item.get('cve', {})
                cve_id = cve_data.get('id', '')
                
                # Kernel ile ilgili olup olmadığını kontrol et
                descriptions = cve_data.get('descriptions', [])
                description = ''
                for desc in descriptions:
                    if desc.get('lang') == 'en':
                        description = desc.get('value', '')
                        break
                
                if 'linux' in description.lower() and 'kernel' in description.lower():
                    # CVSS skorunu al
                    cvss_score = 0
                    metrics = cve_data.get('metrics', {})
                    if 'cvssMetricV31' in metrics:
                        cvss_score = metrics['cvssMetricV31'][0]['cvssData'].get('baseScore', 0)
                    elif 'cvssMetricV3' in metrics:
                        cvss_score = metrics['cvssMetricV3'][0]['cvssData'].get('baseScore', 0)
                    elif 'cvssMetricV2' in metrics:
                        cvss_score = metrics['cvssMetricV2'][0]['cvssData'].get('baseScore', 0)
                    
                    # Tarihi al
                    published = cve_data.get('published', '')
                    
                    cves.append({
                        'cve_id': cve_id,
                        'description': description[:200] + '...' if len(description) > 200 else description,
                        'cvss_score': cvss_score,
                        'severity': self._calculate_severity(cvss_score),
                        'published_date': published.split('T')[0] if published else '',
                        'source': 'NIST NVD',
                        'affected_versions': self._extract_kernel_versions(description),
                        'exploits': []
                    })
            
            return cves
            
        except Exception as e:
            if self.verbose:
                console.print(f"[red]NVD API error: {str(e)}[/red]")
            return []
    
    def _search_vulners_cves(self, kernel_version):
        """Vulners API'dan CVE ara"""
        try:
            query = f'linux AND kernel AND {kernel_version}'
            
            payload = {
                'query': query,
                'size': 30,
                'fields': ['id', 'title', 'description', 'cvss', 'published', 'type']
            }
            
            if self.verbose:
                console.print("[dim]Querying Vulners API...[/dim]")
            
            response = self._make_request(
                self.vulners_api, 
                method='POST',
                json=payload
            )
            
            if not response:
                return []
            
            data = response.json()
            cves = []
            
            for item in data.get('data', {}).get('search', []):
                doc = item.get('_source', {})
                
                if doc.get('type') == 'cve':
                    cve_id = doc.get('id', '')
                    title = doc.get('title', '')
                    description = doc.get('description', '')
                    cvss_score = doc.get('cvss', {}).get('score', 0)
                    published = doc.get('published', '')
                    
                    cves.append({
                        'cve_id': cve_id,
                        'description': description[:200] + '...' if len(description) > 200 else description,
                        'cvss_score': cvss_score,
                        'severity': self._calculate_severity(cvss_score),
                        'published_date': published.split('T')[0] if published else '',
                        'source': 'Vulners',
                        'affected_versions': self._extract_kernel_versions(f"{title} {description}"),
                        'exploits': []
                    })
            
            return cves
            
        except Exception as e:
            if self.verbose:
                console.print(f"[red]Vulners API error: {str(e)}[/red]")
            return []
    
    def _find_exploits_for_cve(self, cve_id):
        """CVE için exploit linklerini bul"""
        exploits = []
        
        try:
            # ExploitDB'den ara
            exploitdb_url = f"https://www.exploit-db.com/search?cve={cve_id}"
            
            # GitHub'dan ara
            github_search = f"https://api.github.com/search/repositories?q={cve_id}+exploit"
            
            # Basit link oluştur
            exploits.append({
                'source': 'ExploitDB',
                'url': exploitdb_url,
                'type': 'search'
            })
            
            # PacketStorm
            packetstorm_url = f"https://packetstormsecurity.com/search/?q={cve_id}"
            exploits.append({
                'source': 'PacketStorm',
                'url': packetstorm_url,
                'type': 'search'
            })
            
        except Exception as e:
            if self.verbose:
                console.print(f"[yellow]Exploit search error for {cve_id}: {str(e)}[/yellow]")
        
        return exploits
    
    def search_non_vulnerable_info(self, kernel_version):
        """Exploit olmayan kernel için genel CVE bilgisi"""
        console.print(f"[cyan]Searching general vulnerability info for kernel {kernel_version}...[/cyan]")
        
        try:
            # Genel kernel güvenlik durumunu kontrol et
            major_version = kernel_version.split('.')[0]
            
            general_info = {
                'kernel_version': kernel_version,
                'security_status': 'No critical exploits found',
                'recommendations': [
                    'Keep kernel updated to latest stable version',
                    'Monitor security advisories regularly',
                    'Apply security patches promptly',
                    'Use kernel hardening features'
                ],
                'general_cves': [],
                'kernel_eol_info': self._get_kernel_eol_info(kernel_version)
            }
            
            # Son 30 gün içindeki genel Linux kernel CVE'leri
            recent_cves = self._get_recent_kernel_cves()
            general_info['recent_cves'] = recent_cves
            
            return general_info
            
        except Exception as e:
            if self.verbose:
                console.print(f"[red]General info search error: {str(e)}[/red]")
            return None
    
    def _get_recent_kernel_cves(self):
        """Son dönem kernel CVE'lerini al"""
        try:
            # Son 30 günlük CVE'ler
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            params = {
                'keywordSearch': 'linux kernel',
                'pubStartDate': start_date.strftime('%Y-%m-%dT%H:%M:%S.000'),
                'pubEndDate': end_date.strftime('%Y-%m-%dT%H:%M:%S.000'),
                'resultsPerPage': 20
            }
            
            response = self._make_request(self.nvd_api, params=params)
            if not response:
                return []
            
            data = response.json()
            recent_cves = []
            
            for item in data.get('vulnerabilities', [])[:10]:  # Son 10 CVE
                cve_data = item.get('cve', {})
                cve_id = cve_data.get('id', '')
                
                descriptions = cve_data.get('descriptions', [])
                description = ''
                for desc in descriptions:
                    if desc.get('lang') == 'en':
                        description = desc.get('value', '')
                        break
                
                recent_cves.append({
                    'cve_id': cve_id,
                    'description': description[:150] + '...' if len(description) > 150 else description,
                    'published_date': cve_data.get('published', '').split('T')[0]
                })
            
            return recent_cves
            
        except Exception as e:
            if self.verbose:
                console.print(f"[yellow]Recent CVEs fetch error: {str(e)}[/yellow]")
            return []
    
    def _get_kernel_eol_info(self, kernel_version):
        """Kernel End-of-Life bilgisi"""
        # Basit EOL database
        kernel_eol = {
            '6.1': 'LTS - Supported until 2026',
            '5.15': 'LTS - Supported until 2026', 
            '5.10': 'LTS - Supported until 2026',
            '5.4': 'LTS - Supported until 2025',
            '4.19': 'LTS - EOL December 2024',
            '4.14': 'LTS - EOL January 2024',
            '4.9': 'LTS - EOL January 2023',
            '4.4': 'LTS - EOL February 2022'
        }
        
        major_minor = '.'.join(kernel_version.split('.')[:2])
        return kernel_eol.get(major_minor, 'Check kernel.org for support status')
    
    def _extract_kernel_versions(self, text):
        """Metinden kernel versiyonlarını çıkar"""
        pattern = r'(\d+\.\d+(?:\.\d+)?)'
        versions = re.findall(pattern, text)
        return list(set(versions))  # Tekrarları kaldır
    
    def _calculate_severity(self, cvss_score):
        """CVSS skoruna göre severity hesapla"""
        if cvss_score >= 9.0:
            return 'CRITICAL'
        elif cvss_score >= 7.0:
            return 'HIGH'
        elif cvss_score >= 4.0:
            return 'MEDIUM'
        elif cvss_score > 0:
            return 'LOW'
        else:
            return 'UNKNOWN'
    
    def _remove_duplicate_cves(self, cves):
        """Tekrar eden CVE'leri temizle"""
        seen = set()
        unique_cves = []
        
        for cve in cves:
            if cve['cve_id'] not in seen:
                seen.add(cve['cve_id'])
                unique_cves.append(cve)
        
        return unique_cves
    
    def _make_request(self, url, method='GET', **kwargs):
        """HTTP request yapma"""
        try:
            if method.upper() == 'POST':
                response = self.session.post(url, timeout=30, **kwargs)
            else:
                response = self.session.get(url, timeout=30, **kwargs)
            
            # Rate limiting
            time.sleep(0.5)
            
            if response.status_code == 200:
                return response
            else:
                if self.verbose:
                    console.print(f"[yellow]HTTP {response.status_code} for {url}[/yellow]")
                return None
                
        except requests.exceptions.RequestException as e:
            if self.verbose:
                console.print(f"[red]Request error: {str(e)}[/red]")
            return None
    
    def test_connection(self):
        """Internet bağlantısını test et"""
        test_urls = [
            "https://services.nvd.nist.gov",
            "https://vulners.com",
            "https://www.exploit-db.com"
        ]
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    console.print(f"[green]Connection OK: {url}[/green]")
                    return True
            except:
                continue
        
        console.print("[red]No internet connection or APIs unavailable[/red]")
        return False 