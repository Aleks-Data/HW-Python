from db_operations import (
    get_all_users_statistics,
    add_user_to_database,
    user_exists_in_database,
    fetch_user_info,
    get_user_statistics,
    change_user_information,
    fetch_table_rows,
    database_is_exists,
    get_user_id,
    save_query_results,
    find_films_by_year,
    get_film_statistics
)

from db_setup import (
    create_struct_database,
    #database_is_exists,
    get_connection_read
)

from search_engine import find_documents


def main():
    if not database_is_exists("sumarokovav_300924"):
        create_struct_database()

    username = input("Введите ваш логин:")
    if user_exists_in_database(username):
        user_data = fetch_user_info(username)
        print(f"Привет, {user_data['first_name']} {user_data['last_name']}!")
    else:
        first_name = input("Введи своё имя:")
        last_name = input("Введи свою фамилию:")
        add_user_to_database(username, first_name, last_name)

    while True:
        action = input(
            "Выберите действие: 1 - Найти фильм, 2 - Получить статистику, 3 - Изменить данные, 0 - Выход\n"
        )

        if action == "1":
            query_action = input(
                "Выберите действие: 1 - Поиск по ключевым словам, 2 - Поиск по году выпуска\n")

            if query_action == "1":
                with open(r"c:\Users\sumar\Downloads\python_24_02_25-main\Film_searcher\stopwords.txt", "r", encoding="utf-8") as file:
                    list_stop_words = {word.strip().lower()
                                       for word in file if word.strip()}

                if conn := get_connection_read(db_name="sakila"):
                    documents = fetch_table_rows(conn, "film")
                    conn.close()
                else:
                    print("Ошибка подключения.")
                    continue

                query = input("Введите название, жанр или ключевые слова: ")

                results = find_documents(documents, list_stop_words, query)

                if results:
                    for document_id, relevance in results:
                        print(
                            f"Фильм id={document_id} | релевантность={relevance}")

                    if user_id := get_user_id(username):
                        film_ids = [doc_id for doc_id, _ in results]
                        save_query_results(user_id, query, film_ids)
                    else:
                        print("Ошибка: пользователь не найден.")
                else:
                    print("Фильмы не найдены.")

            elif query_action == "2":
                year = int(input("Введите год выпуска фильма: "))
                if conn := get_connection_read(db_name="sakila"):
                    results = find_films_by_year(conn, "film", year)
                    conn.close()

                    film_ids = [row[0] for row in results]

                    if film_ids:
                        print(film_ids)
                    else:
                        print("Фильмы за этот год не найдены.")

                    if user_id := get_user_id(username):
                        save_query_results(
                            user_id, f"Поиск по году: {year}", film_ids)
                    else:
                        print("Ошибка: пользователь не найден.")

                else:
                    print("Ошибка подключения.")
            else:
                print("Неверный ввод. Измените запрос.")

        elif action == "2":
            stat_action = input(
                "1 - Статистика по всем пользователям, 2 - Статистика по Вам, 3 - Рейтинг фильмов\n")
            if stat_action == "1":
                print(get_all_users_statistics())
            elif stat_action == "2":
                print(get_user_statistics(username))
            elif stat_action == "3":
                print(get_film_statistics())
            else:
                print("Неверный ввод")

        elif action == "3":
            field_action = input(
                "Выберите действие: 1 - Сменить first_name, 2 - Сменить last_name, 3 - Сменить user_name\n")
            new_value = input("Введите новое значение: ")
            fields = {"1": "first_name", "2": "last_name", "3": "user_name"}
            if field_action in fields:
                change_user_information(
                    username, fields[field_action], new_value)
                print("Данные успешно обновлены")
            else:
                print("Неверный ввод")
        elif action == "0":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Неверный ввод, попробуйте снова.")


if __name__ == "__main__":
    main()
