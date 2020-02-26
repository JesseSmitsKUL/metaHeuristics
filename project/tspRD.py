from project.customer import *
from ACO.aco import *
from ACO.run import *
from random import seed, random, choice, shuffle, randint
from project.clustering import cluster
from copy import deepcopy
from math import sqrt
from datetime import datetime


def distance(c1,c2):
    x1,y1 = c1.coordinate
    x2,y2 = c2.coordinate

    return sqrt( (x1-x2)**2 + (y1-y2)**2 )

def earliestStart(route):
    routeEarly = 0
    for stop in route:
        stopRD = stop.release
        if stopRD > routeEarly:
            routeEarly = stopRD

    return routeEarly

class TspRD:

    def __init__(self,costumers,depot, generations=200):
        self.costumers = costumers
        self.depot = depot
        self.bestSol = (None,900000000000000)
        self.solution = []
        self.toEval = []
        self.timeStart = 0
        self.generations = generations
        self.initialize()

    def initialize(self):
        self.solution = [self.costumers]
        delayStart = earliestStart(self.costumers)


        (score, path) = run([self.depot] + self.costumers, True)

        if score < self.bestSol[1]:
            self.bestSol = (self.solution,score + delayStart)

        self.toEval.append(self.solution)

        self.timeStart = datetime.now()

    def destroyRepair(self,alpha):
        pass

    def getScore(self,sol):
        print("Calculating new score")
        totalScore = 0
        sol.sort(key=lambda x: earliestStart(x))
        for route in sol:
            # if earliest start of route is after return of vehicle we need to add waiting time
            delayStart = max(0, earliestStart(route) - totalScore)
            route = route + [self.depot]
            (score, path) = run(route, False)
            totalScore += score + delayStart
            print("score: ", totalScore)

        if totalScore < self.bestSol[1]:
            print("Better solution: ", totalScore)
            print("\n\n")
        return totalScore


    def optimization(self):
        print("START! initial solution", self.bestSol[1])
        # sol = self.solution
        # print(sol)
        # sol = cluster(2,sol[0])

        self.toEval = [self.bestSol[0]]

        for x in range(self.generations):

            print("TIME: ",(datetime.now() - self.timeStart).total_seconds() / 60.0)

            newSol = []
            sol = choice(self.toEval)
            sol = [x for x in sol if x != []]

            newSol.append(self.split(sol))
            newSol.append(self.move(sol))
            newSol.append(self.shift(sol))
            newSol.append(self.merge(sol))


            scores = [(s,self.getScore(s)) for s in newSol]
            scores.sort(key=lambda x: x[1])


            if scores[0][1] <  self.bestSol[1]:
                self.bestSol = scores[0]
                print("new best score: ", self.bestSol[1])

            print("Current best score: ", self.bestSol[1])

            self.toEval = [self.bestSol[0],choice(scores)[0]]  #, choice(scores)[0], choice(scores)[0]]



    def merge(self,solution):
        solution = deepcopy(solution)
        if len(solution) == 1:
            return solution
        part1 = choice(solution)
        solution.remove(part1)

        part2 = choice(solution)
        solution.remove(part2)

        newPart = part1 + part2
        solution.append(newPart)
        return solution


    def split(self,solution):
        solution = deepcopy(solution)
        part = choice(solution)
        if len(part) < 2:
            return solution

        solution.remove(part)

        split = cluster(randint(2,min(len(part),6)),part)


        split.sort(key=lambda x: earliestStart(x))

        if randint(0,1) == 0:
            rest = []
            for x in split[1:]:
                rest += x

            solution.append(split[0])
            solution.append(rest)
        else:
            rest = []
            for x in split[:-1]:
                rest += x

            solution.append(split[-1])
            solution.append(rest)

        return solution


    def shift(self,solution):
        solution = deepcopy(solution)
        if len(solution) == 1:
            return solution
        index = randint(0,len(solution)-1)
        part1 = solution[index]
        part1.sort(key=lambda x: x.release)

        scoreLeft  = "N" if index == 0 else part1[0].release -sorted(solution[index-1],key=lambda x : x.release)[-1].release
        scoreRight = "N" if index == len(solution)-1 else sorted(solution[index+1],key=lambda x : x.release)[0].release - part1[-1].release

        if scoreLeft == "N":
            print("RIGHT ")
            i = randint(0, len(part1) - 1)
            if len(part1) > 0:
                solution[index+1].extend(part1[i:])
                del part1[i:]

        elif scoreRight == "N":
            i = randint(0, len(solution[index-1]) - 1)
            if len(solution[index-1]) > 0:
                solution[index - 1].sort(key=lambda x: x.release)
                part1.extend(solution[index-1][i:])
                del solution[index-1][i:]

        else:
            r = randint(0,1)
            if r == 0:
                if len(part1) > 0:
                    i = randint(0, len(part1) - 1)
                    solution[index+1].extend(part1[i:])
                    del part1[i:]
            else:
                i = randint(0, len(solution[index - 1]) - 1)
                if len(solution[index - 1]) > 0:
                    solution[index - 1].sort(key=lambda x: x.release)
                    part1.extend(solution[index - 1][i:])
                    del solution[index - 1][i:]

        return solution


    def move(self,solution):
        solution = deepcopy(solution)
        if len(solution) == 1:
            return solution





        part1 = choice(solution)
        c1 = choice(part1)
        part1.remove(c1)

        # part2 = choice(solution)
        # solution.remove(part2)

        sDistance = 100000000000
        sRoute = 0
        for route in solution:
            for v in route:
                d = distance(c1,v)
                if d < sDistance:
                    sRoute = route
                    sDistance = d



        route.append(c1)
        solution = [x for x in solution if x != []]
        return solution
