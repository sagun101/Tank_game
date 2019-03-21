import pygame
from setting import *
from math import *
import random
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
def font(window,text,x,y,size = 20,color = (0,0,0)):
    global dir_path
    font = pygame.font.Font(r'{}\assets\codeman38_press-start-2p\PressStart2P.ttf'.format(dir_path),size)
    textSurf = font.render(str(text),True,color)
    textRect = textSurf.get_rect()
    textRect.center = (x,y)
    window.blit(textSurf,textRect)

def vecAngle(a,b):
    dot = sum(i*j for i,j in zip(a,b))
    magA = sqrt(sum(i*i for i in a))
    magB = sqrt(sum(i*i for i in b))
    ang = degrees(acos(dot/(magA*magB)))
    if a.x < 0:
        return (360 - ang)
    else:    
        return ang
def magnitude(a,b):
    return sqrt(sum((j - i)**2 for i,j in zip(a,b)))


def rotate(image, pivot, offset, angle =0):
    rotated_img = pygame.transform.rotozoom(image,-angle,1)
    rotated_offset =- offset.rotate(angle)
    rect = rotated_img.get_rect(center = pivot + rotated_offset)
    return rotated_img, rect

def scale(value,istart,iend,ostart,oend):
        return (ostart + (oend - ostart)*((value - istart)/(iend - istart)))
    
    
def teamSide(num):
    if num ==0:
        return random.randint(0,(WIDTH/2) -51)
    else:
        return random.randint((WIDTH/2) +45,WIDTH -51)
    
def shuffle(dictionary):
    team1 = {}
    team2 ={}
    for i in dictionary.keys():
        if i % 2 == 0:
            team1[i] = dictionary[i]
        else:
            team2[i] = dictionary[i]
    return team1,team2
        