import pygame
from utilites import *
gravity = pygame.math.Vector2(0,500)

class Bullet:
    def __init__(self,x,y, a, power = 0):
        self.pos = pygame.math.Vector2(x,y)
        self.angle = a
        self.vel = pygame.math.Vector2()
        self.vel.from_polar((power,self.angle))
        self.dmg = 25
        self.destroy = False
        self.player = None
        self.box = None
        
        
    def draw(self,window):
        color = (255,150,0)
        self.box = pygame.draw.circle(window,color,[int(self.pos.x),int(self.pos.y)],3)
        
    def update(self,dt):
        self.pos += self.vel * dt
        self.vel += gravity * dt
        
        
class Tank:
    def __init__(self,name,x,y, team):
        self.name = name
        self.hull = ""
        self.tur = ""
        self.team = team
        self.bullet = None
        self.pos = pygame.math.Vector2(x,y)
        self.pivot = pygame.math.Vector2(self.pos.x + 25,self.pos.y +4)
        self.vel = pygame.math.Vector2(60,0)
        self.hp = 100
        self.power = 0   #max660
        self.fire =False
        self.destroy = False
        self.mouse = None
        self.angle = -45 * team
        self.offset = pygame.math.Vector2(0,12)
        self.bullet = None
        self.shot = pygame.math.Vector2()
        self.box = None
        
        
    def draw(self,window):
        self.pivot = pygame.math.Vector2(self.pos.x + 25,self.pos.y +4)
        tur = pygame.image.load(self.tur)
        roto,rect = rotate(tur,self.pivot,self.offset,self.angle)
        self.shot.from_polar((23,self.angle - 90))
        self.shot = self.shot + self.pivot
        window.blit(roto,rect)
        hull = pygame.image.load(self.hull)
        self.box = hull.get_rect(x=self.pos.x,y=self.pos.y)
        font(window,str(self.name),self.pos.x + 25,self.pos.y - 15 ,10)
        window.blit(hull,(self.pos.x,self.pos.y))
        
    def cannon(self,window,mouse,dt):
        self.angle = vecAngle(mouse - self.pivot, -self.offset)
        self.power = magnitude(mouse,self.shot)
        if self.power < 1:
            self.power = 1
        if self.power > 200:
            self.power = 200
        self.power = scale(self.power,1,200,160,660)
        temPos = self.shot
        temVel = pygame.math.Vector2()
        temVel.from_polar((self.power,self.angle -90))
        for i in range(5):
            temPos += temVel * dt * 3
            temVel += gravity * dt * 3
            pygame.draw.circle(window,(0,0,0),[int(temPos.x),int(temPos.y)],2)
        
        
        
    def move(self,dt,x):
        self.pos += self.vel * dt * x
        
    def shoot(self):
        if self.fire == True:
            self.bullet = Bullet(self.shot.x,self.shot.y,self.angle-90, power = self.power)
        else:
            self.bullet = None
        
        
        
        
    
        
        
        
        
        
        