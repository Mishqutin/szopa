#!/usr/bin/python3
import sys

# -- Data. --



def split_into_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

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


def printUsage():
    print("Either invalid syntax or -h parameter given.")
    print("  cx [options] <from> [<to>]")
    print("  cx program reads a list of numbers from file and saves them in a")
    print("  binary format as specified.")
    print("  One can specify number of bytes occupied by single number and if it's signed.")
    print("  options:")
    print("    -c, --compile (default)")
    print("          Compile list from given file into a c7 binary file.")
    print("    -d, --decompile")
    print("          Decompile a c7 binary file to a number list.")
    print("    -e, --print-errors")
    print("          When an error occurs, prints what's happened into stdout.")
    print("")
    print("    -b, --bytes (default: 8)")
    print("          Specify amount of bytes single number will occupy.")
    print("    -s, --signed")
    print("          Will make the numbers signed. By default thi option is disabled.")
    print("    -h, --help")
    print("          This help message.")


def compilecn(filefrom, fileto, byteAmount=8, byteOrder="big", signed=False):
    print("Reading...")
    f = open(filefrom, 'r')
    l = eval(f.read())
    f.close()

    print("Compiling...")
    out = []
    
    for n in l:
        b = list( n.to_bytes(byteAmount, byteOrder, signed=signed) )
        for i in b:
            out.append(i)

    print("Writing...")
    f = open(fileto, 'wb')
    f.write( bytes(out) )
    f.close()

    print("Done.")


def decompilecn(filefrom, fileto, byteAmount=8, byteOrder="big", signed=False):
    print("Reading...")
    f = open(filefrom, 'rb')
    l = list(f.read())
    f.close()

    print("Decompiling...")
    out = []
    b = list(split_into_chunks(l, byteAmount))
    for i in b:
        n = int.from_bytes(i, byteOrder, signed=signed)
        out.append(n)

    print("Writing...")
    f = open(fileto, 'w')
    f.write(str(out))
    f.close()
    print("Done.")
    
# -- Code. --

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        printUsage()
        sys.exit(1)

    if "-h" in args or "--help" in args:
        printUsage()
        sys.exit(0)

    usedParameters = ["-c", "--compile", "-d", "--decompile", "-e", "--print-error", "-b", "--bytes", "-s", "--signed"]
    mode = ""
    modePrintErr = False
    modeSigned = False
    modeByteAmount = 8
    modeByteOrder = "big" # Not changed currently.
    if "-c" in args or "--compile" in args:
        mode = 'c'
    elif "-d" in args or "--decompile" in args:
        mode = 'd'
    else:
        mode = 'c'

    if "-e" in args or "--print-errors" in args:
        modePrintErr = True

    try:
        if "-b" in args or "--bytes" in args:
            i = listFind(args, "-b") if listFind(args, "-b") != -1 else listFind(args, "--bytes")
            i += 1
            modeByteAmount = int( args[i] )
            args.remove(args[i])
    except:
        printUsage()
        sys.exit(3)

    if "-s" in args or "--signed" in args:
        modeSigned = True
    
    for i in usedParameters:
        if i in args: args.remove(i)
    
    if len(args) == 1:
        filefrom = args[0]
        fileto   = "./c7.out"
    elif len(args) == 2:
        filefrom = args[0]
        fileto   = args[1]
    else:
        printUsage()
        sys.exit(1)

    err = None
    if mode == 'c':
        try:
            compilecn(filefrom, fileto, modeByteAmount, modeByteOrder, modeSigned)
        except Exception as e:
            print("  An error occured!")
            err = e
    elif mode == 'd':
        try:
            decompilecn(filefrom, fileto, modeByteAmount, modeByteOrder, modeSigned)
        except Exception as e:
            print("  An error occured!")
            err = e
    else:
        printUsage()
        sys.exit(4)

    if err and modePrintErr:
        raise err

    if err:
        sys.exit(2)
    
