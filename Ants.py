from random import randrange

class Ants(object):

    def __init__(self, numCities):

       self.tabulist = [0]*numCities
       #Where the ant will be
       self.currentCity = randrange(0,numCities)
       self.nextCity = 0
       #tour list for ant
       self.tour = [0]*numCities
       self.tourIndex = 0
       #length of tour
       self.tourlength = 0.0

