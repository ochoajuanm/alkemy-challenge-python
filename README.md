# Challenge Data Analytics - Python

**Autor: Juan Ochoa**

¡Hola! Este es un proyecto desafío que consume datos desde 3 fuentes distintas para popular una base de datos SQL con información cultural sobre bibliotecas, museos y salas de cines argentinos.

> NOTA: Este procedimiento será detallado en un ambiente de Windows con WSL Ubuntu, pueden existir variaciones respecto a algunos comandos

Para ello, primero se debe descargar el repositorio y crear un ambiente virtual, por ejemplo con:

    python3 -m venv .venv

Luego, se debe activar el ambiente virtual:

    source .venv/bin/activate

E instalar los requerimientos con el comando:

    pip install -m requirements.txt

Se debe configurar el idioma español ya que, al utilizarse la librería datetime, cuando se generen carpetas y directorios se realizará en inglés por defecto, para ello se debe ejecutar en la consola:

    export LC_ALL="en_US.UTF-8"
    export LC_CTYPE="en_US.UTF-8"
    sudo dpkg-reconfigure locales

En el menú que aparecerá luego de esta ejecución, se debe elegir es_AR.UTF-8 
https://stackoverflow.com/questions/14547631/python-locale-error-unsupported-locale-setting

Se debe crear un archivo de nombre `.env` en la raíz del proyecto con la siguiente información:

    PG_HOST='tu_host'
    PG_USER='tu_usuario'
    PG_PASSWORD='tu_contraseña'
    PG_PORT='tu_puerto'
    PG_DB='tu_db'

En mi caso fueron:

    PG_HOST='winhost' 
    PG_USER='postgres'
    PG_PASSWORD='******'
    PG_PORT='5432'
    PG_DB='cultura'

El host generalmente será localhost, para WSL tuve que reconfigurar el host, se explica [acá](https://stackoverflow.com/questions/56824788/how-to-connect-to-windows-postgres-database-from-wsl)


# Módulos

Dentro del proyecto podemos encontrar tres módulos diferenciados:

 - **get_data.py:** aquí es donde se produce la extracción de la información solicitada mediante la librería `requests` a las URLs solicitadas. Éstas están guardadas en un diccionario por llave-valor siendo la llave la categoría, y el valor el link del archivo.

 - **process_data.py**: es el módulo que realiza las transformaciones correspondiente de los archivos csv descargados y mediante la librería `pandas` permite exportarlos a la carpeta `temp_data` para luego ser utilizados por el módulo de actualización de la base de datos
 
 - **update_db_data.py**: lee los archivos previamente procesados y guardados, y mediante una conexión a PostgreSQL (recordar crear antes el archivo `.env` para definir las variables de entorno, éstas serán utilizadas por la librería `decouple` para obtener la conexión al motor de la base de datos

Cabe destacar que, ejecutando el archivo **main.py**, éstos tres se ejecutarán secuencialmente en el orden descripto.

También existen otros dos módulos adicionales, uno para la conexión a la base de datos **db_connection.py** y otro para creación de tablas **create_tables.py**

Todos los módulos importan variables de configuración y funciones de corrección desde el archivo **utils.py**

Se adjunta un notebook definido como **data_analysis.ipynb** donde se fueron probando las transformaciones que se debían realizar en los datos.

# Carpetas
Tenemos cuatro carpetas en el proyecto:

 - **categorias:** aquí se guardarán todas las extracciones de información en "crudo" de los datos del gobierno solicitados en el challenge.
 - **logs:** se guardarán los archivos log referidos por su nombre según el módulo ejecutado. Ya que funcionan por jerarquía, dentro del mismo se mostrarán como root aquellas ejecuciones que corresponden al módulo padre y con su nombre a los módulos hijos.
 - **temp_data:** servirá para almacenar el output de la ejecución del módulo **process_data** en archivos csv. Si se ejecuta el **main** no se guardará porque las variables estarán en memoria.
 - **sql_scripts:** acá figuran los scripts de creación de las tablas en PostgreSQL que serán llamados al ser ejecutado el módulo **create_tables** (y este llamará a **db_connection**)