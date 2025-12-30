class Car:
    #INITIALIZE OBJECT    
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        #DEFAULT ATTRIBUTE
        self.odometer_reading = 0
    
    def get_descriptive_name(self):
        #RETURN A NEATLY FORMATTED NAME
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()
    
    def read_odometer(self):
        print(f"This car has {self.odometer_reading} miles on it.")

    def update_odometer(self, mileage):
        if mileage >= self.odometer_reading:
            self.odometer_reading = mileage
        else:
            print("You can't roll back an odometer!")
    
    def increment_odometer(self, miles):
        self.odometer_reading += miles

    def fill_gas_tank(self):
        print("Filling gas tank...")

class Battery:
    def __init__(self, battery_size=40):
        self.battery_size = battery_size

    def describe_battery(self):
        print(f"This car has a {self.battery_size}-kWh battery.")

    def get_range(self):
        if self.battery_size == 40:
            range = 150
        elif self.battery_size == 65:
            range = 225
    
        print(f"This car can go about {range} miles on a full charge.")

class ElectricCar(Car):
    def __init__(self, make, model, year):
        super().__init__(make, model, year)
        #CREATES A NEW INSTANCE OF BATTERY
        #HELPFUL TO THINK OF AS OBJECTS SPECIFICALLY
        self.battery = Battery()