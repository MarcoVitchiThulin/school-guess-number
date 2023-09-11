import kivy # Importera Kivy
import random # Importera random modul
kivy.require('2.2.1')

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory

from kivy.properties import StringProperty

from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

userInput = '' # Håller TextInput värde från spelaren
targetNumber = 0 # Håller det nummer som ska gissas
guessAmount = 0 # Håller mängden gissningar som gjorts

class WinPopup(Popup): # Klass för att skapa popup för vinst

    # Definiera innehåll av kivy labels
    winLabelContent = StringProperty()

    def __init__(self, **kwargs):
        global guessAmount
        super(WinPopup, self).__init__(**kwargs)
        self.winLabelContent = f"Antal gissningar: {guessAmount}"

    # Funktion för att lämna programmet när man är klar
    def exitGame(x):
        exit()

class MainView(Screen): # Skapa klass för huvudmeny view

    # Funktion som körs när spelaren väljer att gissa tal
    def startPlayerGuess(x):
        global targetNumber
        targetNumber = random.randint(1,50)
        print(targetNumber)

class PlayerGuessView(Screen): # Skapa klass för view när spelaren gissar tal

    # Definiera innehåll av kivy labels
    labelContent = StringProperty()
    guessAmountContent = StringProperty()

    # Initialisera klassen
    def __init__(self, **kwargs):
        super(PlayerGuessView, self).__init__(**kwargs)
        self.labelContent = "Börja gissa!"
        self.guessAmountContent = "Gissningar: 0"

    # Event som körs när InputField:et uppdateras
    def onInput(x, y):
        global userInput
        global targetNumber
        userInput = y

    # Event som körs när spelarenn bekräftar att gissa ett tal
    def onEnter(self):
        global userInput
        global guessAmount

        # Lägg till en gissning i gissningsräknaren
        guessAmount += 1
        self.guessAmountContent = "Gissningar: "+str(guessAmount)

        # Lång ifsats för att kolla det nummer spelaren gissade
        if not userInput.isnumeric():
            self.labelContent = "Ange ett nummer!"
        elif int(userInput) > 50 or int(userInput) < 1:
            self.labelContent = "Talet ska vara mellan 1-50."
        elif int(userInput) > targetNumber:
            self.labelContent = f"{userInput}? Det är för stort."
        elif int(userInput) < targetNumber:
            self.labelContent = f"{userInput}? Det är för litet."
        else:
            self.labelContent = f"{userInput} är rätt!"
            Factory.WinPopup().open()


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