import mss
import numpy as np
import cv2
import time
import pyautogui as auto
import os.path as os
import platform


def mssMon(shape):
    # Takes a resolution in the form of a 1,4 list and prepares it for input into mss screenshot function
    mon = {"top": shape[1], "left": shape[0], "width": shape[2]-shape[0], "height": shape[3]-shape[1]}
    return mon


def osResGen():
    res_val = auto.size()
    if platform.system() == 'Darwin':
        os_val = 'mac'
    elif platform.system() == 'Windows':
        os_val = 'pc'
    else:
        os_val = ''
    os_res = '_'.join([os_val, str(res_val[0])])
    return os_res


def loadCoords(os_res):
    if os_res == 'pc_1680':
        levels = {
            'wiz': (647, 765),
            'kro': (794, 760),
            'mar': (975, 776),
            'mus': (1117, 771),
            'dra': (1288, 766)
        }
        coords = {
            'left': (633, 907),
            'right': (1272, 906),
            'snack': (640, 751),
            'arrow': (906, 942, 1006, 1024),  # box
            'levels': levels  # nested dictionary
        }
    elif os_res == 'mac_1440':
        levels = {
            'wiz': (480, 610),
            'kro': (590, 610),
            'mar': (715, 610),
            'mus': (830, 610),
            'dra': (950, 610)
        }
        coords = {
            'left': (484, 712),
            'right': (944, 712),
            'snack': (480, 610),
            'arrow': (670, 730, 760, 810),  # box
            'levels': levels  # nested dictionary
        }
        return coords


def loadTemplates(os_res):
    # This function loads arrow templates into the workspace
    # Loading templates
    tpl_l = cv2.imread(os.join('templates', os_res, 'left_tpl.png'))
    tpl_r = cv2.imread(os.join('templates', os_res, 'right_tpl.png'))
    tpl_u = cv2.imread(os.join('templates', os_res, 'up_tpl.png'))
    tpl_d = cv2.imread(os.join('templates', os_res, 'down_tpl.png'))
    tpl_0 = cv2.imread(os.join('templates', os_res, 'blank_tpl.png'))
    tpl_done = cv2.imread(os.join('templates', os_res, 'done_tpl.png'))
    tpl_go = cv2.imread(os.join('templates', os_res, 'go_tpl.png'))
    tpl_match = cv2.imread(os.join('templates', os_res, 'match_tpl.png'))
    tpl_dance = cv2.imread(os.join('templates', os_res, 'dance_tpl.png'))           # (840 160 1080 200)
    tpl_reward = cv2.imread(os.join('templates', os_res, 'reward_tpl.png'))         # (820 160 1080 200)
    tpl_feed = cv2.imread(os.join('templates', os_res, 'feed_tpl.png'))             # (820 160 1080 200)
    tpl_fed = cv2.imread(os.join('templates', os_res, 'fed_tpl.png'))               # (810 160 1090 200)
    tpl_no_snack = cv2.imread(os.join('templates', os_res, 'no_snack_tpl.png'))     # (746 738 1159 788)    REPLACE!!!
    tpl_in_client = cv2.imread(os.join('templates', os_res, 'in_client_tpl.png'))        # (1772 886 1920 1080)
    tpl_no_energy = cv2.imread(os.join('templates', os_res, 'no_energy_tpl.png'))   # REPLACE!!!

    # Converting to grayscale for cv2 processing
    tpl_l = cv2.cvtColor(np.array(tpl_l), cv2.COLOR_BGR2GRAY)
    tpl_r = cv2.cvtColor(np.array(tpl_r), cv2.COLOR_BGR2GRAY)
    tpl_u = cv2.cvtColor(np.array(tpl_u), cv2.COLOR_BGR2GRAY)
    tpl_d = cv2.cvtColor(np.array(tpl_d), cv2.COLOR_BGR2GRAY)
    tpl_0 = cv2.cvtColor(np.array(tpl_0), cv2.COLOR_BGR2GRAY)
    tpl_done = cv2.cvtColor(np.array(tpl_done), cv2.COLOR_BGR2GRAY)
    tpl_go = cv2.cvtColor(np.array(tpl_go), cv2.COLOR_BGR2GRAY)
    tpl_dance = cv2.cvtColor(np.array(tpl_dance), cv2.COLOR_BGR2GRAY)
    tpl_reward = cv2.cvtColor(np.array(tpl_reward), cv2.COLOR_BGR2GRAY)
    tpl_match = cv2.cvtColor(np.array(tpl_match), cv2.COLOR_BGR2GRAY)
    tpl_feed = cv2.cvtColor(np.array(tpl_feed), cv2.COLOR_BGR2GRAY)
    tpl_fed = cv2.cvtColor(np.array(tpl_fed), cv2.COLOR_BGR2GRAY)
    tpl_no_snack = cv2.cvtColor(np.array(tpl_no_snack), cv2.COLOR_BGR2GRAY)
    tpl_in_client = cv2.cvtColor(np.array(tpl_in_client), cv2.COLOR_BGR2GRAY)
    tpl_no_energy = cv2.cvtColor(np.array(tpl_no_energy), cv2.COLOR_BGR2GRAY)

    templates = {
        'l': tpl_l,
        'r': tpl_r,
        'u': tpl_u,
        'd': tpl_d,
        '0': tpl_0,
        'done': tpl_done,
        'go': tpl_go,
        'match': tpl_match,
        'dance': tpl_dance,
        'reward': tpl_reward,
        'feed': tpl_feed,
        'fed': tpl_fed,
        'no_snack': tpl_no_snack,
        'in_client': tpl_in_client,
        'no_energy': tpl_no_energy,
    }
    return templates


def tplComp(image, tpl):
    # This function compares template and image to identify text or arrows
    # Perform match operations.
    res = cv2.matchTemplate(image, tpl, cv2.TM_CCOEFF_NORMED)

    # Specify a threshold
    threshold = 0.8

    # Store the coordinates of matched area in a numpy array
    loc = np.where(res >= threshold)

    # If matched area coordinates exist, arrow is identified. Return positive
    if len(loc[0]) > 0:
        return 1
    else:
        return 0


def checkGen(tpl):
    # This function takes a screenshot and calls tplComp to identify one template
    # Pulling screenshot
    with mss.mss() as sct:
        pic = sct.grab(sct.monitors[1])

    # Converting to grayscale for cv2 processing
    pic = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY)

    # Checking arrows against templates
    if tplComp(pic, tpl):
        identified = 1
    else:
        identified = 0

    return identified


def checkBlank(pic, tpl):
    # This function calls tplComp to compare a given, cv2-ready image to a template
    # Checking arrows against templates
    if tplComp(pic, tpl):
        arrow = 'blank'
    else:
        arrow = 0

    return arrow


def checkStatus(templates):
    # This function checks for Go!, Match This!, and Done! indicators
    # Predefine output
    status = []

    # Pulling screenshot
    with mss.mss() as sct:
        pic = sct.grab(sct.monitors[1])

    # Converting to grayscale for cv2 processing
    pic = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY)

    # Checking arrows against templates
    if tplComp(pic, templates['done']):
        status = 'done'
    elif tplComp(pic, templates['go']):
        status = 'go'
    elif tplComp(pic, templates['match']):
        status = 'match'

    return status


def checkArrow(pic, templates):
    # This function checks for any direction arrow and or a blank space where the arrow resides
    # Predefine output
    arrow = []

    # Checking arrows against templates
    if tplComp(pic, templates['l']):
        arrow = 'left'
    elif tplComp(pic, templates['r']):
        arrow = 'right'
    elif tplComp(pic, templates['u']):
        arrow = 'up'
    elif tplComp(pic, templates['d']):
        arrow = 'down'
    elif tplComp(pic, templates['0']):
        arrow = 'blank'

    return arrow


def recordSequence(duration, coords):
    # Records as many screenshots as computationally allowed in the specified timeframe
    memory = []  # Establishing memory list for screenshots

    now = time.time()

    mon = mssMon(coords['arrow'])
    with mss.mss() as sct:
        while time.time() < now + duration:
            memory.append(sct.grab(mon))

    return memory


def analyzeSequence(memory, templates):
    # Analyzes the memory to deduce a sequence of arrows
    # Reformatting memory to only include around 80 screenshots
    # This balances accuracy and computational load
    slice = int(len(memory) / 80)
    slice = 1 if slice < 1 else slice  # Making sure we don't end up with a 0 slice
    mem_slice = memory[::slice]

    mem_conv = []  # Predefining converted memory list

    # Converting memory screenshots to suitable cv2 template images to allow calling of tplComp
    for pic in mem_slice:
        mem_conv.append(cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY))

    blank = 1  # Blank tracker to avoid double counting arrows
    sequence = []  # Predefining arrow sequence list

    for pic in mem_conv:
        # Identify if a blank or directional arrow is in the image
        arrow = checkArrow(pic, templates)
        if arrow and blank and arrow != 'blank':
            # If an arrow is identified and a blank was identified beforehand, add the arrow to the sequence
            sequence.append(arrow)
            # Reset the blank indicator, requiring that a blank re-trigger it to prevent double counting
            blank = 0
        elif arrow == 'blank':
            # Blank indicator tracking
            blank = 1

    return sequence


def runRound(round, now, runtime, templates, coords):
    # The window that needs to be recorded increases with each round by this function
    roundtime = 3.2 + 1.1 * round
    # Record for the round duration
    memory = recordSequence(roundtime, coords)
    # Analyze recorded screenshots for arrow sequence
    sequence = analyzeSequence(memory, templates)
    # Scanning for start of user input portion
    while time.time() < now + runtime:
        # If game is ready for user input
        if checkGen(templates["go"]):
            # Execute arrow sequence on keyboard
            auto.press(sequence, interval=2)
            break


def runGame(round, now, runtime, templates, coords):
    while time.time() < now + runtime:
        if checkGen(templates["match"]):
            break  # Checking for 'Match This!' to see if game has started

    runRound(round, now, runtime, templates, coords)  # Running round
    # Keeping track of the active round
    round += 1
    # Subsequent round begins with 'Done!' instead of 'Match This!'
    while round <= 4:
        if checkGen(templates["done"]):
            runRound(round, now, runtime, templates, coords)
            round += 1


def startGame(coords):
    keys = list(coords['levels'].keys())
    select = np.random.randint(0, 5)
    button(coords['levels'][keys[select]])
    button(coords['right'])


def button(coords):
    auto.moveTo(coords)
    time.sleep(0.1)
    auto.click()
    time.sleep(0.1)


def jiggle():
    # Jiggles mouse to reactivate some buttons
    pos = auto.position()

    auto.moveTo((pos[0] + 2, pos[1] + 2))
    time.sleep(0.05)
    auto.moveTo((pos[0], pos[1]))


def feedSnack(templates, coords):
    time.sleep(0.3)
    # Checking if there are any snacks available
    if not checkGen(templates['no_snack']):
        button(coords['snack'])
        button(coords['right'])


def autoRun(runtime, snack):
    os_res = osResGen()
    coords = loadCoords(os_res)
    templates = loadTemplates(os_res='temp')
    now = time.time()  # This is used to allow the program to run for a desired duration
    round = 0  # Initializing round tracker

    # Scanning for start of game - round one has different start indicator than other rounds so
    # it is treated individually
    print('Starting game...')
    while time.time() < now + runtime:
        if checkGen(templates['in_client']):
            auto.press('x')  # Attempting to interact with sigil
        # If successful, should detect dance game pre game screen
        if checkGen(templates['dance']):
            # Checking to see if there is insufficient energy
            if checkGen(templates['no_energy']):
                button(coords['left'])  # Closing game
                print('Insufficient energy, autoRun terminated.')
                return  # Ending function
            startGame(coords)  # Auto select a level and start game
            runGame(round, now, runtime, templates, coords)  # Running game
            while time.time() < now + runtime:
                if checkGen(templates['reward']):
                    break  # Waiting for the post game screen to load in
            jiggle()
            button(coords['right'])
            if snack:
                feedSnack(templates, coords)
            button(coords['left'])
    print('Runtime completed, autoRun terminated.')


    # Future work: exiting out of pet level up automatically
    # On mac_1440, X button for this is at (975 675)
