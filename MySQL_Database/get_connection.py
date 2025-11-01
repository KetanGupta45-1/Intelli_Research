from MySQL_Database.db_config import db_config
import mysql
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print('\n Connection Established')
            return connection
    except Error as e:
        print(f"❌ Database connection error: {e}")
        return None