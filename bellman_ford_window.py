import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from algorithmes.bellman_ford import bellman_ford

class BellmanFordWindow(QMainWindow):
    def __init__(self, G, pos):
        super().__init__()
        self.G = G
        self.pos = pos
        self.initUI()
        self.animation_steps = []

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
        self.draw_graph()

    def start_bellman_ford(self):
        if self.source_node:
            try:
                distances, predecessors, levels = bellman_ford(self.G, self.source_node)
                self.path = self.extract_path(predecessors, self.source_node)
                self.timer.start(1000)
                # Utiliser les niveaux pour mettre à jour les positions
                self.update_positions(levels)
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))
                self.timer.stop()

    def update_positions(self, levels):
        max_level = max(levels.values()) + 1
        level_width = max_level * 2  # Espace horizontal entre les niveaux
        new_pos = {node: (levels[node] * level_width, -levels[node]) for node in self.G.nodes()}
        nx.draw(self.G, pos=new_pos, ax=self.ax, with_labels=True, node_color='lightblue', edge_color='gray')
        self.canvas.draw()

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

    def highlight_node(self, node, color):
        nx.draw_networkx_nodes(self.G, self.pos, nodelist=[node], node_color=color, ax=self.ax, node_size=500)
        self.canvas.draw()

    def draw_graph(self):
        self.ax.clear()
        nx.draw(self.G, self.pos, ax=self.ax, with_labels=True, node_color='lightblue', edge_color='gray')
        self.canvas.draw()
