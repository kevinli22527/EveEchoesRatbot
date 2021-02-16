import pyautogui
from playsound import playsound
from globals import *

import time
import random
DEFAULT_WAIT_TIME = 0.4

lock_region = (1108, 12, 500, 120)
menu_region = (1413, 0, 500, 1070)
scroll_here = (1754, 500)
ship_status = (639, 809, 600, 270)
rat_region = (1351, 400, 300, 300)
local_region = (0, 839, 200, 100)
middle_region = (300, 300, 1200, 650)
open_space = (587, 382)
hotbar_region = (1165, 778, 754, 301)
right_half = (960, 0, 959, 1079)
left_half = (0, 0, 959, 1079)


def move_to_and_click(loc, duration=0.5):
    """
    Moves the mouse to loc in the given duration and clicks.
    The moving happens immediately after function call.
    """
    pyautogui.moveTo(loc, duration=duration, tween=pyautogui.easeOutQuad)
    pyautogui.click(loc)


def is_docked():
    ss = pyautogui.locateCenterOnScreen('UndockButton.png', confidence=0.98)
    if ss:
        return True
    else:
        return False


def get_into_eye_view():
    found = pyautogui.locateCenterOnScreen('navBar.png', confidence=0.95)
    if found:
        print("Already in eye view.")
    else:
        eye = pyautogui.locateCenterOnScreen('eye.png', confidence=0.9)
        move_to_and_click(eye)
        print("Opened eye view.")
        time.sleep(DEFAULT_WAIT_TIME)


def get_out_of_eye_view():
    found = pyautogui.locateCenterOnScreen('navBar.png', confidence=0.9)
    if found:
        eye = pyautogui.locateCenterOnScreen('eye.png', confidence=0.9)
        move_to_and_click(eye)
        print('closed eye view')
        time.sleep(DEFAULT_WAIT_TIME)
    else:
        print('Already not in eye view')


def click_nav_bar():
    tries = 3
    while tries:
        found = pyautogui.locateCenterOnScreen('navBar.png', confidence=0.98, region=menu_region)
        if found:
            x, y = found
            x -= 50  # offset a little bit
            move_to_and_click((x, y))
            print("Clicked on the nav bar.")
            time.sleep(DEFAULT_WAIT_TIME)
            break
        else:
            print(f"Couldn't find the nav bar. Trying {tries-1}")
        tries -= 1
        time.sleep(0.5)


def click_cosmic_anomaly():
    tries = 3
    while tries:
        found = pyautogui.locateOnScreen('cosmicAnomaly.png', confidence=0.9)
        if found:
            move_to_and_click(found)
            print("Clicked on cosmic anomaly tab.")
            time.sleep(DEFAULT_WAIT_TIME)
            break
        else:
            print(f"Couldln't find cosmic anomaly tab. Trying {tries-1}")
        tries -= 1
        time.sleep(0.3)


def click_celestial_body():
    tries = 3
    while tries:
        found = pyautogui.locateCenterOnScreen('celestialBody.png', confidence=0.9)
        if found:
            move_to_and_click(found)
            print("Clicked on celestial body.")
            time.sleep(DEFAULT_WAIT_TIME)
            break
        else:
            print(f"Couldn't find celestial body. Trying {tries-1} more times")
        tries -= 1
        time.sleep(0.5)


def click_suitable_anomaly(attempts=10):

    while attempts > 0:
        number = random.randint(0, 2)
        found = 0
        point_list = []

        if number == 0:
            found = pyautogui.locateAllOnScreen('guristasSmallAnom.png', confidence=0.97, region=menu_region)
        elif number == 1:
            found = pyautogui.locateAllOnScreen('guristasMedAnom.png', confidence=0.97, region=menu_region)
        elif number == 2:
            found = pyautogui.locateAllOnScreen('guristasLargeAnom.png', confidence=0.97, region=menu_region)

        for entry in found:
            point_list.append(entry)

        if len(point_list) == 0:
            print(f"Couldn't find suitable anomaly, trying {attempts} more time(s)")
            attempts -= 1
        else:
            random_index = random.randint(0, len(point_list) - 1)
            selected_point = point_list[random_index]
            move_to_and_click(selected_point)
            time.sleep(DEFAULT_WAIT_TIME)
            return True
    return False


def warp_random_planet(attempts=10):
    global recently_jumped_planet_coords
    point_list = []

    while attempts > 0:
        found = pyautogui.locateAllOnScreen('planetSymbol.png', confidence=0.98, region=menu_region)
        for entry in found:
            point_list.append(entry)
        if len(point_list) == 0:
            print(f"Couldn't find suitable planet, trying {attempts} more time(s)")
            attempts -= 1
        else:
            random_index = random.randint(0, len(point_list) - 1)
            location = point_list[random_index]
            selected_point = box_to_point(location)
            if recently_jumped_planet_coords:
                if not is_different(recently_jumped_planet_coords, selected_point):
                    attempts -= 1
                    continue
            move_to_and_click(selected_point)
            recently_jumped_planet_coords = selected_point
            time.sleep(0.3)
            warp = pyautogui.locateCenterOnScreen("Warp.png", confidence=0.95)
            warpX, warpY = warp
            pyautogui.moveTo(warp, duration=0.5, tween=pyautogui.easeOutQuad)
            pyautogui.mouseDown()
            time.sleep(1)
            pyautogui.moveTo(warpX - 600, warpY, duration=0.3, tween=pyautogui.easeOutQuad)
            pyautogui.mouseUp()
            return True
    return False


def are_coords_different(point1, point2):
    """
    determines whether 2 coordinates are different
    """
    point1_x, point1_y = point1
    point2_x, point2_y = point2
    rank = abs(point2_x - point1_x + point2_y - point1_y)
    if rank > 40:
        return True
    else:
        return False


def is_alone():
    """
    returns whether the player is alone in local chat
    """
    if pyautogui.locateCenterOnScreen("alone.png", confidence=0.95, region=local_region):
        print("Nobody else detected in local")
        return True
    else:
        print("Others have been detected in local")
        return False


def execute_evasive_manuevers():
    """
    gets to the nearest planet
    """
    print("Executing evasive maneuvers")
    get_into_eye_view()
    click_nav_bar()
    click_celestial_body()
    warp_random_planet()
    playsound('evasive.mp3')
    current_time = 0
    while not (warp_is_done() and current_time > 15):
        time.sleep(1)
        print("Warp not done yet")
        current_time += 1
        print("Time since warp: " + str(current_time))


def flash_jump():
    """
    builds on the evasion jumping and simplifies it
    """
    time.sleep(DEFAULT_WAIT_TIME)
    warp_random_planet()
    playsound("flashjump.mp3")
    current_time = 0
    while not (warp_is_done() and current_time > 15):
        time.sleep(1)
        print("Warp not done yet")
        current_time += 1
        print("Time since warp: " + str(current_time))


def refresh_scroll():
    """
    If an unlockable object is obstructing the easy lock button, scroll to refresh
    """
    open_space_x, open_space_y = open_space
    pyautogui.moveTo(open_space_x, open_space_y)
    pyautogui.mouseDown()
    pyautogui.moveTo(open_space_x - 300, open_space_y + 300, duration=0.5, tween=pyautogui.easeOutQuad)
    pyautogui.mouseUp()
    time.sleep(DEFAULT_WAIT_TIME)


def cannot_lock_detected():
    """
    detects if the cannot lock symbol appears on the screen
    """
    if pyautogui.locateCenterOnScreen("cannotLock.png", confidence=0.95, region=middle_region):
        return True
    else:
        return False


def handle_cannot_lock():
    """
    checks for and handles the case in which an unlockable object is obstructing the screen
    """
    if cannot_lock_detected():
        print("Cannot lock detected, executing refresh scroll")
        refresh_scroll()
    else:
        return


def warp_is_done():
    little_speed = pyautogui.locateCenterOnScreen('littleSpeed.png', confidence=0.97, region=ship_status)
    little_speed_glitch = pyautogui.locateCenterOnScreen('littleSpeedGlitch.png', confidence=0.97, region=ship_status)
    if little_speed or little_speed_glitch:
        return True
    else:
        return False


def is_different(point1, point2, threshold=200):
    """
    Uses weighted sum in order to determine if two points are radically different
    """
    x1, y1 = point1
    x2, y2 = point2
    score = pow((y2 - y1), 2) + pow((x2 - x1), 2)
    if score >= threshold:
        return True
    else:
        return False


def box_to_point(box):
    x, y, width, height = box
    x += int(width / 2)
    y += int(width / 2)
    return x, y


def scan_for_special_anoms():
    """
    scans for special anoms provided that the cosmic anomaly tab is already open. Checks for scout, inquisitor, and deadspace(guristas)
    """
    inquistor = pyautogui.locateCenterOnScreen('inquisitorImage.png', confidence=0.93, region=menu_region)
    scout = pyautogui.locateCenterOnScreen('scoutImage.png', confidence=0.93, region=menu_region)
    deadspace = pyautogui.locateCenterOnScreen('deadspaceImage.png', confidence=0.93, region=menu_region)

    if inquistor:
        playsound('inquisitor.mp3')
    if scout:
        playsound('scout.mp3')
    if deadspace:
        playsound('deadspace.mp3')
