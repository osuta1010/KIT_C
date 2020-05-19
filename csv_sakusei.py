import csv
import random
man = list(range(100,150,1))
woman = list(range(200,250,1))
with open('kekka.csv', 'w') as f:
    for M in man:
        for F in woman:
            f.write(str(M) + "," + str(F) + "," + str(random.randint(1,1000)) + "\n")