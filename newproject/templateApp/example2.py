from abc import ABC, abstractmethod

class Car(ABC):
	@abstractmethod
	def mileage(self):
		pass

class Bmw(Car):
	def mileage(self):
		print('The mileage of BMW is 60km/h')


class Audi(Car):
	def mileage(self):
		print('The mileage of Audi is 55km/h')

class Duster(Car):
	def mileage(self):
		print('The mileage of Duster is 30km/h')

b = Bmw()
b.mileage()

a = Audi()
a.mileage()

d = Duster()
d.mileage()