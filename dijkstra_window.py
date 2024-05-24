from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import matplotlib.pyplot as plt
import heapq

import numpy as np


class DijkstraWindow(QMainWindow):
    def __init__(self, G, pos):
        super().__init__()
        self.G = G
        self.pos = pos
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Animation Dijkstra")
        self.setGeometry(150, 150, 800, 600)
        self.source_node = None
        self.target_node = None
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

        self.reset_button = QPushButton("Recommencer", self)
        self.reset_button.clicked.connect(self.reset)
        layout.addWidget(self.reset_button)

        self.canvas.mpl_connect("button_press_event", self.on_click_djik)
        self.draw_graph()

    def run_dijkstra(self):
        if self.source_node is not None and self.target_node is not None:
            self.animation_steps = []
            self.distances, self.previous_nodes = self.dijkstra(
                self.G, self.source_node, self.visualize_step
            )
            self.shortest_path = self.extract_shortest_path(
                self.previous_nodes, self.source_node, self.target_node
            )
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_graph_dijkstra)
            self.timer.start(1000)
        else:
            QMessageBox.warning(
                self,
                "Attention",
                "Veuillez sélectionner à la fois les nœuds source et cible avant d'exécuter Dijkstra.",
            )

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
            QMessageBox.warning(self, "Erreur", "Aucun chemin trouvé de la source à la cible.")
            return []

    def on_click_djik(self, event):
        x_click, y_click = event.xdata, event.ydata
        # Find closest node
        closest_node = min(
            self.G.nodes,
            key=lambda node: np.hypot(
                self.pos[node][0] - x_click, self.pos[node][1] - y_click
            ),
        )
        if not self.source_node:
            self.source_node = closest_node
            self.highlight_node(self.source_node, "green")
        elif not self.target_node and self.source_node != closest_node:
            self.target_node = closest_node
            self.highlight_node(self.target_node, "red")
            self.run_dijkstra()

    def highlight_node(self, node, color):
        nx.draw_networkx_nodes(
            self.G,
            self.pos,
            nodelist=[node],
            node_color=color,
            ax=self.ax,
            node_size=500,
        )
        self.canvas.draw()

    def reset(self):
        self.source_node = None
        self.target_node = None
        self.ax.clear()
        self.draw_graph()
        self.canvas.draw()

    def draw_graph(self):
        self.ax.clear()
        nx.draw(
            self.G,
            self.pos,
            ax=self.ax,
            with_labels=True,
            node_color="lightblue",
            edge_color="gray",
        )
        self.canvas.draw()
