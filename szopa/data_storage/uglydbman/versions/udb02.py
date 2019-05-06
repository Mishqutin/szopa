#!/usr/bin/python3
# UDB v0.1, the shitiest version.
import sys, os

print("UDB version 0.2")

# dict = {'meta': {}, 'main': {}}

def listFind(l, v):
    r = -1
    c = 0
    for i in l:
        if i == v:
            r = c
            break
        else:
            c += 1
    return r

def argValue(l, s):
    i = listFind(l, s)
    v = l[i+1]
    l.remove(v)
    return v


def udbRead(path):
    f = open(path, 'r')
    txt = f.read()
    f.close()

    try: d = eval(txt)
    except Exception as e:
        print("No dict found.")
        raise e

    if type(d) != dict:
        raise ValueError("File doesn't contain dict")

    return d

def udbWrite(path, d):
    f = open(path, 'w')
    f.write(str(d))
    f.close()

def udbCreate(path, name="none", desc="none"):
    d = {}
    d["meta"] = {}
    d["main"] = {}

    d["meta"]["name"] = name
    d["meta"]["udbver"] = "0.2"
    d["meta"]["desc"] = desc
    
    udbWrite(path, d)

def udbPrintKeys(path, sep="\n"):
    d = udbRead(path)
    dmeta = d["meta"]
    ddata = d["main"]

    keyStr = sep.join(ddata.keys())

    print("udb:", dmeta["name"])
    print(keyStr)

usageMessage = """\
udb - ugly database. Stores everything in plain text.
Usage:
  udb [options] file
  Options:
    -c
        Will create a new udb file.
    -n name
        Set udb name.
    -d desc
        Set udb description.
    
    -k key
        Key to operate on.
    -v value
        Value to operate with.
    -w
        Write value to key.
    -p
        Print key's value.
    
    -l
        List keys.

    -h
        This help."""
def printUsage():
    print(usageMessage)

# -- Code. --
if __name__=="__main__":
    args = sys.argv[1:]
    name = "unnamed"
    desc = "none"
    key   = ""
    value = ""

    mode = ""

    if "-h" in args:
        printUsage()
        sys.exit(0)
    
    if "-n" in args:
        name = argValue(args, "-n")
    if "-d" in args:
        desc = argValue(args, "-d")
    if "-k" in args:
        key = argValue(args, "-k")
    if "-v" in args:
        value = argValue(args, "-v")
        
    if "-w" in args: mode = "w"
    elif "-p" in args: mode = "p"
    elif "-l" in args: mode = "l"
    elif "-i" in args: mode = "i"
    
    for i in "ndkvwpli":
        if "-"+i in args: args.remove("-"+i)
    
    if "-c" in args:
        args.remove("-c")
        try: path = args[0]
        except: printUsage(); sys.exit(1)
        if os.path.isfile(path):
            print("File already exists.")
            sys.exit(2)
        else:
            udbCreate(path, name, desc)

    try: path = args[0]
    except: printUsage(); sys.exit(1)
    
    d = udbRead(path) # Handles errors on it's own.

    if mode == "w":
        d["main"][key] = value
        udbWrite(path, d)
        print("Written '"+value+"' to '"+key+"'" )
    elif mode == "p":
        if key in d["main"]:
            print(key+":", d["main"][key])
        else:
            print("No such entry:"+key)
    elif mode == "l":
        print('\n'.join(d["main"].keys()))
    elif mode == "i":
        for i in d["meta"]:
            print(i+": "+d["meta"][i])
              
    

    
