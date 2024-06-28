# 0N17 --> the best dev :)

#region import
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
from data_viewer import RepresentFileApp
# endregion

# region top
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
app = settings()

with open(tempVarfile, "r") as varFile:
    path = json.load(varFile)["setting_sheet_path"]
    if path is None:
        path = "source/config/pack1/jsonbasecontent.json"
    with open(path, "r") as SettingsFile:
        Settings = json.load(SettingsFile)

#print(Settings)
# endregion


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
        main.unsized_window.blit(self.surf, self.rect)

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

    def move_of(self, deplacement : Vector2, max : float | None=None):
        x = deplacement.x
        y = deplacement.y
        if x == y == 0:
            return None
        if max is not None:
            hyp = sqrt((x**2) + (y**2))
            if hyp > max:
                ratio = max/hyp
                deplacement.x *= ratio
                deplacement.y *= ratio
        self.move(deplacement + self.pos)

    def move_angle(self, angle, norm):
        pos = Vector2(cos(angle * pi/360), sin(angle * pi/360))*norm
        self.move_of(pos)

    def collides(self, other:"Sprite"):
        return self.rect.colliderect(other.rect)


class Cow(Sprite):
    def __init__(self, index) -> None:
        super().__init__(main.Cow_surf)
        self.imobilisated = False
        self.brain_move_thread= th.Thread(target=TertiaryThreads.cow_brain_move, args=(self,))
        self.brain_move_thread.start()
        self.brain_collide_thread= th.Thread(target=TertiaryThreads.cow_brain_collides_JP, args=(self,))
        self.brain_collide_thread.start()
        self.index = index
    
    def __del__(self):
        try:
            #print("don't worry if an threading error apear before 1 or 2 second") #because it will destroy some threads
            del self.brain_thread
            del self.brain_move_thread
        except:pass

class JP_caracteristics():
    def __init__(self) -> None:
        self.selfishness = Settings["selfishness"]["base selfishness"]

    def modify(self, base : 'JP_caracteristics'):
        self.selfishness = min(max(base.selfishness + random.choice([-10, 10]), 0), 100)

class JP():
    def __init__(self, caracteristics : JP_caracteristics | None = None) -> None:
        if caracteristics is None :
            self.caracteristics = JP_caracteristics()
        else:
            self.caracteristics = caracteristics
        self.sprite = Sprite(functions.get_a_JP())
        self.sprite.move((main.screen_size/2) - (Vector2(self.sprite.base_rect.size)/2))#
        self.eaten = 0
        self.move_speed = main.screen_size.norm()/200 * Settings["JP speed"]#
        self.alive = True
        self.occuped = False
        main.JP_colliders.append(th.Thread(target=TertiaryThreads.JP_collider, args=(self,)))
        main.JP_colliders[-1].start()
        main.JP_brains.append(th.Thread(target=TertiaryThreads.JP_brain, args=(self,)))
        main.JP_brains[-1].start()


    def move(self, angle:float)-> None:
        self.sprite.move_angle(angle, self.move_speed)

    def move_to(self, pos:Vector2)->None:
        self.sprite.move_of(pos - self.sprite.pos, self.move_speed)


class main(): # Global_Vars
    pyg.init()
    devise = pyg.display.Info()
    screen_width : int = 1600
    screen_heigth : int = 900
    screen_size = Vector2((screen_width, screen_heigth))
    unsized_window = pyg.Surface(screen_size.tuple())
    window = pyg.display.set_mode((devise.current_w, devise.current_h // 1.1), pyg.RESIZABLE)
    running = True

    window_color = (115, 192, 21)

    KeyDown = []
    KeyUp = []
    Mouse = ["None", "None", "None"]

    wait_next_tick = th.Event()

    hutte = pyg.transform.scale(pyg.image.load("source/picture/simulation/Hutte.png"), (screen_width/16, screen_heigth//14))
    hutte_rect = hutte.get_rect()
    hutte_pos = screen_size//2 #
    hutte_rect.move_ip(((screen_size - Vector2(hutte.get_size()))//2).tuple())#

    layers : Dict[str, Layer]
    Carrot_surf = pyg.transform.scale(pyg.image.load("source/picture/simulation/carrot.png"), (screen_width/90, screen_heigth/30))
    Cow_surf = pyg.transform.scale(pyg.image.load("source/picture/simulation/cow.png"), (screen_width/40, screen_heigth/20))
    JP_surf = pyg.transform.scale(pyg.image.load("source/picture/simulation/JP.png"), (screen_width/90, screen_heigth/30))
    Buttons : Dict[str, button] = {}
    ActiveButtons : List[button] = []
    list_of_JP : List[JP] = []
    free_JPs = 1
    list_of_carrots : List[Sprite] = []
    list_of_cows : List[Cow | None] = []
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

    writing_temp_var = False
    temp_var = {}


def Start():
    # region Before_whiles
    main.layers = {
        "buttons" : Layer(),
        "carrots" : Layer(),
        "cows" : Layer(),
        "JPs" : Layer(),
        "hutte" : Layer(),
    }
    main.layers["hutte"].surf.blit(main.hutte, main.hutte_rect)

    main.list_of_JP.append(JP())
    # endregion

    # region While_Threads
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

    display_cow = th.Thread(target=SecondaryThreads.cow_display)
    display_cow.start()

    if Settings["carrots"]["activated"]:
        carrot_summon = th.Thread(target=SecondaryThreads.carrot_summon)
        carrot_summon.start()

    if Settings["selfishness"]["activated"]:
        cow_summon = th.Thread(target=SecondaryThreads.cow_summon)
        cow_summon.start()

    time_bot = th.Thread(target=SecondaryThreads.hour_gestionnary)
    time_bot.start()

    free_JPs_getter = th.Thread(target=SecondaryThreads.get_free_JPs)
    free_JPs_getter.start()

    InfoDisplay = th.Thread(target=SecondaryThreads.display_data)
    InfoDisplay.start()
    #endregion
        
    while main.running :# Remember that the following while is another thread, the main thread 
            main.wait_next_tick.wait()
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
            main.unsized_window.fill(main.window_color)
            for key in list(main.layers.keys()):
                main.layers[key].add()
            for key in list(main.filters.keys()):
                if main.filters[key]:
                    functions.apply_filter(key)
            main.window.blit(pyg.transform.scale(main.unsized_window, main.window.get_size()), (0,0))
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

    def cow_display():
        while main.running:
            main.wait_next_tick.wait()
            void_layer = Layer()
            for this_cow in main.list_of_cows:
                if this_cow is not None:
                    void_layer.surf.blit(this_cow.surf, this_cow.rect)
            main.layers["cow"] = Layer()
            main.layers["cow"].surf.blit(void_layer.surf, void_layer.rect)

    def ticking():
        while main.running:
            time.sleep(0.09)
            main.wait_next_tick.set()
            main.wait_next_tick.clear()

    def carrot_summon():
        while main.running:
            main.wait_next_tick.wait()
            if main.list_of_carrots.__len__()<Settings["carrots"]["max number"]:
                functions.wait_for_ticks(Settings["carrots"]["ticks before new"] - 1)
                functions.Summon_A_Carrot()

    def cow_summon():
        def Wait():
            functions.wait_for_ticks(Settings["selfishness"]["cows"]["ticks before new"] - 1)

        while main.running:
            main.wait_next_tick.wait()
            if main.list_of_cows.__len__()<Settings["selfishness"]["cows"]["max number"]:
                functions.Summon_A_Cow()
                Wait()
            elif None in main.list_of_cows:
                index = main.list_of_cows.index(None)
                functions.Summon_A_Cow(index = index, replace = True)
                Wait()

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
                functions.save_dev_vars()
                try:
                    RepresentFileApp._instance.display_json()
                except:...
                functions.unactivate_filter(main.filter_names["Night"])
                main.hour = "dawn"
            elif main.hour == "dawn":
                functions.activate_filter(main.filter_names["Dawn"])
                functions.wait_for_ticks(Settings["dawn time"])
                functions.unactivate_filter(main.filter_names["Dawn"])
                main.hour = "day"

    def get_free_JPs():
        while main.running:
            main.wait_next_tick.wait()
            free = 0
            for jp in main.list_of_JP:
                free += not jp.occuped
            main.free_JPs = free

    def display_data():
        RepresentFileApp(tempVarfile).mainloop()


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
            occuped = False
            for i in range(main.list_of_cows.__len__()):
                try:
                    if main.list_of_cows[i] is not None:
                        if self.sprite.collides(main.list_of_cows[i]):
                            occuped = True
                except IndexError:
                    break
            self.occuped = occuped

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

    def cow_brain_move(self : Cow):
        set_objective = True
        objective : Vector2
        while main.running:
            main.wait_next_tick.wait()
            if set_objective:
                objective = functions.Generate_Random_Pos(Vector2((150, 100)), main.screen_size, True)
                set_objective = False
            if not self.imobilisated:
                self.move_of(objective - self.pos, Settings["selfishness"]["cows"]["move speed"] * main.screen_size.norm()/200)
            if self.rect.collidepoint(objective.tuple()):
                set_objective = True
    
    def cow_brain_collides_JP(self : Cow):
        running = True
        while main.running and running:
            main.wait_next_tick.wait()
            indexs : List[int] = []
            collided = 0
            for i in range(main.list_of_JP.__len__()):
                jp = main.list_of_JP[i]
                if self.collides(jp.sprite):
                    collided += 1
                    indexs.append(i)
                    if collided == 2:
                        break
            if collided == 0:
                self.imobilisated = False
            elif collided == 1:
                self.imobilisated = True
            elif collided == 2:
                jp1 = main.list_of_JP[indexs[0]]
                jp2 = main.list_of_JP[indexs[1]]

                jp1_selfishness = jp1.caracteristics.selfishness
                jp2_selfishness = jp2.caracteristics.selfishness

                inter = jp1_selfishness + jp2_selfishness - 100
                if inter >= 0:
                    jp1.eaten += jp1_selfishness - inter # total collected = eaten 1 +  2
                    jp2.eaten += jp2_selfishness - inter # = selfish 1 + 2 - inter - inter = 100 - inter.
                else :
                    jp1.eaten += jp1_selfishness - (inter / 2) # inter is negative, so it's -rest
                    jp2.eaten += jp2_selfishness - (inter / 2) # so it give a half of rest to one and rest to other
                main.list_of_cows[self.index] = None #Replace the cow by a None
                self.__del__()#normally it auto destroys the object, where is this Thread, but it's better as that
                running = False# to be sure, so normally this is never called


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

    def Generate_Random_Pos(cases : Vector2, final_size : Vector2 | None = None, rounded : bool = False, only_edges : bool = False)->Vector2:
        if only_edges:
            if random.random() <= cases.x/(cases.y+cases.x): # Positives_issues/total_issues.
                x = random.randint(0, cases.x-1)
                y = random.choice([0, cases.y-1])
            else:
                y = random.randint(0, cases.y-1)
                x = random.choice([0, cases.x-1])
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

    def Summon_A_Carrot(pos : Vector2 | None = None):
        if pos is None:
            pos = functions.Generate_Random_Pos(Vector2((150, 100)), main.screen_size, True)
        main.list_of_carrots.append(Sprite(functions.re_get_surf(main.Carrot_surf)))
        main.list_of_carrots[-1].move(pos)

    def Summon_A_Cow(pos : Vector2 | None = None, index : int | None = None, replace : bool = False): 
        if index == None:
            index = main.list_of_cows.__len__()
        if pos is None:
            pos = functions.Generate_Random_Pos(Vector2((150, 100)), main.screen_size, True, True)
        if replace:
            main.list_of_cows[index] = Cow(index)
        else:
            main.list_of_cows.insert(index, Cow(index))
        main.list_of_cows[index].move(pos)

    def Get_the_closest_food(pos : Vector2)->Vector2:
        closest : float = -1
        saved : Vector2 = pos
        for carrot in main.list_of_carrots:
            dist = carrot.pos.dist(pos) /Settings["carrots"]["interst"]
            if closest > dist or closest == -1:
                closest = dist
                saved = carrot.pos
        if main.free_JPs >= 2:
            for cow in main.list_of_cows:
                if cow is not None:
                    dist = cow.pos.dist(pos) /Settings["selfishness"]["cows"]["interst"]
                    if closest > dist or closest == -1:
                        closest = dist
                        saved = cow.pos

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
        main.unsized_window.blit(surf, rect)

    def reproduction():
        for i in range(main.list_of_JP.__len__()):
            try : 
                jp = main.list_of_JP[i]
            except IndexError:
                break
            if jp.eaten > Settings["food"]["to survive"]:
                jp.eaten -= Settings["food"]["to survive"]
                child_number = round(jp.eaten//Settings["food"]["to reproduce"])
                jp.eaten -= child_number * Settings["food"]["to reproduce"]
                for j in range(child_number):
                    if Settings["maximum of JP"] > main.list_of_JP.__len__():
                        new_JP = JP()
                        new_JP.caracteristics.modify(jp.caracteristics)
                        main.list_of_JP.append(new_JP)
                jp.eaten = 0
            else:
                jp.alive = False
                main.list_of_JP.pop(i)
                main.JP_brains.pop(i)
                main.JP_colliders.pop(i)
                del jp
        if main.list_of_JP.__len__() == 0:
            main.running = False

    def save_dev_vars():
        class caracteristic_of_jp:
            def __init__(self, name : str) -> None:
                self.name = name
                self.values : List[int] = []
                self.average : float | None = 0.0
                self.median : float | None = 0.0
                self.variance : float | None = 0.0
                self.calc()

            def calc(self):

                self.values = []
                for jp in main.list_of_JP:           #List of values
                    self.values.append(getattr(jp.caracteristics, self.name, None))

                lenght = self.values.__len__()

                if lenght == 0:
                    self.average = None
                    self.median = None      #No Stats
                    self.variance = None
                else:
                    self.average = sum(self.values)/lenght   #Average
                
                    median_index = (lenght-1)/2
                    if median_index == (lenght-1)//2:
                        self.median = self.values[round(median_index)]         #Median
                    else:
                        self.median = (sum(self.values[floor(median_index): ceil(median_index)+1]))/2 

                    self.variance = 0.0
                    for value in self.values:                       #variance
                        self.variance += (value - self.average)**2
                    self.variance /= lenght

            def get_dict(self) -> dict:
                self.calc()
                returned : dict = {
                    "list": self.values,
                    "average" : self.average,
                    "median" : self.median,
                    "variance" : self.variance,
                }
                return returned

        selfishness = caracteristic_of_jp("selfishness")

        with open(tempVarfile, "r") as File_r:
            File_r = json.load(File_r)
                
            File_r["selfishness"] = selfishness.get_dict()

            main.temp_var = File_r
            main.writing_temp_var = True
            with open(tempVarfile, "w") as File_w:
                json.dump(File_r, File_w, indent=4)
            main.writing_temp_var = False

# region bottom
Start()
for thread in th.enumerate():
    del thread
    
RepresentFileApp._instance.running = False

try:
    os.remove(tempVarfile)
    print(f"deleted file : {tempVarfile}")
except:
    pass

# endregion
