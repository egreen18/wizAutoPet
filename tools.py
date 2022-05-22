import PIL.ImageGrab
import numpy as np
import numpy as np
import cv2
import time
import pyautogui as auto

def loadArrow():
    #Loading templates
    tpl_l = cv2.imread('templates/left_tpl.png')
    tpl_r = cv2.imread('templates/right_tpl.png')
    tpl_u = cv2.imread('templates/up_tpl.png')
    tpl_d = cv2.imread('templates/down_tpl.png')
    tpl_0 = cv2.imread('templates/blank_tpl.png')

    #Converting to grayscale for cv2 processing
    tpl_l = cv2.cvtColor(np.array(tpl_l), cv2.COLOR_BGR2GRAY)
    tpl_r = cv2.cvtColor(np.array(tpl_r), cv2.COLOR_BGR2GRAY)
    tpl_u = cv2.cvtColor(np.array(tpl_u), cv2.COLOR_BGR2GRAY)
    tpl_d = cv2.cvtColor(np.array(tpl_d), cv2.COLOR_BGR2GRAY)
    tpl_0 = cv2.cvtColor(np.array(tpl_0), cv2.COLOR_BGR2GRAY)

    return tpl_l, tpl_r, tpl_u, tpl_d, tpl_0

def loadArrow_f():
    #Loading templates
    tpl_l = cv2.imread('templates/f_left_tpl.png')
    tpl_r = cv2.imread('templates/f_right_tpl.png')
    tpl_u = cv2.imread('templates/f_up_tpl.png')
    tpl_d = cv2.imread('templates/f_down_tpl.png')
    tpl_0 = cv2.imread('templates/blank_tpl.png')

    #Converting to grayscale for cv2 processing
    tpl_l = cv2.cvtColor(np.array(tpl_l), cv2.COLOR_BGR2GRAY)
    tpl_r = cv2.cvtColor(np.array(tpl_r), cv2.COLOR_BGR2GRAY)
    tpl_u = cv2.cvtColor(np.array(tpl_u), cv2.COLOR_BGR2GRAY)
    tpl_d = cv2.cvtColor(np.array(tpl_d), cv2.COLOR_BGR2GRAY)
    tpl_0 = cv2.cvtColor(np.array(tpl_0), cv2.COLOR_BGR2GRAY)

    return tpl_l, tpl_r, tpl_u, tpl_d, tpl_0

def loadText():
    #Loading templates
    tpl_done = cv2.imread('templates/done_tpl.png')
    tpl_go = cv2.imread('templates/go_tpl.png')
    tpl_match = cv2.imread('templates/match_tpl.png')

    #Converting to grayscale for cv2 processing
    tpl_done = cv2.cvtColor(np.array(tpl_done), cv2.COLOR_BGR2GRAY)
    tpl_go = cv2.cvtColor(np.array(tpl_go), cv2.COLOR_BGR2GRAY)
    tpl_match = cv2.cvtColor(np.array(tpl_match), cv2.COLOR_BGR2GRAY)

    return tpl_done, tpl_go, tpl_match

def loadText_f():
    #Loading templates
    tpl_done = cv2.imread('templates/f_done_tpl.png')
    tpl_go = cv2.imread('templates/f_go_tpl.png')
    tpl_match = cv2.imread('templates/f_match_tpl.png')

    #Converting to grayscale for cv2 processing
    tpl_done = cv2.cvtColor(np.array(tpl_done), cv2.COLOR_BGR2GRAY)
    tpl_go = cv2.cvtColor(np.array(tpl_go), cv2.COLOR_BGR2GRAY)
    tpl_match = cv2.cvtColor(np.array(tpl_match), cv2.COLOR_BGR2GRAY)

    return tpl_done, tpl_go, tpl_match

def tplComp(status,tpl):
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
    #Checking arrows against templates
    if tplComp(pic,tpl):
        arrow = 'blank'
    else:
        arrow = 0

    return arrow

def checkStatus(tpl_done, tpl_go, tpl_match):
    #Predfine output
    status = []

    #Pulling screenshot
    pic = PIL.ImageGrab.grab()

    #Converting to grayscale for cv2 processing
    pic = cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY)

    #Checking arrows against templates
    if tplComp(pic,tpl_done):
        status = 'done'
    elif tplComp(pic,tpl_go):
        status = 'go'
    elif tplComp(pic,tpl_match):
        status = 'match'
    
    return status


def checkArrow(pic, tpl_l, tpl_r, tpl_u, tpl_d, tpl_0):
    #Predfine output
    arrow = []
    
    #Checking arrows against templates
    if tplComp(pic,tpl_l):
        arrow = 'left'
    elif tplComp(pic,tpl_r):
        arrow = 'right'
    elif tplComp(pic,tpl_u):
        arrow = 'up'
    elif tplComp(pic,tpl_d):
        arrow = 'down'
    elif tplComp(pic,tpl_0):
        arrow = 'blank'

    return arrow

def recordSequence(duration):
    #Records as many screenshots as computationally allowed in the specified timeframe
    memory = [] #Establishing memory list for screenshots

    now = time.time()

    while time.time() < now + duration:
        memory.append(PIL.ImageGrab.grab(bbox = (906,942,1006,1024)))
    
    return memory

def analyzeSequence(memory, tpl_l, tpl_r, tpl_u, tpl_d, tpl_0):
    mem_conv = [] #Predefining converted memory list

    #Converting memory screenshots to suitable cv2 template images
    for pic in memory:
        mem_conv.append(cv2.cvtColor(np.array(pic), cv2.COLOR_RGB2GRAY))

    #Reformatting memory to only include around 80 screenshots
    #This balances accuracy and computational load
    slice = int(len(mem_conv)/80)
    mem_slice = mem_conv[::slice]
    
    blank = 1 #Blank tracker to avoid double counting arrows
    sequence = [] #Predefining arrow sequence list

    for pic in mem_slice:
        arrow = checkArrow(pic, tpl_l, tpl_r, tpl_u, tpl_d, tpl_0)
        if arrow and blank and arrow != 'blank':
            sequence.append(arrow)
            blank = 0
        elif arrow == 'blank':
            blank = 1

    return sequence

def runRound(round,now,runtime,tpl_l, tpl_r, tpl_u, tpl_d, tpl_0,tpl_go):
    roundtime = 3 + 1.1*round
    #Record for the round duration
    memory = recordSequence(roundtime)
    #Analyze recorded screenshots for arrow sequence
    sequence = analyzeSequence(memory, tpl_l, tpl_r, tpl_u, tpl_d, tpl_0)
    #Scanning for start of user input portion
    while time.time() < now+runtime:
        #If game is ready for user input
        if checkGen(tpl_go):
            #Execute arrow sequence on keyboard
            auto.press(sequence,interval=2)
            print(sequence)
            break