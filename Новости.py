import sys
import requests
from bs4 import BeautifulSoup
url = 'https://news.am/rus/news/allregions/allthemes/'
try:
    response = requests.get(url)
except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as err:
      print(f"Ошибка - Невозможно установить соединение: {err}.")
except Exception as err:
      print(f"Ошибка - Произошла неизвестная ошибка: {err}.")
      sys.exit()
else:
    print("Успешное подключение к ", url)
    filteredNews = []
    NewsBlock = []
    # Получаем текст страницы
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features="html.parser")
    NewsBlock = soup.findAll('a') #весь блок под тегом <а с новостями

    for data in NewsBlock:
     if data.find('span', class_='title') is not None:
        Tstr=data.text.replace('\n', ' ') #замена перревода строки на пробел
        Tstr = Tstr.replace('  ', ' ')    #замена двойных пробелов на один
        filteredNews.append(Tstr)                     #запись строк в список
    #print(NewsBlock)
    for data in filteredNews:
      print(data)
