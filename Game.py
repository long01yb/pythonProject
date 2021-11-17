import random
import threading
import pygame
import os
import ManageAnimation
from Comunication import Communicate
from Window import  Window
import Player
import Obtacles
from Question import  Question
PLANE_ENEMY = [pygame.image.load(os.path.join("Assets/Obtacle", "Rocket_Enemy.png")),
                pygame.image.load(os.path.join("Assets/Obtacle", "Enemy.png"))]
BULLET = [pygame.image.load(os.path.join("Assets/Dino", "Bullet.png"))]
BULLET_ENEMY = [pygame.image.load(os.path.join("Assets/Obtacle", "Bullet_enemy.png"))]
class Game(Window):
    COLLISION = 10
    def __init__(self,background,screen,windowStack,state,Player_sprite):
        super().__init__(background,screen,windowStack,state)
        self.talk_to_player = Communicate()
        self.speed = 4
        self.player = Player.Dinosaur(self.screen,Player_sprite)
        self.obtacleList = Obtacles.ObtacleList()
        BG_ques = pygame.image.load(os.path.join("Assets/Other", "Question_BG.png"))
        self.ques = Question(self.screen,BG_ques)
        self.locked = threading.Lock()
        self.animations = ManageAnimation.Animation(
            self.background,self.screen,
            self.player,self.obtacleList,
            self.talk_to_player,self.locked,
            self.ques
        )
        self.fps = 30
        self.points = 0
        self.userInput = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()
        self.scroll = 0
        self.inc = 1
    def initButtons(self):
        # add button of game here
        pass
    def isQUIT(self):
        return self.state == self.QUIT
    def updateState(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or self.player.isDead():
                self.state = self.QUIT
                self.talk_to_player.setRunning(False)
                self.windowStack.pop()
        IOinput = pygame.key.get_pressed()
        if self.state != self.COLLISION and IOinput[pygame.K_SPACE]:
            if self.state == self.STOP:
                self.state = self.PLAYING
                self.talk_to_player.continue_game()
            else:
                self.state = self.STOP
                self.inc = self.talk_to_player.stop()
        if self.state == self.PLAYING and self.player.isCollision():
            self.state = self.COLLISION
            self.talk_to_player.setCollision(True)
            self.talk_to_player.stop()
        if self.state == self.COLLISION and not self.talk_to_player.isCollision():
            self.state = self.PLAYING
    def generateObtacle(self):
        if self.obtacleList.isEmpty():
            for x in range(self.speed // 2):
                obs = Obtacles.EnemyPlane(self.screen,PLANE_ENEMY)
                self.obtacleList.add(obs)
                rand = random.choice([1, 2])
                if rand == 1:
                    self.obtacleList.add(Obtacles.BulletEnemy(self.screen, BULLET_ENEMY,obs.getRect() ))
    def updateInfomation(self):
        if pygame.mouse.get_pressed()[0]:
            self.player.shoot(self.speed,BULLET,self.screen)
        self.inc = self.talk_to_player.getInc()
        if self.points % 200 == 0:
            self.speed += self.inc
        self.userInput = pygame.key.get_pressed()
        self.player.updateSpeedGame(self.speed,self.inc)
        self.obtacleList.updateSpeed(self.speed,self.inc)
        self.points += self.inc
        self.scroll += self.inc*4
        self.talk_to_player.updateInfomation(self.scroll,self.points,self.speed)
    def runThread(self):
        self.animations.start()
    def run(self):
            self.updateState()
            self.updateInfomation()
            self.clock.tick(30)
            pygame.display.update()
            self.generateObtacle()

