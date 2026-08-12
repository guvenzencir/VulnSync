from scapy.all import sniff, ARP, Ether, srp
import subprocess
import time
import os

# Veritabanı istihbarat modülümüz
from threat_matcher import check_target_vulnerabilities

# --- KULLANICI YAPILANDIRMASI ---
GATEWAY_IP = "10.0.2.1" # Kendi modem/gateway IP'ni yazmayı unutma
IFACE = "eth0"          # Kendi arayüzünü (örn: eth0 veya wlan0) yaz
REAL_GATEWAY_MAC = None
UNDER_ATTACK = False
BLOCKED_MACS = set()    # Kara listemiz (Tekrarlayan işlemleri engeller)

def get_real_mac(ip):
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    answered, _ = srp(arp_request, timeout=2, verbose=False, iface=IFACE)
    if answered:
        return answered[0][1].hwsrc
    return None

def iptables_block_attacker(attacker_mac):
    """Saldırganı engeller ama senin internetini kesmez."""
    print(f"[!] İptables Kalkanı: Saldırgan ({attacker_mac}) engelleniyor!")
    # Sadece saldırganın MAC adresinden gelen paketleri çöpe atıyoruz
    subprocess.call(["iptables", "-A", "INPUT", "-m", "mac", "--mac-source", attacker_mac, "-j", "DROP"])
    print("[+] Saldırgan başarıyla kilitlendi.")

def restore_network_cache():
    """İnterneti kesmeden sadece zehirlenmiş ARP tablosunu temizler."""
    print("[*] Sistemdeki zehirli ARP önbelleği (cache) temizleniyor...")
    # 'ip neigh flush all' komutu ağ bağlantısını koparmaz, sadece MAC eşleşmelerini sıfırlar
    subprocess.call(["ip", "neigh", "flush", "all"])
    print("[+] Ağ temizlendi, internet bağlantısı güvende!\n")

def process_packet(packet):
    global UNDER_ATTACK
    
    if UNDER_ATTACK:
        return

    if packet.haslayer(ARP) and packet[ARP].op in (1, 2):
        if packet[ARP].psrc == GATEWAY_IP:
            claimed_mac = packet[ARP].hwsrc
            
            if claimed_mac != REAL_GATEWAY_MAC:
                # EĞER BU MAC ZATEN BLOKLANDIYSA, HİÇBİR ŞEY YAPMA VE SESSİZCE GEÇ
                if claimed_mac in BLOCKED_MACS:
                    return

                UNDER_ATTACK = True
                print(f"\n[!] TEHLİKE! ARP Zehirlenmesi Tespit Edildi!")
                print(f"    Saldırgan MAC : {claimed_mac}")
                print(f"    Gerçek Modem  : {REAL_GATEWAY_MAC}")
                
                # --- VULNSYNC İSTİHBARAT ENTEGRASYONU ---
                print("\n[*] Saldırgan profili veritabanında analiz ediliyor...")
                hedef_os = "Linux" # Örnek saldırgan platformu
                
                tehditler = check_target_vulnerabilities(hedef_os, max_results=2)
                
                if tehditler:
                    print(f"[!] Saldırgan platformu ({hedef_os}) için risk bulundu!")
                    
                # 1. Aşama: Sadece saldırganı blokla (İnternetin gitmez)
                iptables_block_attacker(claimed_mac)
                
                # Kara listeye ekle ki aynı kişi için sürekli veritabanı yorulmasın!
                BLOCKED_MACS.add(claimed_mac)
                
                # 2. Aşama: Zehri temizle (İnternetin gitmez)
                restore_network_cache()
                
                print("[*] Yeni saldırılar için dinlemeye devam ediliyor (3 saniye mola)...")
                time.sleep(3)
                UNDER_ATTACK = False

def main():
    global REAL_GATEWAY_MAC
    
    # Root yetkisi kontrolü
    if os.geteuid() != 0:
        print("[-] HATA: İptables ve önbellek temizliği için sudo yetkisi gereklidir!")
        print("    Lütfen 'sudo python3 arp_detector.py' şeklinde çalıştırın.")
        return

    print("[*] Ağ geçidinin gerçek MAC adresi tespit ediliyor...")
    REAL_GATEWAY_MAC = get_real_mac(GATEWAY_IP)
    
    if not REAL_GATEWAY_MAC:
        print(f"[-] Ağ geçidine ({GATEWAY_IP}) ulaşılamadı. IP ve arayüz ayarlarını kontrol et.")
        return

    print(f"[+] Gerçek Gateway MAC Adresi: {REAL_GATEWAY_MAC}")
    print(f"[*] {IFACE} üzerinden ARP trafiği dinleniyor... (Durdurmak için Ctrl+C)")
    
    try:
        sniff(filter="arp", store=False, prn=process_packet, iface=IFACE)
    except KeyboardInterrupt:
        print("\n[*] Dinleme sonlandırıldı.")

if __name__ == "__main__":
    main()
