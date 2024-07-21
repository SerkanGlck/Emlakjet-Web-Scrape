import re
from datetime import datetime, timedelta


ay_sözlüğü = {
    'ocak': '01', 'şubat': '02', 'mart': '03', 'nisan': '04', 'mayıs': '05', 'haziran': '06',
    'temmuz': '07', 'ağustos': '08', 'eylül': '09', 'ekim': '10', 'kasım': '11', 'aralık': '12',
    'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07',
    'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12',
    'oca': '01', 'şub': '02', 'mar': '03', 'nis': '04', 'may': '05', 'haz': '06',
    'tem': '07', 'ağu': '08', 'eyl': '09', 'eki': '10', 'kas': '11', 'ara': '12',
}

def am_pm_to_24h(saat_str):
    if 'am' in saat_str.lower():
        saat_str = saat_str.lower().replace('am', '').strip()
        saat, dakika = saat_str.split(':')
        saat = '00' if saat == '12' else saat.zfill(2)
    elif 'pm' in saat_str.lower():
        saat_str = saat_str.lower().replace('pm', '').strip()
        saat, dakika = saat_str.split(':')
        saat = str(int(saat) + 12) if saat != '12' else saat
        saat = saat.zfill(2)
    else:
        saat, dakika = saat_str.split(':')
        saat = saat.zfill(2)
    return f"{saat}:{dakika.zfill(2)}"

def tarihi_çevir(tarih_str):
    # ISO 8601 formatında olup olmadığını kontrol et 
    if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}([+\-]\d{2}:\d{2}|Z)?$", tarih_str):
        return tarih_str

    # Varsa giriş tarihini temizle
    tarih_str = tarih_str.lower().strip()
    tarih_str = tarih_str.replace('yayınlanma tarihi:', '').replace('pazartesi', '').replace('salı', '').replace('çarşamba', '').replace('perşembe', '').replace('cumartesi', '').replace('cuma', '').replace('pazar', '').replace(',', '').replace('.', '').replace('|', '').strip()

    if 'saat önce' in tarih_str:
        saat_önce = int(tarih_str.split(' ')[0])
        çevrilmiş_tarih = datetime.now() - timedelta(hours=saat_önce)
        return çevrilmiş_tarih.isoformat()
    
    if 'gün önce' in tarih_str:
        gün_önce = int(tarih_str.split(' ')[0])
        çevrilmiş_tarih = datetime.now() - timedelta(days=gün_önce)
        return çevrilmiş_tarih.isoformat()
    
    if 'ay önce' in tarih_str:
        ay_önce = int(tarih_str.split(' ')[0])
        çevrilmiş_tarih = datetime.now()
        ay = (çevrilmiş_tarih.month - ay_önce) % 12 or 12
        yıl = çevrilmiş_tarih.year - (çevrilmiş_tarih.month - ay_önce) // 12
        gün = min(çevrilmiş_tarih.day, [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][ay-1])
        çevrilmiş_tarih = datetime(yıl, ay, gün)
        return çevrilmiş_tarih.isoformat()
    
    if 'yıl önce' in tarih_str:
        yıl_önce = int(tarih_str.split(' ')[0])
        çevrilmiş_tarih = datetime.now() - timedelta(days=yıl_önce * 365)
        return çevrilmiş_tarih.isoformat()
    
    if 'hafta önce' in tarih_str:
        hafta_önce = int(tarih_str.split(' ')[0])
        çevrilmiş_tarih = datetime.now() - timedelta(weeks=hafta_önce)
        return çevrilmiş_tarih.isoformat()
    
    # Tarih bileşenlerini bulmak için
    tarih_bileşenleri = tarih_str.split()
    gün = None
    ay = None
    yıl = None
    saat = '00:00'

    for bileşen in tarih_bileşenleri:
        if bileşen.isdigit() and len(bileşen) in [1, 2]:  # Gün
            gün = bileşen.zfill(2)
        elif bileşen.isdigit() and len(bileşen) in [2, 4]:  # Yıl
            yıl = bileşen
        elif ':' in bileşen:  # Saat
            saat = bileşen
        elif bileşen.lower() in ['am', 'pm']:  # AM/PM
            saat = am_pm_to_24h(saat + ' ' + bileşen)
        elif bileşen.lower() in ay_sözlüğü:  # Ay
            ay = bileşen.lower()

    # Eğer yıl yoksa, günümüz yılını kullan
    if not yıl:
        yıl = str(datetime.now().year)

    # Eğer ay yoksa, Ocak ayını kullan
    if not ay:
        ay = 'ocak'

    # Eğer gün yoksa, 01 gününü kullan
    if not gün:
        gün = '01'

    # Ay ismini numaraya çevir
    ay = ay_sözlüğü.get(ay, '01').zfill(2)

    # İki basamaklı yıllar
    yıl = '20' + yıl if len(yıl) == 2 and int(yıl) < 50 else '19' + yıl if len(yıl) == 2 else yıl

    çevrilmiş_tarih_str = f"{yıl}-{ay}-{gün}T{saat}:00"
    return çevrilmiş_tarih_str
