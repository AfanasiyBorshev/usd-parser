import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)
import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

url = "https://www.psbank.ru/personal/rates"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    print("Запрашиваем курсы с ПСБ...")
    response = requests.get(url, headers=headers, verify=False, timeout=10)
    
    if response.status_code == 200:
        print("✅ Сайт ПСБ успешно открыт!")
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr', class_='exchange-rates__table-row')
        
        if len(rows) > 1:
            target_row = rows[1] 
            cells = target_row.find_all('td')
            
            if len(cells) >= 3:
                buy_rate = cells[1].text.strip()
                sell_rate = cells[2].text.strip()
                
                print(f"\n💵 Наличный курс доллара (USD):")
                print(f"   Покупка: {buy_rate} ₽")
                print(f"   Продажа: {sell_rate} ₽")
                
                now = datetime.now()
                date_str = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M")
                
                csv_path = 'rates.csv'
                file_exists = os.path.isfile(csv_path)
                
                with open(csv_path, 'a', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file, delimiter=';')
                    
                    if not file_exists:
                        writer.writerow(['Дата', 'Время', 'Покупка', 'Продажа'])
                    
                    writer.writerow([date_str, time_str, buy_rate, sell_rate])
                    
                print(f"💾 Данные сохранены в rates.csv!")
            else:
                print("❌ В строке недостаточно ячеек")
        else:
            print(" Не удалось найти нужную строку")
    else:
        print(f"❌ Ошибка при открытии сайта: {response.status_code}")
        
except Exception as e:
    print(f"❌ Произошла ошибка: {e}")
