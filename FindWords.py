import mysql.connector

def count_occurrences(substring):
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1545",
        database="DCRB"
    )
    cursor = db_connection.cursor()

    query = "SELECT FULL_PATH_NAME, FILE_TYPE, CONTENT FROM FILESYST WHERE FILE_NAME LIKE %s OR CONTENT LIKE %s"
    cursor.execute(query, ("%" + substring + "%", "%" + substring + "%"))

    occurrences_count = 0

    for (file_name, file_type, content) in cursor:
        if content is None:
            content = ""

        occurrences_in_file_name = file_name.count(substring)
        occurrences_in_content = content.count(substring)

        occurrences_count += occurrences_in_file_name + occurrences_in_content

        found_in_content = False

        if occurrences_in_file_name > 0:
            print(
                f"Found {occurrences_in_file_name} occurrencies of '{substring}' in FULL_PATH_NAME '{file_name}' with type '{file_type}'")

        if occurrences_in_content > 0:
            print(
                f"Found {occurrences_in_content} occurrencies of '{substring}' in CONTENT of '{file_name}' with type '{file_type}'")
            found_in_content = True

        print("")
    print(f"\nTotal of '{substring}': {occurrences_count}")

    cursor.close()
    db_connection.close()

substring = "Food"
count_occurrences(substring)