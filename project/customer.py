
class Customer:

    def __init__(self,x,y,rd,id):
        self.coordinate = (x,y)
        self.release = rd
        self.id = id

class Depot:

    def __init__(self,x,y):
        self.coordinate = (x,y)
        self.release = 0
        self.id = 0
