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
    
