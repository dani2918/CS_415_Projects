
import random
import copy
import math
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


basefitness = 99
savedDNA = []
mr = [0.0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.1, 0.15, 0.2, 0.3]
for i in range(0,20):
    for j in range(0,10):
        savedDNA.append([])
        savedDNA[i].append(random.uniform(-10,10))


class creature:

    length = 10
    def __init__(self, mr, i):
        self.fitness = 0
        self.DNA = []
        self.mutRate = mr # means 5%
        # for i in range(0,self.length):
        #     self.DNA.append(random.uniform(-10,10))
        self.DNA = copy.deepcopy(savedDNA[i])
        self.calcFitness()

    def printCreature(self):
      #  print(self.DNA)
        for i in range(0,self.length):
            print("%0.2f" % self.DNA[i], end = " ")
        print("  %0.2f" % self.fitness)

    def writeCreature(self):
    #     # self.writer.writerow([self.fitness])
    #     # next(self.writer)
        return self.fitness

    def calcFitness(self):
        self.fitness = 0.0
        tot = 0.0
        # print(self.length)
        for i in range(self.length):
            # Schweffel function
            tot += self.DNA[i] * math.sin(math.sqrt(math.fabs(self.DNA[i])))
        self.fitness = 418.9829 * self.length * tot

    def mutate(self):
        #mutRate = self.DNA[0]
        for i in range(0,self.length):
            if(random.randrange(0,100) < self.mutRate):
                self.DNA[i] += random.uniform(-2,2)

    def crossover(self,other,crossoverVal):
        #mutation from class
        if(crossoverVal == 0):
            for i in range(0,self.length):
                if(random.randrange(0,100) < 50):
                    temp = self.DNA[i]
                    self.DNA[i] = other.DNA[i]
                    other.DNA[i] = temp
        # crossover switching first half of self with first half of other
        elif (crossoverVal == 1):
            halfLen = self.length / 2
            for i in range(0, int(halfLen)):
                temp = self.DNA[i]
                self.DNA[i] = other.DNA[i]
                other.DNA[i] = temp

        # crossover picking a random split point then swapping x..y of the data
        elif (crossoverVal == 2):
            startlen = random.randrange(0,self.length)
            endlen = random.randrange(startlen, self.length)
            for i in range(int(startlen), int(endlen)):
                temp = self.DNA[i]
                self.DNA[i] = other.DNA[i]
                other.DNA[i] = temp

        # crossover switching every other value
        elif (crossoverVal == 3):
            for i in range(0,self.length):
                if(i % 2 == 0):
                    temp = self.DNA[i]
                    self.DNA[i] = other.DNA[i]
                    other.DNA[i] = temp

        # crossover switching every 5th value
        elif (crossoverVal == 4):
            for i in range(0,self.length):
                if(i % 5 == 0):
                    temp = self.DNA[i]
                    self.DNA[i] = other.DNA[i]
                    other.DNA[i] = temp

        # crossover
        elif (crossoverVal == 5):
            x = 0



class population:
    popSize = 20

    resultsFile =  open('results.csv', 'w', newline = '')
    writer = csv.writer(resultsFile, delimiter=',', quotechar='|',
     quoting = csv.QUOTE_MINIMAL)

    def __init__(self, mr):
        self.pop = []
        self.fitnessList = []
        self.fitnessListCSV = []
        self.meansList = []
        for i in range(0,self.popSize):
            self.pop.append(creature(mr,i))

    def printPop(self):
        # self.writer.writerows(self.pop)
        for i in range(0,self.popSize):
            self.pop[i].printCreature()

    def writePop(self):
        # for i in range(0,self.popSize):
        l = []
        for i in range(0,self.popSize):
            l.append(self.pop[i].fitness)
        self.fitnessList.append(l)
        self.fitnessListCSV.append(l)

    def writePopToCSV(self, row, col):
        flcsv = []
        fl = []
        for i in range(0,len(self.fitnessListCSV)):
            if not self.fitnessListCSV[i]:
                print(row, col)
                flcsv.append(["mutation: %d crossover: %d" % (row, col)])
            else:
                fl.append([np.mean(self.fitnessListCSV[i])])
                flcsv.append([np.mean(self.fitnessListCSV[i])]) #, np.std(self.fitnessList[i])])
        self.writer.writerows(flcsv)
        self.meansList = copy.deepcopy(fl)


    def plotPop(self, col, alp, mut, crs ):
        x = []
        # for i in range(0,40):
        #     x.apped
        # plt.plot(x,y,c=c)
        plt.plot(self.meansList, color = col, alpha = alp, label = "mutation: %d crossover: %d" % (mut, crs))


    def selectParent(self):
        winner = random.randrange(0,self.popSize)
        winningFitness = self.pop[winner].fitness
        for i in range(0,3):
            temp = random.randrange(0,self.popSize)
            tempFit = self.pop[temp].fitness
            if(tempFit > winningFitness):
                winner = temp
                winningFitness = tempFit
        return winner

    def selectLoser(self):
        winner = random.randrange(0,self.popSize)
        winningFitness = self.pop[winner].fitness
        for i in range(0,3):
            temp = random.randrange(0,self.popSize)
            tempFit = self.pop[temp].fitness
            if(tempFit < winningFitness):
                winner = temp
                winningFitness = tempFit
        return winner

    def iterate(self, cross):
        # find a good individual
        p = self.selectParent()
        p2 = self.selectParent()
        while(p == p2):
            p2 = self.selectParent()
        #print(p, end = " ")
        #self.pop[p].printCreature()
        # find a poor individual
        l = self.selectLoser()
        while(l == p or l == p2):
            l = self.selectLoser()
        l2 = self.selectLoser()
        while(l2 == l or l2 == p or l2 == p2):
            l2 = self.selectLoser()
        # replace the poor with a copy of the good
        self.pop[l] = copy.deepcopy(self.pop[p])
        self.pop[l2] = copy.deepcopy(self.pop[p2])
        # "crossover" l and l2
        self.pop[l].crossover(self.pop[l2], cross)
        # mutate the copy ("offspring")
        self.pop[l].mutate()
        self.pop[l2].mutate()
        # recalculate fitness of offspring
        self.pop[l].calcFitness()
        self.pop[l2].calcFitness()
        #self.pop[p].printCreature()
        #self.pop[l].printCreature()


cols = ['black', 'red', 'green', 'blue', 'yellow', 'orange', 'purple', 'aqua', 'tan', 'navy']
for mutNo in range(0,len(mr)):
    for cross in range(0,5):
        p = population(mr[mutNo])
        p.printPop()
        p.fitnessListCSV.append([])
        # p.writePop()
        for i in range(0,40):
            p.iterate(cross)
            p.writePop()

        print("")
        print("")
        p.printPop()
        p.writePopToCSV(mutNo, cross)

        col= cols[cross]
        alp = mutNo/15 + 0.15

        col = cols[mutNo]
        alp = cross/6 + 0.15
        p.plotPop(col, alp, mutNo, cross)
p.resultsFile.close()
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
    # print(p.fitnessList)
