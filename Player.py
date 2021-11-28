import random

import pygame
import os
COLLISION = 1
ISALIVE = 2
DEAD = 3
SHOOTING = 4
class Bullet:
    def __init__(self, speed, bulletList, screen, x,y, type=0,inc = 0):
        self.speed = speed
        self.screen = screen
        self.type = type
        self.bulletList = bulletList
        self.bullet = self.bulletList[type]
        self.position = self.bullet.get_rect()
        self.position.x = x
        self.position.y = y
        self.state = ISALIVE
        self.damage = 1
        self.inc = inc
        self.stable = random.choice([-1,1])
        self.hp = 10
        if self.type == 2:
            self.stable *= -1
            self.hp = 30
        elif self.type == 0:
            self.damage = 2
    def isCollision(self, enemy):
        if self.position.colliderect(enemy):
            self.hp -= 10
            self.state = COLLISION
            enemy.isCollision(self.damage)
    def onCircle(self):
        pass
    def isDead(self):
        return (self.hp <= 0 or self.position.x >= 1100 or self.position.x <= 0)
    def update(self):
        if self.state == COLLISION and self.type == 2:
            self.position.y += 10*self.stable
        elif self.type == 1:
            self.position.y += self.inc
        self.position.x += (5*self.speed)
    def draw(self):
        self.screen.blit(self.bullet,(self.position))
class Player():
    BULLET = [pygame.image.load(os.path.join("Assets/Player", "Rocket_Bullet_3.png")),
              pygame.image.load(os.path.join("Assets/Player", "Rocket_Bullet.png")),
              pygame.image.load(os.path.join("Assets/Player", "Rocket_Bullet_2.png"))]
    def __init__(self,screen,characterList,type):
        self.count = 0
        self.type = type
        self.characterList = characterList # a surface
        self.character = self.characterList[type]
        self.position = self.character.get_rect()
        self.position.x = 50
        self.position.y = 380
        self.hp = 50
        self.state = ISALIVE
        self.screen = screen
        self.bullet = []
        if self.type == 1:
            self.limit = 18
        else:
            self.limit = 10
        self.userInput = pygame.key.get_pressed()
        self.speed = 0
        self.inc = 1
    def getState(self):
        return self.state
    def getPosition(self):
        return self.position
    def getBullet(self):
        return self.bullet
    def alive(self):
        self.state = ISALIVE
    def isAlive(self):
        return self.state == ISALIVE
    def isDead(self):
        return self.hp < 0
    def heal(self):
        self.hp += 10
    def isCollision(self,enemy = None):
        if enemy != None and self.position.colliderect(enemy.getRect()):
            self.state = COLLISION
            enemy.isCollision()
        return self.state == COLLISION
    def shoot(self):
        self.state = SHOOTING
        rect_x = self.position.x + self.character.get_width()//2
        rect_y = self.position.y + self.character.get_height() // 2
        if len(self.bullet) < self.limit:
            self.bullet.append(Bullet(self.speed,self.BULLET,self.screen,rect_x,rect_y,self.type))
            if self.type == 1:
                self.bullet.append(Bullet(self.speed, self.BULLET, self.screen, rect_x, rect_y + 4, self.type,5))
                self.bullet.append(Bullet(self.speed, self.BULLET, self.screen, rect_x, rect_y - 4, self.type,-5))
    def updateSpeedGame(self,speed,inc):
        self.userInput = pygame.key.get_pressed()
        self.speed = speed
        self.inc = inc
    def updatePosition(self):
        if self.userInput[pygame.K_s] and self.position.y <550:
            self.position.y += 4* self.speed *self.inc
        elif self.userInput[pygame.K_w] and self.position.y > -50:
            self.position.y -=4 * self.speed *self.inc
        elif self.userInput[pygame.K_d] and self.position.x <1100:
            self.position.x += 4 * self.speed * self.inc
        elif self.userInput[pygame.K_a] and self.position.x > -50:
            self.position.x -= 4 * self.speed * self.inc
    def updateState(self):
        if self.state == COLLISION:
            self.hp -= 10
            self.state = ISALIVE
        elif self.state == SHOOTING:
            self.state = ISALIVE
        if self.isDead():
            self.state = DEAD
    def updateBullet(self):
        for i in self.bullet:
            if i.isDead():
                self.bullet.remove(i)
            i.update()
    def update(self):
        if self.inc != 0:
            self.updateBullet()
        self.updatePosition()
        self.updateState()
    def draw(self):
        for i in self.bullet:
            i.draw()
        self.screen.blit(self.character, (self.position.x, self.position.y))
        