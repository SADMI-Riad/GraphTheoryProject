import networkx as nx

class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, set1, set2):
        root1 = self.find(set1)
        root2 = self.find(set2)
        if root1 != root2:
            self.parent[root1] = root2

def kruskal_mst(graph, callback=None):
    undirected_graph = graph.to_undirected()
    uf = UnionFind()
    mst = nx.Graph()

    for node in undirected_graph.nodes():
        uf.parent[node] = node

    edges = list(undirected_graph.edges(data=True))
    edges.sort(key=lambda x: x[2]['weight'])

    for edge in edges:
        u, v, weight = edge
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst.add_edge(u, v, weight=weight['weight'])
            if callback:
                callback(mst.copy())
            if mst.number_of_edges() == undirected_graph.number_of_nodes() - 1:
                break

    return mst
