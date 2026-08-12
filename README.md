# 🛡️ VulnSync: Dynamic Vulnerability Intelligence Engine
*([Türkçe sürüm için aşağı kaydırın / Scroll down for Turkish version](#türkçe-sürüm))*

VulnSync is a dynamic threat matching engine that automatically scrapes up-to-date threat intelligence from open-source vulnerability databases (Exploit-DB), structures it in a local relational database (MariaDB), and integrates seamlessly with other network security/scanning tools.

It is specifically designed to provide a real-time vulnerability ruleset for **Active Defense** systems, **IDS/IPS** architectures, and network scanners.

## ✨ Features
*   **Automated Scraping:** Retrieves clean JSON data via Exploit-DB's background API without dealing with HTML parsing.
*   **Anti-Bot & WAF Bypass:** Bypasses Cloudflare and bot protections using dynamic headers and session parameters.
*   **Smart Database Logging:** Uses `INSERT IGNORE` logic on MariaDB. It only logs **new** vulnerabilities, preventing resource exhaustion and duplicate entries.
*   **Modular Threat Matcher:** Instantly analyzes risks based on target OS/platform information (e.g., "Windows", "Linux", "Hardware").

## 📂 Project Structure
1.  `vulnsync_scraper.py`: The intelligence agent that runs in the background to keep the database updated.
2.  `threat_matcher.py`: The analysis module that can be imported into other Python projects to query MariaDB for specific target platforms.
3.  `database_schema.sql`: The SQL skeleton that builds the required database and table hierarchy.

## 🚀 Installation & Setup

### 1. Requirements
Python 3 and MariaDB/MySQL are required. Install the necessary libraries:
```bash
pip install requests mysql-connector-python
```

### 2. Database Setup
Start your MariaDB service and import the SQL file:
```bash
mysql -u root -p < database_schema.sql
```

### 3. Configuration
Update the database connection details in `vulnsync_scraper.py` and `threat_matcher.py`:
```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD', # IMPORTANT: Update with your DB password
    'database': 'vulnsync_db'
}
```

## 💻 Usage & Integration

### 1. Updating the Intelligence Database
Run the scraper to fetch and log vulnerabilities to MariaDB:
```bash
python3 vulnsync_scraper.py
```

### 2. Integrating into Your Security Tools
Import the module into your custom port scanner or Active Defense tool:
```python
from threat_matcher import check_target_vulnerabilities

target_os = "Windows" 
risk_report = check_target_vulnerabilities(target_os, max_results=3)

if risk_report:
    print("ALERT: Target is at risk! Initiate defense protocols.")
```

---
---

<a name="türkçe-sürüm"></a>
# 🛡️ VulnSync: Dinamik Zafiyet İstihbarat Motoru

VulnSync, açık kaynaklı zafiyet veritabanlarından (Exploit-DB) güncel tehdit istihbaratını otomatik olarak çeken, bu verileri yerel bir ilişkisel veritabanında (MariaDB) yapılandıran ve diğer ağ güvenlik/tarama araçlarıyla entegre çalışabilen dinamik bir tehdit eşleştirme (Threat Matching) motorudur.

Özellikle **Aktif Savunma (Active Defense)** sistemleri, **IDS/IPS** mimarileri ve ağ tarayıcıları için gerçek zamanlı bir zafiyet kural seti sağlamak amacıyla tasarlanmıştır.

## ✨ Özellikler
*   **Otomatize Veri Kazıma (Scraping):** Exploit-DB'nin arka plan API'si ile haberleşerek, HTML karmaşasına girmeden temiz JSON formatında veri çeker.
*   **Anti-Bot & WAF Bypass:** Dinamik başlıklar (headers) ve oturum parametreleri kullanarak Cloudflare ve bot engellemelerini aşar.
*   **Akıllı Veritabanı Loglama:** MariaDB üzerinde `INSERT IGNORE` mantığıyla çalışır. Sadece **yeni** eklenen zafiyetleri loglayarak sistem kaynaklarını yormaz.
*   **Modüler Eşleştirme Motoru:** Dışarıdan gelen herhangi bir işletim sistemi veya platform bilgisine (Örn: "Windows", "Linux", "Hardware") göre anında risk analizi yapar.

## 📂 Proje Yapısı
1.  `vulnsync_scraper.py`: Arka planda periyodik olarak çalıştırılarak veritabanını güncel tutan istihbarat ajanı.
2.  `threat_matcher.py`: Diğer Python projelerine `import` edilerek kullanılabilen analiz modülü.
3.  `database_schema.sql`: Projenin ihtiyaç duyduğu veritabanı ve tablo hiyerarşisini kuran SQL iskeleti.

## 🚀 Kurulum ve Hazırlık

### 1. Gereksinimler
Sistemin çalışması için Python 3 ve MariaDB/MySQL kurulu olmalıdır. Gerekli kütüphaneleri yüklemek için:
```bash
pip install requests mysql-connector-python
```

### 2. Veritabanının Hazırlanması
MariaDB servisinizi başlatın ve proje dizinindeki SQL dosyasını içeri aktarın:
```bash
mysql -u root -p < database_schema.sql
```

### 3. Konfigürasyon
`vulnsync_scraper.py` ve `threat_matcher.py` dosyalarının içindeki veritabanı bağlantı bilgilerini kendi sisteminize göre güncelleyin:
```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD', # ÖNEMLİ: Veritabanı şifrenizle güncelleyin
    'database': 'vulnsync_db'
}
```

## 💻 Kullanım Senaryoları

### 1. İstihbarat Veritabanını Güncellemek
Zafiyet listesini çekmek ve MariaDB'ye loglamak için aracı çalıştırın:
```bash
python3 vulnsync_scraper.py
```

### 2. Kendi Güvenlik Aracınıza Entegre Etmek
Ağ tarayıcınız veya savunma aracınız hedef cihazı tespit ettiğinde VulnSync'e risk durumunu sorabilirsiniz:
```python
from threat_matcher import check_target_vulnerabilities

hedef_os = "Windows" 
risk_raporu = check_target_vulnerabilities(hedef_os, max_results=3)

if risk_raporu:
    print("DİKKAT: Cihaz güncel bir risk altında! Savunma protokollerini başlatın.")
```
