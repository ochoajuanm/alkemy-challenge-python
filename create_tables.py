from db_connection import get_engine_from_settings
import logging
import os
from sqlalchemy import exc
from sqlalchemy.sql.expression import text
from utils import main_logger

logger = logging.getLogger("").getChild(__name__)


def create_tables():

    """Crea las tablas en la base de PostgreSQL en caso de que no existan"""

    engine = get_engine_from_settings()
    if engine is not None:
        logger.info('Intentando crear tablas...')
        with engine.connect() as con:
            for script in os.listdir('./sql_scripts'):
                file = open('sql_scripts/' + script)
                query = text(file.read())
                try:
                    con.execute(query, echo=False)
                    logger.info(f'Se creó la tabla con el script {script}')
                except exc.ProgrammingError:
                    logger.info(f'No se ejecutó {script}, la tabla ya existe')
        con.close()
        logger.debug('Se ha cerrado la conexión a la base de datos')
    else:
        logger.debug('No hay engine')


if __name__ == '__main__':
    logger = main_logger(__file__)
    create_tables()