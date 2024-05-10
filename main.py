import sys
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QInputDialog,
    QMessageBox,
)
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import FancyArrowPatch
from algorithmes.coloration import welch_powell
from algorithmes.prim import prim_mst


class GraphDesigner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mode = "creating_nodes"
        self.selected_node_for_edge_creation = None
        self.G = nx.DiGraph()
        self.pos = {}
        self.stable_set = []

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

    def findStableSet(self):
        self.stable_set = welch_powell(self.G)
        self.redrawGraph()

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

    def on_click(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            if self.mode == "creating_nodes":
                self.addNode(x, y)
            elif self.mode == "creating_edges":
                self.createEdge(x, y)

    def addNode(self, x, y):
        node_id = len(self.pos) + 1
        self.pos[node_id] = (x, y)
        self.G.add_node(node_id)
        self.redrawGraph()

    def createEdge(self, x, y):
        closest_node = self.get_closest_node(x, y)
        if self.selected_node_for_edge_creation is None:
            self.selected_node_for_edge_creation = closest_node
        else:
            weight, ok = QInputDialog.getInt(
                self, "Poids de l'arc", "Entrez le poids de l'arc:", min=1
            )
            if ok:
                self.G.add_edge(
                    self.selected_node_for_edge_creation, closest_node, weight=weight
                )
            self.selected_node_for_edge_creation = None
            self.redrawGraph()

    def get_closest_node(self, x, y):
        return min(
            self.G.nodes, key=lambda n: np.hypot(self.pos[n][0] - x, self.pos[n][1] - y)
        )

    def redrawGraph(self):
        self.ax.clear()
        self.ax.set_xlim([0, 1])
        self.ax.set_ylim([0, 1])
        self.ax.axis("off")
        nx.draw_networkx_nodes(
            self.G,
            self.pos,
            ax=self.ax,
            node_size=700,
            node_color=[
                "red" if node in self.stable_set else "skyblue"
                for node in self.G.nodes()
            ],
            alpha=0.9,
        )
        nx.draw_networkx_labels(
            self.G, self.pos, ax=self.ax, font_size=10, font_color="white"
        )
        self.draw_edges()
        self.canvas.draw()

    def draw_edges(self):
        for node1, node2, data in self.G.edges(data=True):
            self.draw_edge(node1, node2, data.get("weight", 1))

    def draw_edge(self, node1, node2, weight=0.5):
        x1, y1 = self.pos[node1]
        x2, y2 = self.pos[node2]
        if node1 != node2:
            rad = 0.35
            arrow = FancyArrowPatch(
                (x1, y1),
                (x2, y2),
                arrowstyle="-|>",
                color="black",
                lw=1,
                connectionstyle=f"arc3,rad={rad}",
                shrinkA=12,
                shrinkB=12,
                mutation_scale=15,
            )
            self.ax.add_patch(arrow)
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            offset_x, offset_y = (y2 - y1) * rad, (x1 - x2) * rad
            text_x, text_y = mid_x + offset_x, mid_y + offset_y
            self.ax.text(
                text_x,
                text_y,
                str(weight),
                color="red",
                fontsize=8,
                ha="center",
                va="center",
            )
        else:
            rad = 0.3
            loop = FancyArrowPatch(
                (x1, y1),
                (x1, y1),
                arrowstyle="-|>",
                color="black",
                lw=1,
                connectionstyle=f"arc3,rad={rad}",
                shrinkA=10,
                shrinkB=10,
                mutation_scale=20,
            )
            self.ax.add_patch(loop)
            self.ax.text(
                x1, y1 + rad * 1.5, str(weight), color="red", fontsize=12, ha="center"
            )

    def endNodesCreation(self):
        self.mode = "creating_edges"
        self.endNodesCreationButton.setDisabled(True)


def main():
    app = QApplication(sys.argv)
    ex = GraphDesigner()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
