# LES-Modern v3.0 - Dynamic Linux Exploit Suggester

## linux-exploit-suggester-3 (v3) - Gelişmiş Sürüm
**Based on:** linux-exploit-suggester-2 by @jondonas

### Hakkında
linux-exploit-suggester-3, @jondonas tarafından geliştirilen ve Linux çekirdek sürümlerine göre olası yerel ayrıcalık yükseltme (local privilege escalation) açıklarını listeleyen LES2 (v2) aracının **2025 yılına uyarlanmış**, daha akıllı ve genişletilebilir halidir.

Bu yeni versiyon:
- **Çekirdek + Dağıtım uyumlu** analiz yapar
- **API üzerinden güncel CVE** ve ExploitDB verilerini çeker
- **Paket versiyonlarını kontrol** ederek uygulama tabanlı zafiyetler de sunar
- **JSON / HTML / Markdown** gibi raporlama çıktıları üretir

### Neden v3?
Orijinal LES2 çok güçlü bir temel sağladı, fakat günümüz güvenlik analizlerinde aşağıdaki nedenlerle yetersiz kalabiliyor:

| v2 (klasik LES) | v3 (gelişmiş versiyon) |
|-----------------|------------------------|
| Statik exploit listesi | **Dinamik CVE + ExploitDB API desteği** |
| Sadece kernel sürüm kontrolü | **OS bilgisi + dpkg/rpm + PoC önerisi** |
| CLI çıktı | **JSON / HTML / renkli terminal raporu** |
| Manuel kullanım | **Otomatik mod + modüler yapı** |
| Perl dili | **Python 3 (modern, modüler kod)** |

### Temel Özellikler
- **Kernel + OS + Paket sürümlerine** göre öneri
- **Exploit-DB ve CVE veritabanı** ile eşleşme
- **2023–2025 CVE'lerine** özel filtreleme
- **Zafiyetli paket versiyonlarına** karşı uyarı (örn. openssl, polkit, bash, sudo)
- **JSON, Markdown ve HTML** rapor çıktısı
- **Opsiyonel PoC test** desteği (isteğe bağlı)

### Kullanım Senaryosu
1. Kullanıcı hedef Linux sistemde **les-v3'ü** çalıştırır.
2. Sistem bilgisi, çekirdek ve dağıtım verisi toplanır.
3. **ExploitDB veritabanı ve CVE listesiyle** eşleştirilerek olası zafiyetler çıkarılır.
4. Kullanıcıya **renkli terminal çıktısı + JSON/HTML raporu** sunulur.

### Örnek Komutlar
```bash
# Temel analiz
python3 main.py

# Rapor oluşturma
python3 main.py -o ./reports -v

# Internet bağlantı testi
python3 main.py --test

# Detaylı güvenlik analizi
python3 main.py --no-warning -v -o /tmp/security_report
```

---

**Real-time Internet-based CVE and Exploit Analysis System**

## Overview

LES-Modern v3.0 is a revolutionary upgrade that transforms the traditional static exploit database approach into a **dynamic, internet-connected vulnerability assessment system**. Unlike static tools, LES-Modern fetches real-time CVE data from multiple authoritative sources including NIST NVD, Vulners, and ExploitDB.

## Key Features

### Dynamic CVE Fetching
- **Real-time CVE Database**: Fetches current vulnerabilities from NIST NVD API
- **Multiple Data Sources**: Integrates Vulners API, ExploitDB, and PacketStorm
- **Kernel-Specific Analysis**: Matches kernel versions with specific CVEs
- **Internet Fallback**: Gracefully handles offline scenarios

### Advanced Analysis Engine
- **CVSS Scoring**: Real CVSS scores from official databases
- **Severity Classification**: CRITICAL, HIGH, MEDIUM, LOW rankings
- **Exploit Availability**: Direct links to working exploits
- **Recent Vulnerability Tracking**: Last 30 days CVE monitoring

### Professional Reporting
- **Multiple Output Formats**: JSON, HTML, Markdown, Text
- **CVE Link Export**: Direct links to exploits and documentation
- **Executive Summaries**: Business-ready vulnerability reports
- **Technical Details**: Complete system and vulnerability analysis

## Installation

### Quick Install
```bash
# Clone repository
git clone https://github.com/your-repo/les-modern
cd les-modern

# Install dependencies
pip3 install -r requirements.txt

# Make executable
chmod +x main.py
```

### System Requirements
- **Linux System**: Required (analyzes Linux vulnerabilities)
- **Python 3.8+**: Modern Python version
- **Internet Connection**: For real-time CVE fetching
- **Root/Sudo Access**: Optional (for complete system analysis)

## Usage

### Basic Analysis
```bash
# Simple vulnerability scan
python3 main.py

# Verbose mode with detailed output
python3 main.py -v

# Generate comprehensive reports
python3 main.py -o /tmp/security_report -v
```

### Advanced Options
```bash
# Test internet connectivity and APIs
python3 main.py --test

# Automated mode (skip warnings)
python3 main.py --no-warning -o /tmp/report

# Full analysis with all reports
python3 main.py -v -o ./security_analysis
```

## Internet-Based Features

### CVE Data Sources
- **NIST NVD**: Official US government vulnerability database
- **Vulners**: Commercial vulnerability intelligence
- **ExploitDB**: Offensive Security exploit database
- **PacketStorm**: Security research and exploits

### Online vs Offline Mode
- **Online Mode**: Real-time CVE fetching with current data
- **Offline Mode**: Automatic fallback with basic analysis
- **Hybrid Mode**: Cached data with periodic updates

## Sample Output

```
LES-Modern v3.0 - Linux Exploit Suggester
Dynamic CVE and Exploit Analysis System

Step 1/3: Collecting system information
✓ Kernel version: 5.15.0-91-generic
✓ Distribution: Ubuntu 22.04.3 LTS
✓ Package analysis: 2,847 packages scanned

Step 2/3: Dynamic vulnerability analysis
Searching CVEs for kernel 5.15.0...
✓ Found 23 potential vulnerabilities

Step 3/3: Generating reports and displaying results

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                    Vulnerability Summary                                         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total CVEs          │ 23                                                                         │
│ Critical            │ 2                                                                          │
│ High                │ 8                                                                          │
│ Medium              │ 13                                                                         │
│ With Exploits       │ 5                                                                          │
│ Highest CVSS        │ 9.8                                                                        │
└─────────────────────┴────────────────────────────────────────────────────────────────────────────┘

WARNING: 2 CRITICAL vulnerabilities found!
```

## Technical Architecture

### Dynamic Analysis Engine
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   System Info   │ -> │   CVE Fetcher   │ -> │  Exploit Links  │
│   Collection    │    │   (Internet)    │    │   Generation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         |                       |                       |
         v                       v                       v
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Kernel Match   │    │  CVSS Scoring   │    │ Report Output   │
│   Algorithm     │    │   & Severity    │    │  (Multi-format) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### API Integration
- **NIST NVD API v2.0**: Official CVE database
- **Vulners API v3**: Commercial threat intelligence
- **ExploitDB Search**: Proof-of-concept exploits
- **GitHub Search**: Community exploits and tools

## API Rate Limiting

The tool implements intelligent rate limiting:
- **0.5 second delays** between API calls
- **Timeout handling** (30 seconds)
- **Error recovery** with graceful fallbacks
- **Connection testing** before analysis

## Report Formats

### JSON Report
```json
{
  "kernel_version": "5.15.0",
  "total_cves": 23,
  "critical_count": 2,
  "cves": [
    {
      "cve_id": "CVE-2024-1086",
      "cvss_score": 9.8,
      "severity": "CRITICAL",
      "description": "Netfilter Use-After-Free...",
      "exploits": [
        {
          "source": "ExploitDB",
          "url": "https://www.exploit-db.com/search?cve=CVE-2024-1086"
        }
      ]
    }
  ]
}
```

### HTML Report
Professional web-based report with:
- Interactive CVE tables
- Severity distribution charts
- Exploit availability indicators
- Executive summary section

### CVE Links Export
```
CVE and Exploit Links for Kernel 5.15.0
========================================

CVE: CVE-2024-1086
CVSS: 9.8 (CRITICAL)
Description: Netfilter Use-After-Free Privilege Escalation
Exploit Links:
  - ExploitDB: https://www.exploit-db.com/search?cve=CVE-2024-1086
  - PacketStorm: https://packetstormsecurity.com/search/?q=CVE-2024-1086
```

## Security Recommendations

### For Security Teams
1. **Regular Scanning**: Run weekly vulnerability assessments
2. **Patch Management**: Prioritize CRITICAL and HIGH severity CVEs
3. **Monitoring**: Track new CVEs for your kernel versions
4. **Documentation**: Maintain vulnerability remediation records

### For Penetration Testers
1. **Authorized Testing**: Only use on authorized systems
2. **Documentation**: Record all findings and methods
3. **Responsible Disclosure**: Report vulnerabilities appropriately
4. **Legal Compliance**: Ensure all activities are legally authorized

## Troubleshooting

### Internet Connectivity Issues
```bash
# Test API connectivity
python3 main.py --test

# Check firewall/proxy settings
curl -I https://services.nvd.nist.gov
curl -I https://vulners.com
```

### Python Dependencies
```bash
# Install specific versions
pip3 install requests>=2.31.0
pip3 install rich>=13.7.0

# Upgrade all dependencies
pip3 install -r requirements.txt --upgrade
```

### Permission Issues
```bash
# Run with appropriate permissions
sudo python3 main.py -v -o /tmp/report

# Or change output directory
python3 main.py -o ~/security_report
```

## Development

### Adding New CVE Sources
```python
# In modules/cve_fetcher.py
def _search_new_api(self, kernel_version):
    """Add new CVE data source"""
    # Implementation here
    pass
```

### Custom Exploit Patterns
```python
# In modules/dynamic_exploit_checker.py
def _check_custom_patterns(self, kernel_version):
    """Add custom vulnerability patterns"""
    # Implementation here
    pass
```

## Legal Notice

This tool is provided for educational and authorized security testing purposes only. Users must:

- Only test systems they own or have explicit written permission to test
- Comply with all applicable laws and regulations
- Use the tool responsibly and ethically
- Accept full responsibility for their actions

## Changelog

### v3.0 (2025)
- **Major Rewrite**: Internet-based dynamic CVE fetching
- **Real-time Data**: NIST NVD and Vulners API integration
- **Modern Architecture**: Python 3.8+ with Rich CLI interface
- **Enhanced Reporting**: Multi-format reports with executive summaries
- **Professional UI**: Clean, emoji-free enterprise interface

### v2.x (Legacy)
- Static exploit database
- Basic kernel matching
- Limited CVE coverage

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is licensed under the GPL v3.0 License - see the LICENSE file for details.

## Authors

- **LES-Modern Team** - Modern Python implementation
- **Original LES Contributors** - Foundation and inspiration

## Acknowledgments

- NIST National Vulnerability Database
- Vulners Vulnerability Database  
- Offensive Security ExploitDB
- Linux Kernel Security Team
- Security Research Community 
