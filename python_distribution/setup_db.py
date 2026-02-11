
import MySQLdb as msd
import sys

# Database Configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'riju000346>R#' # potential password from original code

def setup_database():
    try:
        # Connect to MySQL Server
        print("Connecting to MySQL server...")
        db = msd.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
        cursor = db.cursor()
        
        # Create Database
        print("Creating database 'library_management' if it doesn't exist...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS library_management")
        cursor.execute("USE library_management")
        
        # Create Tables
        print("Creating tables...")
        
        # author table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS author (
                idauthor int(11) AUTO_INCREMENT PRIMARY KEY,
                author_name varchar(45)
            )
        """)
        
        # category table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                idcategory int(11) AUTO_INCREMENT PRIMARY KEY,
                category_name varchar(45)
            )
        """)
        
        # publisher table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS publisher (
                idpublisher int(11) AUTO_INCREMENT PRIMARY KEY,
                publisher_name varchar(45)
            )
        """)
        
        # book table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS book (
                id int(11) AUTO_INCREMENT PRIMARY KEY,
                book_name varchar(45),
                book_description varchar(255),
                book_code varchar(45),
                book_category varchar(45),
                book_author varchar(45),
                book_publisher varchar(45),
                book_price int(11)
            )
        """)
        
        # client table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS client (
                idclient int(11) AUTO_INCREMENT PRIMARY KEY,
                clientName varchar(45),
                clientEmail varchar(45),
                clientNid varchar(45)
            )
        """)
        
        # dayoperations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dayoperations (
                iddayoperations int(11) AUTO_INCREMENT PRIMARY KEY,
                bookname varchar(45),
                type varchar(30),
                days int(11),
                fromDate datetime,
                toDate datetime,
                clientName varchar(45)
            )
        """)
        
        # users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id_users int(11) AUTO_INCREMENT PRIMARY KEY,
                username varchar(45),
                useremail varchar(45),
                userspassword varchar(45)
            )
        """)
        
        # Insert Default User
        print("Checking for existing users...")
        cursor.execute("SELECT * FROM users")
        if not cursor.fetchall():
            print("Creating default user (admin/admin)...")
            cursor.execute("INSERT INTO users (username, useremail, userspassword) VALUES ('admin', 'admin@example.com', 'admin')")
            db.commit()
            print("Default user created: Username='admin', Password='admin'")
        else:
            print("Users already exist. Skipping default user creation.")
        
        print("Database setup completed successfully.")
        db.close()
        
    except msd.Error as e:
        print(f"MySQL Error: {e}")
        print("Please ensure MySQL is running and credentials are correct.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_database()
