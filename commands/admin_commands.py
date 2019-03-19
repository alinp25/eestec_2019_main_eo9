# import asyncio
import socketio
import sys
import json
import requests
import time

IP = 'http://10.81.176.51/'
ADMIN_KEY = 'rt1n0qwaaxydy5ok'

emitted = 0

jsonMenuAdmin = {
	"key": ADMIN_KEY,
	"type": "menu_command",
	"menu_key": "",
	"is_player_2": False,
}

socketMenu = socketio.Client()

def press_key_in_menu(key_to_press, isPlayer2): 
	socketMenu.connect(IP + 'admin')
	jsonMenuAdmin["menu_key"] = key_to_press
	jsonMenuAdmin["is_player_2"] = isPlayer2
	socketMenu.emit('admin', jsonMenuAdmin)
	time.sleep(0.8)
	socketMenu.disconnect()

def rematch():
	print("A")
	press_key_in_menu("enter", True)
	time.sleep(1)
	print("A")
	press_key_in_menu("enter", False)

# up down left right enter escape
if sys.argv[1] == "rematch":
	rematch()
else:
	press_key_in_menu(sys.argv[1], True)
# press_key_in_menu("up", False)
# press_key_in_menu("escape", False)
# press_key_in_menu("enter", False)
# press_key_in_menu("down", False)
# print("DA")
# time.sleep(1)
# print("DA")
# while (True):
# 	rematch()
# 	time.sleep(5)
