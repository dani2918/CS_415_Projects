import enchant
import random
import copy
import scoringMatrix

# English Dictionary
dic = enchant.Dict("en_US")

class creature:
    length = 50
    def __init__(self):
        self.fitness = 0
        self.DNA = ""
        self.mutRate = 20 # means x%
        for i in range(0,self.length):
            # choose a random letter from the amino dictionary
            self.DNA += (random.choice(list(scoringMatrix.aminoDictionary.keys())))
        self.calcFitness()

    def printCreature(self):
        for i in range(0,self.length):
            print(self.DNA[i], end = " ")
        print(self.fitness)

    # write the first and last creatures with the highest fitness
    # to a separate file
    def writeStartEnd(self):
        for i in range(0,self.length):
            fFirstLast.write(str(self.DNA[i]))
        fFirstLast.write("\n")

    def writeCreature(self, it):
        # write the generation # to the solution file
        fAns.write(str(it) + "\t")
        for i in range(0,self.length):
            # write the creature to the soution and data files
            f.write(str(self.DNA[i]))
            fAns.write(str(self.DNA[i]))
        f.write("\n")
        fAns.write("\n")

    # print the words found (used for the most fit creature)
    def printWords(self):
        for i in range(0,self.length):
            for j in range(i+2,self.length):
                if dic.check(self.DNA[i:j]):
                    print(self.DNA[i:j], end=" ")
        print(self.fitness)

    # fitness += 1 foreach word found
    def calcFitness(self):
        self.fitness = 0
        # take each letter in string as starting letter
        for i in range(0,self.length):
            # look at potential words of length 2 to end of sting
            for j in range(i+2,self.length):
                # Check slices against English dictionary,
                # Add 1 to fitness we find an English word
                if dic.check(self.DNA[i:j]):
                    self.fitness +=1

    # mutate at rate in init, subst. a random amino
    def mutate(self):
        oldD = self.DNA
        listSelf = list(self.DNA)
        for i in range(0,self.length):
            if(random.randrange(0,100) < self.mutRate):
                randNum = random.randrange(0,10)
                col = scoringMatrix.aminoDictionary.get(self.DNA[i])
                found = False
                # if another amino has a score ≥ a rand between 0,10
                # mutate to that amino
                for j in range(0, len(scoringMatrix.blosum50[col])):
                    if(scoringMatrix.blosum50[j][col] >= randNum):
                        # print("j is", j)
                        for k, v in scoringMatrix.aminoDictionary.items():
                            if(j == v):
                                listSelf[i] = k
                                found = True
                        break
                # safeguard in case no score was founnd
                if(not found):
                    listSelf[i] = random.choice(list(scoringMatrix.aminoDictionary.keys()))
        self.DNA = ''.join(listSelf)

    def crossover(self,other):
        listSelf = list(self.DNA)
        listOther = list(other.DNA)
        for i in range(0,self.length):
            if(random.randrange(0,100) < 50):
                temp = listSelf[i]
                listSelf[i] = listOther[i]
                listOther[i] = temp
        self.DNA = ''.join(listSelf)
        other.DNA = ''.join(listOther)

class population:
    popSize = 50
    def __init__(self):
        self.pop = []
        for i in range(0,self.popSize):
            self.pop.append(creature())

    def printPop(self):
        for i in range(0,self.popSize):
            self.pop[i].printCreature()
        print()

    def printWords(self):
        self.pop[0].printWords()

    def getBest(self):
        bestFit = -999999
        bestCreature = 0
        for i in range(0,self.popSize):
            if(self.pop[i].fitness > bestFit):
                bestFit = self.pop[i].fitness
                bestCreature = i
        return bestCreature

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
        loser = random.randrange(0,self.popSize)
        losingFitness = self.pop[loser].fitness
        for i in range(0,3):
            temp = random.randrange(0,self.popSize)
            tempFit = self.pop[temp].fitness
            if(tempFit < losingFitness):
                loser = temp
                losingFitness = tempFit
        return loser

    def iterate(self, it):
        # find a good individual
        p = self.selectParent()
        p2 = self.selectParent()
        while(p == p2):
            p2 = self.selectParent()
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
        self.pop[l].crossover(self.pop[l2])
        # mutate the copy ("offspring")
        self.pop[l].mutate()
        self.pop[l2].mutate()
        # recalculate fitness of offspring
        self.pop[l].calcFitness()
        self.pop[l2].calcFitness()

        # write best in population to file
        nthIteration = 1
        if((it+1) % nthIteration == 0):
            best = self.getBest()
            self.pop[best].writeCreature(it)


f = open("data.txt","w")
fAns = open("dataWGen.txt","w")
fFirstLast = open("dataFirstLast.txt", "w")
p = population()
# p.printPop()
# write best creature from init population to file as original creature
best = p.getBest()
p.pop[best].writeStartEnd()

maxIt = 1000
for i in range(0,maxIt):
    if(i % 100 == 0):
        print(i) # Debug to see how far along we are
    p.iterate(i)
print("")
print("")
# p.printPop()

# write most fit from last iteration to file
best = p.getBest()
p.pop[best].printWords()
p.pop[best].writeStartEnd()

f.close()
fAns.close()
fFirstLast.close()
