
import sqlite3
import sys
import logging

logger = logging.getLogger(__name__)

DB_NAME = 'library_management.db'

def get_db_connection(parent_widget=None):
    try:
        logger.debug(f"Connecting to SQLite database: {DB_NAME}")
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        logger.error(f"Connection failed: {e}")
        return None

def setup_database_schema(parent_widget=None):
    logger.info("Setting up database schema...")
    db = get_db_connection(parent_widget)
    if not db:
        logger.error("Could not get DB connection for schema setup.")
        return False
        
    try:
        cursor = db.cursor()
        
        # SQLite uses INTEGER PRIMARY KEY AUTOINCREMENT
        tables = [
             """CREATE TABLE IF NOT EXISTS author (
                idauthor INTEGER PRIMARY KEY AUTOINCREMENT,
                author_name TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS category (
                idcategory INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS publisher (
                idpublisher INTEGER PRIMARY KEY AUTOINCREMENT,
                publisher_name TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_name TEXT,
                book_description TEXT,
                book_code TEXT,
                book_category TEXT,
                book_author TEXT,
                book_publisher TEXT,
                book_price INTEGER
            )""",
            """CREATE TABLE IF NOT EXISTS client (
                idclient INTEGER PRIMARY KEY AUTOINCREMENT,
                clientName TEXT,
                clientEmail TEXT,
                clientNid TEXT
            )""",
             """CREATE TABLE IF NOT EXISTS dayoperations (
                iddayoperations INTEGER PRIMARY KEY AUTOINCREMENT,
                bookname TEXT,
                type TEXT,
                days INTEGER,
                fromDate TEXT,
                toDate TEXT,
                clientName TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS users (
                id_users INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                useremail TEXT,
                userspassword TEXT
            )"""
        ]
        
        for table_sql in tables:
            cursor.execute(table_sql)
            
        # Check and create default user
        cursor.execute("SELECT * FROM users")
        if not cursor.fetchall():
            logger.info("Creating default user...")
            cursor.execute("INSERT INTO users (username, useremail, userspassword) VALUES ('admin', 'admin@example.com', 'admin')")
            db.commit()
            
        db.close()
        logger.info("Database schema setup successful.")
        return True
    except sqlite3.Error as e:
        logger.error(f"Database schema setup error: {e}")
        print(f"Error setting up database: {e}")
        return False
