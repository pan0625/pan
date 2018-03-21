import re
import networkx as nx

G = nx.Graph()
filepath = r"C:\Users\PAN\Desktop\STUDY\UOA\GD\COMPSCI 380\Hamsterster friendships.gexf"

def getNetworkxFromGexf(filepath):
    G = nx.Graph()
    with open(filepath) as f:
        test = f.read()
        nodes = re.findall(r'node id=\"\d*\"', test)
        edges = re.findall(r'edge id=\"\d*\" source=\"\d*\" target=\"\d*\"', test)
        for node in nodes:
            G.add_node((int)(node[9:-1]))
        for edge in edges:
            nums = re.findall(r'\d\d*', (str)(edge))
            G.add_edge((int)(nums[1]), (int)(nums[2]))  
    return G

G = getNetworkxFromGexf(filepath)
print(G.number_of_nodes())
