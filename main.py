class Node:
    id = -1
    neighbors = []

    def __init__ (self, id):
        self.id = id


class Neighbor:
    id = -1
    cost = -1

    def __init__(self, id, cost):
        self.id = id
        self.cost = cost

if __name__ == '__main__':

    topology = [] #array de nodes

    #usuario digita a topologia
    while True:
        userInput = raw_input("Entre com o no ou digite -1 para encerrar:")
        # se -1, encerre input
        # senao pergunte sobre os vizinhos
        if userInput == "-1":
            break
        else:
            input = userInput.split(";")
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

    #começa a criar os nós
    #1) instanciar os nodes do array
    #2) criar tabela
