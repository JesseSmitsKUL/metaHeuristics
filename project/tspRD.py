from project.customer import *
from ACO.aco import *
from ACO.run import *
from random import seed, random, choice, shuffle, randint, uniform
from project.clustering import cluster
from copy import deepcopy
from math import sqrt
from datetime import datetime

def getSizeSol(sol):
    count = 0
    for r in sol:
        count += len(r)
    return count


def toTupleIds(customers):
    c = [v.id for v in customers]
    return tuple(c)

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

def rmEL(sol):
    newroute = [x for x in sol[0] if x]
    return (newroute,sol[1])

class TspRD:

    def __init__(self,costumers,depot, generations=200):
        self.costumers = costumers
        self.depot = depot
        self.bestSol = (None,None)
        self.solution = []
        self.toEval = []
        self.timeStart = 0
        self.generations = generations
        self.control = 0
        self.validatedScores = dict()
        self.currentSol = 0
        self.initialScore = 10000000000000
        self.initialize()

    def initialize(self):
        self.solution = [self.costumers]
        delayStart = earliestStart(self.costumers)


        (score, path) = run([self.depot] + self.costumers, False, False)

        self.initialize = score + delayStart
        self.bestSol = (self.solution, score + delayStart)

        self.toEval.append(self.bestSol)

        self.timeStart = datetime.now()

    def printinfo(self):
        print("control: ", self.control, " currentSol ", self.currentSol, ' routes: ', len(self.toEval[0][0]))

    def destroyRepair(self,solpair):

        if len(solpair[0]) == 1 or self.control == 0.0:
            return solpair

        sol = deepcopy(solpair[0])
        # merge or split randomly
        if randint(0,1) == 0:
            if len(sol) > 1:
                p1 = choice(sol)
                sol.remove(p1)
                p2 = choice(sol)
                p2.extend(p1)
        else:
            newRoute = []
            part = choice(sol)
            if len(part) < 2:
                sol.append([])
            else:
                part.sort(key=lambda x: x.release)
                newRoute.append(part[0])
                del part[0]
                sol.append(newRoute)
                print(sol)



        cost = [x for x in range(len(self.costumers))]
        shuffle(cost)
        index = int((self.control/5.0)*len(cost))-1
        toShuffle = cost[:index]


        for x in toShuffle:
            customer = 0
            for route in sol:
                for c in route:
                    if(c.id == x):
                        customer = deepcopy(c)
                        route.remove(c)
            routeToInsert = choice(sol)
            routeToInsert.append(customer)


        # move customers randomly

        score = self.getScore(sol)
        self.currentSol = score
        if self.control == 1.0:
            self.control = 0

        if score > self.initialScore:
            return solpair
        else:
            return (sol,score)

    def getScorePerformance(self,sol):
        totalScore = 0
        # print("start Scoring")
        sol.sort(key=lambda x: earliestStart(x))
        for route in sol:
            route.sort(key=lambda x: x.id)
            score = 0
            tuppleroute = toTupleIds(route)
            if tuppleroute in self.validatedScores:
                score = self.validatedScores[tuppleroute]
            else:
                routeWD = route + [self.depot]
                (score, path) = run(routeWD, True, False)
                self.validatedScores[tuppleroute] = score

            # if earliest start of route is after return of vehicle we need to add waiting time
            delayStart = max(0, earliestStart(route) - totalScore)
            totalScore += score + delayStart
        # print("end Scoring")
        return totalScore


    def getScore(self,sol):
        totalScore = 0
        # print("start Scoring")
        sol.sort(key=lambda x: earliestStart(x))
        for route in sol:
            route.sort(key=lambda x: x.id)
            score = 0
            tuppleroute = toTupleIds(route)
            if tuppleroute in self.validatedScores:
                score = self.validatedScores[tuppleroute]
            else:
                routeWD = route + [self.depot]
                (score, path) = run(routeWD,False, False)
                self.validatedScores[tuppleroute] = score

            # if earliest start of route is after return of vehicle we need to add waiting time
            delayStart = max(0, earliestStart(route) - totalScore)
            totalScore += score + delayStart
        # print("end Scoring")
        return totalScore


    def optimization(self,dataset):
        print("START! initial solution", self.bestSol[1])
        print("LEN! ", getSizeSol(self.bestSol[0]))
        print(self.bestSol[0])
        # sol = self.solution
        # print(sol)
        # sol = cluster(2,sol[0])



        self.toEval = [self.bestSol]

        for x in range(self.generations):

            print("TIME: ",(datetime.now() - self.timeStart).total_seconds() / 60.0)

            # decision = uniform(0,1)
            # sol = self.toEval[0] if self.control <= decision else self.toEval[1]

            sol = self.toEval[0]
            path = [x for x in sol[0] if x != []]
            sol = (path, sol[1])


            # # same for each
            # newSol.append(self.split(sol))
            # newSol.append(self.move(sol))
            # newSol.append(self.shift(sol))
            # newSol.append(self.merge(sol))

            newSol = self.split(rmEL(sol))
            newSol = self.hSplit(rmEL(newSol))
            newSol = self.merge(rmEL(newSol))
            newSol = self.shift(rmEL(newSol))
            newSol = self.move(rmEL(newSol))
            newSol = rmEL(newSol)


            # newSol.sort(key=lambda x: x[1])

            if newSol[1] < self.bestSol[1]:
                self.bestSol = newSol
                print("new best score: ", self.bestSol[1])
                self.control = 0.0
            elif newSol[1] >= self.currentSol:
                self.control = min(self.control+0.2,1.0)
            else:
                self.currentSol = newSol[1]
                self.toEval = [newSol]
                print("Current best score: ", self.bestSol[1], ' with ', len(self.bestSol[0]), ' routes')
                self.printinfo()
                continue

            print("Current best score: ", self.bestSol[1], ' with ', len(self.bestSol[0]), ' routes')
            self.printinfo()

            repairedSol = self.destroyRepair(self.bestSol)
            self.toEval = [repairedSol]  #, choice(scores)[0], choice(scores)[0]]

        print("##############\nFinal score with performance ACO:")
        score = self.getScorePerformance(self.bestSol[0])
        print(score)
        print("##############")
        f = open("TSPResults.txt", "a")
        f.write(dataset + ": " + str(score) + "\n")
        f.close()






    def merge(self,solutionpair):
        current_score = solutionpair[1]
        solution = deepcopy(solutionpair[0])
        if len(solution) == 1:
            return solutionpair

        # try out until better solution or ran out of tries


        for x in range(len(solution)-2):
            solution = deepcopy(solutionpair[0])
            solution.sort(key=lambda x: earliestStart(x))
            p1 = solution[x]
            p2 = solution[x+1]
            solution.remove(p1)
            solution.remove(p2)
            newRoute = p1 + p2
            solution.append(newRoute)
            score = self.getScore(solution)
            if score < current_score:
                return (solution,score)

        return solutionpair



        # Randomized part

        # part1 = choice(solution)
        # solution.remove(part1)
        #
        # part2 = choice(solution)
        # solution.remove(part2)
        #
        # newPart = part1 + part2
        # solution.append(newPart)
        # return solution

    def hSplit(self,solutionpair):
        current_score = solutionpair[1]
        solution = deepcopy(solutionpair[0])

        for x in range(len(solutionpair[0])):
            if len(solution[x]) == 1:
                continue

            solution[x].sort(key=lambda x: x.release)

            split = [[solution[x][0]], solution[x][1:]]
            del solution[x]
            solution.extend(split)
            score = self.getScore(solution)


            if score < current_score:
                return (solution, score)

            solution = deepcopy(solutionpair[0])

        return solutionpair

    def split(self,solutionpair):

        current_score = solutionpair[1]
        solution = deepcopy(solutionpair[0])

        for x in range(len(solutionpair[0])):
            if len(solution[x]) == 1:
                continue
            split = cluster(randint(2, min(len(solution[x]), 4)), solution[x])
            del solution[x]
            split.sort(key=lambda x: earliestStart(x))

            # take 1 and concat later ones
            rest = []
            for x in split[1:]:
                rest += x


            copysol = deepcopy(solution)
            copysol.append(split[0])
            copysol.append(rest)
            score = self.getScore(copysol)
            if score < current_score:
                return (copysol,score)

            # take last and concat earlier ones
            rest = []
            for x in split[:-1]:
                rest += x

            copysol = deepcopy(solution)
            copysol.append(split[-1])
            copysol.append(rest)
            score = self.getScore(copysol)
            if score < current_score:
                return (copysol, score)


            solution = deepcopy(solutionpair[0])

        return solutionpair

        # random solution

        # solution = deepcopy(solution)
        # part = choice(solution)
        # if len(part) < 2:
        #     return solution
        #
        # solution.remove(part)
        #
        # split = cluster(randint(2,min(len(part),4)),part)
        #
        #
        # split.sort(key=lambda x: earliestStart(x))
        #
        # if randint(0,1) == 0:
        #     rest = []
        #     for x in split[1:]:
        #         rest += x
        #
        #     solution.append(split[0])
        #     solution.append(rest)
        # else:
        #     rest = []
        #     for x in split[:-1]:
        #         rest += x
        #
        #     solution.append(split[-1])
        #     solution.append(rest)
        #
        # return solution


    def shift(self,solutionpair):

        current_score = solutionpair[1]
        solution = deepcopy(solutionpair[0])

        if len(solution) == 1:
            return solutionpair


        for index in range(len(solutionpair[0])-1):
            part1 = solution[index]
            if len(part1) < 2:
                continue
            if index == 0:
                i = randint(0, len(part1) - 1)
                if len(part1) > 0:
                    solution[index+1].extend(part1[i:])
                    del part1[i:]

            elif index == len(solution)-1:
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
                    if len(solution[index - 1]) > 0:
                        i = randint(0, len(solution[index - 1]) - 1)
                        solution[index - 1].sort(key=lambda x: x.release)
                        part1.extend(solution[index - 1][i:])
                        del solution[index - 1][i:]

            score = self.getScore(solution)
            if score < current_score:
                return (solution, score)
            solution = deepcopy(solutionpair[0])
        return solutionpair




        # randomized

        # index = randint(0,len(solution)-1)
        # part1 = solution[index]
        # part1.sort(key=lambda x: x.release)
        #
        # scoreLeft  = "N" if index == 0 else part1[0].release -sorted(solution[index-1],key=lambda x : x.release)[-1].release
        # scoreRight = "N" if index == len(solution)-1 else sorted(solution[index+1],key=lambda x : x.release)[0].release - part1[-1].release
        #
        # if scoreLeft == "N":
        #     i = randint(0, len(part1) - 1)
        #     if len(part1) > 0:
        #         solution[index+1].extend(part1[i:])
        #         del part1[i:]
        #
        # elif scoreRight == "N":
        #     i = randint(0, len(solution[index-1]) - 1)
        #     if len(solution[index-1]) > 0:
        #         solution[index - 1].sort(key=lambda x: x.release)
        #         part1.extend(solution[index-1][i:])
        #         del solution[index-1][i:]
        #
        # else:
        #     r = randint(0,1)
        #     if r == 0:
        #         if len(part1) > 0:
        #             i = randint(0, len(part1) - 1)
        #             solution[index+1].extend(part1[i:])
        #             del part1[i:]
        #     else:
        #         i = randint(0, len(solution[index - 1]) - 1)
        #         if len(solution[index - 1]) > 0:
        #             solution[index - 1].sort(key=lambda x: x.release)
        #             part1.extend(solution[index - 1][i:])
        #             del solution[index - 1][i:]
        #
        # return solution


    def move(self,solutionpair):

        current_score = solutionpair[1]
        solution = deepcopy(solutionpair[0])
        if len(solution) == 1:
            return solutionpair


        part1 = choice(solution)
        solution.remove(part1)
        other = solution
        for c1 in part1:
            copyPart1 = deepcopy(part1)
            copyPart1.remove(c1)


            for r in range(len(other)):
                copyOther = deepcopy(other)
                copyOther[r].append(c1)
                s = [copyPart1]
                s.extend(copyOther)
                score = self.getScore(s)
                if score < current_score:
                    return (s, score)

        return solutionpair
