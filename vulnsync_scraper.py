import requests
import mysql.connector
from mysql.connector import Error

def fetch_and_log_exploits():
    # Database Connection Configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'YOUR_PASSWORD', # IMPORTANT: Update with your DB password
        'database': 'vulnsync_db'
    }

    try:
        print("[*] MariaDB'ye bağlanılıyor...")
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        print("[+] Veritabanı bağlantısı başarılı.")

        # Request Headers & Parameters (Anti-Bot / WAF Bypass)
        url = 'https://www.exploit-db.com/'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.exploit-db.com/'
        }

        # DataTables parameters required to trigger JSON response
        params = {
            'draw': '1',
            'length': '15',
            'start': '0'
        }
        
        print("[*] Exploit-DB üzerinden güncel zafiyetler çekiliyor...")
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code != 200:
            print(f"[-] Sunucu başarısız bir yanıt döndürdü. Durum Kodu: {response.status_code}")
            return 

        try:
            jsonData = response.json()
        except ValueError:
            print("[-] Sunucudan JSON formatında veri gelmedi! Muhtemelen bir bot engeline takıldık.")
            return

        exploits = jsonData.get('data', [])
        print(f"[+] Toplam {len(exploits)} adet zafiyet kaydı bulundu. Veritabanına işleniyor...")

        # SQL Query: INSERT IGNORE prevents duplicate entries based on ID
        insert_query = """
            INSERT IGNORE INTO exploits 
            (id, title, type, platform, author, link) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        yeni_kayit_sayisi = 0

        for exploit in exploits:
            try:
                exp_id = exploit.get('id')
                title = exploit['description'][1] if 'description' in exploit else "Başlık Yok"
                exp_type = exploit['type']['display'] if 'type' in exploit else "Bilinmiyor"
                platform = exploit['platform']['platform'] if 'platform' in exploit else "Bilinmiyor"
                author = exploit['author']['name'] if 'author' in exploit else "Bilinmiyor"
                
                # Extract clean URL from HTML tag
                raw_download = exploit.get('download', '')
                if '"' in raw_download:
                    link = "https://www.exploit-db.com/" + raw_download.split('"')[1]
                else:
                    link = "Link Yok"

                data_tuple = (exp_id, title, exp_type, platform, author, link)
                cursor.execute(insert_query, data_tuple)
                
                if cursor.rowcount == 1:
                    yeni_kayit_sayisi += 1
                    print(f"  [YENİ] Eklendi: {title} | Platform: {platform}")

            except Exception as e:
                print(f"  [-] Bir JSON kaydı ayrıştırılırken hata oluştu: {e}")
                continue
        
        connection.commit()
        print(f"\n[+] İşlem Tamamlandı! Veritabanına toplam {yeni_kayit_sayisi} adet YENİ zafiyet loglandı.")

    except requests.exceptions.RequestException as re:
        print(f"[-] Web isteği sırasında ağ hatası oluştu: {re}")
    except Error as db_err:
        print(f"[-] MariaDB veritabanı hatası: {db_err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("[*] MariaDB bağlantısı güvenli bir şekilde kapatıldı.")

if __name__ == "__main__":
    fetch_and_log_exploits()
