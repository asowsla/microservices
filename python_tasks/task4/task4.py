from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.top_grade = 5

    @abstractmethod
    def print_info(self): 
        pass

    @abstractmethod
    def get_grant(self): 
        pass

    def compare_grant(self, other):
        if self.get_grant() < other.get_grant(): 
            return -1
        elif self.get_grant() > other.get_grant(): 
            return 1
        else: 0
        
class Student(Person):
    def __init__(self, name, age, group, avg_grade):
        super().__init__(name, age)
        self.group = group
        self.avg_grade = avg_grade
        self.low_grant, self.high_grant = [4000, 6000]

    def print_info(self):
        print(f"Student's name: {self.name}, age: {self.age}, "
              f"group: {self.group}, gpa: {self.avg_grade}")

    def get_grant(self):
        return (
            self.high_grant if self.avg_grade == self.top_grade
            else self.low_grant if self.avg_grade < self.top_grade
            else 0
        )
        
class PhDStudent(Student):
    def __init__(self, name, age, group, avg_grade, research_title):
        super().__init__(name, age, group, avg_grade)
        self.research_title = research_title
        self.low_grant, self.high_grant = [6000, 8000]

    def print_info(self):
        print(f"PhD's name: {self.name}, age: {self.age}, "
              f"group: {self.group}, gpa: {self.avg_grade}")
        print(f"scientific works: {self.research_title}")

    def get_grant(self):
        return (
            self.high_grant if self.avg_grade == self.top_grade
            else self.low_grant if self.avg_grade < self.top_grade
            else 0
        )

def comparisons():
    student = Student("Jane Doe", 18, "5130101/50001", 5.0)
    PhD = PhDStudent("John Doe", 25, "None", 4.6,
                     "Machine Learning Algorithms")

    student.print_info()
    print(f"scholarship: {student.get_grant()} RUB\n")

    PhD.print_info()
    print(f"scholarship: {PhD.get_grant()} RUB\n")

    comparison_result = student.compare_grant(PhD)
    
    if comparison_result == -1:
        print(f"{student.name} scholarship < {PhD.name} scholarship")
    elif comparison_result == 1:
        print(f"{student.name} scholarship > {PhD.name} scholarship")
    else:
        print(f"{student.name} scholarship = {PhD.name} scholarship")


if __name__ == "__main__":        
    comparisons()