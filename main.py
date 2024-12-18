from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.popup import Popup
import random

# class of the settings popup
class SettingsPopup(Popup):
    # sending the info about the main app to the popup
    def sendInfo(self, caller):
        self.caller = caller
        self.gridSize = caller.gridSize

    # method for applying the selected settings
    def apply(self):
        self.caller.gridSize = int(self.ids.gridSizeSlider.value)
        self.caller.reset()
        self.dismiss()

    # method for updating the grid size label with the right slider number
    def updateSliderNumber(self):
        self.ids.gridSizeLabel.text = "Grid Size: " + str(round(self.ids.gridSizeSlider.value, 1))

# class of the grid buttons/cells
class GridButton(Button):
    # sending all the important info to the button/cell
    def sendInfo(self, caller, id):
        self.id = id
        self.caller = caller

    # method for selecting/deselecting the button and changing its colour accordingly
    def clicked(self):
        if self.bothColours[0] == self.background_color:
            self.background_color = self.bothColours[1]
            self.caller.selectedButtons.append(self.id)
        else:
            self.background_color = self.bothColours[0]
            self.caller.selectedButtons.remove(self.id)

# class of the main apps grid
class MainGrid(GridLayout):
    # method for creating the grid of the cells/buttons
    def fillGrid(self):
        button_number = 0
        grid = self.ids.grid
        grid.clear_widgets()
        for i in range (self.gridSize):
            for j in range (self.gridSize):
                button = GridButton()
                button.sendInfo(self, button_number) # there is propably a simpler way to do this, but for now this will do
                grid.add_widget(button)
                self.allButtons.append(button)
                button_number+=1

    # method for changing the speed of the cells loop
    def sliderFunc(self):
        slider = self.ids.speedSlider
        self.speed = slider.value
        print(slider.value)

    # method used for handling the play/stop button presses
    def playStop(self):
        button = self.ids.playStopButton
        if button.text == 'Play':
            button.text = 'Stop'
            button.background_color = [1,1,0,1]
            for i in self.selectedButtons:
                self.allButtons[i].background_color = [0,1,0,1]
            self.play()
        else:
            button.text = "Play"
            button.background_color = [0,1,0,1]

    # method for starting the game loop of the cells
    def play(self):
        # the main game logic will later be added here
        #print(self.allButtons)
        #print(self.selectedButtons)
        pass

    # method for starting the colour changing of the main label, this is called only once, when the app starts
    def colourChanges(self):
        self.clockEvent = Clock.schedule_interval(self.updateColour, self.speed)
    # this method makes the main label change colours
    def updateColour(self, t):
        label = self.ids.mainLabel
        for i in range(3):
            temp = True
            for object in self.changingColoursOfTheMainLabel:
                if object[0] == i:
                    temp = False
            if temp:
                if label.color[i] == 1 and i:
                    self.changingColoursOfTheMainLabel.append((i, "down"))
                    break
                elif label.color[i] == 0 and i:
                    self.changingColoursOfTheMainLabel.append((i, "up"))
                    break
                else:
                    self.changingColoursOfTheMainLabel.append((i, random.choice(["up", "down"])))
        for i in self.changingColoursOfTheMainLabel:
            if i[1] == "up":
                label.color[i[0]] += 0.09
            elif i[1] == "down":
                label.color[i[0]] -= 0.09
        for l in range(3):
            label.color[l] = round(label.color[l], 1) # this is to prevent the weird computer floats with like 1000 decimal places
        for colour in self.changingColoursOfTheMainLabel:
            if colour[1] == "up" and label.color[colour[0]] >= 1:
                self.changingColoursOfTheMainLabel.remove(colour)
            elif colour[1] == "down" and label.color[colour[0]] <= 0:
                self.changingColoursOfTheMainLabel.remove(colour)

    # method for opening the settings popup
    def settings(self):
        popup = SettingsPopup()
        popup.sendInfo(self) # there is propably a simpler way to do this, but for now this will do
        popup.open()

    # method for reseting the game
    def reset(self):
        self.selectedButtons = []
        self.allButtons = []
        self.ids.playStopButton.text = "Play"
        self.ids.playStopButton.background_color = [0,1,0,1]
        self.fillGrid()

# the main app class
class GameOfLifeApp(App):
    def build(self):
        return MainGrid()

# running the app
if __name__ == '__main__':
    GameOfLifeApp().run()