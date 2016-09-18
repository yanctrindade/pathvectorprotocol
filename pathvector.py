import time
import sys

##Variavel que controla se houve algum tipo de atualizacao entre
# as tabelas de roteamento dos nos
isChanged = True

##Classe que representa os nos assim como suas respectivas funcoes
class Node:
    id = -1
    neighbors = []
    routingTable = {}
    
    ##Construtor da classe
    def __init__ (self, id):
        self.id = id
        self.neighbors = []
        self.routingTable = {}
    
    ##Funcao que cria a primeira tabela de encaminhamento com base
    # nos vizinhos e seus respectivos custos em relacao ao no
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
    
    ##Funcao responsavel por atualizar a tabela de roteamento
    def updatingPathTable(self, routingTable, id):
        for key in routingTable:
            ## Caso ja exista o no na tabela compara os custos, senao adiciona um novo registro na tabela
            if self.routingTable.has_key(key):
                ## Registros de custo zero nao sao avaliados
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
                       isChanged = True
                    ## Caso os custos sejam iguais eh avaliado o numero de saltos realizados
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
                           isChanged = True
                   
            else:
                list = []
                list.append(routingTable.get(key)[0])
                pathList = [self.id] + routingTable.get(key)[2]
                list.append(len(pathList))
                list.append(pathList)
                self.routingTable[key] = list
                isChanged = True
    
    ##Funcao que mostra a tabela de um no. 
    # Executada para um no escolhido pelo usuario ao final do programa
    def showPathTable(self):
        print "\nNo destino -------- Custo -------- Saltos --------- Nos percorridos"
        for key in self.routingTable:
            print str(key)+"------------------ "+str(self.routingTable.get(key)[0])+"------------- "+str(self.routingTable.get(key)[1])+"--------------- "+str(self.routingTable.get(key)[2])

## Classe que mapeia os vizinhos de um no    
class Neighbor:
    id = -1
    cost = -1

    def __init__(self, id, cost):
        self.id = id
        self.cost = cost

## Funcao principal do programa
if __name__ == '__main__':
    initialTime = time.time()
    topology = [] #array de nodes
    listThreads = []
    
    print("Montando a topologia da rede...")
    
    sys.argv.pop(0)
    
    #Monta a topologia dos nos de acordo com o q foi passado nos argumentos
    for nodeLine in sys.argv:
        input = nodeLine.split(";")
        #new node
        node = Node(input[0])
        #remote FIRST and LAST element of list
        input.pop(0)
        input.pop()
        for neighbor in input:
            list = neighbor.split("[") #list[0] is ID and list[1] is COST
            #remove whitespace from id
            id = "".join(list[0].split())
            #remove ] from cost
            cost = list[1][:-1]
            
            newNeighbor = Neighbor(id, cost)
            node.neighbors.append(newNeighbor)
        topology.append(node)    
    
    print("Topologia montada...")    
    #Monta a Path Table para cada no       
    for node in topology:
        node.creatingPathTable()
    
    # Cada no manda sua Path Vector para cada um dos seus vizinhos.
    # Cada vizinho verifica se existe alguma rota melhor baseado no custo e na quantidade de saltos
    # Caso todas as trocas de tabelas ocorram e nenhuma atualizacao aconteca,
    #     o algoritmo entende que houve convergencia     
    while isChanged:
        isChanged = False
        for node in topology:
            for neighbor in node.neighbors:
                topology[int(neighbor.id)-1].updatingPathTable(node.routingTable, node.id)
                
    finalTime = time.time()
    
    # Registro do tempo de execucao
    print ("\nO protocolo convergiu em %f ms\n" %(finalTime - initialTime))
    
    #O usuario escolhe um no para mostrar a Path Table final
    showNode = raw_input("Escolha um no entre 1 e %d para mostrar a path table: " %len(topology))
    
    #Caso seja informado um numero de no invalido, nenhuma informacao e mostrada e o programa e finalizado
    if (int(showNode) > int(len(topology)) or int(showNode) < 1):
        print "\nNao foi possivel mostrar a Path Table pois o no informado e invalido!"
    else:
        topology[int(showNode)-1].showPathTable()