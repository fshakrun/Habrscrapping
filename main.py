import requests
import bs4
import re


# ключевые слова
KEYWORDS = {'дизайн', 'фото', 'web', 'python'}

key_articles = {}

response = requests.get(url='https://habr.com/ru/all/')
response.raise_for_status()
text = response.text

soup = bs4.BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article')
for article in articles:
    previews = article.find_all(class_='tm-article-snippet')
    title = article.find('a', 'tm-article-snippet__title-link')
    title_article = title.find('span').text
    href = title['href']
    url = 'https://habr.com' + href
    date_time = article.find(class_='tm-article-snippet__datetime-published')
    date = date_time.find('time')['title'][:10]

    for preview in previews:
        preview_lower = preview.text.lower()
        preview_split = re.split('[^a-zа-яё]+', preview_lower, flags=re.IGNORECASE)
        preview_set = set(preview_split)
        if KEYWORDS & preview_set:
            key_articles[url] = [f'{date} - {title_article} - {url}']

    content = requests.get(url=url).text
    more_scrapping = bs4.BeautifulSoup(content, features='html.parser')
    page = more_scrapping.find(id='post-content-body').text
    page_lower = page.lower()
    page_split = re.split('[^a-zа-яё]+', page_lower, flags=re.IGNORECASE)
    page_set = set(page_split)
    if KEYWORDS & page_set:
        key_articles[url] = [f'{date} - {title_article} - {url}']

for key, value in key_articles.items():
    print(value)