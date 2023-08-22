# Boom! Bot x35r3000
## Python Scripts
The bot is divided into 4 different scripts, this helps to keep bugs under control and to manually check if each step was completed correctly. For every of these scripts you will have to manually log in to polycam after running the script.

### main.py
This code uploads all the dishes photos that are in the *selected photos folder to polycam and selects the correct configuration for each dish (Quality: reduced, Object Mask: True).
	The Selected photos folder should have **folders with the names of the dish and inside the photos of the respective dish.

*The path to the photos folder is passed as an argument when run the script with the console

**The name of the folder which contains the photos of the respective dish, is the name that will be used through the entire process 

### export.py
This code is to be run after the models have finished processing, it will export all the current models on polycam to the computer downloads folder in .glb format 

### rename.py
This will rename all the last exported models that are in the downloads folder and move them to the *selected folder.

*The path to the folder is passed as an argument when run the script with the console

### delete.py
This will delete all the models that are in polycam.
