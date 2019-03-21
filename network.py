# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 19:49:44 2019

@author: jrbin
"""

import socket


class Network(object):
    def __init__(self, host_ip, name):
        self.name = name
        self.host_ip = host_ip
        self.port = 6666
        self.addr = (self.host_ip, self.port)
        self.soc = socket.socket()
        self.soc.connect(self.addr)
        self.soc.send(self.name.encode())
        
    def getSocket(self):
        return self.soc