import requests
from bs4 import BeautifulSoup

url = 'https://www.emlakjet.com/gunluk-kiralik-konut/'
response = requests.get(url)
html_data = response.text

soup = BeautifulSoup(html_data, 'html.parser')

ilanlar = soup.find_all('div', class_='_3qUI9q')
ozellikler = soup.find('div', class_='_2UELHn')   

if ilanlar or ozellikler:
 
 for ilan in ilanlar:

            ilan_basligi = ilan.find('h3')
            ilan_fiyati = ilan.find('p', class_='_2C5UCT')
            ilan_konumu = ilan.find('div', class_='_2wVG12')

            ozellik_1 = ozellikler.find('span', {'data-test-selector': 'listing-item-property-category-1'})
            ozellik_2 = ozellikler.find('span', {'data-test-selector': 'listing-item-property-room-count-1'})
            ozellik_3 = ozellikler.find('span', {'data-test-selector': 'listing-item-property-floor-number-1'})
            ozellik_4 = ozellikler.find('span', {'data-test-selector': 'listing-item-property-gross-square-1'})
            ozellik_5 = ozellikler.find('span', {'data-test-selector': 'listing-item-property-updated-at-1'})

            print(f"Ilan Başlığı: {ilan_basligi.text.strip()}")
     
            print(f"Fiyat: {ilan_fiyati.text.strip()}")
                  
            print(f"Konum: {ilan_konumu.text.strip()}")
                   
            print(f"Ev Tipi: {ozellik_1.text.strip()}")
                   
            print(f"Oda Sayisi: {ozellik_2.text.strip()}")
                    
            print(f"Bulundugu Kat: {ozellik_3.text.strip()}")
                   
            print(f"Buyukluk: {ozellik_4.text.strip()}")
                    
            print(f"Tarih: {ozellik_5.text.strip()}")

            print('------------------------------')                
           
else:
        print("İlanlar bulunamadı.")
