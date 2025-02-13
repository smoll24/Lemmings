import os
import time
from readchar import readchar
from replit import audio
import threading

#Lemmings Project

class Jeu:
    GAME = True
    num = 1
    count = 1

    def __init__(self, g, lem):
        self.grotte = g
        self.lemmings = lem
        self.start = Jeu.findStart(self, g)

    def findStart(self, grotte):
        for row in range(len(grotte)):
            for col in range(len(grotte[0])):
                if grotte[row][col] == 0:
                    return (row, col)

    def affiche(self):
        '''afficher la carte avec les positions et directions 
        de tous les lemmings en jeu'''
        for i in range(len(self.grotte)):
            for j in range(len(self.grotte[0])):

                if self.lemmings[i][j] != 0:
                    if self.lemmings[i][j] == 1:
                        new_lemming = Lemming(i, j, game, 1)
                        self.lemmings[i][j] = new_lemming
                        new_case = Case(self.grotte[i][j], new_lemming)
                    else:
                        new_case = Case(self.grotte[i][j], self.lemmings[i][j])
                else:
                    new_case = Case(self.grotte[i][j], None)

                print(new_case, end=" ")

            print("")

        print("\nLemmings saved: ",
              self.num - self.count - (sum(x.count(2) for x in self.grotte)),
              "/", self.num)

        print("\nPress 1 to spawn a new lemming.")

    def tour(self):
        '''fait agir chaque lemming une fois et affiche le nouvel état du jeu'''

        #Keep track of moved lemmings
        moved_lemmings = []

        for i in range(len(self.lemmings)):
            for j in range(len(self.lemmings[0])):
                if isinstance(self.lemmings[i][j], Lemming):
                    if (i, j) not in moved_lemmings:
                        coords = self.lemmings[i][j].action()
                        moved_lemmings.append(coords)

    def handle_input(self):
        key = readchar()
        if key == '1' and self.lemmings[self.start[0]][self.start[1]] == 0:
            print("\u001b[33mLemming spawned.\033[0m")
            self.lemmings[self.start[0]][self.start[1]] = 1
            self.num += 1
            self.count += 1
        else:
            return

    def demarre(self):
        '''lance une boucle infinie attendant les commandes de l’utilisateur'''
        #Game Loop

        self.lemmings[self.start[0]][self.start[1]] = 1

        while True:

            # Create a thread for key input handling
            #Aide: https://replit.com/talk/ask/Need-help-with-python-threading/52970
            input_thread = threading.Thread(target=self.handle_input)
            input_thread.start()

            self.tour()
            os.system("printf '\033c'")
            self.affiche()
            time.sleep(0.5)

            if self.count == 0:  # all lemmings have passed
                lemDead = sum(x.count(2) for x in self.grotte)
                # expression taken from https://stackoverflow.com/questions/17718271/python-count-for-multidimensional-arrays-list-of-lists
                if lemDead == 0:
                    print("\u001b[32mYou saved all the lemmings!\033[0m")
                    exit()
                else:
                    print("\u001b[32mYou saved", self.num - lemDead,
                          "lemmings.\033[0m")
                    exit()


class Lemming:

    def __init__(self, li, col, jeu, dir):
        self.l = li
        self.c = col
        self.j = jeu
        self.d = 1
        self.turn_count = 0

    def __str__(self):
        '''renvoie < ou > selon la direction du lemming'''
        if self.d == 1:
            if self.turn_count >= 5:
                return "\u001b[33m>\033[0m"
            else:
                return "\u001b[32m>\033[0m"
        else:
            if self.turn_count >= 5:
                return "\u001b[33m<\033[0m"
            else:
                return "\u001b[32m<\033[0m"

    def action(self):
        '''déplace ou retourne le lemming'''
        #If out of bounds
        if self.l == len(self.j.lemmings) - 1 or self.c == 0 or self.c == len(
                self.j.lemmings[0]) - 1:
            return self.sort()
        #If can move down, move down
        if self.j.grotte[self.l +
                         1][self.c] == 0 and self.j.lemmings[self.l +
                                                             1][self.c] == 0:
            if self.j.lemmings[self.l + 1][self.c] == 0:
                self.j.lemmings[self.l][self.c] = 0
                self.j.lemmings[self.l + 1][self.c] = self
                self.l += 1
                self.turn_count = 0
                #if it falls out of bounds
                if self.l == len(self.j.grotte) - 1:
                    self.alive = False
                    self.j.grotte[self.l][self.c] = 2
                return (self.l, self.c)
        #Elif can move horizontal, move horizontal
        elif self.j.grotte[self.l][self.c + self.d] == 0 and self.j.lemmings[
                self.l][self.c + self.d] == 0:
            if self.j.lemmings[self.l][self.c + self.d] == 0:
                self.j.lemmings[self.l][self.c] = 0
                self.j.lemmings[self.l][self.c + self.d] = self
                self.c += self.d
                self.turn_count = 0
                return (self.l, self.c)
        #Else change direction
        else:
            self.d = self.d * -1
            self.turn_count += 1
            #if lemming stuck
            if self.turn_count >= 10:
                self.alive = False
                self.j.lemmings[self.l][self.c] = 0
                self.j.grotte[self.l][self.c] = 2
                self.j.count -= 1
            return (self.l, self.c)

    def sort(self):
        '''retire le lemming du jeu'''
        self.j.lemmings[self.l][self.c] = 0
        self.j.count -= 1
        del self


class Case:

    def __init__(self, t, lem):
        self.terrain = t
        self.lemming = lem

    def __str__(self):
        '''renvoie caractère à afficher pour représenter cette 
        case ou son éventuel occupant'''
        if self.terrain == 1:
            return "#"
        elif self.lemming:
            return str(self.lemming)
        elif self.terrain == 2:
            return "\033[1;31mx\033[0m"
        else:
            return " "


#VARIABLES ---------------------------

title = [
    " __    ____  ___   __ ___  ___ __ __  __  ___   __ ",
    " ||    ||    ||\\\//|| ||\\\//|| || ||\ || // \\\ (( \ ",
    " ||    ||==  || \/ || || \/ || || ||\\\||(( ___  \\\ ",
    " ||__| ||___ ||    || ||    || || || \|| \\\_|| \_))"
]

levels = ["level1.txt", "level2.txt", "level3.txt", "level4.txt", "level5.txt"]

#GAME STARTS --------------------------
source = audio.play_file('intro.mp3')
print('\n')
for line in title:
    print(line)
print(('\n') * 2)

niv = input((' ') * 1 + "Quel niveau ? (1 , 2 , 3 , 4) ")
#--------------
#Import tableau de terrain
try:
    my_file = open(levels[int(niv) - 1], "r")
except:
    print("Not a valid level.")
    exit()
tableau_txt = my_file.read()
# split each line into integers and create a list of lists
lines = tableau_txt.strip().split("\n")
tableau_g = []
for line in lines:
    row = [int(num) for num in line.split(", ")]
    tableau_g.append(row)
my_file.close()

#Creer tableau de lemmings
tabl_r = len(tableau_g)
tabl_c = len(tableau_g[0])
tableau_l = [[0 for _ in range(tabl_c)] for _ in range(tabl_r)]
#--------------

game = Jeu(tableau_g, tableau_l)
source.paused = True
audio.play_file("lemming.mp3")
game.affiche()
game.demarre()
