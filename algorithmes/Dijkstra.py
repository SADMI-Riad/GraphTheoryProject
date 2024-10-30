import networkx as nx
import heapq


def dijkstra(graph, source, visualize_step=None):
    # Vérifier la présence de poids négatifs dans le graphe
    for u, v, data in graph.edges(data=True):
        if data["weight"] < 0:
            raise ValueError("Le graphe contient des poids négatifs. L'algorithme de Dijkstra ne peut pas être appliqué.")

    distances = {vertex: float("infinity") for vertex in graph.nodes()}
    previous_nodes = {vertex: None for vertex in graph.nodes()}
    distances[source] = 0

    pq = [(0, source)]

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if visualize_step:
            visualize_step(graph, current_vertex, distances, previous_nodes)
        if distances[current_vertex] < current_distance:
            continue

        for neighbor, data in graph[current_vertex].items():
            distance = current_distance + data["weight"]
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_vertex
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous_nodes
