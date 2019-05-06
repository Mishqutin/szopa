#!/usr/bin/python3
import time
import random

# - Data. -

# Binds.
rint = random.randint

# Constants.
Team_a_name = "FC Pazdan"
Team_b_name = "UKS Petropol"

action_pass = [
    "Nic sie nie dzieje :P",
    "Nic, kurwa, nic.",
    "Nie widac, zeby sie cos dzialo.",
    "Nadal nic.",
    "Brak akcji.",
]

action_score = [
    "{} strzela gola!",
    "{} wkurwia pile do bramki!",
    "{} wkopuje pilke do bramki przeciwnika!",
    "{} mistrzowsko strzela gola kurwa!",
    "{} zdobywa punkt!",
    "{} trafia do bramy!",
]


# Variables.
Team_a = 0
Team_b = 0

plays = rint(8, 20)

# Functions.
def randScore(a, b):
    choice = []
    for i in range(rint(255, 777)):
        choice.append(rint(a, b))

    return random.choice(choice)

def action(n):
    global Team_a, Team_b
    msg = ""
    
    if n == 0:
        msg = random.choice(action_pass)
    elif n == 1:
        msg = random.choice(action_score).format(Team_a_name)
        Team_a += 1
    elif n == 2:
        msg = random.choice(action_score).format(Team_b_name)
        Team_b += 1
        
    print(msg)
        

# - Code. -

time.sleep(6)
print("Rozpoczyna sie mecz miedzy")
time.sleep(3)
print(Team_a_name + ", a " + Team_b_name + "!")
time.sleep(5)
print("")
print("Start!")

c = 0
while c != plays:
    time.sleep(rint(100, 200)/10)
    
    a = randScore(0, 2)
    action(a)
    
    c += 1


time.sleep(6.6)
print("Koniec czasu!")
time.sleep(4)
print("")
print("Wyniki:")
time.sleep(1.6)
print(Team_a_name + ":", Team_a)
print(Team_b_name + ":", Team_b)
time.sleep(6)
print("")
input("Wcisnij <RETURN>, aby wyjsc.")
print("Credits: Mishqutin.")
