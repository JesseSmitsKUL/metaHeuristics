from project.customer import *
from ACO.aco import *
from ACO.run import *
from random import seed, random, choice, shuffle, randint
from project.clustering import cluster



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
        self.generations = generations
        self.initialize()

    def initialize(self):
        self.solution = [self.costumers]
        delayStart = earliestStart(self.costumers)


        (score, path) = run([self.depot] + self.costumers, True)

        if score < self.bestSol[1]:
            self.bestSol = (self.solution,score + delayStart)

        # print(self.bestSol)

    def optimization(self):
        print("START! initial solution", self.bestSol[1])
        sol = self.solution



        print(sol)
        sol = cluster(2,sol[0])



        for x in range(self.generations):
            break
            randomVal = randint(0,4)
            while randomVal != 0:
                if randomVal == 1:
                    sol = self.split(sol)
                elif randomVal == 2:
                    sol = self.move(sol)
                elif randomVal == 3:
                    sol = self.swap(sol)
                elif randomVal == 4:
                    sol = self.merge(sol)
                else:
                    continue
                randomVal = randint(0,4)

            sol.sort(key=lambda x: earliestStart(x))

            self.solution = sol

            #print(sol)
            # for x in sol:
            #     print(earliestStart(x))
            # print('\n')

        totalScore = 0
        for route in sol:
            # if earliest start of route is after return of vehicle we need to add waiting time
            delayStart = max(0,earliestStart(route)-totalScore)
            route = route + [self.depot]
            (score, path) = run(route, True)
            totalScore += score + delayStart
            print("score: ",totalScore)

        if totalScore < self.bestSol[1]:
            print("Better solution: ", totalScore)
            self.bestSol = (self.solution,totalScore)
        print("Best so far: ", self.bestSol[1])

        print("\n\n")


    def merge(self,solution):
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
        part = choice(solution)
        if len(part) == 1:
            return solution

        solution.remove(part)

        shuffle(part)
        cut = randint(1, len(part)-1)
        subPart1 = part[:cut]
        subPart2 = part[cut:]
        solution.extend([subPart1,subPart2])
        return solution


    def swap(self,solution):
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
