from datetime import datetime
from db_connection import get_engine_from_settings
import pandas as pd
import os
import logging
from utils import main_logger, dict_columns_types, dict_columns_types_summary_total, dict_columns_types_summary_cinema, path_temp_total_table, path_temp_total_summary_table, path_temp_cinema_summary_table


logger = logging.getLogger("").getChild(__name__)


def move_df_db(total_table, summary_table, cinema_summary_table, engine):

    """Envía los DataFrame generados a la base de datos de PostgreSQL."""
    
    total_table['creado_el'] = datetime.now()
    summary_table['creado_el'] = datetime.now()
    cinema_summary_table['creado_el'] = datetime.now()

    try:
        total_table.to_sql('total_data', con=engine, if_exists='replace', dtype=dict_columns_types, index=False)
        logger.debug('Tabla total_data enviada correctamente')
        summary_table.to_sql('summary_table_total_data', con=engine, if_exists='replace', dtype=dict_columns_types_summary_total, index=False)
        logger.debug('Tabla total_data enviada correctamente')
        cinema_summary_table.to_sql('summary_table_cinema', con=engine, if_exists='replace',  dtype=dict_columns_types_summary_cinema, index=False)
        logger.debug('Tabla total_data enviada correctamente')
    except Exception as e:
        logger.error('Falló el envío de una o más tablas')
        print(e)
    else:
        logger.info("Se ejecutaron los envíos de las tablas a PostgreSQL")


if __name__ == '__main__':

    logger = main_logger(__file__)
    
    if os.path.exists(path_temp_total_table):
        df_total = pd.read_csv(path_temp_total_table, encoding='utf-8')
    else:
        logger.error(f'No se encontró el archivo {path_temp_total_table}')

    if os.path.exists(path_temp_total_summary_table):
        df_total_summary_table = pd.read_csv(path_temp_total_summary_table, encoding='utf-8')
    else:
        logger.error(f'No se encontró el archivo {path_temp_total_summary_table}')

    if os.path.exists(path_temp_cinema_summary_table):
        df_cinema_summary_table = pd.read_csv(path_temp_cinema_summary_table, encoding='utf-8')
    else:
        logger.error(f'No se encontró el archivo {path_temp_cinema_summary_table}')
    
    engine = get_engine_from_settings()

    try:
        move_df_db(df_total, df_total_summary_table, df_cinema_summary_table, engine)
    except NameError:
        logger.error('No se encontraron todas las tablas para enviarlas a la base de PostgreSQL')