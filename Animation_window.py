from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QScrollArea,
    QLabel,
)
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import matplotlib.pyplot as plt
from algorithmes.coloration import welch_powell
from algorithmes.kruskal_min import kruskal_mst
from algorithmes.prim import prim_mst
from algorithmes.prim_max import prim_max_mst


class AnimationWindow(QMainWindow):
    def __init__(self, G, pos, algorithm="welsh_powell", start_node=None):
        super().__init__()
        self.G = G.to_undirected()
        self.pos = pos
        self.initUI()
        self.stable_sets = {}

        if algorithm == "welsh_powell":
            self.color_map = welch_powell(self.G)
            self.animation_steps = list(self.color_map.items())
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_graph_welsh_powell)
            self.timer.start(1000)
            self.button = QPushButton("Trouver ensemble stable maximal", self)
            self.button.clicked.connect(self.findStableSet)
            layout = QVBoxLayout()
            layout.addWidget(self.button)
            self.setLayout(layout)

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
        elif algorithm == "primMax":
            self.animation_steps = []
            prim_max_mst(self.G, start_node, self.visualize_step_prim)
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_graph_prim)
            self.timer.start(1000)
        elif algorithm == "kruskalMax":
            self.animation_steps = []
            kruskal_mst(self.G, self.visualize_step_kruskal)
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_graph_kruskal)
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
            node_colors = [self.color_map.get(n, "lightgray") for n in self.G.nodes()]
            nx.draw(
                self.G,
                pos=self.pos,
                ax=self.ax,
                with_labels=True,
                node_color=node_colors,
                node_size=700,
            )
            self.canvas.draw()
        else:
            self.timer.stop()

    def visualize_step_kruskal(self, mst):
        self.animation_steps.append(mst)

    def update_graph_kruskal(self):
        if self.animation_steps:
            mst = self.animation_steps.pop(0)
            self.ax.clear()
            nx.draw(
                self.G,
                pos=self.pos,
                ax=self.ax,
                with_labels=True,
                node_color="lightgray",
                node_size=700,
                edge_color="lightgray",
            )
            nx.draw(
                mst,
                pos=self.pos,
                ax=self.ax,
                with_labels=True,
                node_color="blue",
                node_size=700,
                edge_color="blue",
            )
            edge_labels = nx.get_edge_attributes(mst, "weight")
            nx.draw_networkx_edge_labels(
                mst, self.pos, edge_labels=edge_labels, ax=self.ax
            )
            self.canvas.draw()
        else:
            self.timer.stop()

    def visualize_step_prim(self, mst):
        self.animation_steps.append(mst)

    def update_graph_prim(self):
        if self.animation_steps:
            mst = self.animation_steps.pop(0)
            self.ax.clear()
            nx.draw(
                self.G,
                pos=self.pos,
                ax=self.ax,
                with_labels=True,
                node_color="lightgray",
                node_size=700,
                edge_color="lightgray",
            )
            nx.draw(
                mst,
                pos=self.pos,
                ax=self.ax,
                with_labels=True,
                node_color="green",
                node_size=700,
                edge_color="green",
            )
            edge_labels = nx.get_edge_attributes(mst, "weight")
            nx.draw_networkx_edge_labels(
                mst, self.pos, edge_labels=edge_labels, ax=self.ax
            )
            self.canvas.draw()
        else:
            self.timer.stop()

    def findStableSet(self):
        self.stable_sets = self.get_stable_sets_from_colors(self.color_map)
        self.show_stable_sets()

    def show_stable_sets(self):
        stable_window = QMainWindow(self)
        stable_window.setWindowTitle("Stable Sets")
        stable_window.setGeometry(150, 150, 800, 600)
        scroll = QScrollArea()
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        stable_window.setCentralWidget(scroll)

        for index, (color, nodes) in enumerate(self.stable_sets.items(), start=1):
            fig, ax = plt.subplots()
            subgraph = self.G.subgraph(nodes)
            nx.draw(
                subgraph,
                pos=self.pos,
                ax=ax,
                with_labels=True,
                node_color=[color] * len(nodes),
                node_size=700,
            )
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)
            stable_label = QLabel(f"Stable {index}")
            layout.addWidget(stable_label)

        stable_window.show()

    def get_stable_sets_from_colors(self, color_map):
        stable_sets = {}
        for node, color in color_map.items():
            if color not in stable_sets:
                stable_sets[color] = []
            stable_sets[color].append(node)
        return stable_sets
