import socket
import sys
import _thread as thread

IP = ("0.0.0.0", 12341)


class Serwer:

    def __init__(self, IP):
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(IP)
        self.s.listen(5)

    def accept(self, func, args=[]):
        c, addr = self.s.accept()
        thread.start_new_thread(func, (c, addr, *args))



clients = []
def funcTell(b):
    """Broadcast stuff to other clients."""
    global clients
    
    i = 1
    for c in clients:
        try: # Send.
            c.send(b)
        except: # Client disconnected or something.
            print("Client read disconnetced.")
            clients.remove(c)
        i += 1


def func(c, addr):
    """Read from clients."""
    global clients
    clients.append(c) # Add new client to list.

    color = "\u001b[3{}m"
    end = "\u001b[0m"
    esc = "\u001b"
    while True:
        b = c.recv(16)
        if b == b"\x7f": b = b"\x1b[D \x1b[D" # Backspace.
        
        i = clients.index(c)+2
        msg = color.format(i).encode() + b + end.encode()
        
        funcTell(msg) # Broadcast msg.
        #continue
        sys.stdout.write(msg.decode("UTF-8")) # Also show on screen.
        sys.stdout.flush()


        





Ser = Serwer(IP)

while True:
    Ser.accept(func)

