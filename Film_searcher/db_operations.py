import mysql.connector
from db_setup import get_connection


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


def fetch_table_rows(conn, table_name: str) -> list[tuple[int, set[str]]]:
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT film_id, title, description, special_features FROM {table_name}")
        results = cursor.fetchall()

        documents = []
        for row in results:
            key = row[0]
            words = set()

            for val in row[1:]:
                if isinstance(val, set):
                    words.update(" ".join(val).split())
                elif isinstance(val, str):
                    words.update(val.split())

            documents.append((key, words))

        return documents
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()


def find_films_by_year(conn, table_name: str, year: int):
    try:
        cursor = conn.cursor()
        query = f"SELECT film_id FROM {table_name} WHERE release_year = %s"

        cursor.execute(query, (year,))

        results = cursor.fetchall()
        return results if results else []

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()


def get_all_users_statistics() -> str:
    try:

        conn = get_connection(db_name='sumarokovav_300924')
        cursor = conn.cursor()

        query = """
        SELECT u.user_name, COUNT(s.query) AS total_queries
        FROM Users u
        LEFT JOIN Statistics s ON u.id = s.user_id
        GROUP BY u.user_name
        ORDER BY total_queries DESC;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            return "Нет данных о поисковых запросах."

        stats = "Статистика по всем пользователям:\n"
        stats += "\n".join([f"{row[0]}: {row[1]} запросов" for row in results])

        return stats

    except mysql.connector.Error as err:
        return f"Ошибка при получении статистики: {err}"

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def get_user_statistics(username: str) -> str:
    try:
        conn = get_connection(db_name='sumarokovav_300924')
        cursor = conn.cursor()

        # Получаем ID пользователя
        cursor.execute(
            "SELECT id FROM Users WHERE user_name = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return f"Пользователь {username} не найден."

        user_id = user[0]

        # Получаем количество его запросов
        cursor.execute(
            "SELECT COUNT(*) FROM Statistics WHERE user_id = %s", (user_id,))
        total_queries = cursor.fetchone()[0]

        # Получаем запросы пользователя с датами
        cursor.execute(
            "SELECT query, created_at FROM Statistics WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,)
        )
        recent_queries = cursor.fetchall()

        # Формируем строку вывода
        stats = f"Статистика для {username}:\n"
        stats += f"Всего запросов: {total_queries}\n"
        stats += "Все запросы:\n"

        if recent_queries:
            stats += "\n".join(f"{query} | {created_at} " for query,
                               created_at in recent_queries)
        else:
            stats += "Нет запросов."

        return stats

    except mysql.connector.Error as err:
        return f"Ошибка при получении статистики: {err}"

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def change_user_information(username: str, field: str, new_value: str) -> str:
    try:
        conn = get_connection(db_name='sumarokovav_300924')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM Users WHERE user_name = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return f"Ошибка: Пользователь {username} не найден."

        user_id = user[0]

        cursor.execute("SHOW COLUMNS FROM Users;")
        valid_fields = {row[0] for row in cursor.fetchall()}
        if field not in valid_fields:
            return f"Ошибка: Поля '{field}' не существует в таблице Users."

        query = f"UPDATE Users SET {field} = %s WHERE id = %s"
        cursor.execute(query, (new_value, user_id))
        conn.commit()

        return "Данные пользователя успешно обновлены!"

    except mysql.connector.Error as err:
        return f"Ошибка при обновлении данных: {err}"

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def user_exists_in_database(username: str) -> bool:
    conn = get_connection(db_name='sumarokovav_300924')
    cursor = conn.cursor()

    query = "SELECT id FROM Users WHERE user_name = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result is not None


def fetch_user_info(username: str) -> dict[str, str]:
    conn = get_connection(db_name='sumarokovav_300924')
    cursor = conn.cursor()

    query = "SELECT first_name, last_name FROM Users WHERE user_name = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return {"first_name": result[0], "last_name": result[1]}
    else:
        raise ValueError("Пользователь не найден.")


def add_user_to_database(username: str, first_name: str, last_name: str) -> None:
    conn = get_connection(db_name='sumarokovav_300924')
    cursor = conn.cursor()

    query = "INSERT INTO Users (user_name, first_name, last_name) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, first_name, last_name))

    conn.commit()

    cursor.close()
    conn.close()

    print(
        f"Пользователь {first_name} {last_name} успешно добавлен в базу данных.")


def get_user_id(username: str) -> int | None:
    # Получает ID пользователя по username"""
    conn = get_connection(db_name='sumarokovav_300924')
    if not conn:
        print("Ошибка подключения к БД.")
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM Users WHERE user_name = %s", (username,))
        result = cursor.fetchone()
        return result[0] if result else None

    except mysql.connector.Error as err:
        print(f"Ошибка при поиске user_id: {err}")
        return None

    finally:
        cursor.close()
        conn.close()


def find_films_by_year(conn, table_name: str, year: int) -> list[tuple[int]]:
    try:
        cursor = conn.cursor()
        query = f"SELECT film_id FROM {table_name} WHERE release_year = %s"
        # Передаем год безопасно (SQL-инъекции исключены)
        cursor.execute(query, (year,))

        results = cursor.fetchall()  # Получаем список найденных фильмов
        return results if results else []

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()


def save_query_results(user_id: int, query: str, film_ids: list[int]):
    """Сохраняет запрос и найденные фильмы в БД"""
    conn = get_connection(db_name='sumarokovav_300924')
    if not conn:
        print("Ошибка подключения к БД.")
        return

    try:
        cursor = conn.cursor()
        # 🔹 Сохраняем запрос в Statistics
        cursor.execute(
            "INSERT INTO Statistics (query, user_id) VALUES (%s, %s)", (query, user_id))
        query_id = cursor.lastrowid  # Получаем ID вставленного запроса
        if not query_id:
            print("Ошибка: query_id не был создан.")
            return
        # 🔹 Сохраняем фильмы в Responses
        if film_ids:
            cursor.executemany("INSERT INTO Responses (film_id, query_id) VALUES (%s, %s)",
                               [(film_id, query_id) for film_id in film_ids])

        conn.commit()

    except mysql.connector.Error as err:
        print(f"Ошибка при сохранении данных: {err}")

    finally:
        cursor.close()
        conn.close()
