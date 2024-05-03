# 0N17
import os
from PySide6.QtWidgets import QApplication
import sys
import pygame as pyg
import threading as th
import json
from typing import *
from settings_edit import *
import time

tempVarfile = "TempVar.json"

with open("source/config/pack1/devVar.json", "r")as f:
    Content = f.read()

try:
    os.remove(tempVarfile)
    print(f"deleted file : {tempVarfile}")
except:
    pass

with open(tempVarfile, "w+")as File:
    File.write(Content)

settings()

class vector2():

    def __init__(self, value : Tuple[float, float]) -> None:
        self.x = value[0]
        self.y = value[1]

    def V0() -> "vector2" :
        return vector2((0, 0))
    
    def tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def __add__(self, other : "vector2") :

        return vector2((self.x + other.x, self.y + other.y))

    def __sub__(self, other : "vector2") :

        return vector2((self.x - other.x, self.y - other.y))

    def __neg__(self):

        return vector2.V0() - self
    
    def __mul__(self, other : float) :

        return vector2((self.x * other, self.y * other))
    
    def __truediv__(self, other : float) :

        return vector2((self.x / other, self.y / other))
    
    def __floordiv__(self, other : float) :

        return vector2((self.x // other, self.y // other))

class button():
    def __init__(self, surf : pyg.surface,  rect : pyg.Rect, target : Callable[..., None], *args, **kwargs) -> None:
        self.surf = surf
        self.rect = rect

        self.target_if : Callable[..., None] = target
        self.args_if : tuple = args
        self.kwargs_if = kwargs

        self.target_else : Callable[..., None] = None
        self.args_else : tuple
        self.kwargs_else : dict

        self.thread = th.Thread(target = button._while, args=(self,))
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
        self.surf = pyg.Surface(main.screen_size.tuple(), pyg.SRCALPHA)
        self.rect = self.surf.get_rect()
    
    def add(self):
        main.window.blit(self.surf, self.rect)

class JP_caracteristics():
    def __init__(self) -> None:
        pass

class JP():
    def __init__(self, caracteristics : JP_caracteristics = JP_caracteristics()) -> None:
        self.surf = functions.get_a_JP()
        self.rect = self.surf.get_rect()
        self.caracteristics = caracteristics

    def move(self, pos : vector2):
        self.rect.move_ip(pos.tuple())

class main():

    if True: #Here are the global vars
        pyg.init()
        devise = pyg.display.Info()
        screen_width : int = devise.current_w
        screen_heigth : int = round(devise.current_h * 0.95)
        screen_size = vector2((screen_width, screen_heigth))
        window = pyg.display.set_mode(screen_size.tuple())
        running = True

        KeyDown = []
        KeyUp = []
        Mouse = ["None", "None", "None"]

        wait_next_tick = th.Event()

        layers : Dict[str, Layer]

        JP_surf = pyg.transform.scale(pyg.image.load("source/picture/simulation/JP.png"), (screen_width/45, screen_heigth/15))
        Buttons : Dict[str, button] = {}
        ActiveButtons : List[button] = []
        list_of_JP : List[JP] = []

        #with open("source/")

    def Start():
        if True : #Before while

            main.layers = {
                "buttons" : Layer(),
                "hutte" : Layer(),
                "JPs" : Layer()
            }
            
            hutte = pyg.transform.scale(pyg.image.load("source/picture/simulation/Hutte.png"), (main.screen_width/10, main.screen_heigth/10))
            hutte_rect = hutte.get_rect()
            hutte_rect.move_ip(((main.screen_size - vector2(hutte.get_size()))//2).tuple())
            main.layers["hutte"].surf.blit(hutte, hutte_rect)

            if True : #Threads
                tick = th.Thread(target=main.ticking)
                tick.start()

                display = th.Thread(target=main.general_display)
                display.start()

                display_buttons = th.Thread(target=main.button_display)
                display_buttons.start()
                
                display_JP = th.Thread(target=main.JP_display)
                display_JP.start()

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
            main.window.fill((115, 192, 21))
            for key in list(main.layers.keys()):
                main.layers[key].add()
            pyg.display.flip()
            main.wait_next_tick.wait()   
    
    def button_display():
        while main.running:
            void_layer = Layer()
            for this_button in main.ActiveButtons:
                void_layer.surf.blit(this_button.surf, this_button.rect)
            main.layers["buttons"] = Layer()
            main.layers["buttons"].surf.blit(void_layer.surf, void_layer.rect)

    def JP_display():
        while main.running:
            void_layer = Layer()
            for this_JP in main.list_of_JP:
                void_layer.surf.blit(this_JP.surf, this_JP.rect)
            main.layers["JPs"] = Layer()
            main.layers["JPs"].surf.blit(void_layer.surf, void_layer.rect)

    def ticking():
        while main.running:
            time.sleep(0.1)
            main.wait_next_tick.set()

class functions():
    def wait_for_ticks(time):
        for i in range(time):
            main.wait_next_tick.wait()

    def get_a_JP():
        JP = pyg.Surface(main.JP_surf.get_size(), pyg.SRCALPHA)
        JP.blit(main.JP_surf, main.JP_surf.get_rect())
        return JP

main.Start()

try:
    os.remove(tempVarfile)
    print(f"deleted file : {tempVarfile}")
except:
    pass