from project.parser import FileParser
from ACO.run import *
from project.tspRD import TspRD

def main():
    parser = FileParser("ch130_1.5.dat")
    parser.parseFile()

    customers = parser.vertices
    depot = parser.depot

    tsprd = TspRD(customers,depot)
    tsprd.optimization([[0,1,2,3,4,5,6,7,9,10], [33,44]])
    #run(customers)


if __name__ == "__main__":
    # execute only if run as a script
    main()
