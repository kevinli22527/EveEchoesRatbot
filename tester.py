import pyautogui
import time
from playsound import playsound
import threading
from utilFunctions import *
lock_region = (1108, 12, 500, 120)
menu_region = (1413, 0, 506, 1070)
scroll_here = (1754, 500)
rat_region = (1351, 400, 300, 300)
local_region = (0, 839, 200, 100)
open_space = (587, 382)
hotbar_region = (1165, 778, 754, 301)
middle_region = (300, 300, 1200, 650)
right_half = (960, 0, 959, 1079)
left_half = (0, 0, 959, 1079)

while True:
    try:
        print(pyautogui.position())
        print(pyautogui.screenshot().getpixel(pyautogui.position()))
        time.sleep(0.1)
    except IndexError:
        time.sleep(1)
