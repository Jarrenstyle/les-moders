#!/bin/bash

# LES-Modern Installation Script
# ==============================

set -e

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    LES-Modern v3.0.0-beta               ║"
echo "║              Linux Exploit Suggester 2025               ║"
echo "║                    Kurulum Scripti                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Sistem kontrolleri
echo -e "${BLUE} 📋Sistem kontrolleri yapılıyor...${NC}"

# Python sürüm kontrolü
PYTHON_VERSION=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+' | head -1)
REQUIRED_VERSION="3.8"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${RED}❌ Python 3.8+ gerekli. Mevcut sürüm: $PYTHON_VERSION${NC}"
    echo -e "${YELLOW}💡 Python'u güncelleyin: sudo apt update && sudo apt install python3.9${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python sürümü uygun: $PYTHON_VERSION${NC}"

# pip kontrolü
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  pip3 bulunamadı, yükleniyor...${NC}"
    sudo apt update
    sudo apt install -y python3-pip
fi

echo -e "${GREEN}✅ pip3 mevcut${NC}"

# Virtual environment önerisi
echo -e "${BLUE}🐍 Virtual environment kullanmanız önerilir:${NC}"
echo -e "${YELLOW}python3 -m venv les-modern-env${NC}"
echo -e "${YELLOW}source les-modern-env/bin/activate${NC}"
echo ""

read -p "Virtual environment oluşturmak istiyor musunuz? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 -m venv les-modern-env
    source les-modern-env/bin/activate
    echo -e "${GREEN}✅ Virtual environment aktif${NC}"
fi

# Bağımlılık yükleme
echo -e "${BLUE}📦 Bağımlılıklar yükleniyor...${NC}"

if [ -f requirements.txt ]; then
    pip3 install -r requirements.txt
    echo -e "${GREEN}✅ Bağımlılıklar yüklendi${NC}"
else
    echo -e "${YELLOW}⚠️  requirements.txt bulunamadı, manuel yükleme yapılıyor...${NC}"
    pip3 install requests beautifulsoup4 colorama rich tabulate jinja2 click psutil packaging python-dateutil
fi

# Çıktı klasörü oluştur
mkdir -p output
echo -e "${GREEN}✅ Çıktı klasörü oluşturuldu${NC}"

# İzinleri ayarla
chmod +x main.py
echo -e "${GREEN}✅ Çalıştırma izinleri ayarlandı${NC}"

# Test çalıştırma
echo -e "${BLUE}🧪 Test çalıştırması yapılıyor...${NC}"
if python3 main.py --help &> /dev/null; then
    echo -e "${GREEN}✅ Test başarılı!${NC}"
else
    echo -e "${RED}❌ Test başarısız. Lütfen hataları kontrol edin.${NC}"
    exit 1
fi

# Başarı mesajı
echo ""
echo -e "${GREEN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    🎉 KURULUM TAMAMLANDI! 🎉              ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║                                                            ║"
echo "║  Kullanım örnekleri:                                       ║"
echo "║  • python3 main.py                                         ║"
echo "║  • python3 main.py --help                                  ║"
echo "║  • python3 main.py --json-report --html-report             ║"
echo "║                                                            ║"
echo "║  📚 Detaylı dökümantasyon: README_LES_MODERN.md            ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Güvenlik uyarısı
echo -e "${RED}"
echo "⚠️  GÜVENLİK UYARISI ⚠️"
echo "Bu araç SADECE EĞİTİM AMAÇLI geliştirilmiştir."
echo "Yasadışı kullanım kesinlikle yasaktır!"
echo -e "${NC}"

echo -e "${CYAN}🚀 Hemen başlamak için: ${YELLOW}python3 main.py${NC}" 