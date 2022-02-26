import logging
import os
import pandas as pd
from utils import fix_columns, main_logger, path_file_cinema, path_file_library, path_file_museum, categories_urls, reduced_columns, year_month, day_month_year

logger = logging.getLogger("").getChild(__name__)

def total_data_processed():

    """
        Procesa los csv de cada categoría en uno solo y descarta columnas no utilizadas
    """

    df_total = pd.DataFrame(columns=reduced_columns)

    try:
        for category in categories_urls.keys():
            path_file = f'categorias/{category}/{year_month}/{category}-{day_month_year}.csv'
            df_processed = pd.read_csv(path_file, encoding='utf-8')
            fix_columns(df_processed)
            df_processed = df_processed[reduced_columns]
            df_total = pd.concat([df_total, df_processed], axis=0)
            df_total['provincia'].replace({
                                        'Neuquén\xa0': 'Neuquén',
                                        'Santa Fé': 'Santa Fe',
                                        'Tierra del Fuego': 'Tierra del Fuego, Antártida e Islas del Atlántico Sur'
                                        }, inplace=True)

    
        
    except FileNotFoundError:
        logger.error(f'No se pudo leer el archivo en la ruta {path_file}')
    else:
        logger.info('Se procesó el archivo de todas las categorías en una tabla correctamente ')
        return df_total


def summary_tables_total(df=None):

    """
        Resumen de la tabla total según:
        - Cantidad por categoría
        - Cantidad por fuente
        - Cantidad por provincia y categoría
    """
    try:
        if df is None:
            raise ValueError("No existe DataFrame del total de la información")

        else:
            df['provincia_categoria'] = df['provincia'] + ' - ' + df['categoria']
            # Resumen por categoría

            total_resumen_categoria = df.pivot_table(index='categoria', values ='idprovincia', aggfunc='count')
            total_resumen_categoria = total_resumen_categoria.reset_index()
            total_resumen_categoria['tipo_agrupacion'] = 'Categoría'
            total_resumen_categoria.rename(columns={'categoria': 'descripcion', 'idprovincia': 'total'}, inplace=True)
            total_resumen_categoria

            # Resumen por fuente

            total_resumen_fuente = df.pivot_table(index='fuente', values ='idprovincia', aggfunc='count')
            total_resumen_fuente = total_resumen_fuente.reset_index()
            total_resumen_fuente['tipo_agrupacion'] = 'Fuente'
            total_resumen_fuente.rename(columns={'fuente': 'descripcion', 'idprovincia': 'total'}, inplace=True)
            total_resumen_fuente

            # Resumen por provincia y categoría

            total_resumen_prov_cat = df.pivot_table(index='provincia_categoria', values ='idprovincia', aggfunc='count')
            total_resumen_prov_cat = total_resumen_prov_cat.reset_index()
            total_resumen_prov_cat['tipo_agrupacion'] = 'Provincia y Categoría'
            total_resumen_prov_cat.rename(columns={'provincia_categoria': 'descripcion', 'idprovincia': 'total'}, inplace=True)
            total_resumen_prov_cat

            # Concatenación en una tabla

            total = pd.concat([total_resumen_fuente,total_resumen_categoria, total_resumen_prov_cat], axis = 0)
            total = total[['tipo_agrupacion', 'descripcion', 'total']]

    except ValueError:
        logger.error("No existe DataFrame del total de la información")
    except TypeError as e:
        logger.error("No existen datos o no coinciden nombres de columnas")
    else:
        logger.info('Tabla resumen del total de información generada correctamente')
        return total


def summary_tables_cinema():

    """
        Tabla resumen de los datos de salas de cine según:
            - Provincia
            - Cantidad de pantallas
            - Cantidad de butacas
            - Cantidad de espacios INCAA
    """
    
    try:
        df_cinema = pd.read_csv(path_file_cinema)
        df_cinema = fix_columns(df_cinema)
        df_cinema['espacio_incaa'] = df_cinema['espacio_incaa'].apply(lambda x: 1 if x == 'SI' or x == 'si' else 0)
        cinema_summary_table = df_cinema.pivot_table(index='provincia', values = ['pantallas', 'butacas', 'espacio_incaa'], aggfunc='sum')
        cinema_summary_table = cinema_summary_table.reset_index()

    except FileNotFoundError:
            logger.error(f'No se pudo leer el archivo en la ruta {path_file_cinema}')
            logger.error(f'No se generó tabla resumen de cines')
    except KeyError:
            logger.error('Verifique los nombres de columnas')
            logger.error(f'No se generó tabla resumen de cines')

    else:
        logger.info('Tabla resumen de cines se ha generado correctamente')
        return cinema_summary_table
    

if __name__ == '__main__':

    logger = main_logger(__file__)

    if (os.path.exists(path_file_cinema) == True) and (os.path.exists(path_file_museum) == True) and (os.path.exists(path_file_library) == True):
        df_total = total_data_processed()
        df_total.to_csv('temp_data/df_total_table.csv', index=False, encoding='utf-8')
    else:
        logger.error('Falta alguno de los tres archivos')

    if df_total is not None:
        df_total_summary_table = summary_tables_total(df_total)
        df_total_summary_table.to_csv('temp_data/df_total_summary_table.csv', index=False, encoding='utf-8')
    else:
        logger.error('No se ha ejecutado la tabla total')

    if os.path.exists(path_file_cinema) == True:
        df_cinema_summary_table = summary_tables_cinema()
        df_cinema_summary_table.to_csv('temp_data/df_cinema_summary_table.csv', index=False, encoding='utf-8')
    else:
        logger.error('No se encontró el archivo de cine')