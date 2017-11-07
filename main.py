#!/usr/local/bin/python
# coding: latin-1

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from readQRCodeScreen import ReadQRCodeScreen

class MainScreen(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

class InvalidQRCodeScreen(Screen):
    pass

#presentation = Builder.load_file("main.kv")

class MainApp(App):
    def build(self):
        #return presentation
        pass

MainApp().run()