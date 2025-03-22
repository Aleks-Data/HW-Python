# 2. Реализуйте абстрактный базовый класс Shape (фигура), а от него унаследуйте классы Rectangle (прямоугольник) и Circle (круг). 
# Класс Shape должен иметь абстрактный метод area, который должен быть реализован в каждом дочернем классе. Классы Rectangle и Circle 
# также должны иметь метод perimeter для расчета периметра. Выведите площадь и периметр прямоугольника и круга на экран.


from abc import abstractmethod


class Shape():

    @abstractmethod
    def area(self):
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return (self.width + self.height) * 2


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14 * self.radius


rectangle = Rectangle(3, 7)
circle = Circle(8)
print(f"Площадь прямоугольника {rectangle.area()}, периметр прямоугольника {rectangle.perimeter()}")
print(f"Площадь круга {circle.area()}, длина окружности {circle.perimeter()}")
