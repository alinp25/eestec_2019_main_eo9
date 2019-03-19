import socketio
import sys
import json
import requests
import time

IP = 'http://10.81.176.52/'
P1_KEY = 'rt1n0qwaaxydy5ok'
P2_KEY = 'lxtfpcnocvc0xuf0'

socketPlayer = socketio.Client()
socketPlayer.connect(IP + 'command')

class Player:
    secretKey = ""
    commands = {}

    def __init__(self, key):
        self.secretKey = key

    def addKey(self, body, condition):
        return {body: condition}

    def sendCmd(self, socket, cmd, condition, timeout = 0.4):
        jsonToSend = {'key':self.secretKey, 'commands': self.addKey(cmd, condition)}
        print(str(jsonToSend))
        socket.emit('command', jsonToSend)
        time.sleep(timeout)

    def printData(self):
        print(self.secretKey)
        print(str(self.commands))

    def play(self, socket):
        while(True):
            self.sendCmd(socket, "right", True)
            self.sendCmd(socket, "right", False)
            self.sendCmd(socket, "right", True)
            self.sendCmd(socket, "right", False)
            
            self.sendCmd(socket, "down", True, 0.250)
            self.sendCmd(socket, "front_kick", True, 0.250)
            self.sendCmd(socket, "front_kick", False)
            self.sendCmd(socket, "down", False)

            self.sendCmd(socket, "back_punch", True)
            self.sendCmd(socket, "back_punch", False)
            self.sendCmd(socket, "front_punch", True)
            self.sendCmd(socket, "front_punch", False)
            self.sendCmd(socket, "back_punch", True)
            self.sendCmd(socket, "back_punch", False)
            time.sleep(0.5)
        

Scorpio = Player(P1_KEY)
Scorpio.play(socketPlayer)
