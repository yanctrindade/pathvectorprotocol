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
        #print self.routingTable
    
    def updatingPathTable(self, routingTable, id):
        for key in routingTable:
            if self.routingTable.has_key(key):
               if int(routingTable.get(key)[0]) != 0:
                   cost = int(self.routingTable.get(key)[0])
                   newCost = int(routingTable.get(key)[0]) + int(self.routingTable.get(id)[0])
                   if cost > newCost:
                       list = []
                       list.append(newCost)
                       pathList = [self.id] +routingTable.get(key)[2]
                       list.append(len(pathList))
                       list.append(pathList)
                       self.routingTable[key] = list
                   if cost == newCost:
                       hop = int(self.routingTable.get(key)[1])
                       newHop = int(routingTable.get(key)[1])+1
                       if hop > newHop:
                           list = []
                           list.append(newCost)
                           pathList = [self.id] + routingTable.get(key)[2]
                           list.append(len(pathList))
                           list.append(pathList)
                           self.routingTable[key] = list
                   
            else:
                list = []
                list.append(routingTable.get(key)[0])
                pathList = [self.id] + routingTable.get(key)[2]
                list.append(len(pathList))
                list.append(pathList)
                self.routingTable[key] = list

class Neighbor:
    id = -1
    cost = -1

    def __init__(self, id, cost):
        self.id = id
        self.cost = cost

if __name__ == '__main__':

    topology = [] #array de nodes
    listThreads = []
    
    #usuario digita a topologia
    #while True:
    userInput = []
    string1 = "1; 2[4]; 3[1];"
    string2 = "2; 1[4]; 3[2];"
    string3 = "3; 1[1]; 2[2];"
    string4 = "-1"
    userInput.append(string1)
    userInput.append(string2)
    userInput.append(string3)
    userInput.append(string4)
    
    #Monta o vetor de topologia dos nos
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
    
    #Monta a tabela de caminho para cada no       
    for node in topology:
        node.creatingPathTable()
        
    for node in topology:
        for neighbor in node.neighbors:
            topology[int(neighbor.id)-1].updatingPathTable(node.routingTable, node.id)