from tools import loadArrow_f, loadText_f, checkStatus, checkArrow, recordSequence, checkGen, runRound
import time
import pyautogui as auto

tpl_l, tpl_r, tpl_u, tpl_d,tpl_0 = loadArrow_f()
tpl_done, tpl_go, tpl_match = loadText_f()

round = 0
now = time.time()
runtime = 1000 #seconds

#Scanning for start of game - round one has different start indicator than other rounds so it is treated individually
while time.time() < now+runtime:
    #If game has started
    if checkGen(tpl_match):
        runRound(round,now,runtime,tpl_l, tpl_r, tpl_u, tpl_d, tpl_0, tpl_go)
        round += 1
        print(round)
        while round <= 4:
            if checkGen(tpl_done):
                runRound(round,now,runtime,tpl_l, tpl_r, tpl_u, tpl_d, tpl_0, tpl_go)
                round += 1
                print(round)
    if round > 4:
        #Resetting game
        round = 0
