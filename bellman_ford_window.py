import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox, QApplication
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from algorithmes.bellman_ford import bellman_ford

def calculate_levels(graph):
    levels = {node: 0 for node in graph.nodes()}
    for node in graph.nodes():
        levels[node] = len(list(graph.predecessors(node)))
    return levels

def update_positions(levels):
    max_level = max(levels.values())
    level_nodes = {i: [] for i in range(max_level + 1)}

    for node, level in levels.items():
        level_nodes[level].append(node)

    new_pos = {}
    for level, nodes in level_nodes.items():
        num_nodes = len(nodes)
        spacing = 1.0 / (num_nodes + 1)
        for i, node in enumerate(nodes):
            new_pos[node] = ((i + 1) * spacing, -level)
    return new_pos

class BellmanFordWindow(QMainWindow):
    def __init__(self, G):
        super().__init__()
        self.G = G
        self.source_node = None
        self.target_node = None
        self.animation_steps = []
        self.path = None

        # Calculate initial positions based on levels
        self.initial_levels = calculate_levels(self.G)
        self.pos = update_positions(self.initial_levels)
        self.initUI()
        self.draw_graph()

    def initUI(self):
        self.setWindowTitle("Bellman-Ford Animation")
        self.setGeometry(150, 150, 800, 600)
        widget = QWidget(self)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.axis("off")
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.start_button = QPushButton("Start Bellman-Ford", self)
        self.start_button.clicked.connect(self.start_bellman_ford)
        layout.addWidget(self.start_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_visual)

        self.canvas.mpl_connect("button_press_event", self.on_click_bellman_ford)

    def start_bellman_ford(self):
        if self.source_node and self.target_node:
            try:
                distances, predecessors = bellman_ford(self.G, self.source_node, self.visualize_step)
                self.path = self.extract_path(predecessors, self.source_node, self.target_node)
                self.timer.start(1000)
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))
                self.timer.stop()

    def on_click_bellman_ford(self, event):
        x_click, y_click = event.xdata, event.ydata
        closest_node = min(self.G.nodes, key=lambda node: np.hypot(self.pos[node][0] - x_click, self.pos[node][1] - y_click))
        if not self.source_node:
            self.source_node = closest_node
            self.highlight_node(self.source_node, "green")
            self.start_button.setEnabled(True)
        elif not self.target_node and self.source_node != closest_node:
            self.target_node = closest_node
            self.highlight_node(self.target_node, "red")
            self.run_bellman_ford()

    def highlight_node(self, node, color):
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=[node], node_color=color, ax=self.ax, node_size=500)
        self.canvas.draw()

    def draw_graph(self):
        self.ax.clear()
        nx.draw(self.G, self.pos, ax=self.ax, with_labels=True, node_color='lightblue', edge_color='gray')
        self.draw_edge_weights()
        self.canvas.draw()

    def draw_edge_weights(self):
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels, ax=self.ax, font_color='blue')

    def run_bellman_ford(self):
        if self.source_node is not None and self.target_node is not None:
            self.animation_steps = []
            distances, predecessors = bellman_ford(self.G, self.source_node, self.visualize_step)
            self.shortest_path = self.extract_path(predecessors, self.source_node, self.target_node)
            self.timer.start(1000)
        else:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner à la fois les nœuds source et cible avant d'exécuter Bellman-Ford.")

    def extract_path(self, predecessors, source, target):
        path = []
        current_node = target
        while current_node is not None:
            path.insert(0, current_node)
            current_node = predecessors[current_node]
        if path[0] == source:
            return path
        else:
            QMessageBox.warning(self, "Erreur", "Aucun chemin trouvé de la source à la cible.")
            return []

    def update_visual(self):
        if self.animation_steps:
            u, v, distances, predecessors = self.animation_steps.pop(0)
            self.ax.clear()

            # Draw nodes and edges
            nx.draw(self.G, pos=self.pos, ax=self.ax, with_labels=True, node_color='lightblue')
            nx.draw_networkx_edges(self.G, pos=self.pos, ax=self.ax, edgelist=[(u, v)], edge_color='orange', width=2)

            # Show distances on nodes with a box above each node
            for node, (x, y) in self.pos.items():
                dist = f"{distances[node]:.1f}" if distances[node] != float('inf') else "inf"
                self.ax.text(x, y + 0.1, dist, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'), fontsize=8, ha='center')

            self.draw_edge_weights()
            self.canvas.draw()
        else:
            self.timer.stop()
            if self.path:
                # Visualization of the shortest path
                path_edges = list(zip(self.path[:-1], self.path[1:]))
                nx.draw_networkx_edges(self.G, pos=self.pos, edgelist=path_edges, edge_color='red', width=2, ax=self.ax)
                self.draw_edge_weights()  # Re-draw edge weights to ensure they are not obstructed
                self.canvas.draw()

    def visualize_step(self, graph, u, v, distances, predecessors):
        self.animation_steps.append((u, v, dict(distances), dict(predecessors)))

    def reset(self):
        self.source_node = None
        self.target_node = None
        self.ax.clear()
        self.pos = update_positions(self.initial_levels)  # Restore initial positions
        self.draw_graph()
        self.canvas.draw()
