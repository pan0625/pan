#coding=utf-8
import random
import matplotlib.pyplot as plt
import math
import networkx as nx
from scipy import stats
def powerlawrnd2(gama,xmin):
    alpha=gama-1
    a=random.uniform(0,1)
    x=round(pow(1-a,-1.0/alpha)*(xmin-0.5)+0.5)
    return x
def powerLawDistribution(n,gama,xmin):
    result=[]
    for i in range(n):
        temp=powerlawrnd2(gama,xmin)
        result.append(temp)
    return result
def prob_select(target_list, probability, num):
    selected = []
    i = 0
    while i < num:
        x = random.uniform(0,1)
        cumulative_probability = 0.0
        for item, item_probability in zip(target_list,probability):
            cumulative_probability += item_probability
            if x < cumulative_probability:
                selected.append(item)
                break
        i += 1

    selected_list = list(set(selected))  # remove repeated items
    return selected_list
def generate_onion(Num,gama = 2.5):
	"""
	:param Num: number of nodes
    :param gama:  k^(-gama)
	"""
    data = powerLawDistribution(Num,gama,xmin=2)
    for i in range(Num): data[i] = int(round(data[i]))
    hist = {}
    for i in data:
        i = int(i)
        if not i in hist.keys():
            hist[i] = 0
        hist[i] += 1
    sortedhist = sorted(hist.keys())
    # print sortedhist
    result = []
    for i in data:
        result.append(sortedhist.index(i))

	G = nx.Graph()
    nodes = range(0, Num)
    nodesRemain = []
    for i in nodes:
        nodesRemain.extend([i] * data[i])
    edges = []
    alpha = 3
    tries = 10
    while len(nodesRemain) > 0:
        if (len(edges) == 0 or tries >= 0) and len(set(nodesRemain)) > 1:

            a, b = random.sample(set(nodesRemain), 2)
            if a == b or (a, b) in edges or (b, a) in edges:
                tries -= 1
                continue
            tries = 10
            if random.uniform(0, 1) < (1.0 / (1 + alpha * abs(result[a] - result[b]))):
                edges.append((a, b))
                nodesRemain.remove(a)
                nodesRemain.remove(b)

        else:
            tries = 10
            edge1 = random.choice(edges)
            if (len(nodesRemain) == 1):
                break
            stub1, stub2 = random.sample(nodesRemain, 2)
            if (edge1[0] == stub1 or edge1[1] == stub1) and (edge1[0] == stub2 or edge1[1] == stub2):
                continue
            if (not edge1[0] == stub1) and (not edge1[1] == stub2):
                a1 = (edge1[0], stub1)
                a2 = (stub1, edge1[0])
                b1 = (edge1[1], stub2)
                b2 = (stub2, edge1[1])
            elif (not edge1[0] == stub2) and (not edge1[1] == stub1):
                a1 = (edge1[0], stub2)
                a2 = (stub2, edge1[0])
                b1 = (edge1[1], stub1)
                b2 = (stub1, edge1[1])
            else:
                print "error"
                continue
            if not ((a1 in edges) or (a2 in edges) or (b1 in edges) or (b2 in edges)):
                edges.remove(edge1)
                edges.append(a1)
                edges.append(b1)
                nodesRemain.remove(stub1)
                nodesRemain.remove(stub2)
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G
def rich_club(network,gama,n):
    """
    根据 幂律分布的指数，决定添加一个点的概率为alpha，否则添加一条边

    添边时，随机选出一个源节点，然后以概率选择一目标度数 概率为 度数*该度数的节点数/sum(度数*节点数)
    之后从目标度数下随机选择一点为目标点
    :param network: init network
    :param gama:  k^(-gama)
    :param n:  number of total nodes
    :return:

    onionveils 层数关系 论文中的[k]
    """
    alpha=1-1.0/(gama-1)
    
	times=len(network.nodes())
    while times<n:

        if random.uniform(0,1)<alpha:
            """add a new node"""
            target=random.choice(network.nodes())
            network.add_node(times)
            network.add_edge(times,target)
            
        else:
            hist = nx.degree_histogram(network)
            lhist=len(hist)
            denominator=0
            for i in range(lhist):
                denominator+=i*hist[i]
            prob=[]
            for j in range(lhist):
                prob.append(float(j*hist[j])/denominator)
            bool=True
            for tries in range(4):
                source=random.choice(network.nodes())

                targetveil=prob_select(range(lhist),prob,1)
                target=random.choice(targetveil)
                if source==target or (source,target) in network.edges() or (target,source) in network.edges():
                    continue
                network.add_edge(source,target)
                # print "add 1 edge"
                bool=False
            if bool==True:
                times-=1
                print "exceed max times"
        times=len(network.nodes())
    return network
