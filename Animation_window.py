from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import matplotlib.pyplot as plt
from algorithmes.coloration import welch_powell
from algorithmes.kruskal_min import kruskal_mst
from algorithmes.prim import prim_mst

class AnimationWindow(QMainWindow):
    def __init__(self, G, pos, algorithm="welsh_powell", start_node=None):
        super().__init__()
        self.G = G.to_undirected()
        self.pos = pos
        self.initUI()

        if algorithm == "welsh_powell":
            self.color_map = welch_powell(self.G)
            self.animation_steps = list(self.color_map.items())
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_graph_welsh_powell)
            self.timer.start(1000)
        elif algorithm == "kruskal":
            self.animation_steps = []
            kruskal_mst(self.G, self.visualize_step_kruskal)
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_graph_kruskal)
            self.timer.start(1000)
        elif algorithm == "prim":
            self.animation_steps = []
            prim_mst(self.G, start_node, self.visualize_step_prim)
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_graph_prim)
            self.timer.start(1000)

    def initUI(self):
        self.setWindowTitle("Animation")
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

    def update_graph_welsh_powell(self):
        if self.animation_steps:
            node, color = self.animation_steps.pop(0)
            self.ax.clear()
            node_colors = [self.color_map.get(n, 'lightgray') for n in self.G.nodes()]
            nx.draw(self.G, pos=self.pos, ax=self.ax, with_labels=True, node_color=node_colors, node_size=700)
            self.canvas.draw()
        else:
            self.timer.stop()

    def visualize_step_kruskal(self, mst):
        self.animation_steps.append(mst)

    def update_graph_kruskal(self):
        if self.animation_steps:
            mst = self.animation_steps.pop(0)
            self.ax.clear()
            nx.draw(self.G, pos=self.pos, ax=self.ax, with_labels=True, node_color='lightgray', node_size=700, edge_color='lightgray')
            nx.draw(mst, pos=self.pos, ax=self.ax, with_labels=True, node_color='blue', node_size=700, edge_color='blue')
            self.canvas.draw()
        else:
            self.timer.stop()

    def visualize_step_prim(self, mst):
        self.animation_steps.append(mst)

    def update_graph_prim(self):
        if self.animation_steps:
            mst = self.animation_steps.pop(0)
            self.ax.clear()
            nx.draw(self.G, pos=self.pos, ax=self.ax, with_labels=True, node_color='lightgray', node_size=700, edge_color='lightgray')
            nx.draw(mst, pos=self.pos, ax=self.ax, with_labels=True, node_color='green', node_size=700, edge_color='green')
            self.canvas.draw()
        else:
            self.timer.stop()
