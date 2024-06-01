

from kivy.uix.button import Button
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from speciallabel import SpecialLabel
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.config import Config


import datetime
import input_dialog
from input_dialog import InputBoxLayout
import sys
from numpy import empty
import pandas
import os
from matplotlib.pyplot import text

from events import event


class Loading_layout(BoxLayout):
    pass

class WindowManager(ScreenManager):
    current_event = StringProperty()
    grid_events = ObjectProperty()

class EventWindow(Screen):
    pass

class EventScrollView(ScrollView):
    pass


class MainApp(MDApp):
    dialog = None
    def back(self, button):
        self.root.transition.direction = 'right'
        self.root.current = 'eventwindow'
        window = self.root.children[1]
        self.root.remove_widget(window)
    
    def create_event_dialog(self):

        
        self.dialog = MDDialog(
        title="Create Event ",
        type="custom",
        content_cls = InputBoxLayout(),
        buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=(11/255, 107/255, 59/255, 1),
                    on_release = self.dissmiss_dialog
                ),
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color= (11/255, 107/255, 59/255, 1),
                    on_release = self.create_event

                ),
            ],
        )
        
        self.dialog.open()

    def dissmiss_dialog(self, obj):
        self.dialog.dismiss()
    
    def create_event(self, obj):
        EventNameInput = self.dialog.content_cls.children[4]
        EventDateInput = self.dialog.content_cls.children[3]
        NamesDirectoryLayout = self.dialog.content_cls.children[2]
        QRDirectoryLayout = self.dialog.content_cls.children[1]
        ErrorLabel = self.dialog.content_cls.children[0]

        empty_list = [EventNameInput.empty, EventDateInput.empty, NamesDirectoryLayout.empty, QRDirectoryLayout.empty]


        if any(empty_list):
            ErrorLabel.text = "Cannot create event, there is some missing/incorrect inputs"
            
        else:
        

            event_name = EventNameInput.text
            event_date = EventDateInput.text
            guests_list = NamesDirectoryLayout.guests
            QR_directory = QRDirectoryLayout.directory

            self.add_event_csv(name = event_name,date = event_date)
            self.db_qr_addEvent(name=event_name, guests= guests_list, Qrdirect= QR_directory)
        
            self.root.children[0].children[0].children[0].children[0].add_events()
            self.dialog.dismiss()
            
            
            self.dialog = MDDialog(title = 'Event created successfully!')
            self.dialog.open()
    
    def add_event_csv(self, name, date):
        path = self.get_path()
        if os.path.getsize(path) == 0:
            with open(path, 'w') as f:
                f.write(name +','+ date +'\n')

        else:
            events = []
            with open(path) as f:
                for line in f:
                    events.append(line.replace('\n', '').split(','))
            
            event_tuple = (name,date)
            events.append(event_tuple)
            
            with open(path, 'w') as f:
                for i in range(len(events)):
                    if i == len(events) -1:
                        f.write(events[i][0]+','+events[i][1])
                    else:
                        f.write(events[i][0]+','+events[i][1]+'\n')
        
    def db_qr_addEvent(self, name, guests, Qrdirect):
        event_create = event(event_name= name,guests_list= guests, direct = Qrdirect)
        event_create.insert_into_db()
        event_create.create_qr_codes()
    
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





class EventGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.add_events()
        


    def add_events(self):
        path = self.get_path()
        self.clear_widgets()
        if os.stat(path).st_size == 0:
            self.add_widget(MDLabel(
                text = 'There are no events created',
                halign = 'center',
                valign = 'center',
                theme_text_color = 'Primary'
            ))
        else:
            events = []
            with open(path) as f:
                for line in f:
                    events.append(line.replace('\n', '').split(','))
            d1 = ''
            d2 = ''
            for i in events:
                d1 = datetime.datetime.strptime(i[1], "%d/%m/%Y").date()
                d2 =  datetime.datetime.now().date()
                if d2 > d1: 
                    self.add_widget(SpecialLabel(name= i[0], date = i[1], event_name = i[0], event_date = i[1], date_passed = 1))
                else:
                    self.add_widget(SpecialLabel(name= i[0], date = i[1], event_name = i[0], event_date = i[1], date_passed = 0))
    
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
        
if __name__ == '__main__':
    Config.set('graphics', 'width', '700')
    Config.set('graphics', 'height', '600')
    Config.write()
    MainApp().run()
