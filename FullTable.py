import os
import mysql.connector
from bs4 import BeautifulSoup

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1545",
    database="DCRB",
    autocommit=False  # all INSERT INTO as a single transaction
)
cursor = conn.cursor()

# Inizia la transazione
cursor.execute("START TRANSACTION")

directory = "C:/Users/paolo/OneDrive/Desktop/Università/"

def get_file_type(file_name):
    if '.' in file_name:
        return "file"
    else:
        return "dir"

def get_file_content(file_path):
    if file_path.endswith('.html'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                return soup.get_text()
        except Exception as e:
            print(f"Error: {file_path}: {e}")
            return None
    else:
        return None

def insert_into_mysql(full_path, file_name, file_type, content):
    query = "INSERT INTO FILESYST(FULL_PATH_NAME, FILE_NAME, FILE_TYPE, CONTENT) VALUES (%s, %s, %s, %s)"
    values = (full_path, file_name, file_type, content)
    cursor.execute(query, values)

try:
    for root, dirs, files in os.walk(directory):
        for directory in dirs:
            full_path = os.path.join(root, directory)
            file_name = os.path.basename(full_path)
            file_type = get_file_type(file_name)
            insert_into_mysql(full_path, file_name, file_type, None)

        for file in files:
            full_path = os.path.join(root, file)
            file_name = os.path.basename(full_path)
            file_type = get_file_type(file_name)
            content = get_file_content(full_path)
            insert_into_mysql(full_path, file_name, file_type, content if content else None)

    conn.commit()

except Exception as e:
    print(f"Error: {e}")
    conn.rollback()
    print("Transaction rolled back due to error.")

finally:
    cursor.close()
    conn.close()