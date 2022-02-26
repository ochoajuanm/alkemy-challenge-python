from datetime import datetime
import locale
import logging
import os
import requests
from utils import categories_urls, day_month_year, year_month, main_logger


locale.setlocale(locale.LC_ALL, 'es_AR.UTF-8')
logger = logging.getLogger("").getChild(__name__)

def get_csv():

    """
        Realiza un request a la URL de cada dataset de la web de datos del gobierno
    """
    try:
        for category, url in categories_urls.items():
            with requests.get(url) as r:
                if r.status_code == 200:
                    logger.debug(f'Request a {url} OK')
                    path = f'categorias/{category}/{year_month}/'
                    file_name = f'{category}-{day_month_year}.csv'
                    file_path = path + file_name
                    if os.path.isdir(path) == False:
                        os.makedirs(path)
                    with open(file_path, 'wb') as f:
                        f.write(r.content)
                        f.close()
                        logger.info(f'Se ha generado el archivo {file_name} a partir de la url: {url}')
                else:
                    logger.error('Hubo un error con la conexión a la fuente de datos')
    except ValueError as e:
        logger.error('Ha ocurrido un error con la información')
    except Exception as e:
        logger.error(f'Ha ocurrido el siguiente error: {e}')
    else:
        logger.info('Se ha ejecutado la extracción de toda la información con éxito')


if __name__ == '__main__':
    logger = main_logger(__file__)
    get_csv()