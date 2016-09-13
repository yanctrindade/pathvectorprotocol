import threading

class Node:
    id = -1
    neighbors = []
    routingTable = {}

    def __init__ (self, id):
        self.id = id
        self.neighbors = []
        self.routingTable = {}

    def creatingPathTable(self):

        list = []
        list.append(0) #node itself
        list.append(1) #jump
        pathList = []
        pathList.append(self.id)
        list.append(pathList) #path
        self.routingTable[self.id] = list

        for neighbor in self.neighbors:
            list = []
            list.append(neighbor.cost) #cost
            pathList = []
            pathList.append(self.id)
            pathList.append(neighbor.id)
            list.append(len(pathList))  # number of jumps to destiny -> path list size == number of jumps
            list.append(pathList) #path list
            self.routingTable[neighbor.id] = list #destiny node e a key do dicionario
        print self.routingTable


class Neighbor:
    id = -1
    cost = -1

    def __init__(self, id, cost):
        self.id = id
        self.cost = cost

        
class threadNo(threading.Thread):
    node = None
    
    def __init__(self, element):
        threading.Thread.__init__(self)
        self.node = element
        
    def run(self):
        self.node.creatingPathTable()



if __name__ == '__main__':

    topology = [] #array de nodes
    listThreads = []
    
    #usuario digita a topologia
    #while True:
    userInput = []
    string1 = "1; 2[4]; 3[1];"
    string2 = "2; 1[4]; 3[2];"
    string3 = "3; 1[1]; 2[3];"
    string4 = "-1"
    userInput.append(string1)
    userInput.append(string2)
    userInput.append(string3)
    userInput.append(string4)
    for string in userInput:
        #userInput = raw_input("Entre com o no ou digite -1 para encerrar:")

        # se -1, encerre input
        # senao pergunte sobre os vizinhos
        #if userInput == "-1":
        if string == "-1":
            #break
            var = 1+1
        else:
            #input = userInput.split(";")
            input = string.split(";")
            #new node
            node = Node(input[0])
            #remote FIRST and LAST element of list
            input.pop(0)
            input.pop()
            for neighbor in input:
                #print(neighbor)
                list = neighbor.split("[") #list[0] is ID and list[1] is COST
                #remove whitespace from id
                id = "".join(list[0].split())
                #remove ] from cost
                cost = list[1][:-1]

                newNeighbor = Neighbor(id, cost)
                node.neighbors.append(newNeighbor)
            topology.append(node)
                
    for element in topology:
        thrNo = threadNo(element)
        
        thrNo.start()
        
        listThreads.append(thrNo)
        
    for j in listThreads:
        j.join()
        
