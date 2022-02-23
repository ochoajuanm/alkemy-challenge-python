from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql import text

def get_engine(user, passwd, host, port, db):

    """
        Recibe variables de entorno de postgres para crear el motor. Crea la BD en caso de que no exista
    """

    url = f'postgresql://{user}:{passwd}@{host}:{port}/{db}'
    if not database_exists(url):
        create_database(url)

    engine = create_engine(url, pool_size=50, echo=False)
    return engine

def get_engine_from_settings():

    """
        Configuración de la conexión a la BD con variables de entorno
    """

    return get_engine(config('POSTGRES_USER'),
                    config('POSTGRES_PASSWORD'),
                    config('POSTGRES_HOST'),
                    config('POSTGRES_PORT'),
                    config('POSTGRES_DB'))

def get_session():

    """
        Genera una sesión a partir del motor obtenido
    """
    engine = get_engine_from_settings()
    session = sessionmaker(bind=engine)()
    return session

if __name__ == '__main__':
    # session = get_session()
    engine = get_engine_from_settings()