from project.customer import *
from ACO.aco import *
from ACO.run import *
from random import seed, random, choice, shuffle, randint

class TspRD:

    def __init__(self,costumers,depot, generations=10):
        self.costumers = costumers
        self.depot = depot
        self.bestSol = (None,900000000000000)
        self.solution = []
        self.generations = generations
        # self.initialize()

    def initialize(self):
        self.solution = [self.costumers]
        (score, path) = run([self.depot] + self.costumers, True)

        if score < self.bestSol[1]:
            self.bestSol = (self.solution,score)

        print(self.bestSol)


    def optimization(self,sol):
        print("START: ", sol)
        for x in range(self.generations):
            sol = self.split(sol)
            print('SPLIT: ', sol)
            sol = self.move(sol)
            print('MOVE: ',sol)
            sol = self.swap(sol)
            print('SWAP: ',sol)
            sol = self.merge(sol)
            print('MERGE: ',sol, '\n\n')


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
