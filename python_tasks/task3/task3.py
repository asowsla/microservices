import math
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): 
        pass

    @abstractmethod
    def perimeter(self): 
        pass

    def comparing_area(self, other): 
        return self.area() - other.area()
    
    def comparing_perimeter(self, other): 
        return self.perimeter() - other.perimeter()

class Rectangle(Shape):
    def __init__(self, width, height): 
        self.w, self.h = width, height

    def area(self): 
        return self.w * self.h
    
    def perimeter(self): 
        return 2 * (self.w + self.h)

class Square(Rectangle):
    def __init__(self, side): 
        super().__init__(side, side)

class Triangle(Shape):
    def __init__(self, a, b, c): 
        self.a, self.b, self.c = a, b, c

    def perimeter(self): 
        return self.a + self.b + self.c
    
    def area(self):
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

class Circle(Shape):
    def __init__(self, r): 
        self.r = r

    def area(self): 
        return math.pi * self.r ** 2
    
    def perimeter(self): 
        return 2 * math.pi * self.r

def comparisons() -> None:
    fig1, fig2 = [Rectangle(3, 5), Triangle(3, 5, 7)]

    print("Fig1 square > Fig2 square? ---" , fig1.comparing_area(fig2) > 0)
    print("Fig1 perimeter > Fig2 perimeter? ---" , fig1.comparing_perimeter(fig2) < 0)


if __name__ == "__main__":
    comparisons()