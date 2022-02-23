from sqlalchemy.sql.expression import text
from db_connection import get_engine_from_settings
from sqlalchemy.exc import SQLAlchemyError
import os

def create_tables():

    engine = get_engine_from_settings()
    for script in os.listdir('./sql_scripts'):
            try:
                with engine.connect() as con:
                    file = open('sql_scripts/' + script)
                    query = text(file.read())
                    con.execute(query, echo=False)
            except Exception as e:
                print(f'No se puede ejecutar {script}, la tabla ya existe')
    con.close()

if __name__ == '__main__':
    create_tables()