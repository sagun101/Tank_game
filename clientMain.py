import pygame as pg
from setting import *
import pickle
from utilites import *
import os
import time as ti


enemy = {}
ally = {}
time = None
playerId = -1
player = None
bullet = None
bullets = None
team = 0
state = 1


def setVal(data):
    global ally,enemy,playerId, player, time, state, bullet, bullets
    ally = data[0]
    enemy = data[1]
    playerId = data[2]
    player = ally[playerId]
    #print("clientin", player.destroy)
    time = data[3]
    state = data[4]
    bullets = data[5]
    bullet = bullets[playerId]

def getVal():
    global player, bullet
    return (player, bullet)




def main(conn):
    global ally,enemy,playerId, player, time, state, bullet, bullets
    dir_path = os.path.dirname(os.path.realpath(__file__))
    #print(conn)
    TRACK = 0
    left = False
    right = False
    aim = False
    stop = False
    fire = False
    exit = False
    pg.init()
    clock = pg.time.Clock()
    window = pg.display.set_mode((WIDTH,HEIGHT))
    pg.display.set_caption(TITLE)
    screen = pg.Rect(0,0,WIDTH,HEIGHT)
    ground = pg.image.load(r'{}\assets\ground.png'.format(dir_path))
    brick = pg.image.load(r'{}\assets\brick.png'.format(dir_path))
    brick_collider = pg.Rect(int(WIDTH/2 - 30),int(HEIGHT - 265),60,240)
    fireButton = [pg.image.load(r'{}\assets\fire.png'.format(dir_path))]
    fireButton.append(pg.image.load(r'{}\assets\ready.png'.format(dir_path)))
    fireButton.append(pg.image.load(r'{}\assets\locked.png'.format(dir_path)))
    while exit == False:
        if TRACK != 0:
            data = pickle.loads(conn.recv(2048))   
            setVal(data)
            #print(data)
       
        #global ally,enemy,playerId, player
        #print(ally,enemy)
        dt = clock.tick(FPS)/1000.0
        #print(ally.keys(), enemy.keys())
        
        for i in ally.keys():
            ally[i].hull = r'{}\assets\ally.png'.format(dir_path)
            ally[i].tur = r'{}\assets\allyTur.png'.format(dir_path)
                #print("ally",ally[i].tur, ally[i].hull)
        #print("1",player.destroy)
        player.hull = r'{}\assets\hull.png'.format(dir_path)
        player.tur = r'{}\assets\turret.png'.format(dir_path)
        
        for i in enemy.keys():
            #print("enmey set")
            enemy[i].hull = r'{}\assets\enemy.png'.format(dir_path)
            enemy[i].tur = r'{}\assets\enemyTur.png'.format(dir_path)
        
            #print("enemy",enemy[i].tur, enemy[i].hull)
        
        mouse = pg.math.Vector2(pg.mouse.get_pos())
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
                #pg.quit()
                #quit
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    left = True
                if event.key == pg.K_RIGHT:
                    right = True
                    
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    left = False
                if event.key == pg.K_RIGHT:
                    right = False
                    
            key = pg.mouse.get_pressed()
            if key[0] == True:
                box = fireButton[0].get_rect(center = (WIDTH/2,HEIGHT - 35))
                if box.collidepoint(mouse.x,mouse.y):
                    if player.fire == False:
                        player.fire = True
                        fire = True
                    else:
                        player.fire = False
                        fire = False
                elif aim == False:
                    aim = True
                    bulTime = dt
                    global bulTimme
            elif aim == True:
                aim = False
                    
    
    
        window.fill(SKYBLUE)
        
        window.blit(ground,(0,int(HEIGHT - 110)))
        
        for i in range(4):
            window.blit(brick,(int((WIDTH/2)-30),int(HEIGHT -90-60*(i+1))))
        if state == 1:
            font(window,time,WIDTH/2,HEIGHT/2,80)
            fire = False
        elif state == 2:
            font(window,time,WIDTH/2,30)
            #print("3",player.destroy)
            if fire == False and player.destroy == False:
                #print("4",player.destroy)
                if aim == True:
                    
                    player.cannon(window,mouse,bulTime)
                if left == True:
                    if player.box.colliderect(brick_collider) or player.box.left < screen.left:
                        player.move(dt,1.5)
                    else:
                        player.move(dt,-1)
                
                elif right == True:
                    if player.box.colliderect(brick_collider) or player.box.right > screen.right:
                        player.move(dt,-1.5)
                    else:
                        player.move(dt,1)
        
        elif state == 3:
            font(window,time,WIDTH/2,HEIGHT/2,80)
        elif state == 4:
            print("doing stuff")
            if bullet != None:  
                print("doing stuff")
                bullet.update(dt)
                bullet.draw(window)
                
            for i in bullets.keys():
               temp = bullets[i]
               if temp != None:
                   temp.draw(window)
            #collision detection
            if bullet != None:
                if bullet.outScreen(screen):
                    print("out screen")
                if bullet.hit(brick_collider):
                    print("wall")
                if bullet.hit(ground.get_rect(x =0, y = int(HEIGHT - 80))):
                    print("ground")
                
                for i in ally.keys(): #check player bullet
                    if bullet.hit(ally[i].box):
                        print("hit ",ally[i].name)
                    if bullets[i] != None and player.gotHit(bullets[i].box):
                        print("hit by",ally[i].name)
                    
                for i in enemy.keys():
                    if bullet.hit(enemy[i].box):
                        print("hit ",enemy[i].name)
                    if bullets[i] != None and player.gotHit(bullets[i].box):
                        print("hit by",enemy[i].name)
        elif state == 5:
            font(window,time,WIDTH/2,HEIGHT/2,80)
            ti.sleep(60)
            exit == True
            return 1
        elif state == 6:
            font(window,time,WIDTH/2,HEIGHT/2,80)
            fire = False
                    
        if state == 2 and fire == False:
            window.blit(fireButton[0],(int(WIDTH/2 - 72),int(HEIGHT -65)))
        elif state == 2 and fire == True:
            window.blit(fireButton[1],(int(WIDTH/2 - 72),int(HEIGHT -65)))
        else:
            window.blit(fireButton[2],(int(WIDTH/2 - 72),int(HEIGHT -65)))
        
        for i in ally.keys():
            if i == playerId:
                player.draw(window)
            else:
                ally[i].draw(window)
        for i in enemy.keys():
            enemy[i].draw(window)
        
        TRACK = 1
        #print("clientSend", player.destroy)
        conn.send(pickle.dumps(getVal()))
        pg.display.update()
           
    