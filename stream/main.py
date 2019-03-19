import cv2, sys
import math
import socketio
import requests

# from "../commands/Scorpio.py" import *
# from commands import *

from utils import printTimeDiff, initTimeDiff
from client import startListening, curFrame, frameFragments
import numpy as np
import numpy.core.multiarray
import imutils
flag = 1
last_dist = 49.0



IP = 'http://10.81.176.52/'
P1_KEY = 'rt1n0qwaaxydy5ok'
P2_KEY = 'lxtfpcnocvc0xuf0'



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

    def play(self, socket, dist, fire):
        # while(True):
        if fire == True:
            if self.useOfFire != 1:
                self.sendCmd(socket, self.get_anti_direction(self.direction), True, 0.09)
                self.sendCmd(socket, self.get_anti_direction(self.direction), False, 0.09)
                self.direction = self.get_anti_direction(self.direction)
                # continue
            # else:

        distance = dist
        if distance < self.prag: # Apropiere
            randomCombo = random.randint(1, 8)
            if randomCombo == 1:
                self.takedown(socket, self.direction)
            elif randomCombo == 2:
                self.shin_strike(socket, self.direction)
            elif randomCombo == 3:
                self.combo_teleport_spear_takedown(socket, self.direction)
            elif randomCombo == 4:
                self.eternal_flame(socket, self.direction)
            elif randomCombo == 5:
                self.judgemental_day(socket, self.direction)
            elif randomCombo == 6:
                self.cataclysm(socket, self.direction)
            elif randomCombo == 7:
                self.dead_end(socket, self.direction)
        else: # Departare
            randomCombo = random.randint(1, 4)
            if randomCombo == 1:
                self.combo_teleport_spear_takedown(socket, self.direction)
            elif randomCombo == 2:
                self.get_over_here(socket, self.direction)
            elif randomCombo == 3:
                self.distance_combo(socket, self.direction)



socketPlayer = socketio.Client()
socketPlayer.connect(IP + 'command')

scorpio = Scorpio(P1_KEY)


def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(w), int(h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)

def run_until(frame):
    global scorpio
    global socketPlayer
    scorpio.play(socketPlayer, get_distance(frame), get_fire(frame))
    

def get_fire(img):
    frame = img
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    avg_color_per_row = np.average(res, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)

    if avg_color[0] > 4.7:
        return True

    return False

def get_distance(frame):
    global last_dist
    ret1 = sub_zero(frame)
    ret2 = example(frame)

    if ret1 is None or ret2 is None:
        return last_dist

    [x1, y1] = ret1
    [x2, y2] = ret2
    last_dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 )
    return last_dist

def sub_zero(img): 
    frame = img
    upper_blue = np.array([85, 125, 170])
    lower_blue = np.array([60, 100, 155])
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    mask = cv2.inRange(frame, lower_blue, upper_blue)



    res = cv2.bitwise_and(frame, frame, mask=mask)
    res2 = cv2.cvtColor(res,cv2.COLOR_HSV2BGR)
    res2 = cv2.cvtColor(res2,cv2.COLOR_BGR2GRAY)
    th3 = cv2.adaptiveThreshold(res2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,4)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
    th3 = cv2.erode(th3, kernel)

# tibi is trying to hack
    #check collision if it is to little then 
    if 1 == 1: 
        th3 = cv2.GaussianBlur(th3, (11, 11), 1)
        th3 = cv2.erode(th3, kernel)
        th3 = cv2.erode(th3, kernel)
        contours,hierarchy = cv2.findContours(th3,1, 3)
        
        cnt = []
        x = []
        y = []
        w = []
        h = []

        for j in range(len(contours)):
            cnt.append(contours[j])
            _x,_y,_w,_h = cv2.boundingRect(cnt[j])
            x.append(_x)
            y.append(_y)
            w.append(_w)
            h.append(_h)

        lst_abs = []


        for i in range(len(x)):
            for j in range(len(x)):
                lst_abs.append((i, j, abs(x[i] - x[j]) + abs(y[i] - y[j]), abs(w[i] - w[j]) + abs(h[i] - h[j])))

        sorted_by_second = sorted(lst_abs, key=lambda tup: tup[2])
        ls = sorted_by_second
        


        box = []

        for i in range(1,3):
            if (len(sorted_by_second) < i):
                return
            box.append((img[y[sorted_by_second[len(sorted_by_second) - i][0]] :
                            abs(y[sorted_by_second[len(sorted_by_second) - i][0]] + h[sorted_by_second[len(sorted_by_second) - i][0]]),
                            x[sorted_by_second[len(sorted_by_second) - i][0]] :
                            abs(x[sorted_by_second[len(sorted_by_second) - i][0]] + w[sorted_by_second[len(sorted_by_second) - i][0]])],
                            x[sorted_by_second[len(sorted_by_second) - i][0]],
                            y[sorted_by_second[len(sorted_by_second) - i][0]],
                            w[sorted_by_second[len(sorted_by_second) - i][0]],
                            h[sorted_by_second[len(sorted_by_second) - i][0]]
                            ))


        avg_arr = []

        for i in range(len(box)):
            avg_color_per_row = np.average(box[i][0], axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            avg_arr.append((sum(avg_color), box[i][1], box[i][2], box[i][3], box[i][4]))

        sorted_by_second = sorted(avg_arr, key=lambda tup: tup[0])


#the second one is the good one
        #cv2.rectangle(img,(sorted_by_second[0][1] , sorted_by_second[0][2]), (sorted_by_second[0][1] + sorted_by_second[0][3], sorted_by_second[0][2]+sorted_by_second[0][4]),(0,255,255),2)
        cv2.rectangle(img,(sorted_by_second[1][1] , sorted_by_second[1][2]), (sorted_by_second[1][1] + sorted_by_second[1][3], sorted_by_second[1][2]+sorted_by_second[1][4]),(255,255,0),2)
        return [sorted_by_second[1][1], sorted_by_second[1][2]]


def example(frame):
    #frame = frame[50 : 270, 0 : 800]
   ############ combo fire
   # upper_blue1 = np.array([85, 125, 170])
   # lower_blue1 = np.array([60, 100, 155])

    #lower_blue = np.array([110,50,50])
    #upper_blue = np.array([130,255,255])

    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #mask = cv2.inRange(hsv, lower_blue, upper_blue)
    #res = cv2.bitwise_and(frame,frame, mask= mask)

    #cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #avg_color_per_row = np.average(res, axis=0)
    #avg_color = np.average(avg_color_per_row, axis=0)

    #if avg_color[0] > 4.7:
    #    print("FOC")




    global flag
    img = frame

    get_fire(img)



    upper_blue1 = np.array([51, 84, 121])
    lower_blue1 = np.array([38, 70, 91])


    lower_blue = np.array([104, 64, 39])
    upper_blue = np.array([125, 75, 65])
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    mask = cv2.inRange(frame, lower_blue, upper_blue)



    res = cv2.bitwise_and(frame, frame, mask=mask)
    res2 = cv2.cvtColor(res,cv2.COLOR_HSV2BGR)
    res2 = cv2.cvtColor(res2,cv2.COLOR_BGR2GRAY)
    th3 = cv2.adaptiveThreshold(res2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,4)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
    th3 = cv2.erode(th3, kernel)

    #cv2.imshow('final1', th3)
    # tibi is trying to hack
    #check collision if it is to little then 
    if 1 == 1: 
        th3 = cv2.GaussianBlur(th3, (11, 11), 1)
        th3 = cv2.erode(th3, kernel)
        th3 = cv2.erode(th3, kernel)
        contours,hierarchy = cv2.findContours(th3,1, 3)
        
        cnt = []
        x = []
        y = []
        w = []
        h = []

        for j in range(len(contours)):
            cnt.append(contours[j])
            _x,_y,_w,_h = cv2.boundingRect(cnt[j])
            if (_w < 30 or _h < 30):
                continue
            if (_x < 1):
                continue
            x.append(_x)
            y.append(_y)
            w.append(_w)
            h.append(_h)

        lst_abs = []


        for i in range(len(x)):
            for j in range(len(x)):
                lst_abs.append((i, j, abs(x[i] - x[j]) + abs(y[i] - y[j]), abs(w[i] - w[j]) + abs(h[i] - h[j])))

        sorted_by_second = sorted(lst_abs, key=lambda tup: tup[2])
        ls = sorted_by_second


        box = []

        for i in range(1,3):
            box.append((img[y[sorted_by_second[len(sorted_by_second) - i][0]] :
                            abs(y[sorted_by_second[len(sorted_by_second) - i][0]] + h[sorted_by_second[len(sorted_by_second) - i][0]]),
                            x[sorted_by_second[len(sorted_by_second) - i][0]] :
                            abs(x[sorted_by_second[len(sorted_by_second) - i][0]] + w[sorted_by_second[len(sorted_by_second) - i][0]])],
                            x[sorted_by_second[len(sorted_by_second) - i][0]],
                            y[sorted_by_second[len(sorted_by_second) - i][0]],
                            w[sorted_by_second[len(sorted_by_second) - i][0]],
                            h[sorted_by_second[len(sorted_by_second) - i][0]]
                            ))


        avg_arr = []

        for i in range(len(box)):
            avg_color_per_row = np.average(box[i][0], axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            avg_arr.append((sum(avg_color), box[i][1], box[i][2], box[i][3], box[i][4]))

        sorted_by_second = sorted(avg_arr, key=lambda tup: tup[0])


#        cv2.rectangle(img,(sorted_by_second[0][1] , sorted_by_second[0][2]), (sorted_by_second[0][1] + sorted_by_second[0][3], sorted_by_second[0][2]+sorted_by_second[0][4]),(0,255,0),2)
        cv2.rectangle(img,(sorted_by_second[1][1] , sorted_by_second[1][2]), (sorted_by_second[1][1] + sorted_by_second[1][3], sorted_by_second[1][2]+sorted_by_second[1][4]),(255,0,0),2)





    mask = cv2.inRange(frame, lower_blue1, upper_blue1)



    res = cv2.bitwise_and(frame, frame, mask=mask)
    res2 = cv2.cvtColor(res,cv2.COLOR_HSV2BGR)
    res2 = cv2.cvtColor(res2,cv2.COLOR_BGR2GRAY)
    th3 = cv2.GaussianBlur(res2, (11, 11), 1)
    th3 = cv2.adaptiveThreshold(th3,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,4)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
    th3 = cv2.erode(th3, kernel)


    cv2.imshow('pizda', frame)

    cv2.waitKey(1)
    return [sorted_by_second[1][1], sorted_by_second[1][2]]


UDP_IP = "0.0.0.0"
UDP_PORT = 64012
if (len(sys.argv) > 1):
    UDP_PORT = int(sys.argv[1])
startListening(UDP_IP, UDP_PORT, run_until)

