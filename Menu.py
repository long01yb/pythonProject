import pygame
import  os

import Select
from Window import  Window
from Game import  Game
import button as a
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "Rocket_Player.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png"))]

BG1 = pygame.image.load(os.path.join("Assets/Other", "BG_Game.png"))
START = [pygame.image.load(os.path.join("Assets/Other", "StartIdle.png")),
         pygame.image.load(os.path.join("Assets/Other", "StartHover.png"))]
SETTING = [pygame.image.load(os.path.join("Assets/Other", "SettingIdle.png")),
         pygame.image.load(os.path.join("Assets/Other", "SettingHover.png"))]
QUIT = [pygame.image.load(os.path.join("Assets/Other", "QuitIdle.png")),
         pygame.image.load(os.path.join("Assets/Other", "QuitHover.png"))]
BG_ques = pygame.image.load(os.path.join("Assets/Other", "Question_BG.png"))
class Menu(Window):
    SELECTING = 11
    def __init__(self,bg,screen,windowStack):
        super().__init__(bg,screen,windowStack)
        self.points = 0
        self.initButtons()

        self.selectCharacter = Select.SelectCharacter(self.background,self.screen)
    def initButtons(self):
        self.buttons.add("Start",a.Button(150,190,20,START[0],START[1]))
        self.buttons.add("Setting",a.Button(150, 255,20,SETTING[0],SETTING[1]))
        self.buttons.add("Quit",a.Button(150, 320,20,QUIT[0],QUIT[1]))
    def update(self):
        self.buttons.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.buttons.findButton("Quit").isCLICK():
                self.state = self.QUIT
                self.windowStack.pop()
            elif self.buttons.findButton("Start").isCLICK():
                self.state = self.SELECTING
    def getState(self):
        return self.state
    def draw(self):
        SCREEN.blit(self.background,(0,0))
        self.buttons.draw(self.screen)
    def select(self):
        self.selectCharacter.update()
        type = self.selectCharacter.getAnswer()
        self.selectCharacter.draw()
        if self.selectCharacter.isAnswer():
            pygame.time.delay(500)
            game = Game(BG1, self.screen, self.windowStack,
                        self.state, RUNNING,type)
            game.runThread()
            self.windowStack.append(game)
    def run(self):
        if self.state == self.SELECTING:
            self.select()
        else:
            self.update()
            self.draw()
        pygame.display.update()