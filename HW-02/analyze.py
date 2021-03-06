import random
import copy
import scoringMatrix
import numpy as np

# Read generations from file
f = open('data.txt','r')
dat = f.read().splitlines()
ffirst = open('dataFirstLast.txt','r')
firstDat = ffirst.read().splitlines()
# Randomly reorder
random.shuffle(dat)
scoreArr = []
# get original sequence to compare all against
originalSeq = firstDat[0]
# print(originalSeq)

# Code from lecture
# Init score, direction matrix
scorematrix = [[0] * (len(originalSeq)+1) for _ in range(len(dat[0])+1)]
directionmatrix = [[8] * (len(originalSeq)+1) for _ in range(len(dat[0])+1)]
savedScoreMat = copy.deepcopy(scorematrix)
savedDirectionMat = copy.deepcopy(directionmatrix)
for i in range(0,len(originalSeq)+1):
    scorematrix[0][i] = -8*i
    directionmatrix[0][i]  = 1
for i in range(0,len(dat[0])+1):
    scorematrix[i][0] = -8*i
    directionmatrix[i][0] = 0

# calculate scores for all sequences
for k in range(len(dat)):
    for j in range(1,len(dat[0])+1):
        for i in range(1,len(originalSeq)+1):
            v = scorematrix[j-1][i] + scoringMatrix.gappenalty
            h = scorematrix[j][i-1] + scoringMatrix.gappenalty
            x = scoringMatrix.aminoDictionary[originalSeq[i-1]]
            y = scoringMatrix.aminoDictionary[dat[k][j-1]]
            d = scorematrix[j-1][i-1] + scoringMatrix.blosum50[x][y]
            scorematrix[j][i] = max(v,h,d)
            if(v > h and v > d):
                directionmatrix[j][i] = 0 # 0 - vertical move
            if(h > v and h > d):
                directionmatrix[j][i] = 1 # 1 - horizontal move
            if(d >= v and d >= h):
                directionmatrix[j][i] = 2 # 2 - diagonal move
    x = len(originalSeq)
    y = len(dat[k])
    # print("Score = ",scorematrix[y][x])
    scoreArr.append([scorematrix[y][x], dat[k]])

    #restore score, direction matrices
    scorematrix = copy.deepcopy(savedScoreMat)
    directionmatrix = copy.deepcopy(savedDirectionMat)

# order array based on decending alignment scores
npScoreArr = np.array(scoreArr)
npScoreArr = npScoreArr[np.argsort(npScoreArr[:,0])]
npScoreArr = npScoreArr[::-1]

# Compare against original generation order
for i in range(len(npScoreArr)):
    npScoreArr[i][0] = i
fscored = open('data.txt','r')
finalDat = fscored.read().splitlines()
finalDat = np.array(finalDat)
dist = 0
possibleDist = []
for i in range(len(npScoreArr)):
    for j in range(len(npScoreArr)):
        if(npScoreArr[i][1] == finalDat[j]):
            possibleDist.append(abs(i-j))
    # Sum deviations from expected location
    dist += min(possibleDist)
    possibleDist = []
# print mean of deviations
print(dist/len(npScoreArr))

fscored.close()
f.close()
ffirst.close()
