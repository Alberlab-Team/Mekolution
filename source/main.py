# 0N17
import os
import pygame as pyg
import threading as th
import json
from typing import *
from settings_edit import *
import time
from math import *
from Vector import *

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


Settings = None
settings()
with open(tempVarfile, "r") as varFile:
    path = json.load(varFile)["setting_sheet_path"]
    if path is None:
        path = "source/config/pack1/jsonbasecontent.json"
    with open(path, "r") as SettingsFile:
        Settings = json.load(SettingsFile)

print(Settings)

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

class Sprite() :
    def __init__(self, surf : pyg.Surface) -> None:
        self.surf : pyg.Surface = functions.re_get_surf(surf)
        self.base_rect = self.surf.get_rect()
        self.pos = Vector2.V0()
        self.rect = self.base_rect

    def move(self, pos : Vector2):
        self.pos = pos
        self.rect = self.base_rect.move(pos.tuple())

    def collides(self, other:"Sprite"):
        return self.rect.colliderect(other.rect)
        

class JP():
    def __init__(self, caracteristics : JP_caracteristics = JP_caracteristics()) -> None:
        self.sprite = Sprite(functions.get_a_JP())
        self.sprite.move((main.screen_size/2) - (Vector2(self.sprite.base_rect.size)/2))
        self.caracteristics = caracteristics
        self.eaten = 0
        self.move_speed = 1

    def move(self, angle:float)-> None:
        self.sprite.move()
        pyg.Surface.convert


class main():

    if True: #Here are the global vars
        pyg.init()
        devise = pyg.display.Info()
        screen_width : int = devise.current_w
        screen_heigth : int = round(devise.current_h * 0.95)
        screen_size = Vector2((screen_width, screen_heigth))
        window = pyg.display.set_mode(screen_size.tuple())
        running = True

        KeyDown = []
        KeyUp = []
        Mouse = ["None", "None", "None"]

        wait_next_tick = th.Event()

        layers : Dict[str, Layer]
        Carrot_surf = pyg.transform.scale(pyg.image.load("source/picture/simulation/carrot.png"), (screen_width/45, screen_heigth/15))
        JP_surf = pyg.transform.scale(pyg.image.load("source/picture/simulation/JP.png"), (screen_width/45, screen_heigth/15))
        Buttons : Dict[str, button] = {}
        ActiveButtons : List[button] = []
        list_of_JP : List[JP] = []
        list_of_carrots : List[Sprite] = []

    def Start():
        if True : #Before while

            main.layers = {
                "buttons" : Layer(),
                "carrots" : Layer(),
                "JPs" : Layer(),
                "hutte" : Layer(),
            }
            hutte = pyg.transform.scale(pyg.image.load("source/picture/simulation/Hutte.png"), (main.screen_width/10, main.screen_heigth/10))
            hutte_rect = hutte.get_rect()
            hutte_rect.move_ip(((main.screen_size - Vector2(hutte.get_size()))//2).tuple())
            main.layers["hutte"].surf.blit(hutte, hutte_rect)

            main.list_of_JP.append(JP())
            JP_colliders : List[th.Thread] = []
            JP_colliders.append(th.Thread(target=main.JP_collider, args=(main.list_of_JP[-1],)))
            JP_colliders[-1].start()

        if True : # While Threads
            tick = th.Thread(target=main.ticking)
            tick.start()

            display = th.Thread(target=main.general_display)
            display.start()

            display_buttons = th.Thread(target=main.button_display)
            display_buttons.start()
            
            display_JP = th.Thread(target=main.JP_display)
            display_JP.start()

            display_carrots = th.Thread(target=main.carrot_display)
            display_carrots.start()

            #Remember that the following while is another thread, the main thread
            
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
                void_layer.surf.blit(this_JP.sprite.surf, this_JP.sprite.rect)
            main.layers["JPs"] = Layer()
            main.layers["JPs"].surf.blit(void_layer.surf, void_layer.rect)

    def carrot_display():
        while main.running:
            void_layer = Layer()
            for this_carrot in main.list_of_carrots:
                void_layer.surf.blit(this_carrot.surf, this_carrot.rect)
            main.layers["carrots"] = Layer()
            main.layers["carrots"].surf.blit(void_layer.surf, void_layer.rect)

    def ticking():
        while main.running:
            time.sleep(0.1)
            main.wait_next_tick.set()
            main.wait_next_tick.clear()

    def JP_collider(self : JP):
        while main.running:
            for i in range(main.list_of_carrots.__len__()):
                if self.sprite.collides(main.list_of_carrots[i]):
                    main.list_of_carrots.pop(i)
                    self.eaten +=1




class functions():
    def wait_for_ticks(time):
        for i in range(time):
            main.wait_next_tick.wait()

    def get_a_JP():
        return functions.re_get_surf(main.JP_surf)
    
    def re_get_surf(surf : pyg.Surface) -> pyg.Surface:
        result = pyg.Surface(surf.get_size(), pyg.SRCALPHA)
        result.blit(surf, surf.get_rect())
        return result

    def get_temp_var(path_of_value : List[str] = []) -> dict:
        global tempVarfile
        with open(tempVarfile, "r") as json_file:
            json_file_dict = json.load(json_file)
        wanted_value = json_file_dict
        for key in path_of_value:
            wanted_value = wanted_value[key]
        return wanted_value
    
    def update_temp_var(new : dict):
        global tempVarfile
        with open(tempVarfile, "w") as json_file:
            json.dump(new, json_file, indent=4)
    
    def quick_update_temp_var(new_value : any, path_of_value : List[str]):
        base_content = functions.get_temp_var()
        final_value = new_value
        for i in range(len(path_of_value)):
            value = base_content
            for j in range(len(path_of_value) - i -1):
                value = value[path_of_value[j]]
            value[path_of_value[-i-1]] = final_value
            final_value = value
        functions.update_temp_var(final_value)


main.Start()

try:
    os.remove(tempVarfile)
    print(f"deleted file : {tempVarfile}")
except:
    pass