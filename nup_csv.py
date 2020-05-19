import numpy as np
import math
def index(human_unit):
    if human_unit < 2 * 10**int(math.log10(human_unit)) :
        MF = 0
    elif human_unit >= 2 * 10**int(math.log10(human_unit)) and human_unit < 3 * 10**int(math.log10(human_unit)):
        MF = 1  
    raw_data = open("kekka_9.csv", 'r')
    data = np.loadtxt(raw_data, delimiter=",")
    dd = data[np.where(data[:,MF] == human_unit)]
    raw_data.close()
    dd_sort = dd[np.argsort(dd[:, 2])]
    return dd_sort
if __name__ == "__main__":
    human_unit = int(input())
    if human_unit <= 1 * 10**math.log10(human_unit):
        FM = 1
    elif human_unit >= 2 * 10**int(math.log10(human_unit)) and human_unit < 3 * 10**int(math.log10(human_unit)):
        FM = 0
    #print(2 * 10**int(math.log10(human_unit)))
    dd = index(int(human_unit))
    words=""
    for i in dd:
        words += str(str(int(i[FM]))+"→"+str(int(i[2]))+"\n")
    words = words.rstrip()
    print(words)