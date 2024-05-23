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
        layout = QVBoxLayout(widget)
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
            from bellman_ford import bellman_ford
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
            nx.draw(self.G, pos=self.pos, ax=self.ax, with_labels=True, node_color='lightblue')
            # Ajoutez plus de détails ici pour montrer les poids, etc.
            self.canvas.draw()
        else:
            self.timer.stop()

    def closeEvent(self, event):
        self.timer.stop()  # Assurez-vous que le timer est arrêté lorsque la fenêtre est fermée
