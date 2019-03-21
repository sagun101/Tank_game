# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:16:09 2019

@author: jrbin
"""

import socket
import threading
import time
import pickle
import utilites
import setting
import tank

address = {}
SERVERIP = None


exitFlag = 0
exitGame = 0
waitFlag = 0

READY = 1

STATE = 1
CLOCK = ""
clockTime = 5

players = 0
playerCons = {}
playerName = {}
playerReady = {}
playerDead = {}

team1 = {}
team2 = {}



class connectThread(threading.Thread):
    def __init__(self, threadID, conn):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.conn = conn
    
    def run(self):
        print("Establishing Connection")
        connectingThread(self.conn, self.threadID)
        #print("Disconnected from client")

class listeningThread(threading.Thread):
    def __init__(self, threadID, sock):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.sock = sock
    
    def run(self):
        print("Listing for players...")
        listenThread(self.sock)
        print("No longer making new connections")
    
class Server(object):
    def __init__(self):
        global SERVERIP
        host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(host_name)
        print("Host IP: {}".format(self.host_ip))
        SERVERIP = self.host_ip
        self.port = 6666
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host_ip, self.port))
        self.listThread = listeningThread(0, self.sock)
        self.listThread.start()
        
    def getIP(self):
        return self.host_ip

class clockThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        clockCount()

def clockCount():
    global clockTime, playerReady
    global STATE, READY
    counting = clockTime
    while counting > 0:
        time.sleep(1)
        clockTime -= 1
        counting -= 1
    clockTime = "Start!"
    time.sleep(1.5)
    STATE = 2
    clockTime = 30
    counting = clockTime
    while counting != 0:
        time.sleep(1)
        clockTime -= 1
        counting -= 1
        temp = READY
        for i in playerReady.keys():
            temp *= playerReady[i]
        if temp:
            break
    clockTime = "TIME!"
    time.sleep(1.5)
    STATE = 3
    clockTime = "FIRE!"
    time.sleep(1)
    STATE = 4
    clockTime = ""
    time.sleep(5)
    
    allNone = 1
    while True:
        
        for i in playerName.keys():
            if i in team1:
                if team1[i].bullet != None:
                    allNone *= 0
            else:
                if team2[i].bullet != None:
                    allNone *= 0
        if allNone == 1:
            break
        else:
            allNone = 1
        
    x = 1
    for T in team1.keys():
        x *= playerDead[T]
        playerReady[T] = 0
    y = 1
    for T in team2.keys():
        y *= playerDead[T]
        playerReady[T] = 0
        
    if x == 1 and y == 1:
        STATE = 5
        clockTime = "DRAW!"
        time.sleep(1.5)
    elif x == 1 and y != 1:
        STATE = 5
        clockTime = "Team 2 Wins!"
        time.sleep(1.5)
    elif x != 1 and y == 1:
        STATE = 5
        clockTime = "Team 1 Wins!"
        time.sleep(1.5)
    elif x != 1 and y != 1:
        STATE = 6
        clockTime = "Next Round!"
        time.sleep(1.5)
        STATE = 1
        clockTime = 5
        clockCount()
    
    
    
def setUpThread():
    global CLOCK
    global playerReady
    global waitFlag
    global team1, team2
    for F in playerName.keys():
        playerDead[F] = 0
    for F in playerName.keys():
        playerReady[F] = 0
    team1, team2 = utilites.shuffle(playerName)
    for F in team1.keys():
        team1[F] = tank.Tank(playerName[F], utilites.teamSide(0), -110 + setting.HEIGHT, -1)
    for F in team2.keys():
        team2[F] = tank.Tank(playerName[F], utilites.teamSide(1), -110 + setting.HEIGHT, 1)
    CLOCK = clockThread()
    time.sleep(5)
    CLOCK.start()
    
        

def listenThread(sock):
    global address
    global players
    global playerCons
    global playerName
    while not exitFlag:
        sock.listen(100)
        conn, addr = sock.accept()
        players += 1
        address[players] = conn
        temp = conn.recv(1024)
        playerName[players] = temp.decode()
        print("{} is player number {}".format(playerName[players], players))
        newPlayer = connectThread(players, conn)
        newPlayer.start()
        playerCons[players] = newPlayer
        
def shutdownConn(play):
    global players
    con = address[play]
    con.shutdown(socket.SHUT_RDWR)
    con.close()
    del playerCons[play]
    del playerName[play]
    
    
def connectingThread(conn, player):
    while not exitFlag:
        try:
            conn.send(pickle.dumps((playerName, players, SERVERIP)))
            time.sleep(.5)
        except:
            shutdownConn(player)
            return
    conn.send(pickle.dumps("end"))
    time.sleep(.5)
    while not exitGame:
        #print("sending set")
        #print(clockTime, STATE)
        if player in team1:
            conn.send(pickle.dumps((team1, team2, player, clockTime, STATE, playerName[player])))
        else:
            conn.send(pickle.dumps((team2, team1, player, clockTime, STATE, playerName[player])))
        
        dataRecv = conn.recv(2048)
        try:
            dataRecv = pickle.loads(dataRecv)
        except:
            print(dataRecv)
        
        if not dataRecv.destroy:
            if dataRecv.fire:
                playerReady[player] = 1
                if player in team1:
                    team1[player] = dataRecv.shoot()
                    dataRecv.fire = False
                else:                                
                    team2[player] = dataRecv.shoot()
                    dataRecv.fire = False
            if player in team1:
                team1[player] = dataRecv
            else:                                #stores it
                team2[player] = dataRecv
        else:
            playerReady[player] = True
            if player in team1:
                playerDead[player] = 1
            else:                                
                playerDead[player] = 1
            
    #send to next thread fun


    
    
    
    
