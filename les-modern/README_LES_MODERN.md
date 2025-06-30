# LES-Modern - Linux Exploit Suggester 2025

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![CVE](https://img.shields.io/badge/CVE-2024%2F2025-red?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Linux-orange?style=for-the-badge&logo=linux)

**Modern Python-based Linux Exploit Suggester**  
*CVE-2024/2025 compatible, advanced security analysis tool*

</div>

---

## Project Overview

**LES-Modern** is a 2025-compatible modern Python version of the classic "linux-exploit-suggester-2". This tool detects potential security vulnerabilities in Linux systems and suggests appropriate exploits.

### New Features

- **2024/2025 CVE Support** - Latest exploits included
- **System Analysis** - Comprehensive information gathering
- **Multiple Report Formats** - JSON, HTML, Markdown
- **Modern UI** - Colorful and user-friendly interface
- **Package Analysis** - dpkg, rpm, snap support
- **Security Focused** - Legal warnings and confirmations
- **Fast and Efficient** - Parallel processing support

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/les-modern.git
cd les-modern

# Install dependencies
pip install -r requirements.txt

# Run immediately
python main.py
```

### Basic Usage

```bash
# Default analysis
python main.py

# Generate all reports
python main.py --json-report --html-report --markdown-report

# Download exploits
python main.py --download

# Specify kernel manually
python main.py --kernel 5.15.0

# Verbose mode
python main.py --verbose
```

## Features

### System Analysis

- **Kernel Information**: `uname`, version, architecture
- **Distribution Detection**: `/etc/os-release`, `lsb_release`
- **Package List**: `dpkg`, `rpm`, `snap` packages
- **Security Status**: user, sudo, SUID files
- **System Performance**: CPU, RAM, disk usage

### Exploit Database

#### 2024-2025 Current Exploits
- **CVE-2024-1086** - Netfilter Use-After-Free
- **CVE-2024-0841** - OverlayFS Privilege Escalation
- **CVE-2023-2640/32629** - GameOver(lay) Ubuntu
- **CVE-2023-3269** - StackRot

#### Classic Exploits
- **CVE-2022-0847** - Dirty Pipe
- **CVE-2021-4034** - PwnKit
- **CVE-2021-3156** - Baron Samedit
- **CVE-2016-5195** - Dirty COW

### Report Formats

#### JSON Report
```json
{
  "report_info": {
    "generated_at": "2024-XX-XX",
    "les_modern_version": "3.0.0-beta"
  },
  "system_info": { ... },
  "exploits": { ... }
}
```

#### HTML Report
- Bootstrap-based modern design
- Responsive (mobile compatible)
- Interactive tables and filters
- Visual charts and statistics

#### Markdown Report
- GitHub compatible format
- Direct links
- Checklist format recommendations

## Usage Examples

### Basic Usage
```bash
# Quick analysis
python main.py

# Silent mode (no warnings)
python main.py --no-warning

# Specify output directory
python main.py --output-dir /tmp/les-results
```

### Advanced Usage
```bash
# Full analysis + reports
python main.py \
  --json-report \
  --html-report \
  --markdown-report \
  --download \
  --verbose

# Test for specific kernel
python main.py --kernel 5.4.0

# Dangerous mode (under development)
python main.py --danger-mode
```

## Project Structure

```
les-modern/
├── main.py                 # Main application
├── requirements.txt        # Python dependencies
├── modules/               # Core modules
│   ├── __init__.py
│   ├── system_info.py     # System information gathering
│   ├── exploit_checker.py # Exploit analysis
│   └── report_generator.py # Report generation
├── output/                # Output files
│   ├── system_info.json
│   ├── les_modern_report.html
│   ├── les_modern_report.md
│   └── exploits/          # Downloaded exploits
└── README_LES_MODERN.md
```

## Sample Outputs

### Terminal Output
```
LES-Modern v3.0.0-beta
Linux Exploit Suggester 2025
CVE-2024/2025 Compatible Version

Target System: Ubuntu 22.04
Kernel Version: 5.15.0-91-generic

3 potential exploits found!

+---+------------------+---------------+----------+------+-------------------------------------------+
| # | Exploit Name     | CVE           | Severity | Year | Description                               |
+---+------------------+---------------+----------+------+-------------------------------------------+
| 1 | overlayfs_2024   | CVE-2024-0841 |   HIGH   | 2024 | OverlayFS Privilege Escalation 2024      |
| 2 | dirtypipe        | CVE-2022-0847 |   HIGH   | 2022 | Dirty Pipe - Overwriting Data            |
| 3 | pwnkit           | CVE-2021-4034 | CRITICAL | 2021 | PwnKit - Local Privilege Escalation      |
+---+------------------+---------------+----------+------+-------------------------------------------+
```

## Security Warning

### IMPORTANT: Legal Usage

This tool is developed for **EDUCATIONAL PURPOSES ONLY**:

- **Permitted usage:**
  - Your own systems
  - Authorized penetration tests
  - Educational laboratories
  - Security research

- **Prohibited usage:**
  - Unauthorized system access
  - Malicious attacks
  - Illegal activities

**User accepts all legal responsibility.**

## Contributing

### Development Environment

```bash
# Development dependencies
pip install -r requirements-dev.txt

# Code format check
black . --check
flake8 .

# Run tests
pytest tests/
```

### Adding New Exploits

Add new exploits to the `_load_exploits_database()` function in `modules/exploit_checker.py`:

```python
'new_exploit_name': {
    'cve': 'CVE-2024-XXXX',
    'kernels': ['5.15', '5.16', '5.17'],
    'description': 'Exploit description',
    'severity': 'HIGH',
    'exploit_url': 'https://exploit-db.com/...',
    'year': 2024,
    'distros': ['ubuntu', 'debian']
}
```

## License

This project is published under the MIT license. See [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Linux Exploit Suggester 2** - Original project
- **ExploitDB** - Vulnerability database
- **Rich Library** - Terminal UI
- **All security researchers**

---

<div align="center">

**Star the project if you like it!**

[Bug Report](https://github.com/your-repo/issues) | 
[Feature Request](https://github.com/your-repo/issues) | 
[Wiki](https://github.com/your-repo/wiki)

</div>

---

*This tool is developed for educational purposes. Illegal use is strictly prohibited.* 