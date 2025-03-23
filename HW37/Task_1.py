# В базе данных ich_edit три таблицы. Users с полями (id, name, age), Products с полями (pid,
# prod, quantity) и Sales с полями (sid, id, pid).
# Программа должна запросить у пользователя название таблицы и вывести все ее строки
# или сообщение, что такой таблицы нет.

import mysql.connector

dbconfig = {'host':
            'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
            'user': 'ich1',
            'password': 'password',
            'database': 'ich_edit'}
db_info = {"users": ["id", "name", "age"],
           "product": ["pid", "prod", "quantity"],
           "sales": ["sid", "pid", "id"]}
table = input("Введите название таблицы: ")
if table not in db_info.keys():
    print("Такой таблицы нет в БД")
else:
    connection = mysql.connector.connect(**dbconfig)
cursor = connection.cursor()
_sql = f"SELECT * FROM {table}"
cursor.execute(_sql)
result = cursor.fetchall()
print(*db_info[table], sep="\t\t")
for row in result:
    print(*row, sep="\t\t")
    cursor.close()
    connection.close()
