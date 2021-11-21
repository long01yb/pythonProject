import pygame
import random
from threading import Thread
class ObstacleList: #manage obtacle
    def __init__(self):
        self.obstacles = []
        self.total = 0
        self.speed =0
        self.inc = 1
    def add(self, obstacle):
        self.total += 1
        self.obstacles.append(obstacle)
    def isEmpty(self):
        return self.total == 0
    def canGen(self):
        return self.total <= 2
    def updateSpeed(self,speed,inc):
        self.speed = speed
        self.inc = inc
    def updateCollision(self,player):
        bullets = player.getBullet()
        for obs in self.obstacles:
            if self.total == 0:
                break
            player.isCollision(obs)
            for bullet in bullets:
                if obs.isDead():
                    break
                bullet.isCollision(obs)
    def update(self):    #update with player too
        for obs in self.obstacles:
            obs.update(self.speed*self.inc)
            if obs.getX() <= 0 or obs.isDead():
                self.obstacles.remove(obs)
                self.total -= 1
    def draw(self):
        for obs in self.obstacles:
            obs.draw() #
class Obstacle: # things make noise
    def __init__(self,screen, image,type = 0):
        self.screen = screen
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = 1200
        self.inc = 1
        self.hp = 20
    def isCollision(self,damage = 1):
        self.hp -= 10*damage
    def isDead(self):
        return self.hp <= 0
    def update(self,speed):
        self.rect.x -= 4*speed
    def draw(self):
        self.screen.blit(self.image[self.type], self.rect)
    def getRect(self):
        return self.rect
    def getX(self):
        return self.rect.x
    def getWidth(self):
        return self.rect.width
class EnemyPlane(Obstacle):
    def __init__(self,screen,image,type = 0):
        super().__init__(screen,image,type)
        rand = random.choice([100,150,200,250,300,350,400,450,500,550,600])
        self.rect.y = rand
        rand2 = random.choice([1200,1300,1400])
        self.rect.x = rand2
class BulletEnemy(Obstacle):
    def __init__(self,screen,image,position,type = 0):
        super().__init__(screen,image,type)
        rect_x = position.x + self.image[type].get_width()//2
        rect_y = position.y + self.image[type].get_height() // 2
        self.rect.x = rect_x
        self.rect.y = rect_y
    def update(self,speed):
        self.rect.x -= 5*speed

class RockBig(Obstacle):
    def __init__(self,screen,image,type = 0):
        super().__init__(screen,image,type)
        self.rect.y = random.randint(50,550)
        if (self.rect.y >= 300):
            self.stable = random.choice([-1,-2,-3])
        else:
            self.stable = random.choice([1,2,3])
        rand2 = random.randint(1100,1200)
        self.rect.x = rand2
        rand3 = random.choice([210,260,300,350,500])
        self.hp = rand3

    def update(self,speed):
        if self.rect.y >= 600 or self.rect.y <= 0:
            self.stable *= -1
        self.rect.x -= (speed+1)*self.inc
        self.rect.y += self.stable*self.inc
class RockSmall(Obstacle):
    def __init__(self,screen,image,type = 0):
        super().__init__(screen,image,type)
        if self.type >= 5:
            self.hp = 40
        rand = random.randint(-150,-30)
        self.rect.y = rand
        rand2 = random.randint(500,1100)
        if rand2 % 4 != 1:
            self.rect.x = rand2
        else:
            self.rect.x = rand2 - 400
    def isDead(self):
        return (self.hp <= 0 or self.rect.y >= 600)
    def update(self,speed):
        if self.type >= 5:
            speed -= 2
        self.rect.x -= (speed*2)*self.inc
        self.rect.y += speed*3*self.inc
