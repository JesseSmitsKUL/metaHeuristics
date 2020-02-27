
class Customer:

    def __init__(self,x,y,rd,id):
        self.coordinate = (x,y)
        self.release = rd
        self.id = id

    def getData(self):
        return [self.coordinate[0], self.coordinate[1], self.release]

    def __str__(self):
        return 'CustomerRD ' + str(self.release)

    def __repr__(self):
       return "C " +str(self.id)

    def __eq__(self, other):
        return self.id == other.id

class Depot:

    def __init__(self,x,y):
        self.coordinate = (x,y)
        self.release = 0
        self.id = 0
