from project.customer import *
from ACO.aco import *
from ACO.run import *
from random import seed, random, choice, shuffle, randint
from project.clustering import cluster
from copy import deepcopy



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
        self.generations = generations
        self.initialize()

    def initialize(self):
        self.solution = [self.costumers]
        delayStart = earliestStart(self.costumers)


        (score, path) = run([self.depot] + self.costumers, True)

        if score < self.bestSol[1]:
            self.bestSol = (self.solution,score + delayStart)

        self.toEval.append(self.solution)
        # print(self.bestSol)

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
            (score, path) = run(route, True)
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

        for x in range(self.generations):
            newSol = []
            sol = choice(self.toEval)

            newSol.append(self.split(sol))
            newSol.append(self.move(sol))
            newSol.append(self.swap(sol))
            newSol.append(self.merge(sol))


            scores = [(self.getScore(s),s) for s in newSol]
            scores.sort(key=lambda x: x[0])

            print(scores)
            break


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


    def split(self,solution):   # [  [x] [y] [z] ]
        solution = deepcopy(solution)
        part = choice(solution)
        if len(part) == 1:
            return solution

        solution.remove(part)

        split = cluster(randint(2,6),part)


        split.sort(key=lambda x: earliestStart(x))
        rest = []
        for x in split[1:]:
            rest += x

        print("info")
        print(len(part))
        print(len(split[0]), len(rest))
        solution.append(split[0])
        solution.append(rest)

        return solution


    def swap(self,solution):
        solution = deepcopy(solution)
        if len(solution) == 1:
            return solution
        part1 = choice(solution)
        solution.remove(part1)

        part2 = choice(solution)
        solution.remove(part2)

        c1 = choice(part1)
        c2 = choice(part2)

        part1.remove(c1)
        part1.append(c2)
        part2.remove(c2)
        part2.append(c1)

        solution.extend([part1,part2])
        return solution


    def move(self,solution):
        solution = deepcopy(solution)
        if len(solution) == 1:
            return solution
        part1 = choice(solution)
        solution.remove(part1)

        part2 = choice(solution)
        solution.remove(part2)

        c1 = choice(part1)
        part1.remove(c1)
        part2.append(c1)

        solution.extend([part1,part2])
        solution = [x for x in solution if x != []]
        return solution
