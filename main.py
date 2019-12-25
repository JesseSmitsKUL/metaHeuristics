from project.parser import FileParser
from ACO.run import *
from project.tspRD import TspRD

def main():
    parser = FileParser("eil51_3.dat")
    parser.parseFile()

    customers = parser.vertices
    depot = parser.depot

    tsprd = TspRD(customers,depot)
    tsprd.optimization()
    #run(customers)


if __name__ == "__main__":
    # execute only if run as a script
    main()
