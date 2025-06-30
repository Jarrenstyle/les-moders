#!/bin/bash

# LES-Modern - Kali Linux Kurulum Scripti
# ========================================

set -e

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
echo -e "${CYAN}"
echo "============================================================"
echo "                 LES-Modern Kali Linux                   "
echo "              Penetration Testing Version              "
echo "============================================================"
echo -e "${NC}"

# Kali Linux check
if ! grep -q "kali" /etc/os-release 2>/dev/null; then
    echo -e "${YELLOW}WARNING: This script is optimized for Kali Linux.${NC}"
    read -p "Do you want to continue? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Installation cancelled.${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}Kali Linux detected!${NC}"

# Root check
if [[ $EUID -eq 0 ]]; then
    echo -e "${YELLOW}WARNING: Running as root. Normal user recommended.${NC}"
fi

# System update
echo -e "${BLUE}Updating system...${NC}"
sudo apt update -qq
sudo apt upgrade -y -qq

# Install required packages
echo -e "${BLUE}Installing required system packages...${NC}"
sudo apt install -y python3 python3-pip python3-venv git curl wget

# Python version check
PYTHON_VERSION=$(python3 --version | grep -o '[0-9]\+\.[0-9]\+')
echo -e "${GREEN}Python version: $PYTHON_VERSION${NC}"

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
python3 -m venv les-modern-env
source les-modern-env/bin/activate
echo -e "${GREEN}Virtual environment active${NC}"

# Install Python packages
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip install --upgrade pip wheel setuptools

# Ana paketler
pip install requests beautifulsoup4 colorama rich tabulate jinja2 click psutil packaging python-dateutil

# Additional security tools (optional)
echo -e "${BLUE}Installing additional security tools...${NC}"
pip install pyfiglet python-nmap scapy

echo -e "${GREEN}All dependencies installed${NC}"

# Create directories
mkdir -p output exploits logs
echo -e "${GREEN}Directory structure created${NC}"

# Set permissions
chmod +x main.py
chmod +x *.sh
echo -e "${GREEN}Permissions set${NC}"

# Kali tools integration
echo -e "${BLUE}Checking Kali tools...${NC}"

# searchsploit check
if command -v searchsploit &> /dev/null; then
    echo -e "${GREEN}searchsploit available${NC}"
    # Update ExploitDB
    sudo searchsploit -u
else
    echo -e "${YELLOW}searchsploit not found, installing...${NC}"
    sudo apt install -y exploitdb
fi

# nmap check
if command -v nmap &> /dev/null; then
    echo -e "${GREEN}nmap available${NC}"
else
    echo -e "${YELLOW}Installing nmap...${NC}"
    sudo apt install -y nmap
fi

# Test run
echo -e "${BLUE}Running test...${NC}"
if python3 main.py --help &> /dev/null; then
    echo -e "${GREEN}LES-Modern successfully installed!${NC}"
else
    echo -e "${RED}Test failed!${NC}"
    exit 1
fi

# Add to Kali menu
echo -e "${BLUE}Adding to Kali menu...${NC}"
DESKTOP_FILE="/home/$SUDO_USER/.local/share/applications/les-modern.desktop"
mkdir -p "/home/$SUDO_USER/.local/share/applications"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=LES-Modern
Comment=Linux Exploit Suggester 2025
Exec=/bin/bash -c 'cd $(pwd) && source les-modern-env/bin/activate && python3 main.py; read -p "Press enter to exit..."'
Icon=security-high
Terminal=true
Type=Application
Categories=08-Exploitation Tools;
EOF

chown $SUDO_USER:$SUDO_USER "$DESKTOP_FILE" 2>/dev/null || true
echo -e "${GREEN}Added to Kali menu${NC}"

# Success message
echo ""
echo -e "${GREEN}"
echo "============================================================"
echo "                  INSTALLATION COMPLETED!                "
echo "============================================================"
echo ""
echo "  To get started:"
echo "  • source les-modern-env/bin/activate"
echo "  • python3 main.py"
echo ""
echo "  Kali Menu: Applications -> Exploitation Tools"
echo ""
echo "  Quick commands:"
echo "  • python3 main.py --no-warning"
echo "  • python3 main.py --download --verbose"
echo "  • python3 main.py --json-report --html-report"
echo ""
echo "============================================================"
echo -e "${NC}"

# Security warning
echo -e "${RED}"
echo "SECURITY WARNING"
echo "This tool should only be used for legal penetration"
echo "testing and educational purposes!"
echo -e "${NC}"

echo -e "${CYAN}Happy hacking on Kali Linux! ${YELLOW}python3 main.py${NC}" 