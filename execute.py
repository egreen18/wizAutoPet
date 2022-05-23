from tools import loadTemplates, runGame, checkGen, startGame, leftButton, rightButton, feedSnack
import pyautogui as auto
import time

templates = loadTemplates()

snack = 1 #Decide whether or not to consume snacks with this binary
round = 0 #Initializing round tracker
now = time.time() #This is used to allow the program to run for a desired duration
runtime = 1000 #seconds

#Scanning for start of game - round one has different start indicator than other rounds so it is treated individually
while time.time() < now+runtime:
    if checkGen(templates['in_client']):
        auto.press('x') #Attempting to interact with sigil
    #If successful, should detect dance game pre game screen
    if checkGen(templates['dance']):
        startGame() #Auto select a level and start game
        runGame(round, now, runtime, templates) #Running game
        while time.time() < now+runtime:
            if checkGen(templates['reward']):
                break #Waiting for the post game screen to load in
        rightButton()
        if snack:
            feedSnack(templates)
        leftButton()