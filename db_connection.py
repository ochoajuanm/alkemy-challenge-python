from decouple import config as cfg
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from sqlalchemy.sql import text
from sqlalchemy_utils import database_exists, create_database
from utils import main_logger

logger = logging.getLogger("").getChild(__name__)


def get_engine(user, passwd, host, port, db):

    """Recibe variables de entorno de PG para crear el motor.
    Crea la BD en caso de que no exista.
    """

    url = f'postgresql://{user}:{passwd}@{host}:{port}/{db}'
    try:
        if not database_exists(url):
            create_database(url)
            logger.info(f'Se creó la base de datos {db}')
        else:
            logger.info(f'La base de datos {db} ya existe')
            
        engine = create_engine(url, pool_size=50, echo=False)
        return engine
    except exc.OperationalError:
        logger.error('Las variables de entorno configuradas son incorrectas')

def get_engine_from_settings():
    
    return get_engine(cfg('PG_USER'), 
                        cfg('PG_PASSWORD'), 
                        cfg('PG_HOST'), 
                        cfg('PG_PORT'), 
                        cfg('PG_DB'))


# def get_session():

#     """Genera una sesión a partir del motor obtenido"""

#     engine = get_engine_from_settings()
#     session = sessionmaker(bind=engine)()
#     return session


if __name__ == '__main__':
    # session = get_session()
    
    logger = main_logger(__file__)
    engine = get_engine_from_settings()