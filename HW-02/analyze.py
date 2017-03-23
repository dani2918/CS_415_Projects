import enchant
import random
import copy
import scoringMatrix

# Read generations from file
f = open('data.txt','r')
dat = f.read().splitlines()

# Randomly reorder
random.shuffle(dat)


# TODO: alignment
