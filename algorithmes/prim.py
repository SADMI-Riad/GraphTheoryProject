import networkx as nx
import heapq

def prim_mst(graph, start_node, callback=None):
    undirected_graph = graph.to_undirected()
    #graph faregh to store l'arbre t3na kima rhi mkhdoma
    mst = nx.Graph()
    #set to track which sommets zednahom lel mst , tbda with the start_node
    visited = set([start_node])
    #priority queue where potential arcs ynzado to the mst
    #its organized b tari9a win les arcs li 3ndhom lowest poids are always at the top
    edges = [(data['weight'], start_node, to) for to, data in undirected_graph[start_node].items()]
    heapq.heapify(edges)


    #while loop continue TantQue kayen the arc fel heap
    while edges:
        #removes and returns l'arc sghir ge3 (par poids) de l'arbre ,cet arc raho considered for addition to the mst
        weight, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst.add_edge(frm, to, weight=weight)
            for next_to, data in undirected_graph[to].items():
                if next_to not in visited:
                    heapq.heappush(edges, (data['weight'], to, next_to))
            if callback:
                callback(mst.copy())
    return mst
