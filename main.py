import pygame
import os
import Menu
BG = pygame.image.load(os.path.join("Assets/Other", "Plano-10.png"))
pygame.init()
class Control:
    def __init__(self):
        self.windowStack = []
    def addWindow(self,window):
        self.windowStack.append(window)
    def initWindow(self):
        screen = pygame.display.set_mode((1100,600))
        menu = Menu.Menu(BG,screen,self.windowStack)
        self.addWindow(menu)
    def run(self):
        self.initWindow()
        while(len(self.windowStack) > 0):
            self.windowStack[-1].run()
mainn = Control()
mainn.run()
