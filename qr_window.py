

from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.dialog import MDDialog


from kivy.clock import Clock
import time
import sys

from matplotlib.pyplot import title


import database_management as db_man
import qrreader as reader

class Qr_button(MDRectangleFlatIconButton):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_man = db_man.event_database_manager()
        self.dialog = None
    def on_release(self):
        
        if self.disabled == False:
            self.disabled = True
            qr_reader = reader.qrReader()
            lists_qr = qr_reader.main()
            
        else:
            pass
        self.disabled = False

        if bool(lists_qr) == False:
            pass
        else:
            app = MDApp.get_running_app()
            event = app.root.current_event
            string_dialog = ''
            for i in lists_qr:
                string_dialog = self.db_man.verify_code(qr_code= i, event_name= event) 
            
            self.parent.children[0].remove_widget(self.parent.children[0].children[0])
            self.parent.children[0].add_widget(Cheked_people())

            self.dialog = MDDialog(title = string_dialog)

            self.dialog.open()
            '''Clock.schedule_once(lambda dt: self.close_dialog(), 5)'''
        
            

        
    def close_dialog(self):
        self.dialog.dismiss()




class Cheked_people(MDList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = MDApp.get_running_app()
        event = app.root.current_event
        self.db_man  = db_man.event_database_manager()
        people = self.db_man.people_in_event(event)

        for i in people:
            self.add_widget(OneLineListItem(text = i))
    
        


class Qr_window(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    event_name = StringProperty()

