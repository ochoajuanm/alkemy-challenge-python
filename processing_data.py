import pandas as pd
import numpy as np
from get_data import categories_urls, year_month, day_month_year
from db_connection import get_engine_from_settings

def replace_special_characters(list):

    dict = {'á': 'a', 'é':'e', 'í': 'i', 'ó': 'o', 'ú': 'u', ' ': '_', 'ñ': 'ni'}

    fixed_list = []
    for item in list:
        transTable = item.maketrans(dict)
        fixed_item = item.translate(transTable)
        fixed_list.append(fixed_item)
    

    return fixed_list


def fix_columns(df):
    columns_lower = [i.lower() for i in df.columns]
    columns_lower = replace_special_characters(columns_lower)
    dict_columns = dict(zip(df.columns, columns_lower))
    df.rename(columns=dict_columns, inplace=True)
    try:
        df.rename(columns={'domicilio': 'direccion'}, inplace=True)
    except KeyError:
        pass
        
    return df


def total_data_processed():

    reduced_columns = ['cod_loc',
                        'idprovincia',
                        'iddepartamento',
                        'categoria',
                        'provincia',
                        'localidad',
                        'nombre',
                        'direccion',
                        # 'cp',
                        'telefono',
                        'mail',
                        'fuente']

    df_total = pd.DataFrame(columns=reduced_columns)

    for category, url in categories_urls.items():
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

    return df_total


def summary_tables_total(df):

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

    return total


def summary_tables_cinema():
    df_cinema = pd.read_csv(f'categorias/salas-de-cine/{year_month}/salas-de-cine-{day_month_year}.csv')
    df_cinema = fix_columns(df_cinema)
    df_cinema['espacio_incaa'] = df_cinema['espacio_incaa'].apply(lambda x: 1 if x == 'SI' or x == 'si' else 0)
    cinema_summary_table = df_cinema.pivot_table(index='provincia', values = ['pantallas', 'butacas', 'espacio_incaa'], aggfunc='sum')
    cinema_summary_table = cinema_summary_table.reset_index()

    return cinema_summary_table

def move_csv_db(total_table, summary_table, cinema_summary_table, engine=get_engine_from_settings()):

    total_table.to_sql('total_data', con=engine, if_exists='replace')
    summary_table.to_sql('summary_table_total_data', con=engine, if_exists='replace')
    cinema_summary_table.to_sql('summary_table_cinema', con=engine, if_exists='replace')


if __name__ == '__main__':

    # Proceso de la información

    df_total = total_data_processed()
    total_summary_table = summary_tables_total(df_total)
    cinema_summary_table = summary_tables_cinema()
