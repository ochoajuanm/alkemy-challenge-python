from processing_data import total_data_processed, summary_tables_total, summary_tables_cinema, path_file_cinema
from db_connection import get_engine_from_settings
import pandas as pd
import os


def move_df_db(total_table, summary_table, cinema_summary_table, engine=get_engine_from_settings()):

    """
        Envía los DataFrame generados a la base de datos de PostgreSQL
    """

    try:
        total_table.to_sql('total_data', con=engine, if_exists='replace')
        summary_table.to_sql('summary_table_total_data', con=engine, if_exists='replace')
        cinema_summary_table.to_sql('summary_table_cinema', con=engine, if_exists='replace')
    except:
        print('Falló el envío de una tabla')
    else:
        print("Se ejecutaron los envíos de las tablas a PostgreSQL")


if __name__ == '__main__':
    # df_total = total_data_processed()
    # if df_total is not None:
    #     df_total_summary_table = summary_tables_total(df_total)
    # if os.path.exists(path_file_cinema) == True:
    #     df_cinema_summary_table = summary_tables_cinema()
    
    df_total = pd.read_csv('temp_data/df_total_table.csv', index=False, encoding='utf-8')
    df_total_summary_table = pd.read_csv('temp_data/df_total_summary_table.csv', index=False, encoding='utf-8')
    df_cinema_summary_table = pd.read_csv('temp_data/df_cinema_summary_table.csv', index=False, encoding='utf-8')
    move_df_db(df_total, df_total_summary_table, df_cinema_summary_table)
