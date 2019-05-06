#!/usr/bin/python3
import random
import time
import sys

# Args:
# -/-  - default
# 1: n - from 1 to n
# 2: s, e - from s to e

# Binds.
rint = random.randint

# Functions.
def randomize(a, b):
    choice = []
    for i in range(rint(66, 144)):
        choice.append(rint(a, b))

    return random.choice(choice)


# - Code. -
args = sys.argv[1:]
s, e = 1, 6
if len(args) == 0:
    pass
elif len(args) == 1:
    e = int(args[0])
elif len(args) == 2:
    s = int(args[0])
    e = int(args[1])

n = randomize(s, e)
print("Dice roll!")
time.sleep(0.5)
print("Result:", n)
