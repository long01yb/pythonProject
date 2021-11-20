import sys

import pygame
import  os

import Select
from Window import  Window
#222
from Game import  Game
import button as a
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

START = [pygame.image.load(os.path.join("Assets/Other", "StartIdle.png")),
         pygame.image.load(os.path.join("Assets/Other", "StartHover.png"))]
SETTING = [pygame.image.load(os.path.join("Assets/Other", "SettingIdle.png")),
         pygame.image.load(os.path.join("Assets/Other", "SettingHover.png"))]
QUIT = [pygame.image.load(os.path.join("Assets/Other", "QuitIdle.png")),
         pygame.image.load(os.path.join("Assets/Other", "QuitHover.png"))]
BG_select = pygame.image.load(os.path.join("Assets/Other", "BG_ChoosePlayer.png"))
class Menu(Window):
    SELECTING = 11
    def __init__(self,bg,screen,windowStack):
        super().__init__(bg,screen,windowStack)
        self.points = 0
        self.initButtons()
    def initButtons(self):
        self.buttons.add("Start",a.Button(150,190,20,START[0],START[1]))
        self.buttons.add("Setting",a.Button(150, 255,20,SETTING[0],SETTING[1]))
        self.buttons.add("Quit",a.Button(150, 320,20,QUIT[0],QUIT[1]))
    def update(self):
        self.buttons.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.buttons.findButton("Quit").isCLICK():
                pygame.quit()
                sys.exit()
            elif self.buttons.findButton("Start").isCLICK():
                select = Select.SelectCharacter(BG_select,self.screen,self.windowStack)
                self.windowStack.append(select)
    def getState(self):
        return self.state
    def draw(self):
        self.screen.blit(self.background,(0,0))
        self.buttons.draw(self.screen)
    def run(self):
        self.update()
        self.draw()
        pygame.display.update()
