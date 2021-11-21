class Communicate:
    QUIT = 1
    PLAYING = 2
    def __init__(self):
        self.state = self.PLAYING
        self.running = True
        self.inc = 1
        self.scroll = 0
        self.point = 0
        self.speed = 0
        self.collision = False
    def getInc(self):
        return self.inc
    def quit(self):
        self.state = self.QUIT
    def isQuit(self):
        return self.state == self.QUIT
    def stop(self):
        self.inc = 0
        return self.inc
    def continue_game(self):
        self.inc = 1
        return self.inc
    def get_inc(self):
        return self.inc
    def updateInfomation(self,scroll,point,speed):
        self.scroll = scroll
        self.speed = speed
        self.point = point
    def getPoint(self):
        return self.point
    def getScoll(self):
        return self.scroll
    def isStop(self):
        return self.inc == 0
    def isRunning(self):
        return self.running
    def setRunning(self,boolean):
        self.running = boolean
    def isCollision(self):
        return self.collision
    def setCollision(self,collision):
        self.collision = collision
        