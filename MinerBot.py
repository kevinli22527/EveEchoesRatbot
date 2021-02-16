import pyautogui
import time
DEFAULT_WAIT_TIME = 0.4


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


def perform_undock():
    if is_docked():
        move_to_and_click(undock)
        while not pyautogui.locateCenterOnScreen('eye.png', confidence=0.9, region=menu_region):
            time.sleep(1.5)
        print("Performed an undock.")
        time.sleep(2.5)
    else:
        print("Already undocked.")


def get_into_eye_view():
    found = pyautogui.locateCenterOnScreen('navBar.png', confidence=0.9)
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
        found = pyautogui.locateOnScreen('navBar.png', confidence=0.9)
        if found:
            move_to_and_click(found)
            print("Clicked on the nav bar.")
            time.sleep(DEFAULT_WAIT_TIME)
            break
        else:
            print(f"Couldn't find the nav bar. Trying {tries-1}")
        tries -= 1
        time.sleep(0.3)


def handling_enemy():
    global enemies_detected
    if pyautogui.locateCenterOnScreen('enemy.png', confidence=0.99):
        print('detected enemies, emergency dock initialized')
        get_into_eye_view()
        enemies_detected = True
        if not pyautogui.locateCenterOnScreen('DefaultFitting.png', confidence=0.9):  # check if select screen on
            click_nav_bar()
        station = pyautogui.locateCenterOnScreen('stationDarkIcon.png', confidence=0.9)
        if not station:
            station = pyautogui.locateCenterOnScreen('stationLightIcon.png', confidence=0.9)
        move_to_and_click(station)
        time.sleep(0.5)
        move_to_and_click(pyautogui.locateCenterOnScreen('stationIcon.png', confidence=0.9))
        time.sleep(0.5)
        move_to_and_click(pyautogui.locateCenterOnScreen('dockIcon.png', confidence=0.9))
        time.sleep(DEFAULT_WAIT_TIME)


def check_optimum():
    check = [pyautogui.locateCenterOnScreen('17km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('16km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('15km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('14km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('13km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('12km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('11km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('10km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('8km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('7km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('6km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('5km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('4km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('3km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('1km.png', confidence=0.97, region=menu_region),
             pyautogui.locateCenterOnScreen('0km.png', confidence=0.97, region=menu_region)]
    if any(check):
        return True
    else:
        return False


def dock_to_station():
    get_into_eye_view()
    if not pyautogui.locateCenterOnScreen('DefaultFitting.png', confidence=0.9):
        click_nav_bar()
    coord = pyautogui.locateCenterOnScreen('stationDarkIcon.png', confidence=0.9)
    if not coord:
        coord = pyautogui.locateCenterOnScreen('stationLightIcon.png', confidence=0.9)
    move_to_and_click(coord)
    time.sleep(0.5)
    move_to_and_click(pyautogui.locateCenterOnScreen('stationIcon.png', confidence=0.9))
    time.sleep(0.5)
    move_to_and_click(pyautogui.locateCenterOnScreen('dockIcon.png', confidence=0.9))
    print("docking")
    while not pyautogui.locateCenterOnScreen('UndockButton.png', confidence=0.98):
        time.sleep(1)
    time.sleep(1)


def offload_cargo():
    move_to_and_click(cargo)
    time.sleep(2)
    move_to_and_click(pyautogui.locateCenterOnScreen('oreHold.png', confidence=0.95))
    time.sleep(2)
    move_to_and_click(pyautogui.locateCenterOnScreen('selectAll.png', confidence=0.95))
    time.sleep(2)
    move_to_and_click(pyautogui.locateCenterOnScreen('moveTo.png', confidence=0.95))
    time.sleep(2)
    move_to_and_click(pyautogui.locateCenterOnScreen('itemHangar.png', confidence=0.98))
    time.sleep(2)
    move_to_and_click(pyautogui.locateCenterOnScreen('exit.png', confidence=0.95))
    time.sleep(1)


pyautogui.FAILSAFE = True
UNDOCKED = True
warp = (42, 229)
confirm = (1712, 823)
center = (994, 561)
eye_on_the_right = (1847, 604)
eye_on_the_left = (1469, 604)
expected_eye_color = (169, 185, 181)
undock = (1678, 349)
expected_undock_color = (174, 147, 40)
expected_anomaly_color = (138, 26, 26)
navigate = (1672, 20)
expected_navigate_color = (13, 14, 14)
anomaly_tab = (1641, 621)
mining_tab = (1707, 829)
first_entry_in_nav_tab = (1637, 137)
slot1 = (1531, 994)
warp_to_in_tab = (1239, 258)
expected_warp_color = (169, 185, 181)
easy_lock = (1201, 685)
dock_in_tab = (1387, 157)
scroll_here = (1754, 500)
menu_region = (1413, 0, 500, 1070)
ship_status = (639, 809, 600, 270)
lock_region = (1108, 12, 500, 120)
laser1 = (1521, 991)
laser2 = (1689, 999)
cargo = (90, 150)
width, height = pyautogui.size()

enemies_detected = False

while True:
    enemies_detected = False
    if pyautogui.locateCenterOnScreen('sufficientCargo.png', confidence=0.99):
        offload_cargo()
    perform_undock()  # undocks the ship
    handling_enemy()

    if enemies_detected:
        continue

    get_into_eye_view()  # gets the ship in the eye view
    if not pyautogui.locateCenterOnScreen('DefaultFitting.png', confidence=0.9):  # check if select screen on
        click_nav_bar()
    move_to_and_click(mining_tab)
    print("clicked on mining tab")
    time.sleep(DEFAULT_WAIT_TIME)
    target = pyautogui.locateCenterOnScreen('AsteroidIcon.png', confidence=0.9, region=menu_region)
    if target:
        move_to_and_click(target)
    else:
        print("No available asteroid fields")
        raise Exception("No available asteroid fields")
    print("clicked on an appropriate belt")
    time.sleep(DEFAULT_WAIT_TIME)
    move_to_and_click(pyautogui.locateCenterOnScreen('Warp.png', confidence=0.9))
    print("warping to the appropriate asteroid")
    time.sleep(1)
    pyautogui.keyDown('down')
    time.sleep(5)
    pyautogui.keyUp('down')
    current_time = 0
    while not (pyautogui.locateCenterOnScreen('littleSpeed.png', confidence=0.97, region=ship_status) and current_time > 5):
        time.sleep(1)
        print("Warp not done yet")
        current_time += 1
        print("Time since warp: " + str(current_time))
    print("warp done, finding an asteroid")
    handling_enemy()

    if enemies_detected:
        continue

    time.sleep(3)
    tries = 3
    hasAsteroids = False
    while tries:
        if pyautogui.locateCenterOnScreen('singleAsteroid.png', confidence=0.99, region=menu_region):
            print("Asteroids have loaded in")
            hasAsteroids = True
            break
        else:
            print(f"No asteroids detected. Trying {tries - 1} more time(s)")
            time.sleep(1)
            tries -= 1
    if not hasAsteroids:
        raise Exception("No asteroids in belt")
    pyautogui.moveTo(scroll_here)
    while not pyautogui.locateCenterOnScreen('finishScroll.png', confidence=0.9, region=menu_region):
        pyautogui.scroll(200)
    time.sleep(1.5)
    full = pyautogui.locateCenterOnScreen('fullCargo.png', confidence=0.99)
    while not full:
        target = pyautogui.locateCenterOnScreen('singleAsteroid.png', confidence=0.98, region=menu_region)
        if not target:
            raise Exception("no asteroids")
        move_to_and_click(target)
        time.sleep(DEFAULT_WAIT_TIME)
        move_to_and_click(pyautogui.locateCenterOnScreen('lock.png', confidence=0.95))
        time.sleep(2.5)

        if enemies_detected:
            break

        move_to_and_click(pyautogui.locateCenterOnScreen('lockedAsteroid.png', confidence=0.97, region=menu_region))
        time.sleep(DEFAULT_WAIT_TIME)
        move_to_and_click(pyautogui.locateCenterOnScreen('approach.png', confidence=0.9))
        optimum_reached = False
        while not optimum_reached:
            print("Optimum not reached")
            if check_optimum():
                optimum_reached = True
            time.sleep(2)
            handling_enemy()

            if enemies_detected:
                break

        if enemies_detected:
            break

        get_out_of_eye_view()
        move_to_and_click(laser1)
        move_to_and_click(laser2)
        get_into_eye_view()
        asteroid_done = False
        while not asteroid_done:
            if not pyautogui.locateCenterOnScreen('lockedAsteroid.png', confidence=0.97, region=menu_region):
                asteroid_done = True
                print('asteroid done, finding another')
            print(f"mining loop in progress")
            handling_enemy()
            time.sleep(1)

    dock_to_station()
    offload_cargo()


