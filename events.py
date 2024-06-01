import sys
import string
import random


from pip import main


import image_generator as qr_generator
from generator import QRCodeBIT
import database_management as db_man

class event():
    def __init__(self, event_name: str, guests_list: list, direct: str) -> None:
        self.name = event_name
        self.guest_number = len(guests_list)
        self.guest_list = guests_list
        self.database_man = db_man.event_database_manager()
        self.code_person = []
        self.direct = direct

    def create_guest_codes(self):
        string_length = 6
        codes = []
        codes_in_db = self.database_man.codes_list() # calls a function to return all of the existing codes in the database

        for i in range(self.guest_number):
            bool_condition = True
            
            while bool_condition:
                try:
                    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = string_length))
                    test_gen = QRCodeBIT(random_string)
                    ans = test_gen.bitstring()
                except ValueError:
                    pass
                
                else:
                    if random_string not in codes_in_db and random_string not in codes:
                        codes.append(random_string)
                        bool_condition = False
        
        return codes
    
    def insert_into_db(self):
        codes = self.create_guest_codes()
        # event_name, code, first_name, last_name, entered_party
        people_db_insert = []
        for i in range(len(self.guest_list)):
            tupple_add = (self.name, codes[i], self.guest_list[i], 0)
            self.code_person.append((codes[i], self.direct + '/' +  self.name + '_' + self.guest_list[i] + '.jpeg'))
            people_db_insert.append(tupple_add)
        
        
        self.database_man.add_event_people(people_db_insert)


    def create_qr_codes(self):

        for i in self.code_person:
            qr = qr_generator.QRimage(i[0], i[1])
            qr.main()
    

    
        



if __name__ == '__main__':
    guests = []
    with open ('Events/names.csv') as f:
        for line in f:
            line_people = line.replace('\n', '')
            name_last = tuple(line_people.strip(" ").split(" "))
            guests.append(name_last)
            

            

    event = event(event_name = 'party', guests_list= guests)
    
    event.insert_into_db()
    event.create_qr_codes()

    

    