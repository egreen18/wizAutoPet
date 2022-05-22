from tools import loadArrow_f, loadText_f, checkStatus, checkArrow, recordSequence, checkGen, runRound
import time
import pyautogui as auto

tpl_l, tpl_r, tpl_u, tpl_d,tpl_0 = loadArrow_f()
tpl_done, tpl_go, tpl_match = loadText_f()

round = 0 #Initializing round tracker
now = time.time() #This is used to allow the program to run for a desired duration
runtime = 1000 #seconds

#Scanning for start of game - round one has different start indicator than other rounds so it is treated individually
while time.time() < now+runtime:
    #Checking for 'Match This!' to see if game has started
    if checkGen(tpl_match):
        #This function encompasses screen capture, image analysis, and GUI realization
        runRound(round,now,runtime,tpl_l, tpl_r, tpl_u, tpl_d, tpl_0, tpl_go)
        #Keeping track of the active round
        round += 1
        print(round)
        #Subsequent round begins with 'Done!' instead of 'Match This!'
        while round <= 4:
            if checkGen(tpl_done):
                runRound(round,now,runtime,tpl_l, tpl_r, tpl_u, tpl_d, tpl_0, tpl_go)
                round += 1
                #Testing tool, unecessary
                print(round)
    if round > 4:
        #Resetting game
        round = 0
