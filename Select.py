import pygame
import os

import button
from Tab import Tab
import button as a

ANSWER = [pygame.image.load(os.path.join("Assets/Other", "AnswerIdle.png")),
          pygame.image.load(os.path.join("Assets/Other", "AnswerHover.png")),
          pygame.image.load(os.path.join("Assets/Other", "Question_AC.png")),
          pygame.image.load(os.path.join("Assets/Other", "Question_WA.png"))]
class SelectCharacter(Tab):
    def initButtons(self):
        self.buttonlist.add("character1",button.Button(100,100,30,ANSWER[0],ANSWER[1],"Black Knight"))
        self.buttonlist.add("character2",button.Button(250,100,30,ANSWER[0],ANSWER[1],"Sexy Pig"))
        self.buttonlist.add("character3",button.Button(350,100,30,ANSWER[0],ANSWER[1],"Maria Ozawa"))
    def __init__(self,background,screen):
        super().__init__(background,screen)
        self.initButtons()
        self.type = 0
        self.state = self.THINKING
    def isAnswer(self):
        return self.state == self.ISANSWER
    def getAnswer(self):
        return self.type
    def update(self):
        self.buttonlist.update()
        if self.buttonlist.findButton("character1").isCLICK():
            self.type = 0
            self.state = self.THINKING
        elif self.buttonlist.findButton("character2").isCLICK():
            self.type = 1
            self.state = self.THINKING
        elif self.buttonlist.findButton("character3").isCLICK():
            self.type = 1
            self.state = self.THINKING
    def draw(self):
        self.screen.blit(self.background,(0,0))
        self.buttonlist.draw(self.screen)


