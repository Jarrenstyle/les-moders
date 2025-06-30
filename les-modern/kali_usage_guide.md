# 🐲 LES-Modern Kali Linux Kullanım Kılavuzu

## 🎯 Hızlı Başlangıç

### Kurulum
```bash
# Kali özel kurulum scripti
chmod +x kali_install.sh
sudo ./kali_install.sh

# Virtual environment'ı aktifleştir
source les-modern-env/bin/activate
```

### İlk Çalıştırma
```bash
# Hızlı analiz
python3 main.py --no-warning

# Detaylı analiz
python3 main.py --verbose --json-report
```

## 🔧 Kali Linux Entegrasyonu

### 1. SearchSploit ile Entegrasyon
```bash
# Mevcut kernel için exploit ara
searchsploit $(uname -r | cut -d'-' -f1-2)

# LES-Modern ile karşılaştır
python3 main.py --kernel $(uname -r | cut -d'-' -f1)
```

### 2. Nmap ile Kombinasyon
```bash
# Hedef sistem taraması sonrası
nmap -sV target_ip

# LES-Modern ile yerel analiz
python3 main.py --verbose
```

### 3. Metasploit Hazırlığı
```bash
# Exploitleri indir ve MSF için hazırla
python3 main.py --download --output-dir /tmp/exploits

# Metasploit'te kullanım için
msfconsole
# use exploit/linux/local/[exploit_name]
```

## 📊 Pentesting Senaryoları

### Senaryo 1: Local Privilege Escalation
```bash
# 1. Sistem analizi
python3 main.py --json-report --output-dir /tmp/privesc

# 2. Exploitleri indir
python3 main.py --download

# 3. HTML raporu oluştur
python3 main.py --html-report
firefox output/les_modern_report.html
```

### Senaryo 2: Post-Exploitation Analysis
```bash
# Hedef sistemde çalıştır
python3 main.py --kernel 5.4.0 --no-warning --json-report

# Raporları güvenli bir yere kopyala
cp output/* /home/kali/Documents/pentest-reports/
```

### Senaryo 3: Automated Reconnaissance
```bash
#!/bin/bash
# auto_recon.sh

TARGET_IP=$1
echo "🎯 Target: $TARGET_IP"

# Port taraması
nmap -sS -O $TARGET_IP

# SSH bağlantısı varsa
if nmap -p 22 $TARGET_IP | grep open; then
    echo "📡 SSH tespit edildi"
    # LES-Modern dosyalarını gönder
    scp -r . user@$TARGET_IP:/tmp/les-modern/
    ssh user@$TARGET_IP "cd /tmp/les-modern && python3 main.py --json-report"
fi
```

## 🎨 Çıktı Örnekleri

### Terminal Çıktısı (Kali)
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    🐲 KALI LINUX DETECTED 🐲               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🔍 Hedef Sistem: Kali Linux 2024.1
🔧 Kernel Versiyonu: 6.1.0-kali9-amd64

🎯 5 adet potansiyel exploit bulundu!

┏━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━┓
┃ # ┃ Exploit            ┃ CVE           ┃ Severity ┃ Yıl ┃
┡━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━┩
│ 1 │ netfilter_2024     │ CVE-2024-1086 │ CRITICAL │ 2024│
│ 2 │ overlayfs_2024     │ CVE-2024-0841 │   HIGH   │ 2024│
│ 3 │ stackrot           │ CVE-2023-3269 │   HIGH   │ 2023│
│ 4 │ dirtypipe          │ CVE-2022-0847 │   HIGH   │ 2022│
│ 5 │ pwnkit             │ CVE-2021-4034 │ CRITICAL │ 2021│
└───┴────────────────────┴───────────────┴──────────┴─────┘

🔗 Exploit Linkleri:
1. netfilter_2024: https://github.com/Notselwyn/CVE-2024-1086
2. overlayfs_2024: https://www.exploit-db.com/exploits/51234
3. stackrot: https://github.com/TurtleARM/CVE-2023-3269-exploits
4. dirtypipe: https://www.exploit-db.com/exploits/50808
5. pwnkit: https://www.exploit-db.com/exploits/50689
```

## 🔄 Workflow Entegrasyonu

### 1. Burp Suite ile
```bash
# Burp taraması sonrası
python3 main.py --output-dir /home/kali/.BurpSuite/reports/
```

### 2. OWASP ZAP ile
```bash
# ZAP raporları ile birleştir
python3 main.py --html-report --output-dir /home/kali/zaproxy/reports/
```

### 3. Custom Scripts
```bash
# Özel penetrasyon testi scripti
#!/bin/bash
echo "🚀 Starting pentest workflow..."

# 1. Network discovery
nmap -sn 192.168.1.0/24

# 2. Service enumeration
nmap -sV -sC target

# 3. Local privilege escalation check
python3 main.py --verbose --json-report

# 4. Report generation
python3 main.py --html-report --markdown-report
```

## 📱 GUI Versiyonu (Opsiyonel)

### Kali Menüsü Entegrasyonu
- **Applications** → **Exploitation Tools** → **LES-Modern**
- Otomatik terminal açma
- GUI rapor görüntüleme

### Web Interface (Future)
```bash
# Web arayüzü başlat (geliştirme aşamasında)
python3 -m http.server 8080 -d output/
firefox http://localhost:8080/les_modern_report.html
```

## 🔒 Güvenlik Best Practices

### 1. Virtual Environment Kullanımı
```bash
# Her proje için ayrı env
python3 -m venv /opt/les-modern-env
source /opt/les-modern-env/bin/activate
```

### 2. Log Yönetimi
```bash
# Logları güvenli yerde sakla
python3 main.py --verbose 2>&1 | tee /var/log/les-modern.log
```

### 3. Network Segmentation
```bash
# İzole network'te çalıştır
# VPN veya lab environment kullan
```

## 🎓 Eğitim Amaçlı Kullanım

### 1. CVE Analizi
```bash
# Belirli CVE'yi araştır
python3 main.py | grep "CVE-2024"
```

### 2. Kernel Security Research
```bash
# Farklı kernel versiyonlarını test et
for version in 5.15.0 5.19.0 6.1.0; do
    echo "Testing kernel $version"
    python3 main.py --kernel $version --json-report
done
```

### 3. Compliance Checking
```bash
# Güvenlik uyumluluk kontrolü
python3 main.py --markdown-report --output-dir /audit/reports/
```

---

## ⚡ Hızlı Komut Referansı

```bash
# Temel komutlar
python3 main.py                    # Hızlı analiz
python3 main.py --help             # Yardım
python3 main.py --verbose          # Detaylı çıktı
python3 main.py --no-warning       # Sessiz mod

# Rapor oluşturma
python3 main.py --json-report      # JSON raporu
python3 main.py --html-report      # HTML raporu
python3 main.py --markdown-report  # Markdown raporu

# Exploit yönetimi
python3 main.py --download          # Exploitleri indir
python3 main.py --kernel 5.15.0     # Manuel kernel

# Kombinasyonlar
python3 main.py --json-report --html-report --download --verbose
```

---

🐲 **Happy Hacking on Kali Linux!** 🔥 