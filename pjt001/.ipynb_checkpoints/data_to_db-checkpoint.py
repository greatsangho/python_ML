import pymysql
from sqlalchemy import create_engine


def create_database(database_name, password, username = 'root', host = 'localhost'):

    connection = pymysql.connect(
    host = host,
    user = username, 
    password = password)
    
    with connection.cursor() as cursor:
        cursor.execute(f"create database {database_name}")
    connection.commit()
    connection.close()

def get_connection(database_name, password, username = 'root', host = 'localhost'):

    conn = pymysql.connect(
        host = host,
        user = username,
        password = password,
        database = database_name,
        charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor
    )
    return conn
    
def Insert_data(file, table_name:str, PK:str, database_name, password, username = 'root', host = 'localhost'):

    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database_name}')
    file.to_sql(f'{table_name}', con=engine, if_exists='replace', index=False)
    engine.dispose()

    connection = get_connection(database_name, password)
    if PK != '':
        with connection.cursor() as cursor:
            cursor.execute(f"ALTER TABLE {table_name} ADD PRIMARY KEY ({PK});")
        connection.commit()
        connection.close()
