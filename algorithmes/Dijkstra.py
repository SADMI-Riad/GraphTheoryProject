import networkx as nx
import heapq

def dijkstra(graph, source, visualize_step=None):
    # Initialize distances with infinity and set the distance from the source to itself as 0
    distances = {vertex: float('infinity') for vertex in graph.nodes()}
    previous_nodes = {vertex: None for vertex in graph.nodes()}
    distances[source] = 0
    
    # Priority queue (min-heap) to hold the vertices to be processed
    pq = [(0, source)]  # Stores tuples of (distance, vertex)

    while pq:
        # Extract the vertex with the smallest distance from the priority queue
        current_distance, current_vertex = heapq.heappop(pq)
        
        # Optional visualization callback
        if visualize_step:
            visualize_step(graph, current_vertex, distances, previous_nodes)
        
        # Important: Skip processing if we find a larger distance in the priority queue
        if distances[current_vertex] < current_distance:
            continue

        # Check all neighbors of the current vertex
        for neighbor, data in graph[current_vertex].items():
            # Calculate the distance to each neighbor
            distance = current_distance + data['weight']  # Ensure the weight key is correctly used
            
            # Only consider this new path if it's better
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_vertex
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous_nodes
