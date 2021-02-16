from utilFunctions import *
from playsound import playsound
import pyautogui
import threading

"""
'Remy' bot used for ratting operations in EVE echoes. This is the program entry file. Remy is the rat from Ratatouille apparently
"""

IN_COMBAT = False
EASY_LOCK_COOLDOWN = 0
ARMOR_DMG_COOLDOWN = 0
LOCK = threading.Lock()
IGNORE_LOCAL_PRESENCE = False
ALERT_DISPLAYED = False
EVASION_MODE = False

FINISH_MESSAGE = ['finish.mp3', 'finish2.mp3']

previously_jumped_planet_coords = None

"""
def increment_time():
    LOCK.acquire()
    print("tick")
    global EASY_LOCK_COOLDOWN
    EASY_LOCK_COOLDOWN -= 1
    if EASY_LOCK_COOLDOWN == 0:
        print("Easy lock ready")
    LOCK.release()


timer = threading.Timer(1.0, increment_time)
timer.start()
"""

playsound("activate.mp3")

while True:
    get_out_of_eye_view()
    get_into_eye_view()
    click_nav_bar()
    click_cosmic_anomaly()
    scan_for_special_anoms()
    found_anomaly = click_suitable_anomaly()
    if not found_anomaly:
        execute_evasive_manuevers()
        raise Exception("Ran away to preserve the ship, no anomalies")
    # warp sequence-------------------------------------------------------------------------------------------------
    warp = pyautogui.locateCenterOnScreen('Warp.png', confidence=0.9)
    while not warp:
        click_suitable_anomaly()
        warp = pyautogui.locateCenterOnScreen('Warp.png', confidence=0.9)
        time.sleep(0.5)
    move_to_and_click(warp)

    print("warping to the anomaly")
    playsound('jump.mp3')
    time.sleep(6)
    current_time = 0
    while not (warp_is_done() and current_time > 15):
        time.sleep(1)
        print("Warp not done yet")
        current_time += 1
        print("Time since warp: " + str(current_time))
    # check for rats--------------------------------------------------------------------------------------------------
    print("warp done, checking for rats")
    time.sleep(2.5)
    enemies_present = True
    while enemies_present:
        EASY_LOCK_COOLDOWN -= 1  # prevents spam clicking of easy lock
        ARMOR_DMG_COOLDOWN -= 1  # prevents spam of armor damage audio
        if EASY_LOCK_COOLDOWN < 0:
            print("Easy lock ready")
            EASY_LOCK_COOLDOWN = 0

        if ARMOR_DMG_COOLDOWN < 0:
            ARMOR_DMG_COOLDOWN = 0

        easyLock = pyautogui.locateCenterOnScreen("easyLock.png", confidence=0.9, region=middle_region)
        if easyLock and EASY_LOCK_COOLDOWN == 0:
            move_to_and_click(easyLock)
            print("Locked on")
            EASY_LOCK_COOLDOWN = 2
        else:
            print("no lock button found")

        droneAmp = pyautogui.locateCenterOnScreen("droneDamageAmp.png", confidence=0.95, region=hotbar_region)
        if droneAmp:
            move_to_and_click(droneAmp)
            print("clicked on drone amp")
        else:
            print("Drone amp already active")

        droneX = pyautogui.locateCenterOnScreen("droneDamageAmpX.png", confidence=0.95, region=middle_region)
        if droneX:
            move_to_and_click(droneX)
            print("exited drone error")

        droneMalfunction = pyautogui.locateCenterOnScreen('droneMalfunction.png', confidence=0.93, region=hotbar_region)
        if droneMalfunction:
            print("Drone malfunction detected")
            pyautogui.moveTo(droneMalfunction)
            pyautogui.mouseDown()
            time.sleep(0.1)
            pyautogui.moveRel(0, -50, duration=0.3)
            droneReturn = pyautogui.locateCenterOnScreen('droneReturn.png', confidence=0.95, region=menu_region)
            pyautogui.moveTo(droneReturn, duration=0.3, tween=pyautogui.easeOutQuad)
            time.sleep(0.2)
            pyautogui.mouseUp()

        lowArmor = pyautogui.locateCenterOnScreen("lowHealth.png", confidence=0.95, region=ship_status)
        if lowArmor and ARMOR_DMG_COOLDOWN == 0:
            playsound("armorDmg.mp3")
            ARMOR_DMG_COOLDOWN = 5

        handle_cannot_lock()  # if obstruction happened while clicking easy lock

        if not is_alone():
            if not IGNORE_LOCAL_PRESENCE:
                playsound("warning.mp3")
                playsound("hostiles.mp3")
                if pyautogui.locateCenterOnScreen("scrambled.png", confidence=0.85, region=middle_region):
                    playsound('scrambled.mp3')
                    print("Scrambled, trying this another time")
                else:
                    EVASION_MODE = True
                    execute_evasive_manuevers()
                    while not is_alone():  # hide until strangers go away
                        print("Still strangers, jumping again")
                        flash_jump()
                    break
            else:
                print("Local presence ignored")

        tries = 4
        while tries > 0:
            print("checking for rats")
            if pyautogui.locateCenterOnScreen("ratsPresent.png", confidence=0.93, region=right_half):
                break
            else:
                tries -= 1
                print(f"no rats found, trying {tries} more times")
                time.sleep(1)
        if tries == 0:
            enemies_present = False
            print("Finished one anomaly")
        else:
            time.sleep(2)
            continue
    if not EVASION_MODE:
        playsound(random.choice(FINISH_MESSAGE))
    else:
        playsound('resume.mp3')
        EVASION_MODE = False
