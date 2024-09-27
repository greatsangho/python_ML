import pymysql
import pandas as pd

# 데이터베이스 연결 설정
def get_database_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="mydatabase",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# CREATE: 새로운 레코드 삽입
def insert_record(name, age, city):
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "INSERT INTO news(content) VALUES (%s)"
    cursor.execute(query, (connection)
    connection.commit()
    connection.close()

# READ: 테이블에서 모든 레코드 가져오기
def fetch_all_records():
    connection = get_database_connection()
    query = "SELECT * FROM news"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

# # UPDATE: 특정 레코드 업데이트
# def update_record(record_id, name, age, city):
#     connection = get_database_connection()
#     cursor = connection.cursor()
#     query = "UPDATE your_table_name SET name = %s, age = %s, city = %s WHERE id = %s"
#     cursor.execute(query, (name, age, city, record_id))
#     connection.commit()
#     connection.close()

# # DELETE: 특정 레코드 삭제
# def delete_record(record_id):
#     connection = get_database_connection()
#     cursor = connection.cursor()
#     query = "DELETE FROM your_table_name WHERE id = %s"
#     cursor.execute(query, (record_id,))
#     connection.commit()
#     connection.close()
