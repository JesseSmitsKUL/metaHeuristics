import sys
import os
from project.parser import FileParser
from ACO.run import *
from project.tspRD import TspRD
from copy import deepcopy


DatasetList = os.listdir("./dataTSP/TSPLIB/")
def main():
    print(DatasetList)
    for file in DatasetList:

        parser = FileParser(file)
        parser.parseFile()

        customers = parser.vertices
        depot = parser.depot


        tsprd = TspRD(customers,depot)



        tsprd.optimization(file)
    #run(customers)

if __name__ == "__main__":
    main()
