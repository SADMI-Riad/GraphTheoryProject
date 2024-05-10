import networkx as nx
import heapq

def dijkstra(graph, source, visualize_step=None):
    distances = {vertex: float('infinity') for vertex in graph.nodes}
    previous_nodes = {vertex: None for vertex in graph.nodes}
    distances[source] = 0
    pq = [(0, source)]

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)
        if visualize_step:
            visualize_step(graph, current_vertex, distances, previous_nodes)
        if distances[current_vertex] < current_distance:
            continue
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_vertex
                heapq.heappush(pq, (distance, neighbor))
    return distances, previous_nodes