from sysconfig import get_path
from kivy.uix.label import Label
from kivymd.uix.button import MDIconButton, MDFlatButton, MDRectangleFlatButton
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from matplotlib.pyplot import text
from qr_window import Qr_window
from kivymd.uix.dialog import MDDialog
import sys
import os
import database_management as db_man

class SpecialLabel(Label):
    dialog = None
    def __init__(self, name, date, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.name = name
        self.date = date
        self.db_man = db_man.event_database_manager()

    event_name = StringProperty()
    event_date = StringProperty()
    date_passed_text = StringProperty()
    date_passed = NumericProperty()

    def search_on_release(self):
        self.app.root.transition.direction='left'
        self.app.root.current_event = self.name
        self.app.root.add_widget(Qr_window(event_name = self.name))
        self.app.root.current = 'qr_window'
    
    def erase_on_release(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = 'Are you sure you want to erase this event?',
                buttons = [
                    MDRectangleFlatButton(text = 'ERASE', text_color = (1, 0, 0, 1), line_color = (1, 0, 0, 1), on_release = self.erase_event),
                    MDFlatButton(text = 'CANCEL', on_release = self.dissmiss_dialog)
                ]
                                    )

        self.dialog.open()
        
    
    def dissmiss_dialog(self, obj):
        self.dialog.dismiss()
        
    
    def erase_event(self, obj):
        path = self.get_path()
        # erase event from event csv file
        events = []
        event_name = self.name
        with open(path) as f:
            for line in f:
                events.append(line.replace('\n', '').split(','))
        
        for i in events:
            if i[0] == event_name:
                events.remove(i)
        
        with open(path, 'w') as f:
            for i in range(len(events)):
                if i == len(events) -1:
                    f.write(events[i][0]+','+events[i][1])
                else:
                    f.write(events[i][0]+','+events[i][1]+'\n')

        # erase evry person and code registered for the event in the database
        self.db_man.erase_event(self.name)

        # update parent scroll view
        self.parent.add_events()

        # dissmiss dialog 
        self.dialog.dismiss()
    
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


        
