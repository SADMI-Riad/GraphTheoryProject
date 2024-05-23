import networkx as nx

def bellman_ford(graph, source, callback=None):
    # Initialisation
    distances = {node: float('infinity') for node in graph.nodes()}
    predecessors = {node: None for node in graph.nodes()}
    distances[source] = 0

    # Relaxation des arêtes
    for _ in range(len(graph.nodes()) - 1):
        for u, v, data in graph.edges(data=True):
            if distances[u] + data['weight'] < distances[v]:
                distances[v] = distances[u] + data['weight']
                predecessors[v] = u
                if callback:
                    callback(graph, u, v, distances, predecessors)

    # Vérification des cycles de poids négatif
    for u, v, data in graph.edges(data=True):
        if distances[u] + data['weight'] < distances[v]:
            raise ValueError("Graph contains a negative weight cycle")
    return distances, predecessors
