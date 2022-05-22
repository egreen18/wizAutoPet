from tools import loadArrow_f, loadText_f, loadArrow, loadText, checkGame
import time
import pyautogui as auto

tpl_l, tpl_r, tpl_u, tpl_d,tpl_0 = loadArrow()
tpl_done, tpl_go, tpl_match = loadText()

now = time.time()
runtime = 45 #seconds

sequence = [] #Initializing arrow sequence tracker
blank = 0 #Initialize blank tracker
round = 0 #Initialize round tracker
ready = 0 #Initialize ready to execute tracker

while time.time() < now+runtime:
    arrow, status = checkGame(tpl_l, tpl_r, tpl_u, tpl_d, tpl_0, tpl_done, tpl_go, tpl_match)     
    #If a blank is detected, set off blank tracker to allow for new arrow in sequence
    if arrow == 'blank':
        blank = 1

    #If game is on match, arrow is detected, and blank came before
    if status == 'match' and arrow != 'blank' and blank:
        blank = 0 #Resetting blank tracker to avoid double counting arrows

        sequence.append(arrow) #Track arrow in sequence

        #Checking to see if the appropriate number of arrows have been counted for the round
        if len(sequence) == round + 3:
            ready = 1 #Included incase of undercounting
        else:
            ready = 0 #Included incase of overcounting 
         
    #If game is on go, check sequence and execute
    elif status == 'go':
        #Readiness check
        if ~ready:
            #Fixing overcounted arrow sequence
            if len(sequence) > round + 3:
                sequence = sequence[0:round+3] #Cut off overcounted arrows
            
            #Fixing non-existent sequence to avoid error if this occurs
            elif len(sequence) == 0:
                while len(sequence) < round + 3:
                    sequence.append('up') #Just fill with up, worst case scenario

            #Fixing undercounted arrow sequence
            elif len(sequence) < round + 3: 
                while len(sequence) < round + 3:
                    sequence.append(sequence[-1]) #Duplicate last counted arrow
        
        #Now ready, executing arrow sequence
        auto.press(sequence,interval=2)
        round += 1 #Increase round counter
        #Reset to round 0 to allow for continued gameplay
        if round > 4:
            round = 0
        sequence = [] #Re-initialize sequence for next round
