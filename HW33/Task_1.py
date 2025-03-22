# 1. Реализуйте класс Employee, представляющий сотрудника компании. 
# Класс должен иметь статическое поле company с названием компании, а также методы:
# set_company(cls, name): метод класса для изменения названия компании
# __init__(self, name, position): конструктор, принимающий имя и должность сотрудника
# get_info(self): метод, возвращающий информацию о сотруднике в виде строки (имя, должность, название компании)


class Employee():
    Company = ""
    
    
    @classmethod
    def set_company(cls, name):
        cls.Company = name
        
        
    def __init__(self, name, position):
        self.name = name
        self.position = position
        
        
    def get_info(self):
        print("Name:", self.name)
        print("Position:", self.position)
        print("Company:", self.Company)
        

Employee.set_company("Google")       
employee1 = Employee("John", "Manager")
employee2 = Employee("Alice", "Developer")

print(employee1.get_info())
print(employee2.get_info())
