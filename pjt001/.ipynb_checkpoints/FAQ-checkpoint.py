import pymysql

def get_db_connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        database='mydatabase',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

def get_categories(table_name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT DISTINCT category FROM {table_name}"
            cursor.execute(sql)
            categories = [row['category'] for row in cursor.fetchall()]
        return categories
    finally:
        connection.close()

def get_faq_data(table_name, category=None, search_query=None):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            if category and search_query:
                sql = f"SELECT * FROM {table_name} WHERE category=%s AND (question LIKE %s OR answer LIKE %s)"
                like_query = f"%{search_query}%"
                cursor.execute(sql, (category, like_query, like_query))
            elif category:
                sql = f"SELECT * FROM {table_name} WHERE category=%s"
                cursor.execute(sql, (category,))
            elif search_query:
                sql = f"SELECT * FROM {table_name} WHERE question LIKE %s OR answer LIKE %s"
                like_query = f"%{search_query}%"
                cursor.execute(sql, (like_query, like_query))
            else:
                sql = f"SELECT * FROM {table_name}"
                cursor.execute(sql)
            
            result = cursor.fetchall()
        return result
    finally:
        connection.close()

def create_data(table_name, category, question, answer):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f'INSERT INTO {table_name} (category, question, answer) VALUES (%s, %s, %s)'
    cursor.execute(query, (category, question, answer))
    conn.commit()
    conn.close()
