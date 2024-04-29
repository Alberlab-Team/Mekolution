# Note

## Introduction

Les notes servent aux développeurs pour écrire les problèmes ou des information utile pour les autres développeurs.

## Core Note

Pour la couleurs de l'herbe j'ai trouvé cette couleur sympa je te laisse en jugé : rgb(115, 192, 21), HEX : #73c015

J'ai fais ce code aussi qui fait un dégradé sur la couleur : 

```python
# 0N17

import pygame as pyg
import threading as th
import json
from typing import *
import settings_edit


class main:
    if True:  # Ici sont les variables globales
        pyg.init()
        devise = pyg.display.Info()
        screen_width: int = devise.current_w
        screen_height: int = round(devise.current_h * 0.95)
        screen_size = (screen_width, screen_height)
        window = pyg.display.set_mode(screen_size)
        # Création d'une surface pour le dégradé
        gradient_surface = pyg.Surface(screen_size)
        start_color = (40, 140, 33)
        end_color = (154, 192, 0)
        for y in range(screen_height):
            t = y / screen_height
            r = start_color[0] + (end_color[0] - start_color[0]) * t
            g = start_color[1] + (end_color[1] - start_color[1]) * t
            b = start_color[2] + (end_color[2] - start_color[2]) * t
            pyg.draw.line(gradient_surface, (int(r), int(g), int(b)), (0, y), (screen_width, y))
        running = True

        KeyDown = []
        KeyUp = []
        Mouse = ("None", "None", "None")
    def Start():
        if True : #Before while
            if True : #Threads
                pass
        while main.running :
            # Mettre à jour la logique du jeu...

            # Blitter la surface du dégradé sur la fenêtre principale
            main.window.blit(main.gradient_surface, (0, 0))

            # Mettre à jour l'affichage
            pyg.display.flip()
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
```

## Json Editor Note
