from create_tables import create_tables
from db_connection import get_engine_from_settings
from get_data import get_csv
import logging
from process_data import total_data_processed, summary_tables_total, summary_tables_cinema
from update_db_data import move_df_db
from utils import main_logger

def run():

    try:

        # Extracción de la información
        get_csv()

        # Proceso de la información
        df_total = total_data_processed()
        df_total_summary_table = summary_tables_total(df_total)
        df_cinema_summary_table = summary_tables_cinema()
        logging.info('Se han procesado los datos con éxito')

        # Creado de tablas si ya existen continúa el proceso
        try:
            create_tables()
        except Exception as e:
            logging.warning("Una o más tablas ya existen")

        # Envío de datos a base de postgres
        move_df_db(df_total, df_total_summary_table, df_cinema_summary_table, get_engine_from_settings())

    except Exception as e:
        logging.error(type(e))
    else:
        logging.info('Se han ejecutado todos los procesos con éxito')


if __name__ == '__main__':
    main_logger(__file__)
    run()