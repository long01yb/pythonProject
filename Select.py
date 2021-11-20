import sys

import pygame
import os

import button
from Game import Game
from Window import Window
BG1 = pygame.image.load(os.path.join("Assets/Other", "BG_Game.png"))
RUNNING = [pygame.image.load(os.path.join("Assets/Player", "Rocket_Player.png")),
           pygame.image.load(os.path.join("Assets/Player", "Rocket_Player2.png")),
           pygame.image.load(os.path.join("Assets/Player", "Rocket_Player3.png"))]
CHARACTER = [pygame.image.load(os.path.join("Assets/Player/ButtonRocket", "ButtonRocket_HLHover.png")),
          pygame.image.load(os.path.join("Assets/Player/ButtonRocket", "ButtonRocket_HLIdle.png")),
          pygame.image.load(os.path.join("Assets/Player/ButtonRocket", "ButtonRocket_HDHover.png")),
          pygame.image.load(os.path.join("Assets/Player/ButtonRocket", "ButtonRocket_HDIdle.png")),
             pygame.image.load(os.path.join("Assets/Player/ButtonRocket", "ButtonRocket_HAHover.png")),
             pygame.image.load(os.path.join("Assets/Player/ButtonRocket", "ButtonRocket_HAIdle.png"))]
class SelectCharacter(Window):
    ISANSWER = 20
    THINKING = 21
    def initButtons(self):
        self.buttons.add("character1",button.Button(100,100,30,CHARACTER[0],CHARACTER[1]))
        self.buttons.add("character2",button.Button(450,100,30,CHARACTER[2],CHARACTER[3]))
        self.buttons.add("character3",button.Button(800,100,30,CHARACTER[4],CHARACTER[5]))
    def __init__(self,background,screen,windowstack):
        super().__init__(background,screen,windowstack)
        self.initButtons()
        self.type = -1
        self.state = self.THINKING
    def isAnswer(self):
        return self.state == self.ISANSWER
    def getAnswer(self):
        return self.type
    def update(self):
        self.buttons.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.buttons.findButton("character1").isCLICK():
                self.type = 0
            elif self.buttons.findButton("character2").isCLICK():
                self.type = 1
            elif self.buttons.findButton("character3").isCLICK():
                self.type = 2
            if self.type != -1:
                self.state = self.PLAYING
                game = Game(BG1, self.screen, self.windowStack, self.state, RUNNING, self.type)
                game.runThread()
                self.windowStack.append(game)
    def draw(self):
        self.screen.blit(self.background,(0,0))
        self.buttons.draw(self.screen)
    def run(self):
        if self.state == self.PLAYING:
            self.windowStack.pop()
        self.update()
        self.draw()
        pygame.display.update()



