import math

class Shape:
    def __init__(self, colour):
        self.colour = colour

    @property
    def area(self):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, colour, radius):
        super().__init__(colour)
        self.radius = radius

    @property
    def area(self):
        return math.pi * self.radius**2

class Rectangle(Shape):
    def __init__(self, colour, a, b):
        super().__init__(colour)
        self.a = a
        self.b = b

    @property
    def area(self):
        return self.a * self.b


class Square(Rectangle):
    def __init__(self, colour, a):
        super().__init__(colour, a, a)

class Triangle(Shape):
    def __init__(self, colour, a, b, c):
        super().__init__(colour)
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        return -1

shapes = [Circle("black", 10.), Rectangle("red", 10, 20), 
    Square("blue", 2), Triangle("purple", 1, 2, 3)]
for shape in shapes:
    print(shape.area, shape.colour)
