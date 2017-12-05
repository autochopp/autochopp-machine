#!/usr/local/bin/python
# coding: latin-1

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from embedded_electronics import MachineController


from readQRCodeScreen import ReadQRCodeScreen

class MainScreen(Screen):
    
    machine = MachineController()

    def switch(self):
        
        if self.machine.power_on_nobreak() == True:
            self.manager.current = 'exceptionNoBreakScreen'
        elif self.machine.power_on_nobreak() == False:
            self.manager.current = 'readQRCodeScreen'

class ScreenManagement(ScreenManager):
    pass

class InvalidQRCodeScreen(Screen):
    pass

class ValidQRCodeScreen(Screen):
    pass

class SuccessChopp(Screen):
    pass

class WaitCup(Screen):
    pass

class WaitChopp(Screen):
    pass

class ExceptionScreen(Screen):
    pass

class ExceptionNoBreakScreen(Screen):
    pass

#presentation = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        #return presentation
        pass

MainApp().run()