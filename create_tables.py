# from sqlalchemy import create_engine
from venv import create
from sqlalchemy.sql.expression import text
from db_connection import get_engine_from_settings

def create_tables():

    engine = get_engine_from_settings()

    with engine.connect() as con:
        file = open("create_tables.sql")
        query = text(file.read())
        con.execute(query, echo=False)
        con.close()

if __name__ == '__main__':
    create_tables()