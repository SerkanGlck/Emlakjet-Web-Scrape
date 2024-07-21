import requests
from bs4 import BeautifulSoup
import json
import time
import iso8601
from datetime import datetime, timedelta

url = 'https://www.emlakjet.com/gunluk-kiralik-konut'
previous_ids = set()  
json_file_path = 'ilanlar.json'

def fetch_listing_ids_and_links():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('div', class_='_3qUI9q')

    current_ids_and_links = []
    for listing in listings:
        link_tag = listing.find('a', href=True)
        if link_tag:
            ilan_id = listing.get('data-id')
            if ilan_id:
                current_ids_and_links.append((ilan_id, link_tag['href']))

    return current_ids_and_links

def fetch_listing_details(ilan_id, ilan_link):
    ilan_url = f'https://www.emlakjet.com{ilan_link}'
    ilan_response = requests.get(ilan_url)
    ilan_soup = BeautifulSoup(ilan_response.text, 'html.parser')

    # İlan başlığı kontrolü
    ilan_basligi_tag = ilan_soup.find('h1', class_="_3OKyci")
    ilan_basligi = ilan_basligi_tag.text.strip() if ilan_basligi_tag else "Başlık bulunamadı"

    # İlan fiyatı kontrolü
    ilan_fiyati_tag = ilan_soup.find('div', class_='_2TxNQv')
    ilan_fiyati = ilan_fiyati_tag.text.strip() if ilan_fiyati_tag else "Fiyat bulunamadı"

    # İlan konumu kontrolü
    ilan_konumu_tag = ilan_soup.find('div', class_='_3VQ1JB')
    ilan_konumu = ilan_konumu_tag.find('p').text.strip() if ilan_konumu_tag and ilan_konumu_tag.find('p') else "Konum bulunamadı"

    detaylar = {
        'url': ilan_url,
        'başlık': ilan_basligi,
        'fiyat': ilan_fiyati,
        'konum': ilan_konumu,
        'İlan Numarası': ilan_id
    }

    ilan_detaylari = ilan_soup.find_all('div', class_='_35T4WV')
    for detay in ilan_detaylari:
        bilgi_kategori = detay.find_all('div', class_='_1bVOdb')
        if len(bilgi_kategori) == 2:
            kategori = bilgi_kategori[0].text.strip()
            bilgi = bilgi_kategori[1].text.strip()
            detaylar[kategori] = bilgi

    # İlan oluşturma tarihini ve güncelleme tarihini dönüştürme
    if 'İlan Oluşturma Tarihi' in detaylar:
        try:
            çevrilmiş_tarih = iso8601.tarihi_çevir(detaylar['İlan Oluşturma Tarihi'])
            çevrilmiş_tarih_dt = datetime.fromisoformat(çevrilmiş_tarih)
            if datetime.now() - çevrilmiş_tarih_dt > timedelta(days=3):
                print(f"İlan oluşturulma tarihi {ilan_id} şu anın tarihinden 3 günden eski, listeye alınmayacak.")
                return None
            detaylar['İlan Oluşturma Tarihi'] = çevrilmiş_tarih
        except Exception as e:
            detaylar['İlan Oluşturma Tarihi'] = f"Tarih dönüştürme hatası: {e}"

    if 'İlan Güncelleme Tarihi' in detaylar:
        try:
            detaylar['İlan Güncelleme Tarihi'] = iso8601.tarihi_çevir(detaylar['İlan Güncelleme Tarihi'])
        except Exception as e:
            detaylar['İlan Güncelleme Tarihi'] = f"Tarih dönüştürme hatası: {e}"

    return detaylar

def load_previous_data():
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not isinstance(data, dict):
                print("JSON dosyası geçersiz formatta.")
                return {}
            return data
    except FileNotFoundError:
        print("JSON dosyası bulunamadı. Yeni bir dosya oluşturulacak.")
        return {}
    except json.JSONDecodeError:
        print("JSON dosyası okunamadı veya bozuk. Yeni bir dosya oluşturulacak.")
        return {}

def save_to_json(data):
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

print("Başlangıçta ilanlar kontrol ediliyor...")

previous_data = load_previous_data()
previous_ids = set(previous_data.keys())  # Mevcut ID'leri yükle

while True:
    print("Yeni ilanlar kontrol ediliyor...")
    current_ids_and_links = fetch_listing_ids_and_links()
    
    current_data = {}
    new_ids_and_links = [(ilan_id, link) for ilan_id, link in current_ids_and_links if ilan_id not in previous_ids]
    if new_ids_and_links:
        print(f"Yeni ilanlar bulundu: {len(new_ids_and_links)} adet")
        for ilan_id, link in new_ids_and_links:
            print(f"Yeni ilan işleniyor: ID - {ilan_id}, Link - {link}")
            detaylar = fetch_listing_details(ilan_id, link)
            if detaylar is not None:  # Sadece geçerli ilanları ekle
                current_data[ilan_id] = detaylar
    
    if current_data:
        previous_data.update(current_data)
        save_to_json(previous_data)
        previous_ids.update(current_data.keys())
    
    print("Yeni ilanlar için 2 dakika bekleniyor...")
    time.sleep(120)
