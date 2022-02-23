# Challenge Data Analytics - Python

¡Hola! Este es un proyecto desafío que consume datos desde 3 fuentes distintas para popular una base de datos SQL con información cultural sobre bibliotecas, museos y salas de cines argentinos.

> NOTA: Este procedimiento será detallado en un ambiente de Windows con WSL Ubuntu, pueden existir variaciones respecto a algunos comandos

Para ello, primero se debe descargar el repositorio y crear un ambiente virtual, por ejemplo con:

    python3 -m venv .venv

Luego, se debe activar el ambiente virtual e instalar los requerimientos con el comando:

    pip install -m requirements.txt

Se debe configurar el idioma español ya que, al utilizarse la librería datetime, cuando se generen carpetas y directorios se realizará en inglés por defecto, para ello se debe ejecutar en la consola:

    export LC_ALL="en_US.UTF-8"
    export LC_CTYPE="en_US.UTF-8"
    sudo dpkg-reconfigure locales

En el menú que aparecerá luego de esta ejecución, se debe elegir es_AR.UTF-8 
https://stackoverflow.com/questions/14547631/python-locale-error-unsupported-locale-setting

Se debe crear un archivo de nombre `.env` en la raíz del proyecto con la siguiente información:

    POSTGRES_HOST='tu_host'
    POSTGRES_USER='tu_usuario'
    POSTGRES_PASSWORD='tu_contraseña'
    POSTGRES_PORT='tu_puerto'
    POSTGRES_DB='tu_db'

En mi caso fueron:

    POSTGRES_HOST='winhost' (generalmente será localhost, para WSL tuve que reconfigurar el host, se explica [acá](https://stackoverflow.com/questions/56824788/how-to-connect-to-windows-postgres-database-from-wsl))
    POSTGRES_USER='postgres'
    POSTGRES_PASSWORD='******'
    POSTGRES_PORT='5432'
    POSTGRES_DB='cultura'

# Módulos

Dentro del proyecto podemos encontrar tres módulos diferenciados:

 - **get_data.py:** aquí es donde se produce la extracción de la información solicitada mediante la librería `requests` a las URLs solicitadas. Éstas están guardadas en un diccionario por llave-valor siendo la llave la categoría, y el valor el link del archivo.

 - **processing_data.py**: es el módulo que realiza las transformaciones correspondiente de los archivos csv descargados y mediante la librería `pandas` permite exportarlos a la carpeta `temp_data` para luego ser utilizados por el módulo de actualización de la base de datos
 
 - **update_db_data.py**: lee los archivos previamente procesados y guardados, y mediante una conexión a PostgreSQL (recordar crear antes el archivo `.env` para definir las variables de entorno, éstas serán utilizadas por la librería `decouple` para obtener la conexión al motor de la base de datos