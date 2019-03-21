import tkinter as tk
import server
from network import Network
import threading
import time
import pickle
import clientMain
import setting

exit = 0
gameExit = 0

THREADS = []

class TankGame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.count = tk.StringVar()
        self.player = tk.StringVar()
        self.hostName = tk.StringVar()
        self.nameStr = tk.StringVar()
        self.serverStr = tk.StringVar()
        self.serverIPStr = tk.StringVar()
        for F in (TitlePage, MainPage, PageHost, PageJoin, PageInstruct, PageControls, PageLobby, PageCLobby):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("TitlePage")
        
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        
class TitlePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        empty1 = tk.Label(self, text = "")
        empty1.grid(row = 0, column = 0)
        empty2 = tk.Label(self, text = "")
        empty2.grid(column = 3, row = 0)
        empty3 = tk.Label(self, text = "")
        empty3.grid(row = 0, column = 3)
        empty4 = tk.Label(self, text = "")
        empty4.grid(column = 3, row = 3)
        instructBut = tk.Button(self, text = "Instructions", command = lambda: controller.show_frame("PageInstruct"))
        controlBut = tk.Button(self, text = "Controls", command = lambda: controller.show_frame("PageControls"))
        controlBut.grid(row = 2, column = 1)
        instructBut.grid(row = 3, column = 1)
        playButton = tk.Button(self, text = "Play!", command = lambda: controller.show_frame("MainPage"))
        playButton.grid(row = 1, column = 1)

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        hostButton = tk.Button(self, text = "Host",command = lambda: controller.show_frame("PageHost"))
        joinButton = tk.Button(self, text = "Join",command = lambda: controller.show_frame("PageJoin"))
        joinButton.grid(row = 0,column = 0)
        hostButton.grid(row = 0, column = 1)

class PageInstruct(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        instructLabel = tk.Label(self, text = setting.INSTRUCTIONS)
        instructLabel.grid(row = 0, column = 0)
        backButton = tk.Button(self, text = "Back", command = lambda: controller.show_frame("MainPage"))
        backButton.grid(row = 1, column = 0)
        
class PageControls(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controlLabel = tk.Label(self, text = setting.CONTROLS)
        controlLabel.grid(row = 0, column = 0)
        backButton = tk.Button(self, text = "Back", command = lambda: controller.show_frame("MainPage"))
        backButton.grid(row = 1, column = 0)
        
class PageHost(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text = "Please put username below")
        label.grid(row = 0, column = 0)
        name = tk.Entry(self, textvariable = controller.hostName)
        name.grid(row = 1, column = 0)
        BackButton = tk.Button(self, text = "Back", command = lambda: controller.show_frame("MainPage"))
        BackButton.grid(row = 2, column = 1)
        StartHost = tk.Button(self, text = "Start Server", command = lambda: self.waitForName())
        StartHost.grid(row = 2, column = 0)
        
        
    def waitForName(self):
        host(self.controller.hostName, self.controller.player, self.controller.count, self.controller.serverIPStr)
        self.controller.show_frame("PageLobby")
    
class PageLobby(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.serverIPStr.set("Waiting for Address")
        controller.count.set("0")
        serverIP = tk.Label(self, textvariable = controller.serverIPStr)
        countLbl = tk.Label(self,textvariable= controller.count)
        playerLbl = tk.Label(self,text="Players")
        playerEntry = tk.Label(self,textvariable= controller.player)
        serverIP.grid(row = 1, column = 1)
        playerLbl.grid(column = 0, row = 0)
        countLbl.grid(row = 0,column = 1)
        playerEntry.grid(row = 1,column = 0)
        start = tk.Button(self, text = "Start",command = lambda: startingGame())  #start game from here
        start.grid(row=3,column =0)

class PageJoin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        nameLbl = tk.Label(self,text="Name")
        serverLbl = tk.Label(self,text ="Server Id")
        name = tk.Entry(self,textvariable = controller.nameStr)
        server = tk.Entry(self,textvariable = controller.serverStr)
        nameLbl.grid(row = 0, column =0)
        serverLbl.grid(row = 1, column = 0)
        name.grid(row = 0,column = 1)
        server.grid(row = 1,column = 1)
        backButton = tk.Button(self, text = "Back", command = lambda: controller.show_frame("MainPage"))
        backButton.grid(row = 3, column = 1)
        connect = tk.Button(self, text = "Connect", command = lambda: self.waitFor())
        connect.grid(row=3,column=0)
    
    def waitFor(self):
        connectToLobby(self.controller.serverStr.get(), self.controller.nameStr.get(), self.controller.player, self.controller.count, self.controller.serverIPStr)
        self.controller.show_frame("PageCLobby")
        
class PageCLobby(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.serverIPStr.set("Waiting for Address")
        controller.count.set("0")
        serverIP = tk.Label(self, textvariable = controller.serverIPStr)
        serverIP.grid(row = 1, column = 1)
        countLbl = tk.Label(self, textvariable = controller.count)
        playerLbl = tk.Label(self, text = "Players")
        playerEntry = tk.Label(self, textvariable = controller.player)
        playerLbl.grid(column =0, row =0)
        countLbl.grid(row=0,column =1)
        playerEntry.grid(row=1,column=0)

class lobbyThread(threading.Thread):
    def __init__(self, conn, player, count, serverIp):
        threading.Thread.__init__(self)
        self.player = player
        self.count = count
        self.conn = conn
        self.server = serverIp
        
    def run(self):
        print("Starting Lobby")
        lobbyThreader(self.conn, self.player, self.count, self.server)

class setUpThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        server.setUpThread()

def startingGame():
    global THREADS
    print("Starting game")
    server.exitFlag = 1
    setIt = setUpThread()
    THREADS.append(setIt)
    setIt.start()
    
    #start the pygame and add in the players in lobby

def host(hostName, player, count, serverIp):
    global THREADS
    ser = server.Server()
    net = Network(ser.getIP(), hostName.get())
    temp = net.getSocket()
    lobby = lobbyThread(temp, player, count, serverIp)
    THREADS.append(lobby)
    lobby.start()
    
    
def connectToLobby(serverIP, name, player, count, server):
    global THREADS
    net = Network(serverIP, name)
    conn = net.getSocket()
    cLob = lobbyThread(conn, player, count, server)
    THREADS.append(cLob)
    cLob.start()
       
def lobbyThreader(conn, player, count, serverIP):
    global exit, gameExit, THREADS
    print("entering lobby thread")
    while not exit:
        #receiveData
        temp = pickle.loads(conn.recv(1024))
        if temp == "end":
            exit = 1
        else:
            player.set(temp[0])
            count.set(temp[1])
            serverIP.set(temp[2])
            #conn.send(pickle.dumps(time.time))
            time.sleep(.5)
            #stop lobby cycle after this while
    print("setting up client")
    data = pickle.loads(conn.recv(2048)) #receives data from server
    clientMain.setVal(data)#set data from server
    #time.sleep(.5)
    #conn.send(pickle.dumps(clientMain.getVal())) #sends data from game
    time.sleep(.5)
    #print(conn)
    clientMain.main(conn)
    print("gameover")    
            
def killThreads():
    global THREADS
    for i in THREADS:
        print("thread death")
        THREADS[i].join()
    program.destroy()
    
if __name__ == "__main__":
    program = TankGame()
    #program.protocol("WM_DELETE_WINDOW", killThreads)
    program.mainloop()