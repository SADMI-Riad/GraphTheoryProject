def bellman_ford(graph, source):
    # Initialisation
    distances = {node: float('infinity') for node in graph.nodes()}
    predecessors = {node: None for node in graph.nodes()}
    levels = {node: -1 for node in graph.nodes()}  # Niveau initial non défini
    distances[source] = 0
    levels[source] = 0  # Le niveau du nœud source est 0

    # Relaxation des arêtes
    for _ in range(len(graph.nodes()) - 1):
        for u, v, data in graph.edges(data=True):
            if distances[u] + data['weight'] < distances[v]:
                distances[v] = distances[u] + data['weight']
                predecessors[v] = u
                levels[v] = levels[u] + 1  # Définir le niveau de 'v' un niveau plus que 'u'

    # Vérification des cycles de poids négatif
    for u, v, data in graph.edges(data=True):
        if distances[u] + data['weight'] < distances[v]:
            raise ValueError("Graph contains a negative weight cycle")

    return distances, predecessors, levels
