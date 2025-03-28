# В базе данных ich_edit три таблицы. Users с полями (id, name, age), Products с полями (pid,
# prod, quantity) и Sales с полями (sid, id, pid).
# Программа должна запросить у пользователя название таблицы и вывести все ее строки
# или сообщение, что такой таблицы нет.

import mysql.connector

dbconfig = {'host':
            'ich-db.edu.itcareerhub.de',
            'user': 'ich1',
            'password': 'password',
            'database': 'ich_edit'}

tables = ["Users", "Products", "Sales"]
table = input("Введите название таблицы: ")

if table not in tables:
    print("Такой таблицы нет в БД")


try:
    connection = mysql.connector.connect(**dbconfig)
    cursor = connection.cursor()
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    result = cursor.fetchall()
    column_headers = [desc[0] for desc in cursor.description]
    print(*column_headers, sep="\t\t")

    for row in result:
        print(*row, sep="\t\t")
except mysql.connector.Error as err:
    print(f"Ошибка: {err}")
    
finally:
    cursor.close()
    connection.close()
            
