import kivy # Importera Kivy
import random # Importera random modul
kivy.require('2.2.1') # Bestäm kivy version

# Importera "grundläggande byggstenar", det som gör själva appen
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory

# Importera kivy typer
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty

# Importera kivy UI komponenter
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

userInput = '' # Håller TextInput värde från användaren
targetNumber = 0 # Håller det nummer som ska gissas
guessAmount = 0 # Håller mängden gissningar som gjorts
maxPossible = 50 # Håller högsta möjliga tal (för datorns gissningar)
minPossible = 1 # Håller minsta möjliga tal (för datorns gissningar)
guess = 0 # Håller datorns gissning

class PlayerWinPopup(Popup): # Klass för att skapa popup för spelarvinst

    # Definiera innehåll av kivy labels
    winLabelContent = StringProperty()

    def __init__(self, **kwargs):
        global guessAmount
        super(PlayerWinPopup, self).__init__(**kwargs)
        # Visa slutvärden
        self.winLabelContent = f"Antal gissningar: {guessAmount}"

    # Funktion för att lämna programmet när man är klar
    def exitApp(x):
        exit()

class PCWinPopup(Popup): # Klass för att skapa popup för datorvinst

    # Definiera innehåll av kivy labels
    winLabelContent = StringProperty()

    def __init__(self, **kwargs):
        global guessAmount
        global targetNumber
        global guess
        super(PCWinPopup, self).__init__(**kwargs)
        # Visa slutvärden
        self.winLabelContent = f"Talet var: {targetNumber}\n Jag gissade: {guess}\n Antal gissningar: {guessAmount}"

    # Funktion för att lämna programmet när man är klar
    def exitApp(x):
        exit()

class MainView(Screen): # Skapa klass för huvudmeny view

    # Funktion för att lämna programmet om man inte känner för att vara kvar
    def exitApp(x):
        exit()

    # Funktion som körs när spelaren väljer att gissa tal
    def startPlayerGuess(x):
        global targetNumber
        # Välj ett slumpmässigt nummer för spelaren att gissa
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

    # Event som körs när TextField:et uppdateras
    def onInput(x, y):
        global userInput
        global targetNumber
        userInput = y

    # Event som körs när användaren bekräftar att gissa ett tal
    def onEnter(self):
        global userInput
        global guessAmount

        # Lägg till en gissning i gissningsräknaren
        guessAmount += 1
        self.guessAmountContent = "Gissningar: "+str(guessAmount)

        # Lång ifsats för att kolla det nummer spelaren gissade
        if not userInput.isnumeric():
            # Om input inte är ett nummer, klaga
            self.labelContent = "Ange ett nummer!"
        elif int(userInput) > 50 or int(userInput) < 1:
            # Om input är mer än 50 eller mindre än 1, klaga
            self.labelContent = "Talet ska vara mellan 1-50."
        elif int(userInput) > targetNumber:
            # Om input är större än svaret, säg att det är för stort
            self.labelContent = f"{userInput}? Det är för stort."
        elif int(userInput) < targetNumber:
            # Om input är mindre än svaret, säg att det är för litet
            self.labelContent = f"{userInput}? Det är för litet."
        else:
            # Annars, säg att talet är rätt och öppna popup
            self.labelContent = f"{userInput} är rätt!"
            Factory.PlayerWinPopup().open()

class PCGuessPrepareView(Screen): # Skapa klass för view innan datorn gissar tal

    # Event för att uppdatera userInput när TextInput:en uppdateras
    def onInput(x, y):
        global userInput
        userInput = y

    # Event som körs när användaren bekräftar att gissa ett tal
    def onEnter(x):
        global userInput
        global targetNumber

        # Försök konvertera input till nummer
        try:
            userInput = int(userInput)
        except:
            print("Not a number")
        else:

            # Kolla storlek på nummer, så att det är 1-50
            if not userInput > 50 or userInput < 1:
                targetNumber = userInput
                kv.current = "pcguess"

class PCGuessView(Screen): # Skapa klass för view när datorn gissar tal (kommer bli kaos)

    # Definiera state variabler av kivy knappar (enabled/disabled)
    buttonGuessEnabled = BooleanProperty()
    buttonHighEnabled = BooleanProperty()
    buttonLowEnabled = BooleanProperty()
    buttonCorrectEnabled = BooleanProperty()

    # Definiera string variabel för kivy labels
    labelOutput = StringProperty()
    labelTargetValue = StringProperty()
    labelGuessAmount = StringProperty()
    labelPossibleRange = StringProperty()
    labelPossibleRemaining = StringProperty()

    # Initialisera klassen
    def __init__(self, **kwargs):
        super(PCGuessView, self).__init__(**kwargs)

        # Sätt standardstate för knappar
        self.buttonGuessEnabled = False
        self.buttonHighEnabled = True
        self.buttonLowEnabled = True
        self.buttonCorrectEnabled = True

        # Sätt standardvärde för labels
        self.labelOutput = "Redo att gissa!"
        self.labelTargetValue = "Valt tal: -"
        self.labelGuessAmount = "Gissningar: 0"
        self.labelPossibleRange = "Möjliga: 1..50"
        self.labelPossibleRemaining = "Återstående: 50"

    # Funktion för att lämna programmet om man tröttnar
    def exitApp(self):
        exit()

    # Uppdatera värden på labels för feedback
    def updateLabels(self):

        # Importera globala variabler
        global guessAmount
        global minPossible
        global maxPossible
        global guessAmount

        # Uppdatera värden
        self.labelGuessAmount = f"Gissningar: {guessAmount}"
        self.labelPossibleRange = f"Möjliga: {minPossible}..{maxPossible}"
        self.labelPossibleRemaining = f"Återstående: {maxPossible-minPossible}"

    # Funktion för datorn att gissa värden
    def guessNumber(self):

        # Importera globala variabler
        global guessAmount
        global maxPossible
        global minPossible
        global guess

        # Ta ett slumpmässigt värde inom de gränser som datorn listat ut
        guess = random.randint(minPossible, maxPossible)

        # Höj antalet gissningar
        guessAmount += 1

        # Uppdatera output texten för att låta användaren veta datorns gissning
        self.labelOutput = f"Är talet {guess}?"

        # Uppdatera övrigt
        self.updateLabels()

    # Funktion för datorn att hantera svaret på sin gissning
    def guessAnswer(self, answer):
        
        # Importera globala variabler
        global targetNumber
        global maxPossible
        global minPossible
        global guess

        match answer:

            # Om användaren säger att gissningen var för hög
            case "high":

                maxPossible = guess-1

            # Om användaren säger att gissningen var för låg
            case "low":

                minPossible = guess+1

            # Om användaren säger att gissningen var korrekt
            case "correct":

                self.labelOutput = "Jag vann!"
                Factory.PCWinPopup().open()

        # Ett försök att komma på om användaren ljuger för datorn eller inte, och gör då något åt saken
        if minPossible >= 50 or maxPossible <= 1 or (minPossible == maxPossible and minPossible > guess):

            # Uppdatera output label
            self.labelOutput = "Du ljög för mig!"
            self.updateLabels()

            # Stäng av alla knappar
            self.buttonGuessEnabled = True
            self.buttonHighEnabled = True
            self.buttonLowEnabled = True
            self.buttonCorrectEnabled = True

        else:

            # Fortsätt gissa om användaren inte ljugit
            self.updateLabels()
            self.guessNumber()

    # Event när användaren trycker på "Börja gissa" knappen
    def buttonGuessClick(self):
        
        # Importera globala variabler
        global targetNumber

        # Uppdatera state för knappar (inverterar bara)
        self.buttonGuessEnabled = True
        self.buttonHighEnabled = False
        self.buttonLowEnabled = False
        self.buttonCorrectEnabled = False

        # Uppdatera text för vad det rätta svaret är
        self.labelTargetValue = f"Valt tal: {targetNumber}"

        self.guessNumber()

    # Event när användaren trycker på "För högt" knappen
    def buttonHighClick(self):
        
        # Låt datorn hantera svaret "high"
        self.guessAnswer("high")

    # Event när användaren trycker på "För lågt" knappen
    def buttonLowClick(self):
        
        # Låt datorn hantera svaret "low"
        self.guessAnswer("low")

    # Event när användaren trycker på "Korrekt" knappen
    def buttonCorrectClick(self):
        
        # Låt datorn hantera svaret "correct"
        self.guessAnswer("correct")

class WindowManager(ScreenManager): # Skapa hanteringsklass för olika "vyer" (views)

    pass

# Ladda fil med ui layout
kv = Builder.load_file("ui.kv")

class MainApp(App):   # Skapa app klass, kallas MainApp för att inte förvirra med App.

    def build(self):
        return kv

if __name__ == "__main__":
    MainApp().run()