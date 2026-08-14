import os
import mysql.connector
from mysql.connector import Error


def connect_database():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            port=int(os.environ.get("DB_PORT", 24510)),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME", "defaultdb"),
            ssl_disabled=False,       # Aiven requires SSL
            ssl_verify_identity=False
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        raise
