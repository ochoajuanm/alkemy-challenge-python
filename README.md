# Challenge Data Analytics - Python

¡Hola! Este es un proyecto desafío que consume datos desde 3 fuentes distintas para popular una base de datos SQL con información cultural sobre bibliotecas, museos y salas de cines argentinos.

NOTA: Este procedimiento será detallado en un ambiente de Windows con WSL Ubuntu, pueden existir variaciones respecto a algunos comandos

Para ello, primero se debe descargar el repositorio y crear un ambiente virtual, por ejemplo con 

> python3 -m venv .venv

Luego, se deben instalar los requerimientos con el comando:

> pip install -m requirements.txt

Se debe configurar el idioma español ya que, al utilizarse la librería datetime, cuando se generen carpetas y directorios se realizará en inglés por defecto, para ello se debe ejecutar en la consola:

> export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure locales

En el menú que figura luego de esta ejecución, se debe elegir es_AR.UTF-8 
https://stackoverflow.com/questions/14547631/python-locale-error-unsupported-locale-setting


