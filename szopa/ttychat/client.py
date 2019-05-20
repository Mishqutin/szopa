import socket
import sys
import tty
import _thread as thread

IP = ("83.145.150.166", 12341)

def loop(s):
    esc = "\u001b"
    escCodes = [
        "\u001b[A", "\u001b[B", "\u001b[C", "\u001b[D"
    ]
    c = " "
    while ord(c) != 3:
        c = sys.stdin.read(1)
        cs = c
        if cs == esc:
            while not cs in escCodes:
                if len(cs) > 3:
                    cs = 0
                    break
                else:
                    cs += sys.stdin.read(1)
            if cs == 0: continue
        #print(cs.__repr__())
        if cs == "\r": cs = "\n\r"
        s.send(cs.encode())

def readLoop(s):
    while True:
        b = s.recv(16)
        sys.stdout.write(b.decode("UTF-8"))
        sys.stdout.flush()



s = socket.socket()
s.connect(IP)
print("connected")

flags_def = tty.tcgetattr(sys.stdin)
tty.setraw(sys.stdin)

thread.start_new_thread(readLoop, (s,))
try: loop(s)
finally:
    tty.tcsetattr(sys.stdin, 0, flags_def)
