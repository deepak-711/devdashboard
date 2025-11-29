import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'deepak711',
    'password': 'deepak711',
    'database': 'blueoptimadashboard'
}

def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print('Connected to MySQL database')
            return connection
    except Error as e:
        print(f'Error: {e}')
        return None

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print('MySQL connection closed')

if __name__ == "__main__":
    conn = get_connection()
    if conn:
        # Example query
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        for table in cursor.fetchall():
            print(table)
        close_connection(conn)
