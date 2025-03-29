import mysql.connector
from config import dbconfig_edit, dbconfig_read


def get_connection(db_name=None):
    conn_params = dbconfig_edit.copy()
    if db_name:
        conn_params['database'] = db_name
    return mysql.connector.connect(**conn_params)

def get_connection_read(db_name=None):
    conn_params = dbconfig_read.copy()
    if db_name:
        conn_params['database'] = db_name
    return mysql.connector.connect(**conn_params)

def database_is_exists(db_name: str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]

        cursor.close()
        conn.close()

        return db_name in databases
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False


def create_struct_database():
    try:
        conn = get_connection()
        # conn = mysql.connector.connect(**dbconfig_edit)
        cursor = conn.cursor()

        # Создание базы данных sumarokovav_300924
        cursor.execute("DROP DATABASE IF EXISTS sumarokovav_300924")
        cursor.execute("CREATE DATABASE IF NOT EXISTS sumarokovav_300924")
        print("База данных sumarokovav_300924 успешно создана")

        cursor.execute("USE sumarokovav_300924")

        # Создание таблицы Users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_name VARCHAR(50) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Время создания строки',  
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Время обновления строки'
            )
        """)
        print("Таблица Users успешно создана")

        # Создание таблицы Statistics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Statistics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                query VARCHAR(100) NOT NULL,
                user_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Время создания строки'
            )
        """)
        print("Таблица Statistics успешно создана")

        # Создание таблицы Responses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Responses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                film_id INT NOT NULL,
                query_id INT NOT NULL,      
                FOREIGN KEY (query_id) REFERENCES Statistics(id) ON DELETE CASCADE
            )
        """)
        print("Таблица Responses успешно создана")

    except mysql.connector.Error as err:
        print(f"Ошибка MySQL: {err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с MySQL закрыто")


def insert_sample_data():
    try:
        conn = get_connection()
        # conn = mysql.connector.connect(**dbconfig_edit)
        cursor = conn.cursor()
        cursor.execute("USE sumarokovav_300924")

        users = [
            ("asmith02", "Alice", "Smith"),
            ("bking03", "Bob", "King"),
            ("cwhite04", "Charlie", "White"),
            ("dblack05", "David", "Black"),
            ("elane06", "Emma", "Lane"),
            ("fgray07", "Frank", "Gray"),
            ("gstone08", "Grace", "Stone"),
            ("hyoung09", "Henry", "Young"),
            ("imorris10", "Isla", "Morris"),
            ("jreed11", "Jack", "Reed"),
            ("khall12", "Katherine", "Hall"),
            ("lgreen13", "Liam", "Green"),
            ("mwood14", "Mia", "Wood"),
            ("ncooper15", "Noah", "Cooper"),
            ("oallen16", "Olivia", "Allen"),
            ("pparker17", "Peter", "Parker"),
            ("qevans18", "Quinn", "Evans"),
            ("rthomas19", "Ryan", "Thomas"),
            ("sroberts20", "Sophia", "Roberts"),
            ("tjames21", "Tyler", "James"),
            ("uvance22", "Uma", "Vance"),
            ("wscott23", "William", "Scott")
        ]
        cursor.executemany(
            "INSERT INTO Users (user_name, first_name, last_name) VALUES (%s, %s, %s)", users)

        conn.commit()
        print("Данные успешно добавлены в таблицу")

    except mysql.connector.Error as err:
        print(f"Ошибка MySQL: {err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с MySQL закрыто")


if __name__ == "__main__":
    create_struct_database()
    insert_sample_data()
