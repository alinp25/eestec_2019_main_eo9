import socketio
import sys
import json
import requests
import time
import random

IP = 'http://10.81.176.52/'
P1_KEY = 'rt1n0qwaaxydy5ok'
P2_KEY = 'lxtfpcnocvc0xuf0'

socketPlayer = socketio.Client()
socketPlayer.connect(IP + 'command')

class Scorpio:
    secretKey = ""
    commands = {}
    direction = "left"
    useOfFire = -1
    prag = 80

    def __init__(self, key):
        self.secretKey = key
        self.getStartDirection()

    def addKey(self, body, condition):
        return {body: condition}

    def sendCmd(self, socket, cmd, condition, timeout = 0.4):
        jsonToSend = {'key':self.secretKey, 'commands': self.addKey(cmd, condition)}
        print(str(jsonToSend))
        socket.emit('command', jsonToSend)
        time.sleep(timeout)

    def getStartDirection(self):
        uri = IP + 'get_status'
        r = requests.post(uri, json={'key': self.secretKey})
        res = r.json()
        if res['player'] == 'p1':
            self.direction = 'left'
        else:
            self.direction = 'right'
    
    

    def printData(self):
        print(self.secretKey)
        print(str(self.commands))

    def get_anti_direction(self, direction):
        if (direction == "left"):
            return "right"
        return "left"

    def block_random(self, socket):
        rnd = random.randint(1, 4)
        if rnd == 1:
            self.sendCmd(socket, "down", True, 0.09)
            self.sendCmd(socket, "block", True, 0.8)
            self.sendCmd(socket, "block", False, 0.09)
            self.sendCmd(socket, "down", False, 0.09)
        elif rnd == 2:
            self.sendCmd(socket, self.direction, True, 0.09)
            self.sendCmd(socket, "up", True, 0.1)
            self.sendCmd(socket, self.direction, True, 0.09)
            self.sendCmd(socket, "up", False, 0.09)
        elif rnd == 3:
            self.sendCmd(socket, "block", True, 0.8)
            self.sendCmd(socket, "block", False, 0.09)

    def teleport(self, socket, direction):
        self.useOfFire = 1
        self.sendCmd(socket, "down", True, 0.09)
        self.sendCmd(socket, "down", False, 0.09)
        self.sendCmd(socket, direction, True, 0.09)
        self.sendCmd(socket, "front_kick", True, 0.09)
        self.sendCmd(socket, direction, False, 0.09)
        self.sendCmd(socket, "front_kick", False, 0.3)
        self.useOfFire = -1
        self.direction = self.get_anti_direction(self.direction)

    def spear(self, socket, direction):
        antiDirection = self.get_anti_direction(direction)
        self.sendCmd(socket, direction, True, 0.09)
        self.sendCmd(socket, direction, False, 0.09)
        self.sendCmd(socket, antiDirection, True, 0.09)
        self.sendCmd(socket, "front_punch", True, 0.09)
        self.sendCmd(socket, antiDirection, False, 0.09)
        self.sendCmd(socket, "front_punch", False, 1.4)

    def takedown(self, socket, direction):
        antiDirection = self.get_anti_direction(direction)
        self.sendCmd(socket, antiDirection, True, 0.09)
        self.sendCmd(socket, antiDirection, False, 0.09)
        self.sendCmd(socket, direction, True, 0.09)
        self.sendCmd(socket, "back_kick", True, 0.09)
        self.sendCmd(socket, direction, False, 0.09)
        self.sendCmd(socket, "back_kick", False, 0.4)

    def combo_teleport_spear_takedown(self, socket, direction):
        antiDirection = self.get_anti_direction(direction)
        self.teleport(socket, direction)
        # time.sleep(0.1)
        self.spear(socket, antiDirection)
        # time.sleep(0.1)
        self.takedown(socket, antiDirection)
        time.sleep(0.1)

    def shin_strike(self, socket, direction):
        antiDirection = self.get_anti_direction(direction)
        self.sendCmd(socket, antiDirection, True, 0.09)
        self.sendCmd(socket, "front_kick", True, 0.09)
        self.sendCmd(socket, antiDirection, False, 0.09)
        self.sendCmd(socket, "front_kick", False, 0.09)

    def get_over_here(self, socket, direction):
        antiDirection = self.get_anti_direction(direction)
        self.sendCmd(socket, "left", True, 0.09)
        self.sendCmd(socket, "left", False, 0.1)
        self.sendCmd(socket, "right", True, 0.09)
        self.sendCmd(socket, "front_punch", True, 0.09)
        self.sendCmd(socket, "block", True, 0.09)
        self.sendCmd(socket, "right", False, 0.09)
        self.sendCmd(socket, "front_punch", False, 0.09)
        self.sendCmd(socket, "block", False, 0.09)
        self.sendCmd(socket, "block", True, 0.09)
        self.sendCmd(socket, "block", False, 0.09)

    def eternal_flame(self, socket, direction):
        antiDirection = self.get_anti_direction(direction)
        self.sendCmd(socket, "back_punch", True, 0.09)
        self.sendCmd(socket, "back_punch", False, 0.09)
        self.sendCmd(socket, "front_punch", True, 0.09)
        self.sendCmd(socket, "front_punch", False, 0.11)

    def judgemental_day(self, socket, direction):
        antiDirection = self.get_anti_direction(direction)
        self.sendCmd(socket, direction, True, 0.09)
        self.sendCmd(socket, "front_kick", True, 0.09)
        self.sendCmd(socket, "front_kick", False, 0.09)
        self.sendCmd(socket, direction, False, 0.11)
        self.sendCmd(socket, "back_punch", True, 0.09)
        self.sendCmd(socket, "back_punch", False, 0.09)

    def cataclysm(self, socket, direction):
        antiDirection = self.get_anti_direction(direction)
        self.sendCmd(socket, antiDirection, True, 0.09)
        self.sendCmd(socket, "back_kick", True, 0.09)
        self.sendCmd(socket, antiDirection, False, 0.09)
        self.sendCmd(socket, "back_kick", False, 0.09)
        self.sendCmd(socket, "back_punch", True, 0.09)
        self.sendCmd(socket, "back_punch", False, 0.09)

    def dead_end(self, socket, direction):
        antiDirection = self.get_anti_direction(direction)
        self.sendCmd(socket, "back_punch", True, 0.09)
        self.sendCmd(socket, "back_punch", False, 0.09)
        self.sendCmd(socket, "front_punch", True, 0.09)
        self.sendCmd(socket, "front_punch", False, 0.09)
        self.sendCmd(socket, "back_punch", True, 0.09)
        self.sendCmd(socket, "back_punch", False, 0.09)

    def distance_combo(self, socket, direction):
        antiDirection = self.get_anti_direction(self.direction)
        self.get_over_here(socket, direction)
        self.dead_end(socket, direction)
        self.takedown(socket, direction)

    def play(self, socket):
        while(True):
        # if fire == True:
        #     if self.useOfFire != 1:
        #     #     continue
        #     # else:
        #         self.sendCmd(socket, self.get_anti_direction(self.direction), True, 0.09)
        #         self.sendCmd(socket, self.get_anti_direction(self.direction), False, 0.09)
        #         self.direction = self.get_anti_direction(self.direction)
            self.combo_teleport_spear_takedown(socket, "left")
            self.combo_teleport_spear_takedown(socket, "right")
            self.combo_teleport_spear_takedown(socket, "left")
            self.combo_teleport_spear_takedown(socket, "right")
        # distance = 1150
        # if distance < self.prag: # Apropiere
        #     randomCombo = random.randint(1, 8)
        #     if randomCombo == 1:
        #         self.takedown(socket, self.direction)
        #     elif randomCombo == 2:
        #         self.shin_strike(socket, self.direction)
        #     elif randomCombo == 3:
        #         self.combo_teleport_spear_takedown(socket, self.direction)
        #     elif randomCombo == 4:
        #         self.eternal_flame(socket, self.direction)
        #     elif randomCombo == 5:
        #         self.judgemental_day(socket, self.direction)
        #     elif randomCombo == 6:
        #         self.cataclysm(socket, self.direction)
        #     elif randomCombo == 7:
        #         self.dead_end(socket, self.direction)
        # else: # Departare
        #     randomCombo = random.randint(1, 4)
        #     if randomCombo == 1:
        #         self.combo_teleport_spear_takedown(socket, self.direction)
        #     elif randomCombo == 2:
        #         self.get_over_here(socket, self.direction)
        #     elif randomCombo == 3:
        #         self.distance_combo(socket, self.direction)

scorpion = Scorpio(P1_KEY)
scorpion.play(socketPlayer)