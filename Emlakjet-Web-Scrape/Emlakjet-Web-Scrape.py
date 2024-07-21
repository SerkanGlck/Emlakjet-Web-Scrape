import requests
from bs4 import BeautifulSoup
import json
import time
import iso8601
from datetime import datetime, timedelta

url = 'https://www.emlakjet.com/gunluk-kiralik-konut'
onceki_ids = set()
json_dosya_yolu = 'ilanlar.json'

def ilan_id_ve_linkleri_getir():
    cevap = requests.get(url)
    soup = BeautifulSoup(cevap.text, 'html.parser')
    ilanlar = soup.find_all('div', class_='_3qUI9q')

    mevcut_id_ve_linkler = []
    for ilan in ilanlar:
        link_etiketi = ilan.find('a', href=True)
        if link_etiketi:
            ilan_id = ilan.get('data-id')
            if ilan_id:
                mevcut_id_ve_linkler.append((ilan_id, link_etiketi['href']))

    return mevcut_id_ve_linkler

def ilan_detaylarini_getir(ilan_id, ilan_link):
    ilan_url = f'https://www.emlakjet.com{ilan_link}'
    ilan_cevap = requests.get(ilan_url)
    ilan_soup = BeautifulSoup(ilan_cevap.text, 'html.parser')

  
    ilan_basligi_etiketi = ilan_soup.find('h1', class_="_3OKyci")
    ilan_basligi = ilan_basligi_etiketi.text.strip() if ilan_basligi_etiketi else "Baslik bulunamadi"


    ilan_fiyati_etiketi = ilan_soup.find('div', class_='_2TxNQv')
    ilan_fiyati = ilan_fiyati_etiketi.text.strip() if ilan_fiyati_etiketi else "Fiyat bulunamadi"


    ilan_konumu_etiketi = ilan_soup.find('div', class_='_3VQ1JB')
    ilan_konumu = ilan_konumu_etiketi.find('p').text.strip() if ilan_konumu_etiketi and ilan_konumu_etiketi.find('p') else "Konum bulunamadi"

    detaylar = {
        'url': ilan_url,
        'baslik': ilan_basligi,
        'fiyat': ilan_fiyati,
        'konum': ilan_konumu,
        'Ilan Numarasi': ilan_id
    }

    ilan_detaylari = ilan_soup.find_all('div', class_='_35T4WV')
    for detay in ilan_detaylari:
        bilgi_kategori = detay.find_all('div', class_='_1bVOdb')
        if len(bilgi_kategori) == 2:
            kategori = bilgi_kategori[0].text.strip()
            bilgi = bilgi_kategori[1].text.strip()
            detaylar[kategori] = bilgi

    # Tarihi donusturme
    if 'İlan Oluşturma Tarihi' in detaylar:
        try:
            cevrilmis_tarih = iso8601.tarihi_çevir(detaylar['İlan Oluşturma Tarihi'])
            cevrilmis_tarih_dt = datetime.fromisoformat(cevrilmis_tarih)
            if datetime.now() - cevrilmis_tarih_dt > timedelta(days=3):
                return None
            detaylar['İlan Oluşturma Tarihi'] = cevrilmis_tarih
        except Exception as e:
            detaylar['İlan Oluşturma Tarihi'] = f"Tarih donusturme hatasi: {e}"

    if 'İlan Güncelleme Tarihi' in detaylar:
        try:
            detaylar['İlan Güncelleme Tarihi'] = iso8601.tarihi_çevir(detaylar['İlan Güncelleme Tarihi'])
        except Exception as e:
            detaylar['İlan Güncelleme Tarihi'] = f"Tarih donusturme hatasi: {e}"

    return detaylar

def onceki_verileri_yukle():
    try:
        with open(json_dosya_yolu, 'r', encoding='utf-8') as dosya:
            veri = json.load(dosya)
            if not isinstance(veri, dict):
                print("JSON dosyasi gecersiz formatta.")
                return {}
            return veri
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def jsona_kaydet(veri):
    with open(json_dosya_yolu, 'w', encoding='utf-8') as dosya:
        json.dump(veri, dosya, ensure_ascii=False, indent=4)

onceki_veriler = onceki_verileri_yukle()
onceki_ids = set(onceki_veriler.keys())  

while True:
    mevcut_id_ve_linkler = ilan_id_ve_linkleri_getir()
    mevcut_veri = {}
    yeni_id_ve_linkler = [(ilan_id, link) for ilan_id, link in mevcut_id_ve_linkler if ilan_id not in onceki_ids]
    
    if yeni_id_ve_linkler:
        toplam_yeni_ilan = len(yeni_id_ve_linkler)
        for ilan_id, link in yeni_id_ve_linkler:
            detaylar = ilan_detaylarini_getir(ilan_id, link)
            if detaylar is not None: 
                mevcut_veri[ilan_id] = detaylar
                print(f"Kayit edilen ilan ID'si: {ilan_id}")
    
    if mevcut_veri:
        onceki_veriler.update(mevcut_veri)
        jsona_kaydet(onceki_veriler)
        onceki_ids.update(mevcut_veri.keys())
    
    print(f"Toplam {len(yeni_id_ve_linkler)} ilan bulundu, {len(mevcut_veri)} ilan kaydedildi.")
    print("Yeni ilanlar icin 5 dakika bekleniyor...")
    time.sleep(300)