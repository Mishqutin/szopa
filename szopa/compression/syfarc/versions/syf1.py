#!/usr/bin/python3
import sys

from cn import compilecn
from cn import decompilecn

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

# sepSequence = [0, 0, 0, 255, 255, 255, 255, 0, 0, 0]

chunkSize = 8

def syf(filefrom, fileto, chunkSize, numberSize):
    print("Reading file...")
    f = open(filefrom, 'rb')
    data = list( f.read() )
    f.close()


    # -- Preparations. --
    
    archive_data = {"dict_size": 0, "bytes_over": 0}

    print("Dividing data into chunks...")
    
    chunks = list( split_into_chunks(data, chunkSize) )
    # `chunks` now contains a list of byte-lists, e.g.
    #     [ [1, 2], [1, 2], [1, 2] ]
    lastEntry = chunks[-1]
    lastEntrySize = len(lastEntry)
    if lastEntrySize < chunkSize:
        for i in range( chunkSize - lastEntrySize ):
            lastEntry.append(69) # Append placeholder byte. 69 = E (big E),
                                 # so you will know when something goes wrong
                                 # an 'E' will be left at the end of unpacked
                                 # file.
        
        chunks[-1] = lastEntry
        archive_data["bytes_over"] = chunkSize - lastEntrySize
    
    
    byteDict = [] # List of bytestrings.
    out = [] # List of byteDict indexes.

    print("Storing sequences...")

    # -- Create dictionary. --
    
    for i in chunks:
        # Byte list into bytestring: [1, 2] -> b"\x01\x02"
        byteDict.append(bytes(i))
    # byteDict now contains a list of bytestrings, e.g.
    #     [ b"\x01\x02", b"\x01\x02", b"\x01\x02" ]
    
    # Remove duplicated bytestrings.
    byteDict = list( dict.fromkeys(byteDict) )

    
    print("Indexing data...")

    # -- Create links to dictionary (index bytes). --
    
    for i in chunks:
        # Find sequences from `chunks` in `byteDict`,
        # and replace said sequences with their index in dict,
        # store result in `out`.
        out.append(listFind( byteDict, bytes(i) ))


        
    print("Compiling data...")
    
    encodedByteDict = b""
    for i in byteDict: # Join a list of bytestrings into a single bytestring.
        encodedByteDict += bytes(i)
    #    e.g. b"\x01\x02\x03";
    # And then - turn the bytestring into a list of numbers.
    encodedByteDict = list(encodedByteDict)
    # e.g. [1, 2, 3]

    archive_data["dict_size"] = len(encodedByteDict)

    # Compile dict indexes into numbers of `numberSize` size.
    out = list( compilecn(out, numberSize) )
    # Compile result. End file scheme will look like this:
    # 1. Archive metadata hash (a Python dictionary) stored as string.
    # 2. Byte sequence dictionary (a list!) stored in binary.
    # 3. Byte seq. dict. indexes, also binary.
    res = [*str(archive_data).encode(), *encodedByteDict, *out]


    
    print("Writing file...")
    f = open(fileto, 'wb')
    f.write(bytes( res ))
    f.close()
    print("Creating archive done.")


def unsyf(filefrom, fileto, chunkSize, numberSize):
    print("Reading file...")
    f = open(filefrom, 'rb')
    data_raw = f.read()
    f.close()

    # -- Preparations. --
    print("Reading archive metadata...")
    
    # Read archive metadata.
    archDataEnd = data_raw.find(b'}') # Find end of hash table.
    archive_data = eval(data_raw[:archDataEnd+1]) # Read hash table.

    # Remove hash table from the beginning of the archive file.
    data_raw = data_raw[archDataEnd+1:]
    

    # -- Decompile seq. dict. and indexes part. --
    
    data_dict = [] # Sequence dictionary.
    data_data = [] # Dictionary indexes.

    print("Decompiling data...")
    # Read seq. dictionary and indexes part.
    sep = archive_data["dict_size"] # Look up where does the dict. end.
    data_dict = list( data_raw[:sep] ) # Split into seq. dict. and
    data_data = list( data_raw[sep:] ) # index part.

    # data_dict = e.g. [1, 2, 3, 4].
    # data_data = e.g. [0, 1, 0, 2, 0, 3, 0, 4], if numberSize is set to 2.

    
    ddict = list( split_into_chunks(data_dict, chunkSize) ) # seq. dict.
    ddata = list( decompilecn(data_data, numberSize)      ) # indexes

    # ddict = e.g. [ [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4] ], if chunkSize=4
    # ddata = e.g. [1, 2, 3, 4]


    # -- Decompression (replace indexes w/ values). --
    
    out = [] # Result of function, contains list of bytes, e.g. [1, 2, 3, 4]
    
    for i in ddata:
        # Replace indexes with it's seq. dict. values.
        out += ddict[i]

    # Placeholder bytes added to the last chunk of the seq. dict. to fill
    # it to chunkSize value.
    bytes_over = archive_data["bytes_over"]

    # If there are any placeholder bytes.
    if bytes_over:
        # Cut 'em out.
        out = out[:-bytes_over]


    
    print("Writing file...")
    f = open(fileto, 'wb')
    f.write(bytes( out ))
    f.close()
    print("Unsyfing archive done.")
    
    









# -- Code. --

syf("./from.txt", "./to.syf", 4, 2)
unsyf("./to.syf", "./to.syf.txt", 4, 2)
