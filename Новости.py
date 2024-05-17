import logging
import sys
import datetime
import time
import requests
from bs4 import BeautifulSoup
url = 'https://news.am/rus/news/allregions/allthemes/'
logging.basicConfig(level=logging.INFO, filename="news.log", filemode="w") # настройка log-файла
# если ловим исключение, то просто выход, если нет исключений - работаем
try:
    response = requests.get(url)
except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as err:
      print(f"Ошибка - Невозможно установить соединение: {err}.")
except Exception as err:
      print(f"Ошибка - Произошла неизвестная ошибка: {err}.")
      sys.exit()
else:
    CurDT = datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()  # получаем текущую датувремя и преобразуем в ISO формат
    CDT = datetime.datetime.fromisoformat(CurDT)  # преобразуем текущую датувремя в ISO формате с часовым поясом
    CDT = CDT.replace(microsecond=0)  # убираем доли секунд
    TimeInt = CDT - datetime.timedelta(hours=4)  # задаем смещение по времени от текущего на 4 часа
    print("Успешное подключение к ", url)
    print('Текущая дата и время:', CDT)
    filteredNews = []
    NewsBlock = []
    # Получаем текст страницы
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features="html.parser")
    NewsBlock = soup.findAll('a') #весь блок под тегом <а с новостями

    #перебор всех элементов блока
    for data in NewsBlock:
        if data.find('time', class_='date') is not None:
            DTnews = data.find('time')['datetime'] # получение строки даты новости в ISO формате с часовым поясом
            DTN = datetime.datetime.fromisoformat(DTnews)  # преобразуем строку в датувремя в ISO формате с часовым поясом
            Tstr=data.find('span', class_='title') #получаем строку новости
            Tstr = data.text.replace('\n', ' ')  # замена перевода строки на пробел
            Tstr = Tstr.replace('  ', ' ')  # замена двойных пробелов на один
            print(Tstr)
            # запись в лог новостей не старее 4 часов от стартового времени
            if DTN > TimeInt:
                filteredNews.append(Tstr)
                logging.info(f"Новость {Tstr}")