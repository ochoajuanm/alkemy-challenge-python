import os
import pandas as pd
from get_data import year_month, day_month_year
from categories_url import categories_urls

path_file_cinema = f'categorias/salas-de-cine/{year_month}/salas-de-cine-{day_month_year}.csv'
# total_table, summary_table, cinema_summary_table = None, None, None

def replace_special_characters(list):

    """
        Función que recibe una lista y transforma los caracteres de sus ítems:
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

    """
        Función que estandariza los nombres de columnas para dataframe. Transforma a minúsculas, sin tildes y sin espacios
    """
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

    """
        Procesa los csv de cada categoría en uno solo y descarta columnas no utilizadas
    """

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

    try:
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
        
    except FileNotFoundError:
        print(f'No se pudo leer el archivo en la ruta {path_file}')
    else:
        print('Se procesó el archivo de todas las categorías en una tabla correctamente ')
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
        print("No existe DataFrame del total de la información")
    except TypeError as e:
        print("No existen datos o no coinciden nombres de columnas")
    else:
        print('Tabla resumen del total de información generada correctamente')
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
            print(f'No se pudo leer el archivo en la ruta {path_file_cinema}')
            print(f'No se generó tabla resumen de cines')
    except KeyError:
            print('Verifique los nombres de columnas')
            print(f'No se generó tabla resumen de cines')

    else:
        print('Tabla resumen de cines se ha generado correctamente')
        return cinema_summary_table
    

if __name__ == '__main__':

    df_total = total_data_processed()
    df_total.to_csv('temp_data/total_table.csv', index=False, encoding='utf-8')
    if df_total is not None:
        df_total_summary_table = summary_tables_total(df_total)
        df_total_summary_table.to_csv('temp_data/df_total_summary_table.csv', index=False, encoding='utf-8')
    if os.path.exists(path_file_cinema) == True:
        df_cinema_summary_table = summary_tables_cinema()
        df_cinema_summary_table.to_csv('temp_data/df_cinema_summary_table.csv', index=False, encoding='utf-8')