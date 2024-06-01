import sqlite3
import sys
import os
import qrreader as reader

# events_table
# event_name, code, first_name, last_name, entered_party
class event_database_manager():
    def __init__(self) -> None:
        pass
        
    def add_event_people(self, code_names: list):
        path = self.get_path()

        conn = sqlite3.connect(path)

        cursor = conn.cursor()

        insert_database = code_names

        cursor.executemany("INSERT INTO events_table VALUES (?, ?, ?, ?)", insert_database)

        conn.commit()

        conn.close()
    
    def verify_code(self, qr_code: str, event_name: str):
        path = self.get_path()
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT code FROM events_table")
        codes = cursor.fetchall()

        conn.commit()
        code_list = []
        for i in codes:
            code_list.append(i[0])
        
        if qr_code in code_list:
            
            cursor.execute("SELECT event_name, name, entered_party FROM events_table WHERE code = ?", (qr_code,))
            name_status = cursor.fetchall()
            conn.commit()

            if name_status[0][-1] == 0 and name_status[0][0] == event_name:
                string_to_return = 'Welcome ' + name_status[0][1] + '!'
                
                cursor.execute("UPDATE events_table SET entered_party = 1 WHERE code = ?", (qr_code,))

                conn.commit()

                conn.close()
                return string_to_return
            
            elif name_status[0][-1] == 1 and name_status[0][0] == event_name:
                conn.close()
                string_to_return = name_status[0][1] + ' has already entered the event.'
                return string_to_return
            else:
                conn.close()
                string_to_return = 'This person or code is not registered for the event.'

                return string_to_return
        
        else:
            conn.close()
            string_to_return = 'This person or code is not registered for the event.'

            return string_to_return
         
    
    def codes_list(self):
        path = self.get_path()
        conn = sqlite3.connect(path)

        cursor = conn.cursor()

        cursor.execute("""SELECT code FROM events_table""")

        codes = cursor.fetchall()

        conn.commit()

        conn.close()

        codes_list = []
        for i in codes:
            codes_list.append(i[0])
        
        return codes_list
    
    def people_in_event(self, event_name):
        path = self.get_path()
        conn = sqlite3.connect(path)
        name = event_name
        cursor = conn.cursor()

        cursor.execute("""SELECT name FROM events_table WHERE entered_party = 1 AND  event_name = ?""", (name,))

        people = cursor.fetchall()

        conn.commit()

        conn.close()

        people_list = []
        for i in people:
            people_list.append(i[0])
        
        return people_list
    
    def erase_event(self, event_name):
        path = self.get_path()
        conn = sqlite3.connect(path)

        cursor = conn.cursor()

        cursor.execute("""DELETE FROM events_table WHERE event_name = ?""", (event_name,))

        conn.commit()

        conn.close()
    
    def get_path(self):
        path = os.path.abspath(os.path.dirname(__file__))
        path_list = path.split('\\')

        path_str = ''
        for i in range(len(path_list)):
            if i == len(path_list) - 1:
                path_str += path_list[i]
            else:
                path_str += path_list[i] + '/'
        
        path_str += '/events.db'
        return path_str


if __name__ =='__main__':
    ''''event = 'party'
    entered_event = 0
    people = []
    for i in range(3):
        code = input()
        name = input()
        last_name = input()

        append_ = (event, code, name, last_name, entered_event)
        people.append(append_)
    
    conn = sqlite3.connect('Database/events.db') # reset the entered party

    cursor = conn.cursor()

    cursor.executemany("INSERT INTO events_table VALUES (?, ?, ?, ?, ?)", people)

    conn.commit()

    conn.close()'''

    '''conn = sqlite3.connect('Database/events.db') # reset the entered party

    cursor = conn.cursor()

    cursor.execute("UPDATE events_table SET entered_party = 0 WHERE code = ?", ('BRUH',))

    conn.commit()'''
    
    qrreader = reader.qrReader()
    list_qrs = qrreader.main()

    a = event_database_manager()
    a.erase_event('party')