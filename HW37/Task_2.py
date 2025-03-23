# В базе данных ich_edit три таблицы. Users с полями (id, name, age), Products с полями (pid,
# prod, quantity) и Sales с полями (sid, id, pid).
# Программа должна вывести все имена из таблицы users, дать пользователю выбрать
# одно из них и вывести все покупки этого пользователя

import mysql.connector

dbconfig = {'host':
            'ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com',
            'user': 'ich1',
            'password': 'password',
            'database': 'ich_edit'}
connection = mysql.connector.connect(**dbconfig)
cursor = connection.cursor()
cursor.execute("SELECT DISTINCT name FROM users")
result = cursor.fetchall()
names = [res[0] for res in result]
print("В таблице users есть пользователи: ")
print(*names, sep=", ")
name = input("Выберите одного из них: ")
if name not in names:
    print("Такого пользователя нет")
else:
    cursor.execute("SELECT users.name, users.age, product.prod FROM users JOIN sales ON users.id=sales.id JOIN product ON product.pid=sales.pid WHERE users.name=%s", (name,))
result = cursor.fetchall()
if len(result) == 0:
    print(f"У пользователя {name} нет покупок")
else:
    print("ИМЯ\t\tВОЗРАСТ\t\tТОВАР ")
for row in result:
    print(*row, sep="\t\t")
cursor.close()
connection.close()
