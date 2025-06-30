#!/bin/bash

# LES-Modern v3.0 Installation Script
# Dynamic Linux Exploit Suggester Installation

set -e

echo "================================================"
echo "LES-Modern v3.0 Installation Script"
echo "Dynamic Linux Exploit Suggester"
echo "================================================"

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}ERROR: This tool only works on Linux systems${NC}"
    echo -e "${YELLOW}Detected OS: $OSTYPE${NC}"
    exit 1
fi

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -ge 8 ]]; then
        echo -e "${GREEN}Python $PYTHON_VERSION found - OK${NC}"
    else
        echo -e "${RED}ERROR: Python 3.8+ required, found $PYTHON_VERSION${NC}"
        exit 1
    fi
else
    echo -e "${RED}ERROR: Python 3 not found${NC}"
    echo "Please install Python 3.8+ first:"
    echo "  Ubuntu/Debian: apt update && apt install python3 python3-pip"
    echo "  CentOS/RHEL: yum install python3 python3-pip"
    echo "  Fedora: dnf install python3 python3-pip"
    exit 1
fi

# Check pip
echo -e "${BLUE}Checking pip...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}pip3 not found, installing...${NC}"
    
    # Try to install pip based on distribution
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3-pip
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pip
    else
        echo -e "${RED}Could not install pip3 automatically${NC}"
        echo "Please install pip3 manually"
        exit 1
    fi
fi

# Check internet connectivity
echo -e "${BLUE}Testing internet connectivity...${NC}"
if ping -c 1 8.8.8.8 &> /dev/null; then
    echo -e "${GREEN}Internet connection - OK${NC}"
else
    echo -e "${YELLOW}WARNING: No internet connection detected${NC}"
    echo -e "${YELLOW}Tool will work in offline mode only${NC}"
fi

# Create virtual environment (optional but recommended)
read -p "Create Python virtual environment? (recommended) [y/N]: " -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv les-modern-env
    source les-modern-env/bin/activate
    echo -e "${GREEN}Virtual environment activated${NC}"
    echo -e "${YELLOW}To activate in future: source les-modern-env/bin/activate${NC}"
fi

# Install Python dependencies
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip3 install --upgrade pip

if [[ -f "requirements.txt" ]]; then
    pip3 install -r requirements.txt
    echo -e "${GREEN}Dependencies installed successfully${NC}"
else
    echo -e "${YELLOW}requirements.txt not found, installing manually...${NC}"
    pip3 install requests>=2.31.0 beautifulsoup4>=4.12.2 rich>=13.7.0 click>=8.1.7 psutil>=5.9.0 jinja2>=3.1.2 python-dateutil>=2.8.2 urllib3>=1.26.18 certifi>=2023.7.22 idna>=3.4 charset-normalizer>=3.2.0
fi

# Make main script executable
echo -e "${BLUE}Setting up executable permissions...${NC}"
chmod +x main.py

# Test installation
echo -e "${BLUE}Testing installation...${NC}"
if python3 main.py --test &> /dev/null; then
    echo -e "${GREEN}Installation test - PASSED${NC}"
else
    echo -e "${YELLOW}Installation test completed (check internet connectivity)${NC}"
fi

# Create output directory
mkdir -p output
chmod 755 output

# Summary
echo ""
echo "================================================"
echo -e "${GREEN}LES-Modern v3.0 Installation Complete!${NC}"
echo "================================================"
echo ""
echo "Usage Examples:"
echo "  Basic scan:              python3 main.py"
echo "  Verbose analysis:        python3 main.py -v"
echo "  Generate reports:        python3 main.py -o ./reports"
echo "  Test connectivity:       python3 main.py --test"
echo "  Skip warnings:           python3 main.py --no-warning"
echo ""
echo "Key Features:"
echo "  - Real-time CVE fetching from NIST NVD"
echo "  - Dynamic exploit analysis"
echo "  - Multiple report formats (JSON, HTML, Markdown)"
echo "  - Professional vulnerability assessment"
echo ""
echo -e "${YELLOW}Important:${NC}"
echo "  - Tool requires Linux system to analyze vulnerabilities"
echo "  - Internet connection needed for real-time CVE data"
echo "  - Only use on authorized systems"
echo "  - Read security warnings before use"
echo ""

# Optional: Add to PATH
read -p "Add to system PATH? [y/N]: " -r
if [[ $REPLY =~ ^[Yy]$ ]]; then
    INSTALL_DIR=$(pwd)
    echo "#!/bin/bash" > /tmp/les-modern
    echo "cd $INSTALL_DIR" >> /tmp/les-modern
    echo "python3 main.py \"\$@\"" >> /tmp/les-modern
    
    sudo mv /tmp/les-modern /usr/local/bin/les-modern
    sudo chmod +x /usr/local/bin/les-modern
    
    echo -e "${GREEN}Added to PATH: les-modern command available system-wide${NC}"
    echo "Usage: les-modern -v -o /tmp/report"
fi

echo ""
echo -e "${GREEN}Ready to use! Run: python3 main.py --help${NC}" 