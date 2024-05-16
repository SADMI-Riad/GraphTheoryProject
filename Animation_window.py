# Animation_window.py
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
        current_color = 0
        
        while sorted_nodes:
            node = sorted_nodes.pop(0)
            color[node] = current_color
            non_adjacent_nodes = [node]
            
            for other_node in sorted_nodes[:]:
                if all(not self.G.has_edge(other_node, n) for n in non_adjacent_nodes):
                    color[other_node] = current_color
                    non_adjacent_nodes.append(other_node)
                    sorted_nodes.remove(other_node)
            
            self.animation_steps.append(color.copy())
            current_color += 1
        
        self.timer.start(1000)

    def update_graph(self):
        if self.animation_steps:
            color = self.animation_steps.pop(0)
            self.ax.clear()
            nx.draw_networkx_nodes(
                self.G,
                self.pos,
                ax=self.ax,
                node_size=700,
                node_color=[color.get(node, -1) for node in self.G.nodes()],
                cmap=plt.cm.jet,
                alpha=0.9,
            )
            nx.draw_networkx_edges(self.G, self.pos, ax=self.ax)
            nx.draw_networkx_labels(self.G, self.pos, ax=self.ax, font_size=10, font_color="white")
            self.canvas.draw()
        else:
            self.timer.stop()
