import random
import time
import json

import requests
from bs4 import BeautifulSoup

from utils import format_datetime, format_link, format_news

if __name__ == '__main__':
    print('requesting...')
    target_url = 'https://m.liputan6.com/news'
    response = requests.get(target_url)
    if response.status_code == 200:     # request successful
        print('request successful')
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', attrs={'class': 'article-snippet__image js-article-snippet-image'})
        contents = []
        for div in divs:
            a_tag = div.find('a')
            title = a_tag.get('title')
            link = a_tag.get('href')
            if not title.startswith('FOTO:') and not title.startswith('VIDEO:'):
                # bukan konten foto / video
                temp = {
                    'title': title,
                    'url': format_link(link)
                }
                contents.append(temp)

        print('{} titles & urls successfully extracted'.format(len(contents)))

        # melihat setiap berita
        for idx in range(len(contents)):
            random.seed(time.time())
            sleep_time = random.randrange(30, 90)
            time.sleep(sleep_time)
            print()
            print('requesting page {}'.format(idx))
            c_request = requests.get(contents[idx]['url'])
            if c_request.status_code == 200:
                c_soup = BeautifulSoup(c_request.text, 'html.parser')
                dt_date, dt_time = format_datetime(c_soup.find('span', attrs={'class': 'article-header__datetime'}).text)
                news_paragraph = format_news(c_soup.find_all('p'))      # berita per paragraf
                contents[idx]['date'] = dt_date
                contents[idx]['time'] = dt_time
                contents[idx]['news_content'] = news_paragraph
                print('page {} has been processed'.format(idx))
            else:
                print('page {} failed to be processed'.format(idx))
		
		print('exporting to json')
		with open('data/data.json', 'w') as f_json:
			json.dump(contents, f_json)