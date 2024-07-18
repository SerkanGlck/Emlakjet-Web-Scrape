import requests
from bs4 import BeautifulSoup

url = 'https://www.emlakjet.com/gunluk-kiralik-konut/'
response = requests.get(url)
html_data = response.text

soup = BeautifulSoup(html_data, 'html.parser')

ilanlar = soup.find_all('div', class_='_3qUI9q')

ilan_linkleri = []

for ilan in ilanlar:
    link_tag = ilan.find('a', href=True)
    if link_tag:
        ilan_linkleri.append(link_tag['href'])

for link in ilan_linkleri:
    ilan_url = f'https://www.emlakjet.com{link}'
    ilan_response = requests.get(ilan_url)
    ilan_html_data = ilan_response.text
    ilan_soup = BeautifulSoup(ilan_html_data, 'html.parser')

    ilan_basligi = ilan_soup.find('h1', class_="_3OKyci").text.strip()

    ilan_fiyati = ilan_soup.find('div', class_='_2TxNQv').text.strip()

    ilan_konumu = ilan_soup.find('div', class_='_3VQ1JB').find('p').text.strip()

    print(f"İlan URL: {ilan_url}")
    print(f"İlan Başlığı: {ilan_basligi}")
    print(f"Fiyat: {ilan_fiyati}")
    print(f"Konum: {ilan_konumu}")
  
    ilan_detaylari = ilan_soup.find_all('div', class_='_35T4WV')    
    for detay in ilan_detaylari:
        bilgi_kategori = detay.find_all('div', class_='_1bVOdb')
        if len(bilgi_kategori) == 2:
            kategori = bilgi_kategori[0].text.strip()
            bilgi = bilgi_kategori[1].text.strip()
            print(f"{kategori}: {bilgi}")

    print('------------------------------')