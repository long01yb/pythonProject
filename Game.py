import random
import sys
import threading
import pygame
import os
import ManageAnimation
from Comunication import Communicate
from Window import  Window
import Player
import Obstacles
from Question import  Question
PLANE_ENEMY = [pygame.image.load(os.path.join("Assets/Obtacle", "Rocket_Enemy.png")),
                pygame.image.load(os.path.join("Assets/Obtacle", "Enemy2.png"))]
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
        pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_4_Small.png")),
             pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_5_Medium.png")),
             pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_1_Medium.png")),
             pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_2_Medium.png")),
             pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_3_Medium.png")),
             pygame.image.load(os.path.join("Assets/Obtacle/Rock", "Rock_4_Medium.png"))
             ]
class Game(Window):
    COLLISION = 10
    def __init__(self,background,screen,windowStack,state,Player_sprite,type = 0):
        super().__init__(background,screen,windowStack,state)
        self.talk_to_player = Communicate()
        self.speed = 4
        self.player = Player.Player(self.screen,Player_sprite,type)
        self.obstaclelist = Obstacles.ObstacleList()
        BG_ques = pygame.image.load(os.path.join("Assets/Other", "Question_BG.png"))
        self.ques = Question(self.screen,BG_ques)
        self.locked = threading.Lock()
        self.animations = ManageAnimation.Animation(
            self.background,self.screen,
            self.player,self.obstaclelist,
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
        IOinput = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.talk_to_player.quit()
                pygame.quit()
                sys.exit()
            elif self.player.isDead() or IOinput[pygame.K_BACKSPACE]:
                self.talk_to_player.setRunning(False)
                self.windowStack.pop()
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
        if t%3 == 0 and self.obstaclelist.canGen():
            rand = random.choice([0,1])
            obs = Obstacles.EnemyPlane(self.screen, PLANE_ENEMY,rand)
            self.obstaclelist.add(obs)
            rand = random.choice([1, 2])
            if rand == 1:
                self.obstaclelist.add(Obstacles.BulletEnemy(self.screen, BULLET_ENEMY, obs.getRect()))
        elif t%3 == 1 and self.obstaclelist.canGen():
            obs = Obstacles.RockBig(self.screen, ROCKBIG, rand1%5)
            self.obstaclelist.add(obs)
        elif t%3 == 2 and self.obstaclelist.canGen() :
            obs = Obstacles.RockSmall(self.screen, ROCKSMALL, rand1%10)
            self.obstaclelist.add(obs)


    def updateInfomation(self):
        IOinput = pygame.key.get_pressed()
        if IOinput[pygame.K_0]:
            self.player.shoot()
        self.inc = self.talk_to_player.getInc()
        if self.points % 450 == 0:
            self.speed += self.inc
        self.userInput = pygame.key.get_pressed()
        self.player.updateSpeedGame(self.speed,self.inc)
        self.obstaclelist.updateSpeed(self.speed,self.inc)
        self.points += self.inc
        self.scroll += self.inc*3
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
            self.obstaclelist.updateCollision(self.player)
            self.updateState()
            self.updateInfomation()
            self.clock.tick(40)
            pygame.display.update()
