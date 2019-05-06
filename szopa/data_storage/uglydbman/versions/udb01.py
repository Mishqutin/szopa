#!/usr/bin/python3
# UDB v0.1, the shitiest version.
import sys

print("This UDB version 0.1 is the least reliable and fucked up.")

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
    d["meta"]["udbver"] = "0.1"
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
    -c, --create
        Will create a new udb file.
    -n, --name name
        Set udb name.
    -d, --desc desc
        Set udb description.
    
    -k, --key key
        Key to operate on.
    -v, --value value
        Value to operate with.
    -w, --write
        Write value to key.
    -p, --print
        Print key's value.
    
    -l, --list
        List keys.
        
"""
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
    
    for i in "ndkvwpl":
        if "-"+i in args: args.remove("-"+i)
    
    if "-c" in args:
        args.remove("-c")
        path = args[0]
        udbCreate(path, name, desc)

    path = args[0]
    
    d = udbRead(path)

    if mode == "w":
        d["main"][key] = value
        udbWrite(path, d)
    elif mode == "p":
        print(key+":", d["main"][key])
    elif mode == "l":
        print(d["main"].keys())
              
    

    
