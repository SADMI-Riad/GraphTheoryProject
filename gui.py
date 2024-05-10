from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox, QInputDialog
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from graph_operations import redrawGraph, addNode, draw_edge
from algorithms.coloration import welch_powell
from algorithms.prim import prim_mst

class GraphDesigner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mode = "creating_nodes"
        self.selected_node_for_edge_creation = None
        self.G = nx.DiGraph()
        self.pos = {}
        self.stable_set = []
        self.animation_steps = []

    def initUI(self):
        self.setWindowTitle("Graph Designer")
        self.setGeometry(100, 100, 800, 600)
        widget = QWidget()
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
        self.endNodesCreationButton = QPushButton("Fin création sommets")
        self.endNodesCreationButton.clicked.connect(self.endNodesCreation)
        layout.addWidget(self.endNodesCreationButton)
        self.findStableSetButton = QPushButton("Trouver ensemble stable maximal")
        self.findStableSetButton.clicked.connect(self.findStableSet)
        layout.addWidget(self.findStableSetButton)
        self.primButton = QPushButton("Exécuter Prim")
        self.primButton.clicked.connect(self.run_prim)
        layout.addWidget(self.primButton)
        self.canvas.mpl_connect("button_press_event", self.on_click)

    def endNodesCreation(self):
        self.mode = "creating_edges"
        self.endNodesCreationButton.setDisabled(True)

    def findStableSet(self):
        self.stable_set = welch_powell(self.G)
        redrawGraph(self.ax, self.G, self.pos, self.stable_set, self.canvas)

    def run_prim(self):
        if not self.G.nodes:
            QMessageBox.warning(self, "Erreur", "Aucun nœud présent dans le graphe.")
            return
        start_node = list(self.G.nodes())[0]
        prim_mst(self.G, start_node, self.visualize_step)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)

    def visualize_step(self, mst):
        self.animation_steps.append(mst)

    def update_graph(self):
        if self.animation_steps:
            mst = self.animation_steps.pop(0)
            redrawGraph(self.ax, mst, self.pos, [], self.canvas)
        else:
            self.timer.stop()

    def on_click(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            if self.mode == "creating_nodes":
                addNode(self.G, self.pos, x, y, self.ax, self.canvas)
            elif self.mode == "creating_edges":
                self.handle_edge_creation(x, y)

    def handle_edge_creation(self, x, y):
        node_id = self.get_closest_node(x, y)
        if self.selected_node_for_edge_creation is None:
            self.selected_node_for_edge_creation = node_id
        else:
            weight, ok = QInputDialog.getInt(
                self, "Poids de l'arc", "Entrez le poids de l'arc:", min=1
            )
            if ok:
                self.G.add_edge(
                    self.selected_node_for_edge_creation, node_id, weight=weight
                )
                draw_edge(self.ax, self.pos, self.selected_node_for_edge_creation, node_id, weight, self.canvas)
                self.canvas.draw()
                self.selected_node_for_edge_creation = None

    def get_closest_node(self, x, y):
        return min(
            self.G.nodes, key=lambda n: np.hypot(self.pos[n][0] - x, self.pos[n][1] - y)
        )
