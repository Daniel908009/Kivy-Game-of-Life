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
        if self.ids.randomCellsSpinner.text == "Yes":
            self.caller.selectRandomCells()
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
        if self.bothColours[0] == self.background_color and self.caller.ids.playStopButton.text == "Play":
            self.background_color = self.bothColours[1]
            self.caller.selectedButtons.append(self.id)
        elif self.bothColours[0] == self.background_color and self.caller.ids.playStopButton.text == "Stop":
            self.background_color = self.aliveColour
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
        if self.clockEventCellLoop:
            self.clockEventCellLoop.cancel()
            self.play()
    
    # method for selecting random cells
    def selectRandomCells(self):
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if random.randint(0,2) == 1:
                    self.allButtons[i*self.gridSize+j].clicked()

    # method used for handling the play/stop button presses
    def playStop(self):
        button = self.ids.playStopButton
        if button.text == 'Play':
            button.text = 'Stop'
            button.background_color = [1,1,0,1]
            for i in self.selectedButtons:
                self.allButtons[i].background_color = self.allButtons[0].aliveColour
            self.play()
        else:
            button.text = "Play"
            button.background_color = [0,1,0,1]
            self.selectedButtons = []
            if self.clockEventCellLoop:
                self.clockEventCellLoop.cancel()

    # method for starting the game loop of the cells
    def play(self):
        self.clockEventCellLoop = Clock.schedule_interval(self.cellLoop, self.speed)
    
    # method for the game loop of the cells
    def cellLoop(self, t):
        buttonsToAlive = []
        copyGrid = []
        self.numberOfCycle += 1
        self.ids.cycleLabel.text = "Cycle: " + str(self.numberOfCycle)
        # copying the grid to the copyGrid list, this is technicaly not neccesery, but it makes the code more readable and it was already done like this when I realised it is not neccesery
        for i in range(self.gridSize):
            copyGrid.append([])
            for j in range(self.gridSize):
                copyGrid[i].append(self.allButtons[i*self.gridSize+j].background_color)
        # checking each cell
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                neighbours = 0
                # checking the number of living neighbours around the currently checked cell
                # topleft
                if i - 1 >= 0 and j-1 >=0 and copyGrid[i-1][j-1] == self.allButtons[0].aliveColour:
                    neighbours += 1
                # top center
                if i - 1 >= 0 and copyGrid[i-1][j] == self.allButtons[0].aliveColour:
                    neighbours += 1
                # top right
                if i - 1 >= 0 and j+1 < self.gridSize and copyGrid[i-1][j+1] == self.allButtons[0].aliveColour:
                    neighbours += 1
                # left
                if j-1 >=0 and copyGrid[i][j-1] == self.allButtons[0].aliveColour:
                    neighbours += 1
                # right
                if j+1 < self.gridSize and copyGrid[i][j+1] == self.allButtons[0].aliveColour:
                    neighbours += 1
                # bottom left
                if i+1 < self.gridSize and j-1 >=0 and copyGrid[i+1][j-1] == self.allButtons[0].aliveColour:
                    neighbours += 1
                # bottom center
                if i+1 < self.gridSize and copyGrid[i+1][j] == self.allButtons[0].aliveColour:
                    neighbours += 1
                # bottom right
                if i+1 < self.gridSize and j+1 < self.gridSize and copyGrid[i+1][j+1] == self.allButtons[0].aliveColour:
                    neighbours += 1
                # checking if the currently checked cell is alive
                if self.allButtons[i*self.gridSize+j].background_color == self.allButtons[i*self.gridSize+j].aliveColour:
                    # checking if the cell has 2 or 3 alive neighbours, if so it will stay alive
                    if neighbours == 2 or neighbours == 3:
                        buttonsToAlive.append(self.allButtons[i*self.gridSize+j])
                else:
                    # checking if the cell has 3 alive neighbours, if so it will be set to alive
                    if neighbours == 3:
                        buttonsToAlive.append(self.allButtons[i*self.gridSize+j])
        # resetting the grid to the original state
        for button in self.allButtons:
            button.background_color = button.bothColours[0]
            self.selectedButtons = []
        # setting all the cells in buttonsToAlive list to alive
        for button in buttonsToAlive:
            button.background_color = button.aliveColour
            self.selectedButtons.append(button.id)

    # method for starting the colour changing of the main label, this is called only once, when the app starts
    def colourChanges(self):
        self.clockEventColor = Clock.schedule_interval(self.updateColour, self.speed)

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
                elif label.color[i] == 0.5 and i:
                    self.changingColoursOfTheMainLabel.append((i, "up"))
                    break
                else:
                    self.changingColoursOfTheMainLabel.append((i, random.choice(["up", "down"])))
        for i in self.changingColoursOfTheMainLabel:
            if i[1] == "up":
                label.color[i[0]] += random.randint(1, 5)/100
            elif i[1] == "down":
                label.color[i[0]] -= random.randint(1, 5)/100
        for l in range(3):
            label.color[l] = round(label.color[l], 2) # this is to prevent the weird computer floats with like 1000 decimal places
        for colour in self.changingColoursOfTheMainLabel:
            if colour[1] == "up" and label.color[colour[0]] >= 1:
                self.changingColoursOfTheMainLabel.remove(colour)
            elif colour[1] == "down" and label.color[colour[0]] <= 0.5:
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
        if self.clockEventCellLoop:
            self.clockEventCellLoop.cancel()
        self.ids.cycleLabel.text = "Cycle: 0"
        self.numberOfCycle = 0
        self.fillGrid()

# the main app class
class GameOfLifeApp(App):
    def build(self):
        return MainGrid()

# running the app
if __name__ == '__main__':
    GameOfLifeApp().run()