import sys
from threading import Thread
import pygame.display
class Animation(Thread):
    def __init__(self,background,screen,player,obtacleList,communicate,lock,ques):
        Thread.__init__(self)
        self.background = background
        self.screen = screen
        self.player = player
        self.obtacleList = obtacleList
        self.ques = ques
        self.communicate = communicate
        self.inc = self.communicate.getInc()
        self.clock = pygame.time.Clock()
        self.locked = lock
        self.test = 0
    def drawPoint(self):
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render("Points: " + str(self.communicate.getPoint()//4), True, (150, 50, 50))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        self.screen.blit(text, textRect)
    def draw(self):
        width = self.background.get_width()
        scroll = self.communicate.getScoll()
        for x in range(4):
            self.screen.blit(self.background, (width * x - scroll, 0))
        self.player.draw()
        self.obtacleList.draw()
        self.drawPoint()
    def run(self):
        while self.communicate.isRunning():
            if self.communicate.isQuit():
                break
            if self.communicate.isCollision():
                self.ques.run()
                if self.ques.isTrue():
                    self.player.heal()
                if not self.ques.isTHINKING():
                    self.ques.refresh()
                    self.ques.updateContent()
                    self.communicate.setCollision(False)
                    self.communicate.continue_game()
            self.obtacleList.update()
            self.player.update()

            if not self.communicate.isCollision():
                self.draw()
            self.clock.tick(40)
            pygame.display.update()