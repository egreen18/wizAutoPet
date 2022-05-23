from tools import loadTemplates, runGame, checkGen, startGame, leftButton, rightButton
import pyautogui as auto
import time

templates = loadTemplates()

round = 0 #Initializing round tracker
now = time.time() #This is used to allow the program to run for a desired duration
runtime = 1000 #seconds

#Scanning for start of game - round one has different start indicator than other rounds so it is treated individually
while time.time() < now+runtime:
    auto.press('x') #Attempting to interact with sigil
    auto.sleep(1.5) #Allowing for game to load
    #If successful, should detect dance game pre game screen
    if checkGen(templates['dance']):
        startGame() #Auto select a level and start game
        runGame(round, now, runtime, templates) #Running game
        while time.time() < now+runtime:
            if checkGen(templates['reward']):
                break #Waiting for the post game screen to load in
        rightButton()
        leftButton()