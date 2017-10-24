from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os
from kivy.uix.button import Button

from connected import Connected

class Login(Screen):
    def do_login(self):
        app = App.get_running_app()
        app.config.read(app.get_application_config())

        self.manager.add_widget(Connected(name='connected'))        
        
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'


        s = self.manager.get_screen('connected')

class LoginApp(App):
   
    def build(self):
        manager = ScreenManager()
        manager.add_widget(Login(name='login'))
        manager.transition = SlideTransition(direction="left")

        return manager

if __name__ == '__main__':
    LoginApp().run()

