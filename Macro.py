from tkinter import E
from LolAPI import LeagueOfLegendsCLIENT
import time
import pyautogui
import keyboard
if __name__ == "__main__":
    lol = LeagueOfLegendsCLIENT()
    time.sleep(5)
    while True:
        jngl = lol.UpdateJungle()

        #get keypress and do stuff
        if keyboard.is_pressed("1"):
            if jngl["Blue"] == 1:
                lol.GoToJglMob("Blue")
                
            else:
                print("Jungle has no Blue")
        if keyboard.is_pressed("2"):
            if jngl["Red"] == 1:
                print("Jungle has Red")
                lol.GoToJglMob("Red")
                
            else:
                print("Jungle has no Red")
        if keyboard.is_pressed("3"):
            if jngl["Dragon"] == 1:
                lol.GoToJglMob("Dragon")