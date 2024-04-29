# Mekolution

## Intro

 Mekolution is a simulation of the evolution of the comportement of species in a little world.

## The code

### The Core (main.py)

The code has a base called the core which use for after implement mecanics. The core is the base of the code and it's content is write in the specifications (Cahier des charges), for more information go in the folder "Specifications". 

0N17 : Sometimes you can find "if True:" in the code. It may look strange, but I need it to hide the following code in the editor.

Developper : 0N17

### The Configuration

The code read in a json called "settings.json" for get the information necessary for it operation. The settings can be edit with "settings_edit.py" which is a simple interface to edit the json.

```json
{
	"speed" : 1
}
```

Developper : SkyDeveloppement

### The Mecanics

The mecanics are the rules or addons of the core like the implementation of a cow which can be killed by two individu and these individu can be share this cow with equal portion or not ...
