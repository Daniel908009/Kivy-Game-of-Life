from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock





class GridButton(Button):

    def sendInfo(self, caller, id):
        #print(caller)
        self.id = id
        self.caller = caller

    def clicked(self):
        #print("clicked button at" + str(self.id))
        #print(self.background_color)
        #print(self.bothColours)
        if self.bothColours[0] == self.background_color:
            self.background_color = self.bothColours[1]
            self.caller.selectedButtons.append(self.id)
        else:
            self.background_color = self.bothColours[0]
            self.caller.selectedButtons.remove(self.id)
        #print(self.caller.selectedButtons)

class MainGrid(GridLayout):

    def fillGrid(self):
        #print("somethign")
        button_number = 0
        grid = self.ids.grid
        for i in range (self.gridSize):
            #print("row")
            for j in range (self.gridSize):
                #print("column")
                button = GridButton()
                button.sendInfo(self, button_number)
                grid.add_widget(button)
                self.allButtons.append(button)
                button_number+=1
        #print(self.allButtons)

    def sliderFunc(self):
        slider = self.ids.speedSlider
        self.speed = slider.value
        print(slider.value)

    def playStop(self):
        #print("play")
        button = self.ids.playStopButton
        if button.text == 'Play':
            button.text = 'Stop'
            button.background_color = [1,1,0,1]
            for i in self.selectedButtons:
                self.allButtons[i].background_color = [0,1,0,1]
            self.play()
        else:
            button.text = "Play"
            #print("here")
            button.background_color = [0,1,0,1]

    def play(self):
        # the main game logic will later be added here
        #print(self.allButtons)
        #print(self.selectedButtons)
        pass

    def colourChanges(self):
        self.clockEvent = Clock.schedule_interval(self.updateColour, self.speed)
    def updateColour(self, t):
        label = self.ids.mainLabel
        print(label.color)
        if len(self.changingColoursOfTheMainLabel < 2):
            for i in range(3):
                if label.color[i] == 1.0:
                    self.changingColoursOfTheMainLabel.append(i)
        # more logic iwll be added here
            
        

    def reset(self):
        print("reset")

class GameOfLifeApp(App):
    def build(self):
        return MainGrid()

if __name__ == '__main__':
    GameOfLifeApp().run()