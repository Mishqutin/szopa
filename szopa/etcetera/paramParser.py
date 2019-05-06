#!/usr/bin/python


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


