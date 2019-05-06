#!/usr/bin/python3
import sys
import os
import paramParser
import cnlib

toByteUInt = cnlib.toByteUInt
fromByteUInt = cnlib.fromByteUInt

def sfsCompile(fmeta, fblock):
    # fmeta is a dict
    # fblock is a list
    bmeta = str(fmeta).encode() # bytes
    
    meta_len = len(bmeta) # int
    bmeta_len = toByteUInt(meta_len) # bytes

    bblock = bytes(fblock)

    s = bmeta_len + bmeta + bblock
    return s

def sfsDecompile(s):

    bmeta_len = s[:8] # bytes
    meta_len = fromByteUInt(bmeta_len) # int

    s = s[8:] # remove meta length from data

    bmeta = s[:meta_len] # bytes
    bblock = s[meta_len:] # bytes

    fmeta = eval( bmeta.decode("UTF-8") ) # dict
    fblock = list( bblock ) # list

    return fmeta, fblock

def sfsInitFS():
    fmeta = {}
    fblock = []

    return fmeta, fblock

def sfsAddFile(fmeta, fblock, name, data):
    spoint = len(fblock)
    fblock += list(data)
    epoint = len(fblock)

    fmeta[name] = (spoint, epoint)

def sfsAddDirectory(fmeta, fblock, name):
    fmeta[name] = "dir"

def sfsReadFile(fmeta, fblock, name):
    if fmeta[name] == "dir": return 1
    
    sp, ep = fmeta[name]

    l = fblock[sp:ep]
    s = bytes(l)
    return s

# Commands.

def packPath(fmeta, fblock, path):
    sfsAddDirectory(fmeta, fblock, path)
    
    for name in os.listdir(path):
        fullpath = path+"/"+name
        if os.path.isdir(fullpath):
            print("Dir:", fullpath)
            packPath(fmeta, fblock, fullpath)
        else:
            print("File:", fullpath)
            f = open(fullpath, 'rb')
            sfsAddFile(fmeta, fblock, fullpath, f.read())
            f.close()


def unpackDirs(fmeta, fblock, path):
    dirs = []
    for i in fmeta:
        if fmeta[i] == "dir":
            dirs.append(i)
    
    for name in dirs:
        print(path+"/"+name)
        os.mkdir(path+"/"+name)
    

def unpackFiles(fmeta, fblock, path):
    for name in fmeta:
        if fmeta[name] == "dir": continue
        fullpath = path+"/"+name
        print(fullpath)
        data = sfsReadFile(fmeta, fblock, name)
        f = open(fullpath, 'wb')
        f.write(data)
        f.close()

def unpackPath(fmeta, fblock, path):
    print("Creating directories...")
    unpackDirs(fmeta, fblock, path)
    print("Unpacking files...")
    unpackFiles(fmeta, fblock, path)

def cmdCreateArchive(path, archName):
    print("Init.")
    fmeta, fblock = sfsInitFS()
    print("Packing files...")
    packPath(fmeta, fblock, path)
    print("Compiling...")
    bstr = sfsCompile(fmeta, fblock)
    print("Writing...")
    f = open(archName, 'wb')
    f.write(bstr)
    f.close()
    print("Done.")


def cmdUnpackArchive(path, where):
    print("Reading...")
    f = open(path, 'rb')
    bstr = f.read()
    f.close()
    print("Decompiling...")
    fmeta, fblock = sfsDecompile(bstr)
    print("Unpacking...")
    unpackPath(fmeta, fblock, where)



usageMessage = """\
syfs - turn a directory into a single file.
Doesn't save any metadata. Only name and contents.
Usage:
%#  syfs [-u -e] from [to]
Options:
%#  -u
    Unpack archive.
%#  without -u
    Create archive.
%#  -e (also without -u)
    Do not add .sfs at the end of the new archive.
%#  -h
    This high-quality help.
How tf:
%%  syfs ./folder hello.sfs
  -Puts ./folder and it's subdirs into the file.
%%  syfs -u hello.sfs [./someplace]
  -Unpacks hello.sfs into ./someplace or into . if none specified.
Credits and excuses:
  I am very sorry for such a shitty piece of software, having no competiton
  because of how deeeeep below the level of acceptable quality it is.
  At least this help screen has colors...
  \u001b[33m~mishqutin\u001b[0m""".replace("%%", "\u001b[32m").replace("\n", "\u001b[0m\n").replace("%#", "\u001b[36m")
def printUsage():
    print(usageMessage)

# -- Code. --

if __name__ == "__main__":
    args = sys.argv[1:]
        
    avOpts = {"-u": 0, "-e": 0, "-h": 0}
    options, sargs = paramParser.parseArgs(avOpts, args)

    if options["-h"]:
        printUsage()
        sys.exit(0)
    
    if len(args)<1:
        print("Not enough params use -h for help.")
        sys.exit(1)

    fpath = sargs[0]
    try: dest  = sargs[1]
    except IndexError: dest = "."
    
    if options["-u"]:
        if not os.path.isfile(fpath):
            print("No such file:", fpath)
            sys.exit(2)
        elif not os.path.isdir(dest):
            print("No such directory:", dest)
            sys.exit(3)
        cmdUnpackArchive(fpath, dest)
    else:
        if not os.path.isdir(fpath):
            print("No such directory:", fpath)
            sys.exit(4)
        elif os.path.isfile(dest) or os.path.isdir(dest):
            print("File already exists or it's a directory:", dest)
            sys.exit(5)
        if not options["-e"]:
            dot = ".sfs"
        else:
            dot = ""
        cmdCreateArchive(fpath, dest+dot)

