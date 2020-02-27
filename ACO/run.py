import math

from ACO.aco import ACO, Graph
from ACO.plot import plot


def distance(c1, c2): # customer -> (x-co, y-co)
    return math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)


def run(customers,plotGraph=False):
    points = list(map(lambda c: c.coordinate, customers))
    cost_matrix = []
    rank = len(customers)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(customers[i].coordinate, customers[j].coordinate))
        cost_matrix.append(row)
    aco = ACO(10, 30, 1.0, 10.0, 0.5, 10, 2)
    graph = Graph(cost_matrix, rank)
    path, cost = aco.solve(graph)
    cost = round(cost,2)
    # print('cost: {}, path: {}'.format(cost, path))
    if plotGraph:
        plot(points, path)
    return (cost,path)
