import networkx as nx
import operator
import random
import math as math
G = nx.read_gexf("Pretty Good Privacy.gexf")
'''G = nx.read_gml('dolphin.gml')'''
'''G = nx.read_gexf("sp_data_school_day_1_g.gexf")'''
'''G = nx.karate_club_graph()'''
nodes = G.nodes()



listnodes = {}
neighbors = {}
payofflist = {}


for n in nodes:
    listnodes[n] ="D"
    neighbors[n] = G.neighbors(n)
    payofflist[n] = 0

nodes2 = nx.degree(G)
sortednodes2 = sorted(nodes2.items(), key=operator.itemgetter(1))
sortednodes2 = sortednodes2[::-1]
topnodes = []

for a in range(len(nodes)):
    topnodes += [sortednodes2[a][0]]
print(topnodes)
seed = []

for node in topnodes:
    ratelist = []
    if listnodes[node] == "D":
        seed += [node]
        listnodes[node] = "C"

        while True:
            CO = []
            DE = []
            for n1 in nodes:
                neighborofn = neighbors[n1]
                payoff = 0
                for n2 in neighborofn:
                    if listnodes[n1] == 'C':
                        if listnodes[n2] =='C':
                            payoff += 1
                        else:
                            payoff += 0
                    else:
                        if listnodes[n2] == 'C':
                            payoff += 1.2
                        else:
                            payoff += 0
                payofflist[n1] = payoff

            for n3 in nodes:
                if n3 not in seed:
                    neighbors2 = neighbors[n3]
                    x= len(neighbors2)
                    v = neighbors2[random.randrange(0,x)]

                    if payofflist[n3] < payofflist[v]:

                        rate = random.random()
                        value = (payofflist[v] - payofflist[n3]) / (1.2 * max(x,len(neighbors[v])))

                        if value > rate:
                            if listnodes[v] == 'C':
                                CO += [n3]

                            else:
                                DE += [n3]

            for co in CO:
                listnodes[co] = "C"
            for de in DE:
                listnodes[de] = "D"
            number = 0
            for n5 in nodes:

                if listnodes[n5] == 'C':
                    number += 1
            ratelist += [number/len(nodes)]

            if len(ratelist) >= 30:
                ave = 0
                for loopnumber in range(29):
                    xxx = ratelist[-loopnumber-1]-ratelist[-loopnumber-2]

                    ave += xxx
                a = random.random()
                if a <= (1-(1 / (1 + math.e**(-(500*ave/29))))):

                    print(ave*1000)
                    print(1-(1 / (1 + math.e**(-(500*ave/29)))))

                    break

    number1 = 0
    for n in nodes:

         if listnodes[n] == 'C':
            number1 += 1

    if number1/len(nodes) >= 0.95:
        break

    print(seed)







