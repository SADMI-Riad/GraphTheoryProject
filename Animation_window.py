from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import matplotlib.pyplot as plt
from algorithmes.coloration import welch_powell

class AnimationWindow(QMainWindow):
    def __init__(self, G, pos):
        super().__init__()
        self.G = G.to_undirected()  # Convert directed graph to undirected
        self.pos = pos
        self.initUI()
        self.color_map = welch_powell(self.G)
        self.animation_steps = list(self.color_map.items())
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)  # Pause for 1 second for each step

    def initUI(self):
        self.setWindowTitle("Animation Welsh-Powell")
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

    def update_graph(self):
        if self.animation_steps:
            node, color = self.animation_steps.pop(0)
            print(f"Animating node {node} with color {color}")
            
            self.ax.clear()
            node_colors = [self.color_map.get(n, 'lightgray') for n in self.G.nodes()]
            nx.draw(self.G, pos=self.pos, ax=self.ax, with_labels=True, node_color=node_colors, node_size=700)
            self.canvas.draw()
        else:
            self.timer.stop()
