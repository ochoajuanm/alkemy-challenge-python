from get_data import get_csv
from processing_data import total_data_processed, summary_tables_total, summary_tables_cinema
from update_db_data import move_df_db
from create_tables import create_tables

def run():

    
    get_csv()

    # Proceso de la información
    
    df_total = total_data_processed()
    df_total_summary_table = summary_tables_total(df_total)
    df_cinema_summary_table = summary_tables_cinema()
    print('Se han procesado los datos con éxito')

    # Creado de tablas si ya existen continúa el proceso

    try:
        create_tables()
    except:
        print("Una o más tablas ya existen")

    # Envío de datos a base de postgres

    move_df_db(df_total, df_total_summary_table, df_cinema_summary_table)    
    print('Se han enviado a la base de datos de PostgreSQL')

    return print('Se han ejecutado todos los procesos con éxito')


if __name__ == '__main__':
    run()