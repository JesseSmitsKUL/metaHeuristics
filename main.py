from project.parser import FileParser
from ACO.run import *
from project.tspRD import TspRD
from copy import deepcopy

def main():
    parser = FileParser("kroB100_1.dat")
    parser.parseFile()

    customers = parser.vertices
    depot = parser.depot


    tsprd = TspRD(customers,depot)



    tsprd.optimization()
    #run(customers)


if __name__ == "__main__":
    main()
