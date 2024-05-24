from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import networkx as nx

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

    def start_bellman_ford(self):
        source = list(self.G.nodes())[0]  # Ou choisir dynamiquement
        try:
            from algorithmes.bellman_ford import bellman_ford
            bellman_ford(self.G, source, self.visualize_step)
            self.timer.start(1000)
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.timer.stop()

    def visualize_step(self, graph, u, v, distances, predecessors):
        self.animation_steps.append((u, v, dict(distances), dict(predecessors)))

    def update_visual(self):
        if self.animation_steps:
            u, v, distances, predecessors = self.animation_steps.pop(0)
            self.ax.clear()

            # Organiser les nœuds par niveaux
            levels = {}
            for node, dist in distances.items():
                if dist not in levels:
                    levels[dist] = []
                levels[dist].append(node)

            # Dessiner les nœuds par niveaux
            level_positions = {}
            for level, nodes in levels.items():
                for i, node in enumerate(nodes):
                    level_positions[node] = (i, -level)

            # Vérifier les positions pour éviter les valeurs invalides
            for node, (x, y) in level_positions.items():
                if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
                    raise ValueError(f"Invalid position for node {node}: ({x}, {y})")

            nx.draw(self.G, pos=level_positions, ax=self.ax, with_labels=True, node_color='lightblue')
            nx.draw_networkx_edges(self.G, pos=level_positions, ax=self.ax, edgelist=[(u, v)], edge_color='red', width=2)
            
            # Affichez les distances sur les noeuds
            labels = {node: f"{node}\n{distances[node]}" for node in self.G.nodes()}
            nx.draw_networkx_labels(self.G, pos=level_positions, ax=self.ax, labels=labels)
            self.canvas.draw()
        else:
            self.timer.stop()

    def closeEvent(self, event):
        self.timer.stop()  # Assurez-vous que le timer est arrêté lorsque la fenêtre est fermée
