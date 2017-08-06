from matplotlib import pyplot as plt
from numpy import *
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from Ants import *
import math
from random import randint
import copy as cp
from operator import itemgetter, attrgetter
from random import randint,randrange

class main(object):

    def __init__(self):

        self.ants = []
        self.cities = []
        self.tauMatrix = [[]]
        self.adjMatrix = [[]]
        self.besttour = []
        self.currentIndex = 0
        self.numCities = 0
        self.rho = 0.6
        self.qval = 1.0
        self.alpha = 0.8
        self.beta = 0.8
        self.numAnts = 10

    #intensify trail after every iteration
    def intensifyTrail(self):
        start = 0;
        end = 0;

        for i in range(self.numAnts):
            for j in range(self.numCities):
                start = self.ants[i].tour[j]
                end = self.ants[i].tour[((j+1) % self.numCities)]
                deltatau = (self.qval / self.ants[i].tourlength)
                self.tauMatrix[start][end] = self.tauMatrix[start][end] + deltatau
                self.tauMatrix[start][end] = self.tauMatrix[start][end]

    #calculate best length of tour
    def calculateBest(self):
        bestlength = 0
        bestlength = self.ants[0].tourlength
        if self.besttour == None:
            self.besttour[self.numCities]
            self.besttour = self.ants[0].tour

        for i in range(self.numAnts):
            if self.ants[i].tourlength < bestlength:
                bestlength = self.ants[i].tourlength
                self.besttour = self.ants[i].tour
                #print 'The best tour ', self.besttour
        return bestlength


    #calculate average length
    def calculateAvg(self):
        avglength = self.ants[0].tourlength
        total = 0
        for i in self.ants:
            total += i.tourlength
        avglength = total / 10
        return avglength

    #initialize trail by using tau matrix
    def initTrail(self):
        self.tauMatrix = [[1.0 for i in range(self.numCities)] for j in range(self.numCities)]
        print "tauMatrix: ", self.tauMatrix
        # for i in range(self.numCities-1):
        #     for j in range(self.numCities-1):
        #         if i != j:
        #             self.tauMatrix[i][j] = 1.0
        #         else:
        #             self.tauMatrix[i][j] = 0.0


    #Initialize ants
    def initializeAnts(self):
        self.ants = [None]*self.numAnts
        for i in range(self.numAnts):
            self.ants[i] = Ants(self.numCities)


    def moveAnts(self):
        for i in self.ants:
            self.currentIndex = 0
            if self.currentIndex < self.numCities:
                self.moveToNewCity(i)
                self.currentIndex = self.currentIndex+1

    #move to a new city
    def moveToNewCity(self, ant):
        p = 0.0
        denom = 0.0
        start = ant.currentCity
        #chooses the next shortest path and update the tour, tourindex, tourlength and current city accordingly
        for end in range(self.numCities):
            if start != end:
                #Tabulist contains tour information
                if ant.tabulist[end] == 0 and self.tauMatrix[start][end] != 0 and self.adjMatrix[start][end] != 0:
                    denom += float(math.pow(float(self.tauMatrix[start][end]),self.alpha) * math.pow(float(1.0/self.adjMatrix[start][end]),self.beta))
                    #print denom
            else:
               continue

        end = 0
        while True:
            if start != end:
                #print self.adjMatrix[start][end]
                #print p
                if ant.tabulist[end] == 0 and self.tauMatrix[start][end] != 0 and self.adjMatrix[start][end] != 0:
                    p = (math.pow(float(self.tauMatrix[start][end]),self.alpha) * math.pow(float(1.0/self.adjMatrix[start][end]), self.beta))/denom
                    if random.random() < p:
                        break
            else:
                end = ((end + 1)% self.numCities)
                continue
            end = ((end + 1 ) % self.numCities)

        ant.nextCity = end
        ant.tabulist[ant.nextCity] = 1
        ant.tour[ant.tourIndex] = ant.nextCity
        ant.tourIndex = ant.tourIndex + 1
        ant.tourlength += self.adjMatrix[ant.currentCity][ant.nextCity]
        if ant.tourIndex == self.numCities:
            ant.tourlength += self.adjMatrix[ant.tour[self.numCities-1]][ant.tour[0]]
        ant.currentCity = ant.nextCity


    def evaporatePheromone(self):
        start = 0
        end = 0
        for start in range(self.numCities):
            for end in range(self.numCities):
                self.tauMatrix[start][end] = self.tauMatrix[start][end] * (1.0 - self.rho)
                if self.tauMatrix[start][end] < 0.0:
                    self.tauMatrix[start][end] = 1.0


    def initGraph(self, name):
        #file reading using pandas
        df = pd.read_excel(name, sheetname='Sheet1')
        dim = df['Dimension']
        x = df['X']
        y = df['Y']
        #print x,y
        self.numCities = len(dim)
        #set and fill the adjMatrix
        self.adjMatrix = [[1.0 for i in range(self.numCities)] for j in range(self.numCities) ]
        for i in range(self.numCities):
            for j in range(self.numCities):
        #fill the adjmatrix with city coordinates and calculate euclidean distances
                self.adjMatrix[i][j] = self.calEdge(x[i], x[j], y[i], y[j])

    #calculating edge weights using euclidean distances
    def calEdge(self, x1, x2, y1, y2):
        return math.pow((math.pow((y2-y1),2) + math.pow((x2-x1),2)), 0.5)



    def plotter(self):
      # comment/uncomment to run the other one.
      # extracts X Y co-ordinates of the cities.
        self.initGraph("djibouti.xlsx")
        #self.initGraph('sahara.xlsx')

        avgavg = [0.0] * 10
        avgbest = [0.0] * 10
        besttourlens = [0.0] * 10
        avgtourlens = [0.0] * 10
        iterations = 0
        i = 0
        j = 0
        iterations_values= []

        #init ants.
        self.initTrail()
        while i < 10:
            besttour = None
            j=0
            iterations_values.append(i)
            while j < 500:
                # print i,j
            # initialize all ants
                self.initializeAnts()
            # move ants
                self.moveAnts()
            # intensify pheromone levels
                self.intensifyTrail()
            # compute best and avg tour lengths for every tour for every ant
                besttourlens[i] += self.calculateBest()
                avgtourlens[i]  += self.calculateAvg()
                j=j+1
            self.evaporatePheromone()
            print 'Iteration: {} , Path: {}'.format(i,self.besttour);
            #print "Optimal path: ", self.besttour;
            avgavg[i] = avgtourlens[i]/500.0
            avgbest[i] = besttourlens[i]/500.0
            i=i+1

        print "Average Average: ", avgavg;
        print "Average Best: ", avgbest;

        plt.figure(1)
        plt.plot(iterations_values, avgbest, 'bo', label='avgbest')
        plt.plot(iterations_values, avgavg, 'ro', label='avgavg')
        plt.legend(loc='upper right')
        plt.xlabel('Average best & Average average graph')
        plt.show()




def Main():
    obj = main()
    obj.plotter()
    #obj.initGraph('djibouti.xlsx')

if __name__ == '__main__':
     Main();


