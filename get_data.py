import requests
from datetime import datetime
import os
import locale
from categories_url import categories_urls

locale.setlocale(locale.LC_ALL, 'es_AR.UTF-8')

year_month = str(datetime.today().strftime('%Y')) + '-' + str(datetime.today().strftime('%B'))
day_month_year = str(datetime.today().strftime('%d')) + '-' + str(datetime.today().strftime('%m')) + '-' + str(datetime.today().strftime('%Y'))

def get_csv():

    """
        Realiza un request a la URL de cada dataset de la web de datos del gobierno
    """
    try:
        for category, url in categories_urls.items():
            with requests.get(url) as r:
                if r.status_code == 200:
                    path = f'categorias/{category}/{year_month}/'
                    file_name = f'{category}-{day_month_year}.csv'
                    file_path = path + file_name
                    if os.path.isdir(path) == False:
                        os.makedirs(path)
                    with open(file_path, 'wb') as f:
                        f.write(r.content)
                        f.close()
                        print(f'Se ha generado el archivo {file_name} a partir de la url: {url}')
                else:
                    print('Hubo un error con la conexión a la fuente de datos')
    except ValueError as e:
        print('Ha ocurrido un error con la información')
    except Exception as e:
        pass
    else:
        print('Se ha ejecutado la extracción de toda la información con éxito')


if __name__ == '__main__':
    get_csv()