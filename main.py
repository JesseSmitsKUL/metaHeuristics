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

        if "2." in file or "2.5." in file or "3." in file:

            parser = FileParser(file)
            parser.parseFile()

            customers = parser.vertices
            depot = parser.depot
            contents = ''
            with open('TSPResults.txt', 'r') as c:
                contents = c.read()

            if len(customers) > 125 or file in contents:
                continue

            print("#############\nSOLVING: " + file + "\n#############")

            tsprd = TspRD(customers,depot)



            tsprd.optimization(file)
    #run(customers)

if __name__ == "__main__":
    main()
