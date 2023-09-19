import datetime
from marshmallow import Schema, fields, ValidationError


class Repair:
    def __init__(self, mechanic_name, date, start_time, end_time, number_of_tires, price, notes):
        self.mechanic_name = mechanic_name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.number_of_tires = number_of_tires
        self.price = price
        self.notes= notes
    def __repr__(self):
        return f'"mechanic_name": {self.mechanic_name}, "date": {self.date}, "start_time": {self.start_time}, "end_time": {self.end_time}, "number_of_tires": {self.number_of_tires}, "price": {self.price}'
    def show_details(self):
        return f'mechanic name: {self.mechanic_name}, date: {self.date}, start time: {self.start_time}, end time: {self.end_time}, number of tires: {self.number_of_tires}, price: {self.price}'
    


class Car:
    def __init__(self,numberplate,holdername,manufacture:str,model:str,year,color,tire_size):
        self.numberplate = numberplate
        self.holdername = holdername
        self.manufacture = manufacture
        self.model = model
        self.year = year
        self.color = color
        self.tire_size = tire_size
        self.first_entrance = datetime.date.today().strftime("%d/%m/%Y")
        self.last_entrance = datetime.date.today().strftime("%d/%m/%Y")
        self.repair_history = []

    def quick_info(self) -> str:
        return f"{self.numberplate}, {self.holdername},{self.manufacture},{self.model},{self.year},{self.last_entrance}"

    def new_entrance(self):
        self.last_entrance = datetime.date.today().strftime("%d/%m/%Y")

    def new_repair(self,mechanic_name,date,start_time,end_time,number_of_tires,price,notes):
        self.repair_history.append(Repair(mechanic_name=mechanic_name, date=date, start_time=start_time, end_time=end_time, number_of_tires=number_of_tires, price=price, notes=notes))

    def update_car(self,numberplate,holdername,manufacture,model,year,color,tire_size):
        self.numberplate=numberplate
        self.holdername=holdername
        self.manufacture=manufacture
        self.model=model
        self.year=year
        self.color=color
        self.tire_size=tire_size


def letter_check(value):
    if value.isalpha() == True:
        return value
    else:
        raise ValueError("erorr")




class OnlyLetters(fields.Field):
    """Field that serializes to a string of numbers and deserializes
    to a list of numbers.
    """

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return "".join(str(d) for d in value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return letter_check(value)
        except ValueError as error:
            raise ValidationError("Pin codes must contain only digits.") from error



class RepairSchema(Schema):
    mechanic_name = OnlyLetters()
    date = fields.Date()
    start_time = fields.Time()
    end_time = fields.Time()
    number_of_tires = fields.Integer(min=1, max=4)
    price = fields.Integer(min=0)
    notes = OnlyLetters()


class CarSchema(Schema):
    numberplate = fields.Integer()
    holdername = OnlyLetters()
    manufacture = OnlyLetters()
    model = OnlyLetters()
    year = fields.Integer(min=1900, max=2024)
    color = OnlyLetters()
    tire_size = fields.String()
        
