# 0N17

import pygame as pyg
import threading as th
import json
from typing import *
import settings_edit


class main:
    if True: #Here are the global vars
        pyg.init()
        devise = pyg.display.Info()
        screen_width : int = devise.current_w
        screen_heigth : int = round(devise.current_h * 0.95)
        screen_size = (screen_width, screen_heigth)
        window = pyg.display.set_mode(screen_size)
        running = True

        KeyDown = []
        KeyUp = []
        Mouse = ("None", "None", "None")
    def Start():
        if True : #Before while
            if True : #Threads
                pass
        while main.running : 
            if True: #interactions
                for event in pyg.event.get():
                    if event.type == pyg.QUIT:
                        main.running = False
                    elif event.type == pyg.KEYDOWN:
                        main.Keys.append(event.key)
                        main.key_down.append(event.key)
                    elif event.type == pyg.KEYUP:
                        main.Keys.remove(event.key)
                    elif event.type == pyg.MOUSEBUTTONDOWN:
                        if event.button == 1 :
                            main.clics_souris[0] = "down"
                        elif event.button == 3 :
                            main.clics_souris[1] = "down"
                        main.key_down.append(event.button)
                    elif event.type == pyg.MOUSEBUTTONUP:
                        if event.button == 1 :
                            main.clics_souris[0] = "up"
                        elif event.button == 3 :
                            main.clics_souris[1] = "up"
            
            pyg.display.flip()


main.Start()