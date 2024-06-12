# 0N17
import os
import pygame as pyg
import threading as th
import json
from typing import *
from settings_edit import *
import time
from math import *
import math
from Vector import *
import random
import copy

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
        self.surplus=Vector2(self.surf.get_size())//2
        self.pos = Vector2.V0()
        self.base_rect = self.surf.get_rect()
        self.rect = self.base_rect.move((self.pos-self.surplus).tuple())

    def move(self, pos : Vector2):
        self.pos = pos
        self.rect = self.base_rect.move((self.pos-self.surplus).tuple())

    def move_of(self, deplcement : Vector2):
        self.move(deplcement + self.pos)

    def collides(self, other:"Sprite"):
        return self.rect.colliderect(other.rect)
      
class JP():
    def __init__(self, caracteristics : JP_caracteristics = JP_caracteristics()) -> None:
        self.sprite = Sprite(functions.get_a_JP())
        self.sprite.move((main.screen_size/2) - (Vector2(self.sprite.base_rect.size)/2))
        self.caracteristics = caracteristics
        self.eaten = 0
        self.move_speed = main.screen_size.norm()/100 * Settings["speed"]
        self.alive = True
        main.JP_colliders.append(th.Thread(target=TertiaryThreads.JP_collider, args=(self,)))
        main.JP_colliders[-1].start()
        main.JP_brains.append(th.Thread(target=TertiaryThreads.JP_brain, args=(self,)))
        main.JP_brains[-1].start()


    def move(self, angle:float)-> None:
        pos = Vector2(cos(angle * pi/360), sin(angle * pi/360))*self.move_speed
        self.sprite.move_of(pos)

    def move_to(self, pos:Vector2)->None:
        x = pos.x - self.sprite.pos.x
        y = pos.y - self.sprite.pos.y
        if x == y == 0:
            return None
        hyp = sqrt((x**2) + (y**2))
        ratio = self.move_speed/hyp
        Vector = Vector2((x * ratio, y * ratio))
        self.sprite.move_of(Vector)


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

        hutte = pyg.transform.scale(pyg.image.load("source/picture/simulation/Hutte.png"), (screen_width/8, screen_heigth//7))
        hutte_rect = hutte.get_rect()
        hutte_pos = screen_size//2
        hutte_rect.move_ip(((screen_size - Vector2(hutte.get_size()))//2).tuple())

        layers : Dict[str, Layer]
        Carrot_surf = pyg.transform.scale(pyg.image.load("source/picture/simulation/carrot.png"), (screen_width/45, screen_heigth/15))
        JP_surf = pyg.transform.scale(pyg.image.load("source/picture/simulation/JP.png"), (screen_width/45, screen_heigth/15))
        Buttons : Dict[str, button] = {}
        ActiveButtons : List[button] = []
        list_of_JP : List[JP] = []
        list_of_carrots : List[Sprite] = []
        JP_colliders : List[th.Thread] = []
        JP_brains : List[th.Thread] = []

        hour : str = "day"
        filter_names:Dict[str, Tuple[int, int, int]]={
            "Dark" : (0  , 0  , 0  , 127),
            "Clear": (255, 255, 255, 127),
            "Night": (0  , 0  , 64 , 127),
            "Dawn" : (255, 183, 111, 63 ),
        }
        filters:Dict[Tuple[int, int, int], bool]={}
        for key in list(filter_names.keys()):
            filters[filter_names[key]]=False
    def Start():
        if True : #Before while

            main.layers = {
                "buttons" : Layer(),
                "carrots" : Layer(),
                "JPs" : Layer(),
                "hutte" : Layer(),
            }
            main.layers["hutte"].surf.blit(main.hutte, main.hutte_rect)

            main.list_of_JP.append(JP())

        if True : # While Threads
            tick = th.Thread(target=SecondaryThreads.ticking)
            tick.start()

            display = th.Thread(target=SecondaryThreads.general_display)
            display.start()

            display_buttons = th.Thread(target=SecondaryThreads.button_display)
            display_buttons.start()
            
            display_JP = th.Thread(target=SecondaryThreads.JP_display)
            display_JP.start()

            display_carrots = th.Thread(target=SecondaryThreads.carrot_display)
            display_carrots.start()

            if Settings["carrots"]["activated"]:
                carrot_summon = th.Thread(target=SecondaryThreads.carrot_summon)
                carrot_summon.start()

            night = th.Thread(target=SecondaryThreads.hour_gestionnary)
            night.start()

            #Remember that the following while is another thread, the main thread
            
        while main.running : 
            main.wait_next_tick.wait()
            if True: #interactions
                main.KeyDown = []
                main.KeyUp = []
                for event in pyg.event.get():
                    if event.type == pyg.QUIT:
                        main.running = False
                        print("end")
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
            

class SecondaryThreads():

    def general_display():
        while main.running:
            main.wait_next_tick.wait()  
            main.window.fill((115, 192, 21))
            for key in list(main.layers.keys()):
                main.layers[key].add()
            for key in list(main.filters.keys()):
                if main.filters[key]:
                    functions.apply_filter(key)
            pyg.display.flip()
    
    def button_display():
        while main.running:
            main.wait_next_tick.wait()
            void_layer = Layer()
            for this_button in main.ActiveButtons:
                void_layer.surf.blit(this_button.surf, this_button.rect)
            main.layers["buttons"] = Layer()
            main.layers["buttons"].surf.blit(void_layer.surf, void_layer.rect)

    def JP_display():
        while main.running:
            main.wait_next_tick.wait()
            void_layer = Layer()
            for this_JP in main.list_of_JP:
                void_layer.surf.blit(this_JP.sprite.surf, this_JP.sprite.rect)
            main.layers["JPs"] = Layer()
            main.layers["JPs"].surf.blit(void_layer.surf, void_layer.rect)

    def carrot_display():
        while main.running:
            main.wait_next_tick.wait()
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

    def carrot_summon():
        while main.running:
            main.wait_next_tick.wait()
            if main.list_of_carrots.__len__()<Settings["carrots"]["max number"]:
                functions.wait_for_ticks(Settings["carrots"]["ticks before new"] - 1)
                functions.Summon_A_Carrot()

    def hour_gestionnary():
        while main.running:
            main.wait_next_tick.wait()
            if main.hour == "day":
                functions.wait_for_ticks(Settings["day time"])
                main.hour = "night"
            elif main.hour == "night":
                functions.activate_filter(main.filter_names["Night"])
                functions.wait_for_ticks(Settings["night time"])
                functions.reproduction()
                functions.unactivate_filter(main.filter_names["Night"])
                main.hour = "dawn"
            elif main.hour == "dawn":
                functions.activate_filter(main.filter_names["Dawn"])
                functions.wait_for_ticks(Settings["dawn time"])
                functions.unactivate_filter(main.filter_names["Dawn"])
                main.hour = "day"


class TertiaryThreads():
    def JP_collider(self : JP):
        while main.running and self.alive:
            main.wait_next_tick.wait()
            for i in range(main.list_of_carrots.__len__()):
                try :
                    if self.sprite.collides(main.list_of_carrots[i]):
                        main.list_of_carrots.pop(i)
                        self.eaten += Settings["carrots"]["food points"]
                except IndexError:
                    break

    def JP_brain(self : JP):
        random_objective = functions.Generate_Random_Pos(Vector2((150,100)), main.screen_size, True)
        while main.running and self.alive:
            main.wait_next_tick.wait()
            if main.hour == "day":
                objective = functions.Get_the_closest_food(self.sprite.pos)
            elif main.hour == "night":
                objective = main.hutte_pos
            elif main.hour == "dawn":
                objective = random_objective
            self.move_to(objective)



class functions():
    def wait_for_ticks(time):
        for i in range(time):
            if main.running:
                main.wait_next_tick.wait()
            else:
                break

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

    def Generate_Random_Pos(cases : Vector2, final_size : Union[Vector2, None] = None, rounded : bool = False, only_edges : bool = False)->Vector2:
        if only_edges:
            if random.random() <= cases.x/(cases.y+cases.x): # Positives_issues/total_issues.
                x = random.randint(0, cases.x-1)
                y = random.choice([0, cases.y-1])
            else:
                y = random.randint(0, cases.y-1)
                x = random.choice(0, cases.x-1)
        else:
            x = random.randint(0, cases.x-1)
            y = random.randint(0, cases.y-1)
        if final_size is None:
            returned = Vector2([x,y])
        else:
            returned = Vector2([x*final_size.x/cases.x, y*final_size.y/cases.y])
        if rounded:
            returned.x = round(returned.x)
            returned.y = round(returned.y)
        return returned

    def Summon_A_Carrot(pos : Union[Vector2, None] = None):
        if pos is None:
            pos = functions.Generate_Random_Pos(Vector2((150, 100)), main.screen_size, True)
        main.list_of_carrots.append(Sprite(functions.re_get_surf(main.Carrot_surf)))
        main.list_of_carrots[-1].move(pos)

    def Get_the_closest_food(pos : Vector2)->Vector2:
        closest : float = -1
        saved : Vector2 = pos
        for carrot in main.list_of_carrots:
            dist = carrot.pos.dist(pos)
            if closest > dist or closest == -1:
                closest = dist
                saved = carrot.pos
        return copy.deepcopy(saved)

    def activate_filter(key : Tuple[int, int, int]):
        main.filters[key] = True
    
    def unactivate_filter(key : Tuple[int, int, int]):
        main.filters[key] = False

    def apply_filter(key : Tuple[int, int, int]):
        surf = pyg.Surface(main.screen_size.tuple())
        surf.fill(key)
        surf.set_alpha(key[3])
        rect = surf.get_rect()
        main.window.blit(surf, rect)

    def reproduction():
        for i in range(main.list_of_JP.__len__()):
            try : 
                jp = main.list_of_JP[i]
            except IndexError:
                break
            if jp.eaten > Settings["food"]["to survive"]:
                jp.eaten -= Settings["food"]["to survive"]
                child_number = jp.eaten//Settings["food"]["to reproduce"]
                jp.eaten -= child_number * Settings["food"]["to reproduce"]
                for j in range(child_number):
                    main.list_of_JP.append(JP())
                jp.eaten = 0
            else:
                jp.alive = False
                main.list_of_JP.pop(i)
                main.JP_brains.pop(i)
                main.JP_colliders.pop(i)
                del jp


main.Start()

try:
    os.remove(tempVarfile)
    print(f"deleted file : {tempVarfile}")
except:
    pass