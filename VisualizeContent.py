import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1545",
    database="DCRB"
)
cursor = conn.cursor()

try:
    query = "SELECT CONTENT FROM FILESYST WHERE FILE_ID = %s"
    file_id = 38
    cursor.execute(query, (file_id,))

    result = cursor.fetchone()

    if result:
        content = result[0]
        print("File content:")
        print(content)
    else:
        print("No result found.")
except Exception as e:
    print(f"Error: {e}")

cursor.close()
conn.close()