#!/usr/bin/python3
from pylibs import paramParser
import os, sys, json

def readLoco(path):
    f = open(path, 'r')
    s = f.read()
    f.close()
    d = eval(s)
    if type(d) != dict:
        raise ValueError("File '{}' contains broken Python dictionary.")
    return d

def writeLoco(path, d):
    s = json.dumps(d, sort_keys=True, indent=4)
    f = open(path, 'w')
    f.write(s)
    f.close()

def sendLoco(path, dest):
    path = os.path.realpath(path)
    dest = os.path.realpath(dest)
    
    loco = readLoco(path)
    curpath = loco['current']+"/"
    destpath = dest+"/"
    loconame = os.path.basename(path)
    cargo = loco['cargo']

    #print(path, dest)
    #print(curpath, destpath)
    #print(loconame)
    os.rename(curpath+loconame, destpath+loconame)
    for wagon in cargo:
        os.rename(curpath+wagon, destpath+wagon)

    loco['current'] = dest
    writeLoco(destpath+loconame, loco)
    return destpath+loconame



def funcSend(locoPath, destPath):
    if not os.path.isfile(locoPath):
        print("No such file (loco).")
        sys.exit(3)
    if not os.path.isdir(destPath):
        print("No such directory (destination).")
        sys.exit(4)
    print("Depart...")
    locoEndPath = sendLoco(locoPath, destPath)
    print("OK.")
    
def funcDepart(locoPath):
    if not os.path.isfile(locoPath):
        print("No such file (loco).")
        sys.exit(3)

    loco = readLoco(locoPath)

    if len(loco["track"]) == 0:
        print("This loco doesn't have any destination set.")
        sys.exit(5)

    destPathPrefix = loco["current"]+"/"
    destPath = destPathPrefix + loco["track"][0]
    destPath = os.path.realpath(destPath)
    
    print("Depart to '{}'...".format(destPath))
    locoEndPath = sendLoco(locoPath, destPath)

    # rm used destination.
    loco = readLoco(locoEndPath)
    del loco["track"][0]
    writeLoco(locoEndPath, loco)
    
    print("OK.")

def funcAttach(locoPath, wagon):
    if not os.path.isfile(locoPath):
        print("No such file (loco).")
        sys.exit(3)
    if not os.path.isfile(wagon):
        print("No such file (cargo).")
        sys.exit(4)

    if '/' in wagon or os.path.isdir(wagon):
        print("Destination syntax error (cargo).")
        sys.exit(6)
    
    loco = readLoco(locoPath)
    
    if wagon in loco["cargo"]:
        print("Cargo already attached.")
        sys.exit(7)
        
    loco["cargo"].append(wagon)

    writeLoco(locoPath, loco)
    print("Attached 1 wagon: "+wagon)

def funcDetach(locoPath, wagon):
    if not os.path.isfile(locoPath):
        print("No such file (loco).")
        sys.exit(3)
        
    loco = readLoco(locoPath)
    
    if not wagon in loco["cargo"]:
        print("Cargo is not attached.")
        sys.exit(7)
        
    loco["cargo"].remove(wagon)

    writeLoco(locoPath, loco)
    print("Detached 1 wagon: "+wagon)


def funcAuto(locoPath):
    if not os.path.isfile(locoPath):
        print("No such file (loco).")
        sys.exit(3)
        
    import time

    while True:
        loco = readLoco(locoPath)

        if len(loco["track"]) == 0:
            break
        elif len(loco["track-delay"]) == 0:
            raise IndexError("Destination set but no delay found.")

        current = loco["current"]
        dest = current + '/' + loco["track"][0]
        delay = loco["track-delay"][0]
        
        del loco["track"][0]
        del loco["track-delay"][0]
        writeLoco(locoPath, loco)

        locoPath = sendLoco(locoPath, dest)
        time.sleep(delay)
        
    
    
# -- Code. --
if __name__ == "__main__":
    availOpts = {}
    param, args = paramParser.parseArgs(availOpts, sys.argv[1:])
    if len(args) < 2:
        print("Syntax error")
        sys.exit(1)
    
    locoPath = args[0]
    action = args[1]
    if len(args) == 3:
        destPath = args[2]
    else:
        destPath = False

    if action == "send":
        if not destPath:
            print("Missing destination argument.")
            sys.exit(2)
        funcSend(locoPath, destPath)
    elif action == "depart":
        funcDepart(locoPath)
    elif action == "auto":
        funcAuto(locoPath)
    elif action == "attach":
        if not destPath:
            print("Missing destination argument.")
            sys.exit(2)
        funcAttach(locoPath, destPath)
    elif action == "detach":
        if not destPath:
            print("Missing destination argument.")
            sys.exit(2)
        funcDetach(locoPath, destPath)

