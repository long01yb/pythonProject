import random
import sys
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
ROCKBIG = [pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_5_Big.png")),
        pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_1_Big.png")),
        pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_2_Big.png")),
        pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_3_Big.png")),
        pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_4_Big.png"))]
ROCKSMALL = [pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_5_Small.png")),
        pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_1_Small.png")),
        pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_2_Small.png")),
        pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_3_Small.png")),
        pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_4_Small.png"))]
class Game(Window):
    COLLISION = 10
    def __init__(self,background,screen,windowStack,state,Player_sprite,type = 0):
        super().__init__(background,screen,windowStack,state)
        self.talk_to_player = Communicate()
        self.speed = 4
        self.player = Player.Dinosaur(self.screen,Player_sprite,type)
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
            if event.type == pygame.QUIT:
                self.talk_to_player.quit()
                pygame.quit()
                sys.exit()
            elif self.player.isDead():
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
        t = self.speed*89 + 34
        rand1 = random.randint(1,100)
        if t%3 == 0 and self.obtacleList.canGen():
            obs = Obtacles.EnemyPlane(self.screen, PLANE_ENEMY)
            self.obtacleList.add(obs)
            rand = random.choice([1, 2])
            if rand == 1:
                self.obtacleList.add(Obtacles.BulletEnemy(self.screen, BULLET_ENEMY, obs.getRect()))
        elif t%3 == 1 and self.obtacleList.canGen():
            obs = Obtacles.RockBig(self.screen, ROCKBIG, rand1%5)
            self.obtacleList.add(obs)
        elif t%3 == 2 and self.obtacleList.canGen() :
            obs = Obtacles.RockSmall(self.screen, ROCKSMALL, rand1%5)
            self.obtacleList.add(obs)


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
            if self.state == self.PLAYING:
                self.generateObtacle()
            elif self.state == self.PLAYING and self.player.isCollision():
                self.state = self.COLLISION
                self.talk_to_player.setCollision(True)
            elif self.state == self.COLLISION and not self.player.isCollision():
                self.state = self.PLAYING
            self.obtacleList.updateCollision(self.player)
            self.updateState()
            self.updateInfomation()
            self.clock.tick(40)
            pygame.display.update()

