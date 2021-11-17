import pygame
import button as a
class Window:
    START = 1
    PLAYING = 2
    STOP = 5
    QUIT = 3
    HOWTOPLAY = 4
    def __init__(self,background,screen,windowStack,state = START):
        self.background = background #a variable surface ~ image of background window
        self.screen = screen
        self.windowStack = windowStack
        self.state = state
        self.buttons = a.ButtonList()
        self.hasthread = False
    def hasThread(self):
        return self.hasthread
    def initKey(self):
        pass
    def initButtons(self): # abstract
        pass
    def getState(self):
        pass
    def update(self):
        pass
    def draw(self):
        pass
    def run(self):
        pass