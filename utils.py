from datetime import datetime
import locale
import logging
import os
import pandas as pd
from sqlalchemy.types import INTEGER, String, TIMESTAMP

locale.setlocale(locale.LC_ALL, 'es_AR.UTF-8')
logger = logging.getLogger("").getChild(__name__)

# Dataset variables

# No funciona API http://datos.gob.ar/api/3/action/datastore_search?resource_id={id_dataset}

categories_urls = {
                        "museos": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museo.csv", 
                        "salas-de-cine": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv", 
                        "bibliotecas-populares": "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv"
                    }


# Date variables

year_month = str(datetime.today().strftime('%Y')) + '-' + str(datetime.today().strftime('%B'))
day_month_year = str(datetime.today().strftime('%d')) + '-' + str(datetime.today().strftime('%m')) + '-' + str(datetime.today().strftime('%Y'))

# Path variables

path_file_cinema = f'categorias/salas-de-cine/{year_month}/salas-de-cine-{day_month_year}.csv'
path_file_library = f'categorias/bibliotecas-populares/{year_month}/bibliotecas-populares-{day_month_year}.csv'
path_file_museum = f'categorias/museos/{year_month}/museos-{day_month_year}.csv'

path_temp_total_table = 'temp_data/df_total_table.csv'
path_temp_total_summary_table = 'temp_data/df_total_summary_table.csv'
path_temp_cinema_summary_table = 'temp_data/df_cinema_summary_table.csv'

# Dataframe variables

reduced_columns = ['cod_loc',
                    'idprovincia',
                    'iddepartamento',
                    'categoria',
                    'provincia',
                    'localidad',
                    'nombre',
                    'direccion',
                    'cp',
                    'telefono',
                    'mail',
                    'fuente',
                    'web']

# SQL Dict column types

dict_columns_types = {
                    'cod_loc': INTEGER(),
                    'idprovincia': INTEGER(),
                    'iddepartamento': INTEGER(),
                    'categoria': String(),
                    'provincia': String(),
                    'localidad': String(),
                    'nombre': String(),
                    'direccion': String(),
                    'cp': String(),
                    'telefono': String(),
                    'mail': String(),
                    'fuente': String(),
                    'web': String(),
                    'creado_el': TIMESTAMP()
                    }

dict_columns_types_summary_total = {
                                    'tipo_agrupacion': String(),
                                    'descripcion': String(),
                                    'total': INTEGER(),
                                    'creado_el': TIMESTAMP()
                                    }


dict_columns_types_summary_cinema = {
                                    'provincia': String(),
                                    'butacas': INTEGER(),
                                    'espacio_incaa': INTEGER(),
                                    'pantallas': INTEGER(),
                                    'creado_el': TIMESTAMP()
                                    }


def replace_special_characters(list):

    """Recibe una lista y transforma los caracteres de sus ítems:
        - Con tilde a sin tilde
        - Espacio por guión bajo
        - ñ por ni
    """

    dict = {'á': 'a', 'é':'e', 'í': 'i', 'ó': 'o', 'ú': 'u', ' ': '_', 'ñ': 'ni'}

    fixed_list = []
    for item in list:
        transTable = item.maketrans(dict)
        fixed_item = item.translate(transTable)
        fixed_list.append(fixed_item)
    
    return fixed_list


def fix_columns(df):

    """Estandariza los nombres de columnas para dataframe. 
        Transforma a minúsculas, sin tildes y sin espacios.
    """
    
    columns_lower = [i.lower() for i in df.columns]
    columns_lower = replace_special_characters(columns_lower)
    dict_columns = dict(zip(df.columns, columns_lower))
    df.rename(columns=dict_columns, inplace=True)
    
    try:
        df.rename(columns={'domicilio': 'direccion'}, inplace=True)
    except KeyError:
        logger.debug('No se encontró la columna "domicilio"')
        
    return df


def main_logger(filename):

    """Configuración para el logger dependiendo su nivel de ejecución (root o module name)"""

    if not os.path.exists('logs'):
        os.mkdir('logs')

    logging.basicConfig(
    format = '%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s',
    level  = logging.DEBUG,
    filemode = "a"
    )

    # Si el root logger ya tiene handlers, se eliminan antes de añadir los nuevos.
    # Esto es importante para que los logs no empiezen a duplicarse.

    if logging.getLogger('').hasHandlers():
        logging.getLogger('').handlers.clear()

    # Se añaden dos nuevos handlers al root logger, uno para los niveles de debug o superiores
    # y otro para que se muestre por pantalla los niveles de info o superiores.

    filename = filename.replace('.py', '')
    file_debug_handler = logging.FileHandler(f'logs/{filename}.log' )
    file_debug_handler.setLevel(logging.DEBUG)
    file_debug_format = logging.Formatter('%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s')
    file_debug_handler.setFormatter(file_debug_format)
    logging.getLogger('').addHandler(file_debug_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler_format = logging.Formatter('%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s')
    console_handler.setFormatter(console_handler_format)
    logging.getLogger('').addHandler(console_handler)

    return logging.getLogger('')


if __name__ == '__main__':
    pass