#Доработать мини-интерфейс к базе данных, который был сделан на занятии. Новые
#возможности интерфейса:
#1. Ввести список полей выбранной таблицы.
#2. При вводе искомого значения добавить возможность выбора знака - найти записи, в
#которых выбранное поле больше, меньше или равно введенному значению.



def input_columns(table):
    columns = {"users": ["id", "name", "age"],
               "product": ["pid", "prod", "quantity"],
               "sales": ["sid", "pid", "id"]}
    fields = input(
        f"Выберите одно или несколько полей {columns[table]} этой таблицы или введите * для выбора всех: ").strip().split()
    if fields != ["*"] and not set(fields).issubset(columns[table]):
        print("Введено некорректное значение. Будет использовано значение *")
    elif fields != ["*"] and len(set(fields)) == 1:
        value = input(
            f"Введите искомое значение поля {fields[0]} таблицы {table} или '0', если нужно вывести все значения: ")
    if value != "0":
        sign = input(f"Введите знак - больше, меньше или равно: ").strip()
    if sign not in ["<", ">", ">=", "<=", "="]:
        print("Введено некорректное значение. Будет использовано значение =")
        sign = "="
        return f"SELECT * FROM {table} WHERE {fields[0]}{sign}'{value}'"
    elif len(set(fields)) == 2:
        fields = list(set(fields))
        return f"SELECT {fields[0]}, {fields[1]} FROM {table}"
    return f"SELECT * FROM {table}"