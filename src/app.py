import kivy # Importera Kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class MainView(Screen): # Skapa klass för huvudmeny view

    pass

class PlayerGuessView(Screen): # Skapa klass för view när spelaren gissar tal

    pass

class PCGuessView(Screen): # Skapa klass för view när datorn gissar tal

    pass

class WindowManager(ScreenManager): # Skapa hanteringsklass för olika "vyer" (views)

    pass

kv = Builder.load_file("ui.kv")

class MainApp(App):   # Skapa app klass, kallas MainApp för att inte förvirra med App.

    def build(self):
        return kv

if __name__ == "__main__":
    MainApp().run()