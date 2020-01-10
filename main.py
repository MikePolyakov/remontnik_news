import requests
from bs4 import BeautifulSoup
import pprint

domain = 'https://www.remontnik.ru'
url = f'{domain}/news'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    result = {}

    # ищем все новости
    all_news_tag_a = soup.find_all('a', class_='news-list__item')

    for one_news_tag_a in all_news_tag_a:
        # получаем ссылку на новость
        href = one_news_tag_a.get('href')

        # идем на страницу новости
        url = f'{domain}{href}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # ищем дату новости
        news_date_tag_div = soup.find('div', class_='news-list__date')
        date = news_date_tag_div.text

        # ищем заголовок новости
        news_title = soup.find('h1')
        title = news_title.text

        # ищем текст новости
        news_text = soup.find('p')

        # убираем переносы и пробелы
        news = news_text.text.replace("\n", "").strip()
        news = news.replace("\xa0", "").strip()
        news = news.replace("\r", "").strip()

        # добавим в словарь для хранения
        result[date] = news
        print("добавлена новость от", date, title)

    pprint.pprint(result)
