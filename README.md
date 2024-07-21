# Emlakjet Web Scraper

## Proje Açıklaması

Emlakjet Web Scraper, Emlakjet web sitesindeki gayrimenkul ilanlarını tarayarak ilan detaylarını toplamak için geliştirilmiş bir projedir. Bu proje, çekilen verilerdeki tarihleri ISO 8601 foramtına çevirir ve ilan verilerini JSON formatında saklar.

## Özellikler

- Emlakjet web sitesinden ilan verilerini toplar.
- Çeşitli tarih formatlarını ISO 8601 formatına dönüştürür.
- İlan verilerini JSON formatında saklar.
- Her 2 dakikada bir yeni ilanları kontrol eder ve veri tabanına ekler.

## Gereksinimler

### Yazılım Gereksinimleri

- **Python 3.X** veya üzeri: Proje Python 3.12.4 sürümü ile geliştirilmiştir. Python'un daha yeni sürümleri de uyumlu olabilir, ancak test edilmemiştir.

### Python Kütüphaneleri

Proje, aşağıdaki Python kütüphanelerini kullanmaktadır:

- **requests**: HTTP istekleri yapmak için.
- **beautifulsoup4**: HTML parse etmek için.

## Kurulum ve Çalıştırma

### Docker Kullanarak Çalıştırma

1. **Projeyi konteyner içinde çalıştırmak için.**

   Docker Hub'dan Docker imajını indirin:

   ```sh
   docker pull serkanglck/emlakjet-web-scrape
