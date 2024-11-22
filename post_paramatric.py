#!/usr/bin/python
import sys
import re
import os

#argument: filename, command to be replaced/added, start val, increment
# arg example: 
# C:\\Users\\tony4\\AppData\\Local\\Programs\\Python\\Python313\\python.exe D:\\3d_print\\Qidi\\calibration\\post_paramatric.py -c "M106 P2 S0" -s "0" -i "50" -f ;
# Put the above line into the post processing field of Orca. Make sure to change the file path of python and this script to what's on your computer
# The arguments example is for setting up a 5 floors aux fan tower
# It means: find all "M106 P2 S0", replace them with "M106 P2 S(number)". The number will start at "0" and increment by 50 every 50 layers
# Script will also add a "M106 P2 S(number)" at the start of every layer

#argument interpreter
argv_it = iter(sys.argv)
next(argv_it) #skip 1st argument
for a in argv_it:
    match a:
        case "-f" | "--file": 
            # gcode file location. Orca should fill this
            destFile = next(argv_it)
        case "-c" | "--command": 
            # command to be modified. Include default value. New command will also be added at the begining of all layers
            # command must end with a number
            command = next(argv_it)
        case "-s" | "--start":
            # starting value. Bottom of tower
            start = int(next(argv_it))
        case "-i" | "--increment":
            # increment. Script increment value every 50 layers
            increment = int(next(argv_it))

print("This script modifies gcode to set up calibration tower. See code comments for how to use")
print("Modifing " + destFile+"\n"+ "Target command: "command+" New value from:" + str(start)+" With increment of: "+str(increment))
sourceFile = destFile+".bak"
#back up
print("copy \""+destFile+"\" \""+sourceFile+"\"")
os.system("copy \""+destFile+"\" \""+sourceFile+"\"")

try:
    fin = open(sourceFile, "r")
    fout = open(destFile, "w")

    layer = 0
    newcommand = re.sub("\d+$", "", command)+str(start+increment*int(layer/50))+"\n"
    for line in fin:
        if (line.find("LOG_Z") == 0): #new layer
            if (layer > 1):
                if (layer%50 == 0): #increment value every new layer, don't touch 1st layer
                    newcommand = re.sub("\d+$", "", command)+str(start+increment*int(layer/50))+"\n"
                line = line+newcommand #set new value at all new layer
            layer=layer+1
        elif (line.find(command) == 0 & layer > 1):
            line = line.replace(command, newcommand)
        fout.write(line)

finally:
    fin.close()
    fout.close()
    os.system("del /q \""+sourceFile+"\"")
    os.system("pause")