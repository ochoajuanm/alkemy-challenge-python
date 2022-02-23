import requests
from datetime import datetime
import os
import locale
from categorias_url import categories_urls

locale.setlocale(locale.LC_ALL, 'es_AR.UTF-8')

year_month = str(datetime.today().strftime('%Y')) + '-' + str(datetime.today().strftime('%B'))
day_month_year = str(datetime.today().strftime('%d')) + '-' + str(datetime.today().strftime('%m')) + '-' + str(datetime.today().strftime('%Y'))    


def get_csv():
    for category, url in categories_urls.items():
        with requests.get(url) as r:
            path = f'categorias/{category}/{year_month}/'
            file_path = path + f'{category}-{day_month_year}.csv'
            if os.path.isdir(path) == False:
                os.makedirs(path)
            with open(file_path, 'wb') as f:
                f.write(r.content)

if __name__ == '__main__':
    get_csv()