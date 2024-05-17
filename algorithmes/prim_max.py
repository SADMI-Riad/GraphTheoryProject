import networkx as nx
import heapq

def prim_max_mst(graph, start_node, callback=None):
    undirected_graph = graph.to_undirected()
    # Initialiser un graph vide pour l'arbre couvrant maximum
    mst = nx.Graph()
    # Ensemble pour suivre les sommets ajoutés à l'arbre couvrant maximum
    visited = set([start_node])
    # File de priorité pour les arêtes, mais cette fois-ci avec des poids négatifs
    edges = [(-data['weight'], start_node, to) for to, data in undirected_graph[start_node].items()]
    heapq.heapify(edges)

    while edges:
        # Prendre l'arête avec le "poids le plus faible" (qui est en réalité le poids le plus élevé en négatif)
        weight, frm, to = heapq.heappop(edges)
        weight = -weight  # Convertir le poids en positif pour le stocker dans le MST
        if to not in visited:
            visited.add(to)
            mst.add_edge(frm, to, weight=weight)
            for next_to, data in undirected_graph[to].items():
                if next_to not in visited:
                    heapq.heappush(edges, (-data['weight'], to, next_to))
            if callback:
                callback(mst.copy())
    return mst
