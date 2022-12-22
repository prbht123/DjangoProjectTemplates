from math import pi 

class Shape():
	def __init__(self, name):
		self.name = name

	def area(self):
		print("Each shape has different area")

class Square(Shape):
	def __init__(self, length):
		super().__init__("Square")
		self.length = length

	def area(self):
		return self.length**2

class Circle(Shape):
	def __init__(self, radius):
		super().__init__("Circle")
		self.radius = radius

	def area(self):
		return pi*self.radius**2

a = Square(4)
print(a.area())

b = Circle(4)
print(b.area())

c = Shape()
c.area()