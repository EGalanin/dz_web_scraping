import requests
from bs4 import BeautifulSoup
from pprint import pprint
from fake_headers import Headers
import re

# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
url = 'https://habr.com/ru/all/'
main_url = 'https://habr.com'
HEADERS = Headers(os='win', headers=True).generate()

res = requests.get(url, headers=HEADERS)
# text = res.text
# pprint(text)
soup = BeautifulSoup(res.text, 'html.parser')
articles = soup.find_all('article', class_='tm-articles-list__item')


def get_list_article(articles):
    list_articles = []
    for article in articles:
        public_date = article.find('span', class_='tm-article-snippet__datetime-published').text
        # print(public_date)
        headline = article.h2.a.text
        # print(headline)
        link_ = article.find('a', class_='tm-article-snippet__title-link').get('href')
        # print(link_)
        preview_text = article.find('div', class_='tm-article-body tm-article-snippet__lead').text
        preview_text = re.findall(r'\b\w*\b', preview_text)
        preview_text = {x.lower() for x in preview_text if x != ''}
        # print(preview_text)
        # print()
        # Находим совпадения по превью
        # if set(KEYWORDS).intersection(preview_text):
        #     list_articles.append(f'Дата: {public_date} - Заголовок: {headline} - Ссылка: {main_url}{link_}')

        # поиск совпадений по всему тексту статьи
        url_ = main_url + link_
        res_ = requests.get(url_)
        soup = BeautifulSoup(res_.text, 'html.parser')
        full_text = soup.find('div', class_='tm-article-body').text
        full_text = re.findall(r'\b\w*\b', full_text)
        full_text = {x.lower() for x in full_text if x != ''}

        if set(KEYWORDS).intersection(full_text):
            list_articles.append(f'Дата: {public_date} - Заголовок: {headline} - Ссылка: {main_url}{link_}')

        # for i in KEYWORDS:
        #     if (i.lower() in headline.lower()) or (i.lower() in full_text.lower()):
        #         list_articles.append(f'Дата: {public_date} - Заголовок: {headline} - Ссылка: {main_url}{link_}')

    return list_articles


if __name__ == '__main__':
    pprint(get_list_article(articles))
