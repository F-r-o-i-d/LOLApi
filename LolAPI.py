from calendar import c
import time
import numpy as np
import cv2
import pyautogui
from pytesseract import pytesseract

# Path to tesseract.exe
pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
   


class LeagueOfLegendsCLIENT():
    def __init__(self) -> None:
        self.actualLife = 0
        self.actualMana = 0
        self.actualMaxLife = 0
        self.actualMaxMana = 0
        self.actualPO = 0
        self.mapCoordinates  = ((1662, 820),(1920, 1080))
        self.lifeCoordinates = ((800, 1029),(950, 1050))
        self.manaCoordinates = ((800, 1050),(950, 1070))
        self.POCoodinates    = ((1190, 1043),(1275, 1070))
        self.ItemCoordinates = {"item1": (1130, 1000),
                                "item2": (1170, 1000),
                                "item3": (1220, 1000),
                                "item4": (1092, 1000),}
        self.TimeBeforeRespawnCoordinates = ((593, 1000),(631, 1024))
        self.ErrorCounter = 0
    
        self.JungleSpots = {"Baron": ((1735,882),(1745, 892)),
                            "Dragon": ((1820,986),(1830, 996)),
                            "Blue": ((1712,925), (1721,933)),
                            "Red": ((1690,919),(1698,930)),}
        
        self.JungleStatus = {"Baron": False,
                            "Dragon": False,
                            "Blue": False,
                            "Red": False,}
    def IfPlayerIsDead(self):
        self.update()
        if self.actualLife == 0:
            return True
        else:
            return False

    def UpdateJungle(self):
        # capture the screen and check if yellow is present in the image
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image),
                                cv2.COLOR_RGB2BGR)
        #crop the image to map
        # image = image[self.mapCoordinates[0][1]:self.mapCoordinates[1][1], self.mapCoordinates[0][0]:self.mapCoordinates[1][0]]
        for spot in self.JungleSpots:
            # crop the image
            croppedImage = image[self.JungleSpots[spot][0][1]:self.JungleSpots[spot][1][1], self.JungleSpots[spot][0][0]:self.JungleSpots[spot][1][0]]
            # convert to gray scale
            #croppedImage = cv2.cvtColor(np.array(croppedImage),
            #                           cv2.COLOR_RGB2BGR)
            # check if the (225,155,49) is present in the image
            if (225,155,49) in croppedImage:
                self.JungleStatus[spot] = True
            else:
                self.JungleStatus[spot] = False


        return self.JungleStatus

    def GetTimeBeforeRespawning(self):
        #capture the screen and extract the time before respawn
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image),
                                cv2.COLOR_RGB2BGR)
        # crop the image
        timeBeforeRespawn = image[self.TimeBeforeRespawnCoordinates[0][1]:self.TimeBeforeRespawnCoordinates[1][1], self.TimeBeforeRespawnCoordinates[0][0]:self.TimeBeforeRespawnCoordinates[1][0]]
        # convert to gray scale
        
        # extract the text
        text = pytesseract.image_to_string(timeBeforeRespawn, config='--psm 6')
        # convert to int
        try:
            text = int(text)
        except:
            text = 0
        return text




    def update(self):
        # capture the screen and extract the life and mana
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image),
                            cv2.COLOR_RGB2BGR)
        # crop the image
        map = image[self.mapCoordinates[0][1]:self.mapCoordinates[1][1], self.mapCoordinates[0][0]:self.mapCoordinates[1][0]]
        life = image[self.lifeCoordinates[0][1]:self.lifeCoordinates[1][1], self.lifeCoordinates[0][0]:self.lifeCoordinates[1][0]]
        mana = image[self.manaCoordinates[0][1]:self.manaCoordinates[1][1], self.manaCoordinates[0][0]:self.manaCoordinates[1][0]]
        po = image[self.POCoodinates[0][1]:self.POCoodinates[1][1], self.POCoodinates[0][0]:self.POCoodinates[1][0]]
        # convert to gray
        map = cv2.cvtColor(map, cv2.COLOR_BGR2GRAY)
        life = cv2.cvtColor(life, cv2.COLOR_BGR2GRAY)
        mana = cv2.cvtColor(mana, cv2.COLOR_BGR2GRAY)
        # apply thresholding to preprocess the image
        map = cv2.threshold(map, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        life = cv2.threshold(life, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        mana = cv2.threshold(mana, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        # extract the life and mana
        self.actualLife = pytesseract.image_to_string(life, config='--psm 6')
        self.actualMana = pytesseract.image_to_string(mana, config='--psm 6')
        self.actualPO = pytesseract.image_to_string(po, config='--psm 6')
        # remove spaces
        ElementToRemove = [".", " ", ";", "*", "-", ",", "{", "\n", "}", "(", ")", ":", "!", "?", ">", "<", "[", "]", "$", "ù", "|", "—", "©"]
        for element in ElementToRemove:
            self.actualLife = self.actualLife.replace(element, "")
            self.actualMana = self.actualMana.replace(element, "")
            self.actualPO = self.actualPO.replace(element, "")
        #replace O with 0 ect..
        letterToInt  = {"O": "0", "o": "0", "I": "1", "l": "1", "S": "5", "s": "5", "B": "8", "b": "8", "g": "9", "G": "6", "f": "/"}
        for letter in letterToInt:
            self.actualLife = self.actualLife.replace(letter, letterToInt[letter])
            self.actualMana = self.actualMana.replace(letter, letterToInt[letter])
        # convert to int*
        print(self.actualLife)
        print(self.actualMana)
        print(self.actualPO)

        try:
            self.actualMaxLife = int(self.actualLife.split("/")[1])
            self.actualMaxMana = int(self.actualMana.split("/")[1])
            self.actualLife = int(self.actualLife.split("/")[0])
            self.actualMana = int(self.actualMana.split("/")[0])
        except Exception as e:
            if e == ValueError:
                print("ValueError")
            else:
                print(e)
                print("Error")
            self.ErrorCounter += 1
            if self.ErrorCounter > 10:
                time.sleep(5)
                # that mean that the game is not in top 
                # so we need to wait for the game to be in top
            self.update()
        self.ErrorCounter = 0
        self.actualPO = int(self.actualPO)
    def GoToJglMob(self, mob):
        # go to the mob
        pyautogui.rightClick(self.JungleSpots[mob][0][0], self.JungleSpots[mob][0][1])
        pyautogui.click(self.JungleSpots[mob][0][0], self.JungleSpots[mob][0][1])
        # wait for
#test scrtipt

def LifeWarning(status):
    if status == 1:
        print("Life is low")
    else:
        print("Life is ok")
