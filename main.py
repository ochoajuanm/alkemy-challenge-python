from get_data import get_csv
from processing_data import total_data_processed, summary_tables_total, summary_tables_cinema, move_csv_db
from create_tables import create_tables


def run():

    try:
        get_csv()
        print('Se ha ejecutado la extracción de la información con éxito')

    except ValueError as e:
        print('Ha ocurrido un error con la información')

    # Proceso de la información
    
    df_total = total_data_processed()
    total_summary_table = summary_tables_total(df_total)
    cinema_summary_table = summary_tables_cinema()
    print('\nSe han procesado los datos con éxito')

    # Las dejo en csv

    # df_total.to_csv('data/total_data.csv', index=False, encoding='utf-8')
    # df_total.to_excel('data/total_data2.xlsx', index=False, encoding='utf-8')
    # total_summary_table.to_csv('data/summary_table_total.csv', index=False, encoding='utf-8')
    # cinema_summary_table.to_csv('data/summary_table_cinema.csv', index=False, encoding='utf-8')
    # print('\nSe han guardado los datos en archivos CSV')

    try:
        create_tables()
    except:
        print("Una o más tablas ya existen")

    # Envío de datos a base de postgres

    move_csv_db(df_total, total_summary_table, cinema_summary_table)    
    print('\nSe han enviado a la base de datos de PostgreSQL')

    return print('\n\nSe han ejecutado todos los procesos con éxito')


if __name__ == '__main__':
    run()