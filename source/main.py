# 0N17

from PySide6.QtWidgets import QApplication
import sys
import pygame as pyg
import threading as th
import json
from typing import *
from settings_edit import *
import time

settings()

print("cc")

class bouton() :
    def __init__(self, rect : pyg.Rect, target : Callable[..., None], *args, **kwargs) -> None:
        self.rect = rect

        self.target_if : Callable[..., None] = target
        self.args_if : tuple = args
        self.kwargs_if = kwargs

        self.target_else : Callable[..., None] = None
        self.args_else : tuple
        self.kwargs_else : dict

        self.thread = th.Thread(target = bouton._while, args=(self,))
        self.thread.start()

    def _while(self):
        while main.running:
            if main.clics_souris[0] == "down" and self.rect.collidepoint(main.s_x, main.s_y):
                self.target_if(*self.args_if, **self.kwargs_if)
            elif self.target_else is not None:
                self.target_else(*self.args_else, **self.kwargs_else)
            main.wait_next_tick.wait()

    def set_if(self, target : Callable[..., None], *args, **kwargs):
        self.target_if = target
        self.args_if = args
        self.kwargs_if = kwargs

    def set_else(self, target : Callable[..., None], *args, **kwargs):
        self.target_else = target
        self.args_else = args
        self.kwargs_else = kwargs

class Layer():
    def __init__(self) -> None:
        self.surf = pyg.Surface(main.screen_size, pyg.SRCALPHA)
        self.rect = self.surf.get_rect()
    
    def add(self):
        main.window.blit(self.surf, self.rect)

class main():

    if True: #Here are the global vars
        #settings_edit.settings()
        pyg.init()
        devise = pyg.display.Info()
        screen_width : int = devise.current_w
        screen_heigth : int = round(devise.current_h * 0.95)
        screen_size = (screen_width, screen_heigth)
        window = pyg.display.set_mode(screen_size)
        running = True

        KeyDown = []
        KeyUp = []
        Mouse = ["None", "None", "None"]

        wait_next_tick = th.Event()

        layers : Dict[str, Layer]
    
    
    def Start():

        if True : #Before while

            main.layers = {
                "void" : Layer()
            }

            if True : #Threads
                tick = th.Thread(target=main.ticking)
                tick.start()

                display = th.Thread(target=main.general_display)
                display.start()




        while main.running : 

            if True: #interactions
                main.KeyDown = []
                main.KeyUp = []
                for event in pyg.event.get():
                    if event.type == pyg.QUIT:
                        main.running = False
                    elif event.type == pyg.KEYDOWN:
                        main.KeyDown.append(event.key)
                        main.KeyDown.append(event.key)
                    elif event.type == pyg.KEYUP:
                        main.KeyUp.append(event.key)
                    elif event.type == pyg.MOUSEBUTTONDOWN:
                        if event.button == 1 :
                            main.Mouse[0] = "down"
                        elif event.button == 3 :
                            main.Mouse[1] = "down"
                        main.KeyDown.append(event.button)
                    elif event.type == pyg.MOUSEBUTTONUP:
                        if event.button == 1 :
                            main.Mouse[0] = "up"
                        elif event.button == 3 :
                            main.Mouse[1] = "up"
                        main.KeyUp.append(event.button)
                        
            main.wait_next_tick.wait()

    def general_display():
        while main.running:
            main.window.fill((35, 175, 59))
            for key in list(main.layers.keys()):
                main.layers[key].add()
            pyg.display.flip()
            main.wait_next_tick.wait()   
    
    def ticking():
        while main.running:
            time.sleep(0.1)
            main.wait_next_tick.set()

class functions():
    def wait_for_ticks(time):
        for i in range(time):
            main.wait_next_tick.wait()


main.Start()
