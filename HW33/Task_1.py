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