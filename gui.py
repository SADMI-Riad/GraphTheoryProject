from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox, QInputDialog, QLabel, QGridLayout, QScrollArea
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from networkx import maximal_independent_set
import numpy as np
import networkx as nx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from graph_operations import redrawGraph, addNode, draw_edge
from algorithmes.coloration import welch_powell
from algorithmes.prim import prim_mst
from algorithmes.Dijkstra import dijkstra
from Animation_window import AnimationWindow

button_style = """
QPushButton {
    background-color: white;
    color: black;
    border: 2px solid #555;
    border-radius: 10px;
    padding: 5px;
    font-size: 16px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #eeeeee;
}
QPushButton:pressed {
    background-color: #cccccc;
}
"""

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Graph Theory App")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: pink;")

        widget = QWidget(self)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        widget.setGeometry(250, 200, 300, 200)

        menu_label = QPushButton("Menu", widget)
        menu_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; background: pink; border: none;")
        layout.addWidget(menu_label)

        start_button = QPushButton("Début création du graphe", widget)
        start_button.setStyleSheet(button_style)
        start_button.clicked.connect(self.launchGraphDesigner)
        layout.addWidget(start_button)

    def launchGraphDesigner(self):
        self.graph_designer = GraphDesigner()
        self.graph_designer.show()

class GraphDesigner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mode = "creating_nodes"
        self.selected_node_for_edge_creation = None
        self.G = nx.DiGraph()
        self.pos = {}
        self.stable_sets = {}
        self.animation_steps = []

    def initUI(self):
        self.setWindowTitle("Graph Designer")
        self.setGeometry(100, 100, 800, 600)
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

        self.endNodesCreationButton = QPushButton("Fin création sommets")
        self.endNodesCreationButton.clicked.connect(self.endNodesCreation)
        layout.addWidget(self.endNodesCreationButton)

        self.endEdgesCreationButton = QPushButton("Fin création arcs")
        self.endEdgesCreationButton.setDisabled(True)
        self.endEdgesCreationButton.clicked.connect(self.endEdgesCreation)
        layout.addWidget(self.endEdgesCreationButton)

        self.findStableSetButton = QPushButton("Trouver ensemble stable maximal")
        self.findStableSetButton.setDisabled(True)
        self.findStableSetButton.clicked.connect(self.findStableSet)
        layout.addWidget(self.findStableSetButton)

        self.animateWelshPowellButton = QPushButton("Animer Welsh-Powell")
        self.animateWelshPowellButton.setDisabled(True)
        self.animateWelshPowellButton.clicked.connect(self.animateWelshPowell)
        layout.addWidget(self.animateWelshPowellButton)

        self.primButton = QPushButton("Exécuter Prim")
        self.primButton.setDisabled(True)
        self.primButton.clicked.connect(self.run_prim)
        layout.addWidget(self.primButton)

        self.dijkstraButton = QPushButton("Exécuter Dijkstra")
        self.dijkstraButton.setDisabled(True)
        self.dijkstraButton.clicked.connect(self.run_dijkstra)
        layout.addWidget(self.dijkstraButton)

        self.canvas.mpl_connect("button_press_event", self.on_click)

    def endNodesCreation(self):
        self.mode = "creating_edges"
        self.endNodesCreationButton.setDisabled(True)
        self.endEdgesCreationButton.setEnabled(True)

    def endEdgesCreation(self):
        self.mode = "none"
        self.endEdgesCreationButton.setDisabled(True)
        self.animateWelshPowellButton.setEnabled(True)
        self.primButton.setEnabled(True)
        self.dijkstraButton.setEnabled(True)

    def animateWelshPowell(self):
        self.animation_window = AnimationWindow(self.G, self.pos)
        self.animation_window.show()
        self.stable_sets = self.animation_window.color_map
        self.findStableSetButton.setEnabled(True)

    def findStableSet(self):
        stable_sets = {}
        for node, color in self.stable_sets.items():
            if color not in stable_sets:
                stable_sets[color] = []
            stable_sets[color].append(node)

        self.stable_sets = stable_sets

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
            nx.draw(subgraph, pos=self.pos, ax=ax, with_labels=True, node_color=[color]*len(nodes), node_size=700)
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas)
            stable_label = QLabel(f"Stable {index}")
            layout.addWidget(stable_label)

        stable_window.show()

    def run_prim(self):
        if not self.G.nodes:
            QMessageBox.warning(self, "Erreur", "Aucun nœud présent dans le graphe.")
            return
        start_node = list(self.G.nodes())[0]
        self.animation_steps = []
        prim_mst(self.G, start_node, self.visualize_step)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)

    def visualize_step(self, mst):
        self.animation_steps.append(mst)

    def update_graph(self):
        if self.animation_steps:
            mst = self.animation_steps.pop(0)
            self.ax.clear()
            nx.draw(
                mst,
                pos=self.pos,
                with_labels=True,
                ax=self.ax,
                node_size=700,
                node_color="lightblue",
                edge_color="blue",
            )
            self.canvas.draw()
        else:
            self.timer.stop()

    def run_dijkstra(self):
        if not self.G.nodes:
            QMessageBox.warning(self, "Error", "Aucun nœud présent dans le graphe.")
            return
        source_node = list(self.G.nodes())[0]
        path = dijkstra(self.G, source_node)
        QMessageBox.information(self, "Dijkstra Completed", "Dijkstra's algorithm has completed. Path: " + str(path))

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
            weight, ok = QInputDialog.getInt(self, "Poids de l'arc", "Entrez le poids de l'arc:", min=1)
            if ok:
                self.G.add_edge(self.selected_node_for_edge_creation, node_id, weight=weight)
                draw_edge(self.ax, self.pos, self.selected_node_for_edge_creation, node_id, weight, self.canvas)
                self.selected_node_for_edge_creation = None

    def get_closest_node(self, x, y):
        return min(
            self.G.nodes, key=lambda n: np.hypot(self.pos[n][0] - x, self.pos[n][1] - y)
        )
