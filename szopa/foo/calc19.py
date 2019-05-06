# A stylish calculator.
import time
import sys
import tty

# - Data. -
# Binds
stdin  =  sys.stdin
stdout = sys.stdout

# Vars

l1 = "|  "+"\u250c"+"\u2500"*25+"\u2510"+"     |"
l2 = "|  "+"\u2502"+"                         "+"\u2502"+"     |"
l3 = "|  "+"\u2514"+"\u2500"*25+"\u2518"+"     |"

bodyString = """\
------------------------------------
{}
{}
{}
|                        nigg19\u00a9   |
|                                  |
| [q]             |del| |C|        |
|                                  |
|      |7| |8| |9|  |/| |*| |-|    |
|                                  |
|      |4| |5| |6|          |+|    |
|                                  |
|      |1| |2| |3|          |=|    |
|                           |=|    |
|          |0| |,|                 |
|                                  |
|                               MQ |
------------------------------------
""".format(l1, l2, l3)


screen = []

expr = []

nums = list("1234567890")
operators = list("+-*/")

curDirs = {
    "u": "A",
    "d": "B",
    "r": "C",
    "l": "D"
}

# Functions.

def cMove(d, n=1):
    d = curDirs[d]
    code = "\u001b[{}{}".format(n, d)
    stdout.write(code)


def writeBody():
    stdout.write(" "*(80*25*10)+"\r\n")
    stdout.write(bodyString.replace("\n", "\r\n"))
    stdout.flush()

running = True

def flushScreen():
    global screen
    cMove('d', 3)
    cMove('r', 4)
    stdout.write(''.join(screen[0:25]))
    stdout.write("\r")
    cMove('u', 3)
    stdout.flush()

def clearScreen():
    global screen
    cMove('d', 3)
    cMove('r', 4)
    stdout.write(" "*25)
    stdout.write("\r")
    cMove('u', 3)
    stdout.flush()

    
def processChar(c):
    global running, screen, expr
    
    if ord(c) == 3 or c == "q":
        running = False
    elif c in nums:
        if c == "0" and screen == []: return
        screen.append(c)
    elif c in operators:
        expr.append(''.join(screen))
        expr.append(c)
        screen = []
        return
    elif c == ',':
        screen.append('.')
    elif ord(c) == 13: # Return key
        expr.append(''.join(screen))
        exprStr = ''.join(expr)
        try: r = eval(exprStr)
        except: r = "e"
        if exprStr == "2+2": r = 5
        screen = list(str(r))
        expr = []
    elif c == 'c':
        screen = []
        expr = []
    elif ord(c) == 127:
        screen = screen[0:-1]

    clearScreen()
    time.sleep(0.07)
    flushScreen()

def intro():
    global screen
    screen = list("MISHQUTIN'S SHIT CALC!")
    flushScreen()
    time.sleep(1.5)
    screen = []
    clearScreen()
    
def main():
    writeBody()
    cMove('u', 19)

    intro()
    
    while running:
        c = stdin.read(1)
        processChar(c)


# -- Code. --

try:
    ORIG_STATE = tty.tcgetattr(stdout)
    tty.setraw(stdout)

    main()
finally:
    tty.tcsetattr(stdout, tty.TCSANOW, ORIG_STATE)
