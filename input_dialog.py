from email.errors import MessageError
from importlib.resources import path
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from tkinter import filedialog
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
import datetime
from plyer import filechooser
import os

class EventNameInput(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.empty = True

    def validate_input(self):
        self.empty = True
        if ',' in self.text:
            # Checks if the input has a comma in it
            self.check_error('comma')

        elif len(self.text) > 15:
            # Checks if the input lenght is greater than 15 characters
            self.check_error('len')

        elif self.text.strip(" ") == '' or self.text == '':
            # Cheks if the field is empty
            self.check_error('empty')

        elif self.event_existing(self.text):
            # Checks if an event with that name already exists
            self.check_error('exists')

        else:
            self.error = False
            self.empty = False

    def check_error(self, type):
        if type == 'comma':
            self.helper_text = 'Event Name cannot include commas'
            self.error = True
        
        elif type == 'len':
            self.helper_text = 'Event Name has to be shorter than 15 characters'
            self.error = True

        elif type == 'empty':
            self.helper_text = 'Event Name cannot be empty'
            self.error = True

        elif type == 'exists':
            self.helper_text = 'An event with that name already exists'
            self.error = True
    
    def event_existing(self, event_n):
        path = self.get_path()
        if os.stat(path).st_size == 0:
            return False
        else:
            events = []
            with open(path) as f:
                for line in f:
                    events.append(line.replace('\n', '').split(','))
            
            event_in_list = 0
            for i in events:
                if event_n == i[0]:
                    event_in_list += 1
            
            if event_in_list > 0:
                return True
            else:
                return False
    
    def get_path(self):
        path = os.path.abspath(os.path.dirname(__file__))
        path_list = path.split('\\')

        path_str = ''
        for i in range(len(path_list)):
            if i == len(path_list) - 1:
                path_str += path_list[i]
            else:
                path_str += path_list[i] + '/'
        
        path_str += '/events.csv'
        return path_str

        



class EventDateInput(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.empty = True

    def validate_input(self):
        # Validates the input for the date by trying to create a date object in the form dd/mm/yy
        # If it returns an error, then an error is displayed at the field
        self.empty = True
        try:
            datetime.datetime.strptime(self.text, "%d/%m/%Y")

        except ValueError:
            self.check_error('form')
        
        else:
            self.error = False
            self.empty = False

    def check_error(self, type):
        if type == 'form':
            self.helper_text = 'Event Date can only be in format DD/MM/YYYY'
            self.error = True
        



class NamesDirectoryLayout(BoxLayout):
    file = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.error = False
        self.guests = []
        self.empty = True

    def get_directory(self):
        self.empty = True
        path = filechooser.open_file(title="Load File", filters=['*.csv'])
        if not bool(path):
            self.error = True
            self.error_handling('Please select a .csv file')
        else:
            self.error = False
            path_list = path[0].split('\\')
            file_path = ''
            for i in range(len(path_list)):
                if i == len(path_list) - 1:
                    file_path += path_list[i]
                else:
                    file_path += path_list[i] + '/'
            self.children[0].text = path_list[-1]
            self.children[0].theme_text_color = 'Secondary'

            try:
                with open (file_path) as f:
                    for line in f:
                        line_people = line.replace('\n', '')
                        if line_people != '':
                            name_last = line_people.strip(" ")
                            
                            self.guests.append(name_last)
                
                        else:
                            pass
                
            except:
                self.error = True
                self.error_handling('The file must contain one name per line, first name and last name separated by a whitespace')

            else:
                self.empty = False
            

    
    def error_handling(self, message):
        if self.error == True:
            self.children[0].text = message
            self.children[0].theme_text_color = 'Error'
            
            

            

class QRDirectoryLayout(BoxLayout):
    directory = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.empty = True
        
    def get_directory(self):
        self.empty = True
        path = filechooser.choose_dir(title="Choose Directory")

        if not bool(path):
            self.error = True
            self.error_handling('Please select a valid directory')

        else:
            self.error = False
            path_list = path[0].split('\\')
            file_path = ''
            for i in range(len(path_list)):
                if i == len(path_list) - 1:
                    file_path += path_list[i]
                else:
                    file_path += path_list[i] + '/'
            self.children[0].text = path_list[-1]
            self.children[0].theme_text_color = 'Secondary'

            self.directory = file_path
            self.empty = False

    def error_handling(self, message):
        if self.error == True:
            self.children[0].text = message
            self.children[0].theme_text_color = 'Error'


class InputBoxLayout(BoxLayout):
    pass

class InputDialog(MDDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title = 'Create Event'
        self.type = 'custom'
        self.content_cls = InputBoxLayout()
        self.buttons = [MDFlatButton(text = 'CANCEL'), MDFlatButton(text = 'CREATE')]