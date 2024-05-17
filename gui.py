from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QMessageBox,
    QInputDialog,
    QLabel,
    QGridLayout,
    QScrollArea,
)
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
from algorithmes.prim_max import prim_max_mst
from algorithmes.kruskal_min import kruskal_mst
from Animation_window import AnimationWindow
import random

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
        menu_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: white; background: pink; border: none;"
        )
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
        self.selecting_start_node = False
        self.selecting_end_node = False

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

        self.primButton = QPushButton("Exécuter Prim pour l'arbre minimum")
        self.primButton.setDisabled(True)
        self.primButton.clicked.connect(lambda: self.run_prim(max_spanning_tree=False))
        layout.addWidget(self.primButton)

        self.primmaxButton = QPushButton("Exécuter Prim pour l'arbre maximum")
        self.primmaxButton.setDisabled(True)
        self.primmaxButton.clicked.connect(
            lambda: self.run_prim(max_spanning_tree=True)
        )
        layout.addWidget(self.primmaxButton)

        self.kruskalButton = QPushButton("Exécuter Kruskal pour l'arbre minimum")
        self.kruskalButton.setDisabled(True)
        self.kruskalButton.clicked.connect(self.run_kruskal)
        layout.addWidget(self.kruskalButton)

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
        self.primmaxButton.setEnabled(True)
        self.kruskalButton.setEnabled(True)

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

    def run_prim(self, max_spanning_tree=False):
        if not self.G.nodes:
            QMessageBox.warning(self, "Erreur", "Aucun nœud présent dans le graphe.")
            return
        start_node = random.choice(list(self.G.nodes()))
        self.animation_steps = []
        if max_spanning_tree:
            chosen_prim_algorithm = prim_max_mst
        else:
            chosen_prim_algorithm = prim_mst

        chosen_prim_algorithm(self.G, start_node, self.visualize_step)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)

    def run_kruskal(self):
        if not self.G.nodes:
            QMessageBox.warning(self, "Erreur", "Aucun nœud présent dans le graphe.")
            return
        self.animation_steps = []
        mst = kruskal_mst(self.G, self.visualize_step)
        self.animation_steps = [mst]
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)

    def visualize_step(self, mst):
        self.animation_steps.append(mst)

    def run_dijkstra(self):
        if not self.G.nodes:
            QMessageBox.warning(self, "Erreur", "Aucun nœud présent dans le graphe.")
            return
        self.mode = "selecting_start_node_for_dijkstra"
        QMessageBox.information(
            self, "Dijkstra", "Cliquez sur le nœud de départ pour Dijkstra."
        )
    def perform_dijkstra(self, start_node, end_node):
        try:
            distances, paths = nx.single_source_dijkstra(self.G, source=start_node, target=end_node, weight='weight')
            path = paths[end_node]
            self.redraw_graph_with_path(self,path)  # S'assure que cette méthode est aussi définie
        except KeyError:
            QMessageBox.warning(self, "Erreur", "Aucun chemin trouvé.")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", str(e))

    def redraw_graph_with_path(self, path):
        self.ax.clear()  # Efface le graphe actuel
        pos = nx.spring_layout(self.G)  # Positionne les nœuds

        # Dessine tous les nœuds et les arêtes normalement
        nx.draw_networkx_nodes(self.G, pos, node_color='gray', node_size=300, ax=self.ax)
        nx.draw_networkx_edges(self.G, pos, edge_color='gray', ax=self.ax)

        # Met en évidence le chemin
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_nodes(self.G, pos, nodelist=path, node_color='blue', node_size=300, ax=self.ax)
        nx.draw_networkx_edges(self.G, pos, edgelist=path_edges, edge_color='red', width=2, ax=self.ax)

        # Dessine les étiquettes des nœuds
        nx.draw_networkx_labels(self.G, pos, ax=self.ax, font_size=12, font_color='white')

        self.canvas.draw()  # Redessine le canvas


    # def redraw_graph_with_paths(self, paths):
    #     self.ax.clear()
    #     pos = nx.spring_layout(
    #         self.G
    #     )  # Recalculate positions for clarity in visualizing
    #     nx.draw_networkx_nodes(
    #         self.G, pos, ax=self.ax, node_size=700, node_color="skyblue"
    #     )
    #     nx.draw_networkx_labels(
    #         self.G, pos, ax=self.ax, font_size=10, font_color="white"
    #     )

    #     colors = plt.cm.get_cmap("hsv", len(paths))
    #     for idx, (target, path) in enumerate(paths.items()):
    #         if path:
    #             edges = list(zip(path[:-1], path[1:]))
    #             nx.draw_networkx_edges(
    #                 self.G,
    #                 pos,
    #                 edgelist=edges,
    #                 ax=self.ax,
    #                 edge_color=colors(idx),
    #                 width=2,
    #             )

    #     self.canvas.draw()

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

    # def run_dijkstra(self):
    #     if not self.G.nodes:
    #         QMessageBox.warning(self, "Error", "Aucun nœud présent dans le graphe.")
    #         return
    #     source_node = list(self.G.nodes())[0]
    #     path = dijkstra(self.G, source_node)
    #     QMessageBox.information(self, "Dijkstra Completed", "Dijkstra's algorithm has completed. Path: " + str(path))

    # def update_graph(self):
    #     if self.animation_steps:
    #         mst = self.animation_steps.pop(0)
    #         redrawGraph(self.ax, mst, self.pos, [], self.canvas)
    #     else:
    #         self.timer.stop()

    def on_click(self, event):
        if event.inaxes:  # S'assure que le clic est dans la zone du graphe
            x, y = event.xdata, event.ydata
            node_id = self.get_closest_node(
                x, y
            )  # Récupère l'identifiant du nœud le plus proche du clic

            if self.mode == "selecting_start_node_for_dijkstra":
                self.start_node = node_id  # Stocke le nœud de départ
                self.mode = "selecting_end_node_for_dijkstra"  # Change le mode pour sélectionner le nœud d'arrivée
                QMessageBox.information(
                    self, "Dijkstra", "Cliquez sur le nœud d'arrivée pour Dijkstra."
                )
            elif self.mode == "selecting_end_node_for_dijkstra":
                if (
                    node_id != self.start_node
                ):  # Vérifie que le nœud d'arrivée n'est pas le même que le nœud de départ
                    self.perform_dijkstra(self.start_node, node_id)  # Exécute Dijkstra
                    self.mode = "none"  # Réinitialise le mode
                else:
                    QMessageBox.warning(
                        self,
                        "Erreur",
                        "Le nœud de départ et d'arrivée ne peut pas être le même.",
                    )
            elif self.mode == "creating_nodes":
                addNode(self.G, self.pos, x, y, self.ax, self.canvas)  # Ajoute un nœud
            elif self.mode == "creating_edges":
                self.handle_edge_creation(x, y)  # Gère la création d'arêtes

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
                draw_edge(
                    self.ax,
                    self.pos,
                    self.selected_node_for_edge_creation,
                    node_id,
                    weight,
                    self.canvas,
                )
                self.selected_node_for_edge_creation = None

    def get_closest_node(self, x, y):
        if not self.G.nodes:
            return None
        return min(
            self.G.nodes, key=lambda n: np.hypot(self.pos[n][0] - x, self.pos[n][1] - y)
        )
