from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
# from local_settings import postgresql as settings
from sqlalchemy.sql import text

def get_engine(user, passwd, host, port, db):
    url = f'postgresql://{user}:{passwd}@{host}:{port}/{db}'
    if not database_exists(url):
        create_database(url)

    engine = create_engine(url, pool_size=50, echo=False)
    return engine

def get_engine_from_settings():
    # keys = ['POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_DB']
    
    # if not all(key in keys for key in config.keys()):
    #     raise Exception('Bad config file')

    return get_engine(config('POSTGRES_USER'),
                    config('POSTGRES_PASSWORD'),
                    config('POSTGRES_HOST'),
                    config('POSTGRES_PORT'),
                    config('POSTGRES_DB'))

def get_session():
    engine = get_engine_from_settings()
    session = sessionmaker(bind=engine)()
    return session

if __name__ == '__main__':
    # session = get_session()
    engine = get_engine_from_settings()