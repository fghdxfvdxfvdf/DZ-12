from collections import UserDict
from datetime import datetime
import json

class Field:
    def __init__(self, value):
        self.value = value
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)    

class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if len(str(new_value)) != 10 or not str(new_value).isdigit():
            raise ValueError("Invalid phone number. It should have 10 digits.")
        self._value = new_value


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)
 
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            self.data_birthday = datetime.strptime(new_value, '%d %B %Y')
        except ValueError("Invalid date format for Birthday"):
            return None
        self._value = new_value
    

class Record:
    def __init__(self, name: str, birthday: str=None):
        self.name = Name(name)
        if birthday is not None:
            self.data_birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, phone: str):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def find_phone(self, phone: str = None):
        if self.phones == []:
            return None

        for i in self.phones:
            if i.value == phone:
                return i

    def remove_phone(self, phone: str = None):
        if self.phones == []:
            return None
        
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i) 
        
    def edit_phone(self, old_phone: str, new_phone: str):
            for i in self.phones:
                if i.value == old_phone:
                    i.value = new_phone
                    return
            raise ValueError
    
    def days_to_birthday(self):

        if self.data_birthday is None:
            return None

        self.current_datetime_date = datetime.now().date()
        d1 = datetime(year=self.current_datetime_date.year, month=self.current_datetime_date.month, day=self.current_datetime_date.day)

        if self.data_birthday.data_birthday.month > self.current_datetime_date.month or (self.data_birthday.data_birthday.month == self.current_datetime_date.month and self.data_birthday.data_birthday.day >= self.current_datetime_date.day):
            d2 = datetime(year=self.current_datetime_date.year, month=self.data_birthday.data_birthday.month, day=self.data_birthday.data_birthday.day)
        else:
            d2 = datetime(year=self.current_datetime_date.year + 1, month=self.data_birthday.data_birthday.month, day=self.data_birthday.data_birthday.day)
            
        return (d2 - d1).days
    
    def to_json(self):
        return {
            "name": self.name.value,
            "phones": [phone.value for phone in self.phones]
        }
                
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.current_index = 0

    def add_record(self, record):
       self.data[record.name.value] = record

    def find(self, name: str):
        for i in self.data:
            if i == name:
                return self.data[i]
        return None 
    
    def delete(self, name: str):
            result = self.data.pop(name, None)
            return result is not None
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current_index >= len(self.data.values()):
            raise StopIteration
        else:
            names = list(self.data.keys())
            current_name = names[self.current_index]
            self.current_index += 1
            return self.data[current_name]

    def save_to_file(self, filename: str = None):
        if self.data == {}:
            return None
            
        with open(filename, 'w') as f:
            res = []
            for i in self.data.values():
                res.append(i.to_json())
            json.dump(res, f)
        return 'Data saved successfully'
                
        
    def load_from_file(self, filename: str):
        try:
            with open(filename, 'r') as f:
                d_json = json.load(f)
                return d_json
        except:
            return 'file is not found!'

    def matches_the_string(self, char: str = None) -> list:
        if char is None:
            return 'Please enter your request'
            
        if self.data == {}:
            return None

        result = []
        for record in self.data.values():
            record_str = str(record)
            if char.lower() in record_str.lower():
                result.append(record) 
        return result