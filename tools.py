import PIL.ImageGrab
import numpy as np
import cv2
import time
import pyautogui as auto


def loadTemplates():
    #This function loads arrow templates into the workspace
    #Loading templates
    tpl_l = cv2.imread('templates/f_left_tpl.png')
    tpl_r = cv2.imread('templates/f_right_tpl.png')
    tpl_u = cv2.imread('templates/f_up_tpl.png')
    tpl_d = cv2.imread('templates/f_down_tpl.png')
    tpl_0 = cv2.imread('templates/f_blank_tpl.png')
    tpl_done = cv2.imread('templates/f_done_tpl.png')
    tpl_go = cv2.imread('templates/f_go_tpl.png')
    tpl_match = cv2.imread('templates/f_match_tpl.png')
    tpl_dance = cv2.imread('templates/f_dance_tpl.png')     #(840 160 1080 200)
    tpl_reward = cv2.imread('templates/f_reward_tpl.png')   #(820 160 1080 200)
    tpl_feed = cv2.imread('templates/f_feed_tpl.png')       #(820 160 1080 200)
    tpl_fed = cv2.imread('templates/f_fed_tpl.png')         #(810 160 1090 200)

    #Converting to grayscale for cv2 processing
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
        'fed': tpl_fed
    }
    return templates

def tplComp(status,tpl):
    #This function compares template and image to identify text or arrows
    #Perform match operations.
    res = cv2.matchTemplate(status,tpl,cv2.TM_CCOEFF_NORMED)

    #Specify a threshold
    threshold = 0.8
    
    #Store the coordinates of matched area in a numpy array
    loc = np.where( res >= threshold)

    #If matched area corrdinates exist, arrow is identified. Return postive
    if len(loc[0]) > 0:
        return 1
    else:
       return 0

def checkGen(tpl):
    #This funcion takes a screenshot and calls tplComp to identify one template
    #Pulling screenshot
    pic = PIL.ImageGrab.grab()

    #Converting to grayscale for cv2 processing
    pic = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY)

    #Checking arrows against templates
    if tplComp(pic,tpl):
        identified = 1
    else:
        identified = 0

    return identified

def checkBlank(pic,tpl):
    #This function calls tplComp to compare a given, cv2-ready image to a template
    #Checking arrows against templates
    if tplComp(pic,tpl):
        arrow = 'blank'
    else:
        arrow = 0

    return arrow

def checkStatus(templates):
    #This function checks for Go!, Match This!, and Done! indicators
    #Predfine output
    status = []

    #Pulling screenshot
    pic = PIL.ImageGrab.grab()

    #Converting to grayscale for cv2 processing
    pic = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY)

    #Checking arrows against templates
    if tplComp(pic,templates['done']):
        status = 'done'
    elif tplComp(pic,templates['go']):
        status = 'go'
    elif tplComp(pic,templates['match']):
        status = 'match'
    
    return status


def checkArrow(pic, templates):
    #This function checks for any direction arrow and or a blank space where the arrow resides
    #Predfine output
    arrow = []
    
    #Checking arrows against templates
    if tplComp(pic,templates['l']):
        arrow = 'left'
    elif tplComp(pic,templates['r']):
        arrow = 'right'
    elif tplComp(pic,templates['u']):
        arrow = 'up'
    elif tplComp(pic,templates['d']):
        arrow = 'down'
    elif tplComp(pic,templates['0']):
        arrow = 'blank'

    return arrow

def recordSequence(duration):
    #Records as many screenshots as computationally allowed in the specified timeframe
    memory = [] #Establishing memory list for screenshots

    now = time.time()

    while time.time() < now + duration:
        memory.append(PIL.ImageGrab.grab(bbox = (906,942,1006,1024)))
    
    return memory

def analyzeSequence(memory, templates):
    #Analyzes the memory to deduce a sequence of arrows
    #Reformatting memory to only include around 80 screenshots
    #This balances accuracy and computational load
    slice = int(len(memory)/80)
    slice = 1 if slice < 1 else slice #Making sure we don't end up with a 0 slice
    mem_slice = memory[::slice]

    mem_conv = [] #Predefining converted memory list

    #Converting memory screenshots to suitable cv2 template images to allow calling of tplComp
    for pic in mem_slice:
        mem_conv.append(cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY))
    
    blank = 1 #Blank tracker to avoid double counting arrows
    sequence = [] #Predefining arrow sequence list

    for pic in mem_conv:
        #Identify if a blank or directional arrow is in the image
        arrow = checkArrow(pic, templates)
        if arrow and blank and arrow != 'blank':
            #If an arrow is identifed and a blank was identified beforehand, add the arrow to the sequence
            sequence.append(arrow)
            #Reset the blank indicator, requiring that a blank re-trigger it to prevent double counting 
            blank = 0
        elif arrow == 'blank':
            #Blank indicator tracking
            blank = 1

    return sequence

def runRound(round, now, runtime, templates):
    #The window that needs to be recorded increases with each round by this function
    roundtime = 3.2 + 1.1*round
    #Record for the round duration
    memory = recordSequence(roundtime)
    #Analyze recorded screenshots for arrow sequence
    sequence = analyzeSequence(memory, templates)
    #Scanning for start of user input portion
    while time.time() < now+runtime:
        #If game is ready for user input
        if checkGen(templates["go"]):
            #Execute arrow sequence on keyboard
            auto.press(sequence,interval=2)
            break

def runGame(round, now, runtime, templates):
    while time.time() < now+runtime:
        if checkGen(templates["match"]):
            break #Checking for 'Match This!' to see if game has started
        
    runRound(round, now, runtime, templates) #Running round
    #Keeping track of the active round
    round += 1
    #Subsequent round begins with 'Done!' instead of 'Match This!'
    while round <= 4:
        if checkGen(templates["done"]):
            runRound(round, now, runtime, templates)
            round += 1
    if round > 4:
        #Resetting game
        round = 0

def startGame():
    #Tabulated positions of UI elements
    levels = {
        'wiz': (647,765),
        'kro': (794,760),
        'mar': (975,776),
        'mus': (1117,771),
        'dra': (1288,766)
    }
    keys = list(levels.keys())
    select = np.random.randint(0,5)
    coord = levels[keys[select]]
    auto.moveTo(coord) #Move to selected level
    time.sleep(0.3)
    auto.click() #Select
    time.sleep(0.3)
    auto.moveTo((1272,906)) #Move to play button
    time.sleep(0.3)
    auto.click() #Select

def rightButton():
    auto.moveTo(1272,906)
    time.sleep(0.3)
    auto.click()

def leftButton():
    auto.moveTo(633,907)
    time.sleep(0.3)
    auto.click()