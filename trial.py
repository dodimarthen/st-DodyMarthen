# se1 = ["Software Engineer", "Marthen", 25, "Junior", 5300]
# se2 = ["Software Engineer", "Steven", 23, "Senior", 6300]



class SoftwarEngineer:

    alias="Keyboard Magician"

    def __init__(self, name, age, level, salary):
        self.name = name
        self.age = age
        self.level = level
        self.salary = salary

    def code(self):
        print(f"{self.name} is writing code...")

    def code_in_language(self, language):
        print(f"{self.name} is writing code in {language}")
    
    # def information(self):
    #     information = f"name={self.name}, age={self.age}, salary={self.salary}"
    #     return information
    
    def __str__(self):
        information = f"name={self.name}, age={self.age}, salary={self.salary}"
        return information
    
    def __eq__(self, other):
        return self.name == other.name and self.age==other.age

    @staticmethod
    def entry_salary(age):
        if age < 25:
            return 5000
        if age > 30:
            return 7000
        return 10000
        


se1 = SoftwarEngineer("Marthen", 25, "Junior", 5300)
se2 = SoftwarEngineer("Akmal", 24, "Intermediate", 5500)
# print(se1.name, se1.age)
# print(se1.alias)
# se1.code()
# se2.code()
# se1.code_in_language("SQL")
# print(se1.information())
# print(se1==se2)
print(se2.entry_salary(33))
print(SoftwarEngineer.entry_salary(25))