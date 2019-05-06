#!/usr/bin/python3
import sys
import os

dictDelim = "/"

def parseKey(string, offset=""):
    keylist = string.split(dictDelim)

    if offset:
        keylist.insert(0, offset)

    return keylist

def parseValue(string):
    return string


def udbFormatKeylist(keylist):
    key = ""
    for i in keylist:
        key += "['{}']".format(i)
    return key
    
def udbSetKey(d, keylist, value):
    key = udbFormatKeylist(keylist)
    
    execLocals = {"d": d, "v": value}
    execString = "d{} = v".format(key)
    exec(execString, execLocals, {})

def udbGetKey(d, keylist):
    key = udbFormatKeylist(keylist)

    r = {"r": None}
    execLocals = {"d": d, "r": r}
    execString = "r['r'] = d{}".format(key)
    exec(execString, execLocals, {})

    return r['r']
    #return eval(r['r']) if r['r'] else ""

def udbIsKey(d, keylist):
    try:
        udbGetKey(d, keylist)
        return True
    except KeyError:
        return False

def udbRemoveKey(d, keylist):
    key = udbFormatKeylist(keylist)
    
    execLocals = {"d": d}
    execString = "del d{}".format(key)
    exec(execString, execLocals, {})


def udbReadFile(path):
    try: f = open(path, 'r')
    except:
        print("No such file.")
        sys.exit(7)
    s = f.read()
    f.close()

    d = eval(s)

    if type(d) != dict:
        raise ValueError("file not containing Python dict.")

    return d

def udbWriteFile(path, d):
    f = open(path, 'w')
    f.write(str( d ))
    f.close()


def udbInitDict():
    d = {}
    d["main"] = {}
    d["meta"] = {}

    d["meta"]["udbver"] = "0.3"
    d["meta"]["name"] = ""
    d["meta"]["description"] = ""
    d["meta"]["ownerdata"] = {}

    d["meta"]["ownerdata"]["name"] = ""
    d["meta"]["ownerdata"]["info"] = ""

    return d





def printDictionaryTree(d, indent=""):
    for i in d:
        v = d[i]
        if type(v) == dict:
            print(indent+i+":")
            printDictionaryTree(v, indent=indent+" ")
        else:
            print(indent+"{}: {}".format(i, v.__repr__()))


cmdUsageMessage = """\
udb - Ugly Data Base version 0.3.
Stores all data in plain text file with Python's dict class.
Usage:
%# udb [options] file
%# udb file [options]
Options:
%# -c
   Create new udb.

%# -k key
   Used with conjunction with options below.
%# -v value
   Also used with options below.
%# -m
   Key will access meta info.

%# -p
   Print key's value.
%# -P
   Print key's value with it's type.

%# -a
   Add new key to db.

%# -s
   Set key to be equal value.
%# -t type
   Used to define type of the value. Default is 'str'.

%# -r
   Remove key from db.

%# -l
   Print db's tree.

Short tutorial:
 Create new db:
%%   udb ./test.udb -c

 Set some values:
  Add new key:
%%   udb ./test.udb -a -k "hello"
  Set the key's value to 'str' "Hello world!"
%%   udb ./test.udb -s -k "hello" -v "Hello world!"
  Set the key's value to 'int' 1
%%   udb ./test.udb -s -k "hello" -v 1 -t int

  Create another 'branch':
%%   udb ./test.udb -a -k "lol"
%%   udb ./test.udb -s -k "lol" -v '{}' -t dict
  Now you can:
%%   udb ./test.udb -a -k "lol.sub_lol"
%%   udb ./test.udb -s -k "lol.sub_lol" -v "I am under lol."
  Slash ('/') splits levels. U know.
  
  Set db's info:
%%   udb ./test.udb -s -k "name" -v "my_name" -m
  '-m' changes from db main tree to meta info tree.
  Now you can manage meta info the same way as main tree.
  See '-l' option below.

 Read values:
  Read single value:
%%   udb ./test.udb -p -k "hello"
  Read single value and show it's type:
%%   udb ./test.udb -P -k "hello"
  See a tree-like overview of your db:
%%   udb ./test.udb -l

Credits:
 \u001b[33;1mMishqutin 2019\u001b[0m""".replace("%%", "\u001b[32m").replace("\n", "\u001b[0m\n").replace("%#", "\u001b[36m")
def printUsage():
    print(cmdUsageMessage)




            
# Shell argument parsing.

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

def argValue(l, s, n=1):
    i = listFind(l, s)
    v = l[i+n]
    #l.remove(v)
    return v


def parseArgs(avOpts, args):
    rparams = {}
    rargs = args.copy()
    for i in avOpts:
        optArgN = avOpts[i]
        
        if i in args:
            # Option found.
            if optArgN:
                # Option has n of arguments.
                rparams[i] = []
                for n in range(1, optArgN+1):
                    try: v = argValue(args, i, n)
                    except IndexError: break
                    if v in avOpts:
                        break
                    else:
                        rparams[i].append(v)
                        rargs.remove(v)
                if len(rparams[i]) == 1: rparams[i] = rparams[i][0]
                elif len(rparams[i]) == 0: rparams[i] = False
            else:
                # Option has no arguments.
                rparams[i] = True
            rargs.remove(i)
            
        else:
            # Option not found.
            rparams[i] = False

    return rparams, rargs


# -- Code. --

if __name__ == "__main__": # Gotta do serious cleanup here...
    args = sys.argv[1:]

    if len(args) == 0:
        print("Not a single argument given. Are you joking?")
        print("Try with -h.")
        sys.exit(0)

    availOpts = {
        "-h": 0, # help
        "-k": 1, # key
        "-v": 1, # value
        "-c": 0, # create init dict
        "-m": 0, # access meta
        "-s": 0, # set key's value
        "-t": 1, # set key's type (used with option above)
        "-a": 0, # add key
        "-r": 0, # remove key
        "-p": 0, # print key's value
        "-P": 0, # print key's value with it's type
        "-l": 0, # list db
    }
    options, sargs = parseArgs(availOpts, args.copy())

    if options["-h"]:
        printUsage()
        sys.exit(0)
    
    if len(sargs) == 0:
        print("File argument not given.")
        sys.exit(1)

    path = sargs[0]

    tru = False
    for i in options:
        if options[i]: tru = True; break
    if not tru:
        print("No options given. I don't know what to do with the file.")
        print("Try -h.")
        sys.exit(0)

    if options["-c"]:
        if os.path.isfile(path):
            print("File already exists.")
            sys.exit(2)
        d = udbInitDict()
        udbWriteFile(path, d)
        print("Created empty ugly-database.")
        sys.exit(0)
        
    if options["-l"]:
        d = udbReadFile(path)
        printDictionaryTree(d)
        sys.exit(0)


    if options["-m"]:
        keyoffset = "meta"+dictDelim
    else:
        keyoffset = "main"+dictDelim

    keystr   = keyoffset+options["-k"]
    valuestr = options["-v"]

    key   = parseKey( keystr )
    value = parseValue( valuestr )

    
    d = udbReadFile(path)
    
    if options["-a"]: # add key
        if udbIsKey(d, key):
            print("Key '{}' already exists.".format(keystr))
            sys.exit(3)
        else:
            udbSetKey(d, key, {})
            udbWriteFile(path, d)
            print("Added '{}' to db.".format(keystr))

    if options["-r"]: # remove key
        if udbIsKey(d, key):
            udbRemoveKey(d, key)
            udbWriteFile(path, d)
            print("Removed '{}' from db.".format(keystr))
        else:
            print("Key '{}' doesn't exist.".format(keystr))
            sys.exit(4)

    elif options["-p"] or options["-P"]: # print key's value
        if udbIsKey(d, key):
            kval = udbGetKey(d, key)
            s = "{}: {}".format(keystr, kval.__repr__())
            if options["-P"]: s += " {}".format(type(kval))
            print(s)
        else:
            print("Key '{}' doesn't exist.".format(keystr))
            sys.exit(4)

    elif options["-s"]: # set key
        if udbIsKey(d, key):
            if options["-t"]:
                try: vtype = eval(options["-t"])
                except NameError:
                    print("Invalid type.")
                    sys.exit(5)
                try: value = vtype(value)
                except ValueError:
                    print("Invalid value for given type.")
                    sys.exit(6)
            
            udbSetKey(d, key, value)
            udbWriteFile(path, d)
            print("Key '{}' set.".format(keystr))
        else:
            print("Key '{}' doesn't exist.".format(keystr))
            sys.exit(4)

    

    
    
        
