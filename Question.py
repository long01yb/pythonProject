import pygame
import os

from Tab import Tab
import button as a
QUESTION = [pygame.image.load(os.path.join("Assets/Other", "Question.png"))]
ANSWER = [pygame.image.load(os.path.join("Assets/Other", "AnswerIdle.png")),
          pygame.image.load(os.path.join("Assets/Other", "AnswerHover.png")),
          pygame.image.load(os.path.join("Assets/Other", "Question_AC.png")),
          pygame.image.load(os.path.join("Assets/Other", "Question_WA.png"))]
listQA = []
f = open("QA.txt")
for data in f:
    listQA.append(data.split("-"))
f.close()

class Question(Tab):
    QUESTION = ["","Ans1","Ans2","Ans3","Ans4"]
    ANS_TRUE = 2
    ANS_FALSE = 4
    QUIT = 3
    def initButtons(self):
        self.buttonlist.add("Ques", a.Button(200 + 40, 200,10,QUESTION[0],QUESTION[0],listQA[self.index][0]))
        self.buttonlist.add(self.QUESTION[1], a.Button(240 , 340,10,ANSWER[0],ANSWER[1],listQA[self.index][1]))
        self.buttonlist.add(self.QUESTION[2], a.Button(600 - 70, 340,10,ANSWER[0],ANSWER[1],listQA[self.index][2]))
        self.buttonlist.add(self.QUESTION[3], a.Button(240 , 420,10,ANSWER[0],ANSWER[1],listQA[self.index][3]))
        self.buttonlist.add(self.QUESTION[4], a.Button(600 - 70, 420,10,ANSWER[0],ANSWER[1],listQA[self.index][4]))
    def __init__(self, screen,background):
        super().__init__(screen,background)
        self.index = 0
        self.initButtons()
        self.CorrectAnswerindex =  int(listQA[self.index][5])
        self.buttonAC = self.buttonlist.findButton(self.QUESTION[self.CorrectAnswerindex])
        self.buttonWA = None
        self.clock = pygame.time.Clock()
    def refresh(self):
        if self.index == len(listQA) - 1:
            self.index = -1
        self.index += 1
        self.state = self.THINKING
        self.CorrectAnswerindex =  int(listQA[self.index][5])
        self.buttonAC = self.buttonlist.findButton(self.QUESTION[self.CorrectAnswerindex])
    def isTHINKING(self):
        return self.state == self.THINKING
    def isTrue(self):
        return self.state == self.ANS_TRUE
    def updateContent(self):
        self.buttonlist.findButton("Ques").changeContent(listQA[self.index][0])
        self.buttonlist.findButton(self.QUESTION[1]).changeContent(listQA[self.index][1])
        self.buttonlist.findButton(self.QUESTION[2]).changeContent(listQA[self.index][2])
        self.buttonlist.findButton(self.QUESTION[3]).changeContent(listQA[self.index][3])
        self.buttonlist.findButton(self.QUESTION[4]).changeContent(listQA[self.index][4])
    def update(self):
        self.buttonlist.update()
        if self.buttonAC.isCLICK():
            self.state = self.ANS_TRUE
        for i in range(1, 5):
            buttonx = self.buttonlist.findButton(self.QUESTION[i])
            if buttonx.isCLICK() and buttonx != self.buttonAC:
                self.buttonWA = buttonx
                self.state = self.ANS_FALSE
    def getAnswer(self):
            if self.state == self.ANS_TRUE:
                self.buttonAC.drawAnswer(self.screen,ANSWER[2])
            elif self.state == self.ANS_FALSE:
                self.buttonAC.drawAnswer(self.screen,ANSWER[2])
                self.buttonWA.drawAnswer(self.screen,ANSWER[3])
            if self.state != self.THINKING:
                pygame.time.delay(500)
            pygame.display.update()
    def draw(self):
        self.screen.blit(self.background,(200,160))
        self.buttonlist.draw(self.screen)
    def run(self):
        self.update()
        self.getAnswer()
        self.draw()