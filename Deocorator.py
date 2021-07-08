KEYWORDS = ['Zabbix']
from datetime import datetime
import requests
from bs4 import BeautifulSoup
site = 'https://habr.com/ru/all/'
ret = requests.get('https://habr.com/ru/all/')
text = ret.text
soup = BeautifulSoup(text, 'html.parser')
post_preview = soup.find_all('article', class_='post post_preview')
path ='K:\\Logs.txt'
def parametrized_decor(parameter):
    def log_time(scraping):
        f = open(parameter, 'a', encoding='utf8')
        f.write(f'Имя функции: {scraping.__name__}' + '\n')

        def new_log(*args, **kwargs):
            data_log = datetime.now()
            date = data_log.strftime("%A-%d-%B %Y %I:%M:%S %p")
            result = scraping(post_preview)
            f.write(f'{date} -- Статьи с сайта: {str(site)}' + '\n')
            f.write(f'{date} -- Слова поиска: {str(KEYWORDS)}' + '\n')
            f.write(f'{date} -- Результат скрапинга: {str(result)}' + '\n')
            return result
        return new_log
    return log_time

@parametrized_decor(parameter=path)
def web_scraping(post_preview):
    all_result = []
    for hub in post_preview:
        text = hub.text.strip()
        for vsl in KEYWORDS:
            if vsl in text:
                date = hub.find('span', class_='post__time').text
                heading = hub.find('a', class_='post__title_link').text
                link = hub.find('a', class_='btn btn_x-large btn_outline_blue post__habracut-btn').get('href')
                all_result.append([f'Дата поста: {date.title()}, Название поста: {heading}, Ссылка на пост: {link}'])
    return all_result

s = web_scraping(post_preview)
for val in s:
 print(val[0])