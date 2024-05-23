from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QComboBox,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import matplotlib.pyplot as plt
import heapq


class DijkstraWindow(QMainWindow):
    def __init__(self, G, pos):
        super().__init__()
        self.G = G
        self.pos = pos
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Animation Dijkstra")
        self.setGeometry(150, 150, 800, 600)

        widget = QWidget(self)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim([0, 1])
        self.ax.set_ylim([0, 1])
        self.ax.axis("off")
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.source_label = QLabel("Select Source Node:", self)
        layout.addWidget(self.source_label)
        self.source_combo = QComboBox(self)
        self.source_combo.addItems([str(node) for node in self.G.nodes()])
        layout.addWidget(self.source_combo)

        self.target_label = QLabel("Select Target Node:", self)
        layout.addWidget(self.target_label)
        self.target_combo = QComboBox(self)
        self.target_combo.addItems([str(node) for node in self.G.nodes()])
        layout.addWidget(self.target_combo)

        self.run_button = QPushButton("Run Dijkstra", self)
        self.run_button.clicked.connect(self.run_dijkstra)
        layout.addWidget(self.run_button)

    def run_dijkstra(self):
        source_node = int(self.source_combo.currentText())
        target_node = int(self.target_combo.currentText())
        self.animation_steps = []
        self.distances, self.previous_nodes = self.dijkstra(
            self.G, source_node, self.visualize_step
        )
        self.shortest_path = self.extract_shortest_path(
            self.previous_nodes, source_node, target_node
        )
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph_dijkstra)
        self.timer.start(1000)

    def dijkstra(self, graph, source, visualize_step=None):
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

    def visualize_step(self, graph, current_vertex, distances, previous_nodes):
        self.animation_steps.append(
            (graph, current_vertex, distances.copy(), previous_nodes.copy())
        )

    def update_graph_dijkstra(self):
        if self.animation_steps:
            graph, current_vertex, distances, previous_nodes = self.animation_steps.pop(
                0
            )
            self.ax.clear()
            node_colors = [
                "green" if node == current_vertex else "lightblue"
                for node in graph.nodes()
            ]
            nx.draw(
                graph,
                self.pos,
                ax=self.ax,
                with_labels=True,
                node_color=node_colors,
                node_size=700,
                edge_color="gray",
            )

            # Dessiner les poids des arêtes
            for u, v, data in graph.edges(data=True):
                edge_weight = data["weight"]
                mid_x, mid_y = (self.pos[u][0] + self.pos[v][0]) / 2, (
                    self.pos[u][1] + self.pos[v][1]
                ) / 2
                self.ax.text(
                    mid_x,
                    mid_y,
                    str(edge_weight),
                    color="black",
                    fontsize=9,
                    ha="center",
                    va="center",
                    backgroundcolor="white",
                )

            for node, dist in distances.items():
                if dist < float("infinity"):
                    self.ax.text(
                        self.pos[node][0],
                        self.pos[node][1] + 0.05,
                        f"{dist:.1f}",
                        color="red",
                        fontsize=12,
                        ha="center",
                        va="center",
                    )

            self.canvas.draw()
        else:
            self.highlight_shortest_path()

    def highlight_shortest_path(self):
        self.ax.clear()
        # Dessinez tout le graphe en couleur de base
        nx.draw(
            self.G,
            pos=self.pos,
            ax=self.ax,
            with_labels=True,
            node_color="lightblue",
            node_size=700,
            edge_color="gray",
        )
        # Dessinez les arêtes du chemin le plus court en rouge
        path_edges = list(zip(self.shortest_path[:-1], self.shortest_path[1:]))
        nx.draw_networkx_edges(
            self.G,
            pos=self.pos,
            edgelist=path_edges,
            edge_color="red",
            width=2,
            ax=self.ax,
        )
        # Afficher les poids sur les arêtes du chemin le plus court
        for u, v in path_edges:
            weight = self.G[u][v]["weight"]
            mid_x, mid_y = (self.pos[u][0] + self.pos[v][0]) / 2, (
                self.pos[u][1] + self.pos[v][1]
            ) / 2
            self.ax.text(
                mid_x,
                mid_y,
                str(weight),
                color="red",
                fontsize=10,
                ha="center",
                va="center",
                bbox=dict(
                    facecolor="white", edgecolor="none", boxstyle="round,pad=0.3"
                ),
            )

        self.canvas.draw()
        self.timer.stop()

    def extract_shortest_path(self, previous_nodes, source, target):
        path = []
        current_node = target
        while current_node is not None:
            path.insert(0, current_node)
            current_node = previous_nodes[current_node]
        if path[0] == source:
            return path
        else:
            QMessageBox.warning(self, "Error", "No path found from source to target.")
            return []
