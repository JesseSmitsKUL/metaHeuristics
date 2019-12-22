
from  project.customer import Customer, Depot

class FileParser:

    def __init__(self, file):
        self.filename = file
        self.vertices = []
        self.depot = None

    def parseFile(self):
        fileLoc = open("./dataTSP/TSPLIB/" + self.filename)
        lines = fileLoc.readlines()
        depot = lines[5].split()
        self.depot = Depot(float(depot[0]), float(depot[1]))

        count = 0
        for line in lines[6:]:
            vertex = line.split()
            self.vertices.append(Customer(float(vertex[0]), float(vertex[1]), int(vertex[-1]), count))
            count+=1
        # print(self.vertices[2].coordinate, " ", self.vertices[2].release)
        return
