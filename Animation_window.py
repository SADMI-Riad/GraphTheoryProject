from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import networkx as nx
import matplotlib.pyplot as plt
from algorithmes.coloration import welch_powell

class AnimationWindow(QMainWindow):
    def __init__(self, G, pos):
        super().__init__()
        self.G = G
        self.pos = pos
        self.initUI()
        self.animation_steps = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.run_animation()

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

    def run_animation(self):
        sorted_nodes = sorted(self.G.nodes(), key=lambda x: self.G.degree(x), reverse=True)
        color = {}
        max_color = 0
        for node in sorted_nodes:
            available_colors = {color[neighbor] for neighbor in self.G.neighbors(node) if neighbor in color}
            node_color = next(color for color in range(max_color + 1) if color not in available_colors)
            color[node] = node_color
            if node_color == max_color:
                max_color += 1
            stable_set = [node for node, col in color.items() if col == 0]
            self.animation_steps.append((color.copy(), stable_set))
        self.timer.start(1000)

    def update_graph(self):
        if self.animation_steps:
            color, stable_set = self.animation_steps.pop(0)
            self.ax.clear()
            nx.draw_networkx_nodes(
                self.G,
                self.pos,
                ax=self.ax,
                node_size=700,
                node_color=["red" if node in stable_set else "skyblue" for node in self.G.nodes()],
                alpha=0.9,
            )
            nx.draw_networkx_edges(self.G, self.pos, ax=self.ax)
            nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=10, font_color="white")
            self.canvas.draw()
        else:
            self.timer.stop()
