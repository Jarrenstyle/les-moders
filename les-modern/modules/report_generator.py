#!/usr/bin/env python3
"""
Report Generator Module
======================
JSON, HTML ve Markdown raporu oluşturma modülü
"""

import os
import json
from datetime import datetime
from jinja2 import Template
from rich.console import Console

console = Console()

class ReportGenerator:
    def __init__(self, output_dir):
        self.output_dir = output_dir
    
    def generate_json_report(self, system_info, exploits):
        """JSON formatında rapor oluştur"""
        report_data = {
            'report_info': {
                'generated_at': datetime.now().isoformat(),
                'les_modern_version': '3.0.0-beta',
                'report_type': 'json'
            },
            'system_info': system_info,
            'exploits': {
                'total_found': len(exploits),
                'exploits': exploits
            },
            'summary': self._generate_summary(system_info, exploits)
        }
        
        filename = os.path.join(self.output_dir, 'les_modern_report.json')
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            return filename
        except Exception as e:
            console.print(f"[red]JSON report error: {str(e)}[/red]")
            return None
    
    def generate_html_report(self, system_info, exploits):
        """HTML formatında rapor oluştur"""
        html_template = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LES-Modern Raporu</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .severity-critical { background-color: #dc3545; color: white; }
        .severity-high { background-color: #fd7e14; color: white; }
        .severity-medium { background-color: #ffc107; color: black; }
        .severity-low { background-color: #6c757d; color: white; }
        .exploit-card { margin-bottom: 15px; }
        .system-info { background-color: #f8f9fa; padding: 20px; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="container mt-5">
        <!-- Header -->
        <div class="row">
            <div class="col-12">
                <div class="card bg-primary text-white mb-4">
                    <div class="card-body text-center">
                        <h1><i class="fas fa-shield-alt"></i> LES-Modern Raporu</h1>
                        <p class="mb-0">Linux Exploit Suggester 2025 - Güvenlik Analiz Raporu</p>
                        <small>Oluşturulma: {{ report_time }}</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Özet -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card text-white bg-info">
                    <div class="card-body text-center">
                        <h5><i class="fas fa-server"></i> Sistem</h5>
                        <h3>{{ system_info.distro.name or 'Bilinmiyor' }}</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-warning">
                    <div class="card-body text-center">
                        <h5><i class="fas fa-cog"></i> Kernel</h5>
                        <h3>{{ system_info.kernel.release }}</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-danger">
                    <div class="card-body text-center">
                        <h5><i class="fas fa-bug"></i> Exploitler</h5>
                        <h3>{{ exploits|length }}</h3>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-success">
                    <div class="card-body text-center">
                        <h5><i class="fas fa-exclamation-triangle"></i> Critical</h5>
                        <h3>{{ critical_count }}</h3>
                    </div>
                </div>
            </div>
        </div>

        <!-- Sistem Bilgileri -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-info-circle"></i> Sistem Bilgileri</h5>
                    </div>
                    <div class="card-body system-info">
                        <div class="row">
                            <div class="col-md-6">
                                <h6>Kernel Bilgileri</h6>
                                <ul>
                                    <li><strong>Release:</strong> {{ system_info.kernel.release }}</li>
                                    <li><strong>Version:</strong> {{ system_info.kernel.version }}</li>
                                    <li><strong>Architecture:</strong> {{ system_info.kernel.architecture }}</li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h6>Kullanıcı Bilgileri</h6>
                                <ul>
                                    <li><strong>Kullanıcı:</strong> {{ system_info.security.user.username }}</li>
                                    <li><strong>UID:</strong> {{ system_info.security.user.uid }}</li>
                                    <li><strong>Gruplar:</strong> {{ system_info.security.user.groups }}</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Exploitler -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-bug"></i> Bulunan Exploitler ({{ exploits|length }})</h5>
                    </div>
                    <div class="card-body">
                        {% if exploits %}
                            {% for exploit in exploits %}
                            <div class="card exploit-card">
                                <div class="card-header d-flex justify-content-between align-items-center">
                                    <h6 class="mb-0">{{ loop.index }}. {{ exploit.name }}</h6>
                                    <span class="badge severity-{{ exploit.severity.lower() }}">
                                        {{ exploit.severity }}
                                    </span>
                                </div>
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-8">
                                            <p><strong>CVE:</strong> {{ exploit.cve or 'N/A' }}</p>
                                            <p><strong>Açıklama:</strong> {{ exploit.description }}</p>
                                            <p><strong>Yıl:</strong> {{ exploit.year or 'N/A' }}</p>
                                        </div>
                                        <div class="col-md-4">
                                            {% if exploit.exploit_url and exploit.exploit_url != 'N/A' %}
                                            <a href="{{ exploit.exploit_url }}" class="btn btn-outline-primary btn-sm" target="_blank">
                                                <i class="fas fa-external-link-alt"></i> Exploit Kodu
                                            </a>
                                            {% endif %}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            {% endfor %}
                        {% else %}
                            <div class="alert alert-success" role="alert">
                                <i class="fas fa-check-circle"></i> Bu sistem için potansiyel exploit bulunamadı.
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="row mt-5">
            <div class="col-12">
                <div class="card bg-light">
                    <div class="card-body text-center">
                        <small class="text-muted">
                            <i class="fas fa-shield-alt"></i> LES-Modern v3.0.0-beta | 
                            Sadece eğitim amaçlı kullanılmalıdır | 
                            <i class="fas fa-clock"></i> {{ report_time }}
                        </small>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
        """
        
        # Critical exploit sayısını hesapla
        critical_count = sum(1 for e in exploits if e.get('severity') == 'CRITICAL')
        
        template = Template(html_template)
        html_content = template.render(
            system_info=system_info,
            exploits=exploits,
            critical_count=critical_count,
            report_time=datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        )
        
        filename = os.path.join(self.output_dir, 'les_modern_report.html')
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return filename
        except Exception as e:
            console.print(f"[red]HTML report error: {str(e)}[/red]")
            return None
    
    def generate_markdown_report(self, system_info, exploits):
        """Markdown formatında rapor oluştur"""
        md_template = """#  LES-Modern Güvenlik Raporu

> **Linux Exploit Suggester 2025** - Modern Güvenlik Analiz Raporu  
> **Oluşturulma:** {{ report_time }}  
> **Versiyon:** LES-Modern v3.0.0-beta

---

##  Sistem Özeti

| Özellik | Değer |
|---------|-------|
| **Dağıtım** | {{ system_info.distro.name or 'Bilinmiyor' }} |
| **Kernel** | {{ system_info.kernel.release }} |
| **Mimari** | {{ system_info.kernel.architecture }} |
| **Kullanıcı** | {{ system_info.security.user.username }} (UID: {{ system_info.security.user.uid }}) |
| **Bulunan Exploit** | {{ exploits|length }} |

---

##  Sistem Detayları

###  Kernel Bilgileri
- **Release:** `{{ system_info.kernel.release }}`
- **Version:** `{{ system_info.kernel.version }}`
- **Machine:** `{{ system_info.kernel.machine }}`
- **Platform:** `{{ system_info.kernel.platform }}`

###  Dağıtım Bilgileri
{% if system_info.distro %}
{% for key, value in system_info.distro.items() %}
- **{{ key.title() }}:** {{ value }}
{% endfor %}
{% endif %}

###  Güvenlik Bilgileri
- **Kullanıcı:** {{ system_info.security.user.username }}
- **Gruplar:** {{ system_info.security.user.groups }}
- **Sudo Erişimi:** {% if 'sudo' in system_info.security.sudo %}✅ Var{% else %}❌ Yok{% endif %}

---

##  Bulunan Exploitler ({{ exploits|length }})

{% if exploits %}
{% for exploit in exploits %}
### {{ loop.index }}. {{ exploit.name }}

| Özellik | Değer |
|---------|-------|
| **CVE** | `{{ exploit.cve or 'N/A' }}` |
| **Severity** | {% if exploit.severity == 'CRITICAL' %} **CRITICAL**{% elif exploit.severity == 'HIGH' %} **HIGH**{% elif exploit.severity == 'MEDIUM' %} **MEDIUM**{% else %}⚪ **LOW**{% endif %} |
| **Yıl** | {{ exploit.year or 'N/A' }} |
| **Açıklama** | {{ exploit.description }} |
| **Exploit URL** | {% if exploit.exploit_url and exploit.exploit_url != 'N/A' %}[Exploit Kodu]({{ exploit.exploit_url }}){% else %}N/A{% endif %} |

{% if exploit.match_reason %}
> **Eşleşme Nedeni:** {{ exploit.match_reason }}
{% endif %}

---
{% endfor %}
{% else %}
###  İyi Haber!

Bu sistem için potansiyel exploit bulunamadı. Sistem görece güvenli görünüyor.

> **Not:** Bu sonuç, sistemin %100 güvenli olduğu anlamına gelmez. Düzenli güvenlik güncellemeleri yapmaya devam edin.
{% endif %}

---

##  Güvenlik Önerileri

###  Genel Öneriler
1. **Sistem Güncellemeleri:** Düzenli olarak `apt update && apt upgrade` veya dağıtımınıza uygun komutları çalıştırın
2. **Kernel Güncellemeleri:** Mümkün olduğunca güncel kernel versiyonunu kullanın
3. **Güvenlik Yamaları:** Kritik güvenlik yamalarını hızlıca uygulayın
4. **Minimal Yetki:** Gereksiz root erişimlerini sınırlayın

###  Acil Önlemler
{% set critical_exploits = exploits | selectattr("severity", "equalto", "CRITICAL") | list %}
{% if critical_exploits %}
** CRITICAL seviyede {{ critical_exploits|length }} exploit bulundu!**

{% for exploit in critical_exploits %}
- **{{ exploit.name }}:** {{ exploit.description }}
  - CVE: `{{ exploit.cve }}`
  - Hemen güncelleme yapın: {% if exploit.package_check %}`apt update && apt upgrade {{ exploit.package_check }}`{% else %}Kernel güncellemesi{% endif %}
{% endfor %}
{% else %}
 Critical seviyede exploit bulunamadı.
{% endif %}

---

##  Yasal Uyarı

Bu rapor **sadece eğitim ve güvenlik değerlendirmesi amaçlı** oluşturulmuştur.

-  Kendi sahip olduğunuz sistemlerde
-  Yasal penetrasyon testlerinde  
-  Eğitim laboratuvarlarında

** Yasadışı kullanım kesinlikle yasaktır!**

---

*Bu rapor LES-Modern v3.0.0-beta tarafından oluşturulmuştur.*  
*GitHub: [LES-Modern](https://github.com/example/les-modern)*
"""
        
        template = Template(md_template)
        md_content = template.render(
            system_info=system_info,
            exploits=exploits,
            report_time=datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        )
        
        filename = os.path.join(self.output_dir, 'les_modern_report.md')
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(md_content)
            return filename
        except Exception as e:
            console.print(f"[red]Markdown report error: {str(e)}[/red]")
            return None
    
    def _generate_summary(self, system_info, exploits):
        """Rapor özeti oluştur"""
        summary = {
            'total_exploits': len(exploits),
            'severity_breakdown': {
                'critical': sum(1 for e in exploits if e.get('severity') == 'CRITICAL'),
                'high': sum(1 for e in exploits if e.get('severity') == 'HIGH'),
                'medium': sum(1 for e in exploits if e.get('severity') == 'MEDIUM'),
                'low': sum(1 for e in exploits if e.get('severity') == 'LOW')
            },
            'newest_exploit_year': max([e.get('year', 2000) for e in exploits]) if exploits else None,
            'kernel_version': system_info.get('kernel', {}).get('release', 'Unknown'),
            'distro': system_info.get('distro', {}).get('name', 'Unknown'),
            'risk_level': self._calculate_risk_level(exploits)
        }
        
        return summary
    
    def _calculate_risk_level(self, exploits):
        """Risk seviyesini hesapla"""
        if not exploits:
            return 'LOW'
        
        critical_count = sum(1 for e in exploits if e.get('severity') == 'CRITICAL')
        high_count = sum(1 for e in exploits if e.get('severity') == 'HIGH')
        
        if critical_count > 0:
            return 'CRITICAL'
        elif high_count >= 3:
            return 'HIGH'
        elif high_count > 0:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def generate_all_reports(self, data, output_dir):
        """Tüm rapor formatlarını oluştur"""
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            # JSON raporu
            json_file = self.generate_json_report(
                data.get('system_info', {}), 
                data.get('vulnerability_analysis', {}), 
                output_dir
            )
            
            # HTML raporu  
            html_file = self.generate_html_report(
                data.get('system_info', {}), 
                data.get('vulnerability_analysis', {}), 
                output_dir
            )
            
            # Markdown raporu
            md_file = self.generate_markdown_report(
                data.get('system_info', {}), 
                data.get('vulnerability_analysis', {}), 
                output_dir
            )
            
            console.print(f"[green]JSON report: {json_file}[/green]")
            console.print(f"[green]HTML report: {html_file}[/green]") 
            console.print(f"[green]Markdown report: {md_file}[/green]")
            
            return True
            
        except Exception as e:
            console.print(f"[red]Report generation failed: {str(e)}[/red]")
            return False 
