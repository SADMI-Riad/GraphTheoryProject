import sys
import os
import heapq
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QMessageBox,
    QInputDialog,
    QLabel,
    QLineEdit,
    QApplication,
    QScrollArea,
    QListWidget,
    QToolButton,
    QMenu,
    QAction,
)
import random
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from graph_operations import redrawGraph, addNode, draw_edge
from algorithmes.coloration import welch_powell
from algorithmes.prim import prim_mst
from algorithmes.Dijkstra import dijkstra
from algorithmes.kruskal_min import kruskal_mst
from bellman_ford_window import BellmanFordWindow
from Animation_window import AnimationWindow
from dijkstra_window import DijkstraWindow
import pickle

button_style = """
QPushButton {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #e6e6e6);
    color: #333;
    border: 1px solid #aaa;
    border-radius: 10px;
    padding: 5px 20px;
    font-size: 14px;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
}

QPushButton:hover {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #e9e9e9, stop:1 #d9d9d9);
    border-color: #888;
}

QPushButton:pressed {
    background-color: #d9d9d9;
    border-color: #666;
}

QPushButton:disabled {
    background-color: #f7f7f7;
    color: #aaa;
    border-color: #ddd;
}

"""

def load_user_data():
    if not os.path.exists("user_data.pkl"):
        return {}
    with open("user_data.pkl", "rb") as file:
        data = pickle.load(file)
        return data


def save_user_data(data):
    with open("user_data.pkl", "wb") as file:
        pickle.dump(data, file)


def get_current_user():
    if os.path.exists("current_user.txt"):
        with open("current_user.txt", "r") as file:
            return file.read().strip()
    return None


def set_current_user(username):
    with open("current_user.txt", "w") as file:
        file.write(username)


mock_database = load_user_data()


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Graph Theory App - Main Menu")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #2c3e50; color: white;")

        widget = QWidget(self)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        title = QLabel("Welcome to Graph Theory App", self)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        nouveau_graphe_button = QPushButton("Nouveau Graphe", self)
        nouveau_graphe_button.setFont(QFont("Arial", 12))
        nouveau_graphe_button.setStyleSheet("background-color: #3498db; color: white;")
        nouveau_graphe_button.clicked.connect(self.new_graph)
        layout.addWidget(nouveau_graphe_button)

        collection_button = QPushButton("Collection", self)
        collection_button.setFont(QFont("Arial", 12))
        collection_button.setStyleSheet("background-color: #e74c3c; color: white;")
        collection_button.clicked.connect(self.show_collection)
        layout.addWidget(collection_button)

    def new_graph(self):
        self.graph_designer = GraphDesigner()
        self.graph_designer.show()
        self.close()

    def show_collection(self):
        from Collection_window import CollectionWindow
        self.collection_window = CollectionWindow()
        self.collection_window.show()
        self.close()


class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #2c3e50; color: white;")

        widget = QWidget(self)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        title = QLabel("Login", self)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFont(QFont("Arial", 12))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFont(QFont("Arial", 12))
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_button = QPushButton("Login", self)
        login_button.setFont(QFont("Arial", 12))
        login_button.setStyleSheet("background-color: #3498db; color: white;")
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        register_button = QPushButton("Register", self)
        register_button.setFont(QFont("Arial", 12))
        register_button.setStyleSheet("background-color: #e74c3c; color: white;")
        register_button.clicked.connect(self.show_register)
        layout.addWidget(register_button)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            set_current_user(username)
            print(f"Logged in as: {username}")  # Debug print
            self.main_menu = MainMenu()
            self.main_menu.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")

    def show_register(self):
        self.register_page = RegisterPage()
        self.register_page.show()
        self.close()


class RegisterPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Register")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #2c3e50; color: white;")

        widget = QWidget(self)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        title = QLabel("Register", self)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFont(QFont("Arial", 12))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFont(QFont("Arial", 12))
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        register_button = QPushButton("Register", self)
        register_button.setFont(QFont("Arial", 12))
        register_button.setStyleSheet("background-color: #e74c3c; color: white;")
        register_button.clicked.connect(self.register)
        layout.addWidget(register_button)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user_data = load_user_data()
        if username in user_data:
            QMessageBox.warning(self, "Error", "Username already exists. Try logging in instead.")
        else:
            user_data[username] = {"password": password, "graphs": {}}
            save_user_data(user_data)
            QMessageBox.information(self, "Success", "Registration successful. You can now log in.")
            self.login_page = LoginPage()
            self.login_page.show()
            self.close()


class GraphDesigner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mode = None
        self.selected_node_for_edge_creation = None
        self.G = nx.DiGraph()
        self.G.graph_designer = self  # Assign the graph designer to the graph object
        self.pos = {}
        self.stable_sets = {}
        self.animation_steps = []
        self.animation_windows = []
        self.node_counter = 1  # Initialize the node counter



    def initUI(self):
        self.setWindowTitle("Graph Designer")
        self.setGeometry(100, 100, 1000, 600)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        button_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)

        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim([0, 1])
        self.ax.set_ylim([0, 1])
        self.ax.axis("off")
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        self.algorithmsButton = QToolButton(self)
        self.algorithmsButton.setText("Algorithmes")
        self.algorithmsButton.setStyleSheet(button_style)
        self.algorithmsButton.setFixedWidth(200)
        self.algorithmsMenu = QMenu(self)
        self.algorithmsButton.setMenu(self.algorithmsMenu)
        self.algorithmsButton.setPopupMode(QToolButton.InstantPopup)
        button_layout.addWidget(self.algorithmsButton)

        self.add_action_to_menu(
            self.algorithmsMenu,
            "Animer Welsh-Powell",
            self.animateWelshPowell,
        )
        self.add_action_to_menu(
            self.algorithmsMenu,
            "Animer Prim pour Le Max-st",
            self.animatePrimMax,
        )
        self.add_action_to_menu(
            self.algorithmsMenu,
            "Animer Kruskal pour Le Max-st",
            self.animateKruskalMax,
        )
        self.add_action_to_menu(
            self.algorithmsMenu,
            "Animer Kruskal pour Le Min-st",
            self.animateKruskal,
        )
        self.add_action_to_menu(
            self.algorithmsMenu,
            "Animer Prim pour Le Min-st",
            self.animatePrim,
        )
        self.add_action_to_menu(
            self.algorithmsMenu,
            "Animer Dijkstra",
            self.animateDijkstra,
        )
        self.add_action_to_menu(
            self.algorithmsMenu,
            "Animer Bellman-Ford",
            self.animateBellmanFord,
        )

        self.sauvegarderButton = QPushButton("Sauvegarder")
        self.sauvegarderButton.setFixedWidth(200)
        self.sauvegarderButton.setStyleSheet(button_style)
        self.sauvegarderButton.clicked.connect(self.save_graph)
        self.sauvegarderButton.setDisabled(True)
        button_layout.addWidget(self.sauvegarderButton)

        self.addNodeButton = QPushButton("Add Node", self)
        self.addNodeButton.setFixedWidth(200)
        self.addNodeButton.setStyleSheet(button_style)
        self.addNodeButton.setCheckable(True)
        self.addNodeButton.clicked.connect(self.toggle_add_node_mode)
        button_layout.addWidget(self.addNodeButton)

        self.addEdgeButton = QPushButton("Add Edge", self)
        self.addEdgeButton.setCheckable(True)
        self.addEdgeButton.setFixedWidth(200)
        self.addEdgeButton.setStyleSheet(button_style)
        self.addEdgeButton.setCheckable(True)
        self.addEdgeButton.clicked.connect(self.toggle_add_edge_mode)
        button_layout.addWidget(self.addEdgeButton)

        self.deleteNodeButton = QPushButton("Supprimer sommet")
        self.deleteNodeButton.setCheckable(True)
        self.deleteNodeButton.setFixedWidth(200)
        self.deleteNodeButton.setStyleSheet(button_style)
        self.deleteNodeButton.clicked.connect(self.toggle_delete_node_mode)
        button_layout.addWidget(self.deleteNodeButton)

        self.deleteEdgeButton = QPushButton("Supprimer arc")
        self.deleteEdgeButton.setCheckable(True)
        self.deleteEdgeButton.setFixedWidth(200)
        self.deleteEdgeButton.setStyleSheet(button_style)
        self.deleteEdgeButton.clicked.connect(self.toggle_delete_edge_mode)
        button_layout.addWidget(self.deleteEdgeButton)

        self.canvas.mpl_connect("button_press_event", self.on_click)

        self.set_initial_button_states()

        button_layout.addStretch()

    def toggle_add_node_mode(self):
        if self.addNodeButton.isChecked():
            self.mode = "add_node"
            self.addEdgeButton.setChecked(False)
            self.deleteNodeButton.setChecked(False)
            self.deleteEdgeButton.setChecked(False)
        else:
            self.mode = None
        self.update_button_styles()

    def toggle_add_edge_mode(self):
        if self.addEdgeButton.isChecked():
            self.mode = "add_edge"
            self.addNodeButton.setChecked(False)
            self.deleteNodeButton.setChecked(False)
            self.deleteEdgeButton.setChecked(False)
        else:
            self.mode = None
        self.update_button_styles()


    def toggle_delete_node_mode(self):
        if self.deleteNodeButton.isChecked():
            self.mode = "deleting_nodes"
            self.addNodeButton.setChecked(False)
            self.addEdgeButton.setChecked(False)
            self.deleteEdgeButton.setChecked(False)
        else:
            self.mode = None
        self.update_button_styles()

    def toggle_delete_edge_mode(self):
        if self.deleteEdgeButton.isChecked():
            self.mode = "deleting_edges"
            self.addNodeButton.setChecked(False)
            self.addEdgeButton.setChecked(False)
            self.deleteNodeButton.setChecked(False)
        else:
            self.mode = None
        self.update_button_styles()


    def update_button_styles(self):
        active_style = """
        QPushButton {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #b4ec51, stop:1 #429321);
            color: white;
            border-color: #5fa837;
            border: 1px solid #aaa;
            border-radius: 10px;
            padding: 5px 20px;
            font-size: 14px;
            font-weight: bold;
            text-align: center;
            text-transform: uppercase;
        }
        QPushButton:hover {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #e9e9e9, stop:1 #d9d9d9);
            border-color: #899;
        }
        QPushButton:pressed {
            background-color: #d9d9d9;
            border-color: #670;
        }
        """

        buttons = [self.addNodeButton, self.addEdgeButton, self.deleteNodeButton, self.deleteEdgeButton]

        for button in buttons:
            if button.isChecked():
                button.setStyleSheet(active_style)
            else:
                button.setStyleSheet(button_style)

        # Ensure buttons are enabled appropriately
        self.addNodeButton.setEnabled(True)
        if len(self.G.nodes) > 0:
            self.addEdgeButton.setEnabled(True)
            self.deleteNodeButton.setEnabled(True)
            self.deleteEdgeButton.setEnabled(True)
            self.sauvegarderButton.setEnabled(True)
            self.algorithmsButton.setEnabled(True)
        else:
            self.addEdgeButton.setDisabled(True)
            self.deleteNodeButton.setDisabled(True)
            self.deleteEdgeButton.setDisabled(True)
            self.sauvegarderButton.setDisabled(True)
            self.algorithmsButton.setDisabled(True)

    def set_initial_button_states(self):
        self.addNodeButton.setEnabled(True)
        self.addEdgeButton.setEnabled(True)
        self.deleteNodeButton.setDisabled(True)
        self.deleteEdgeButton.setDisabled(True)
        self.sauvegarderButton.setDisabled(True)
        self.algorithmsButton.setDisabled(True)


    def find_menu_action(self, menu, action_text):
        for action in menu.actions():
            if action.text() == action_text:
                return action
        return None

    def add_action_to_menu(self, menu, action_text, action_func):
        action = QAction(action_text, self)
        action.triggered.connect(action_func)
        menu.addAction(action)

    def save_graph(self):
        name, ok = QInputDialog.getText(
            self, "Sauvegarder le graphe", "Entrez le nom du graphe:"
        )
        if ok and name:
            username = get_current_user()
            user_data = load_user_data()
            if username in user_data:
                existing_graphs = user_data[username]["graphs"]
                if name in existing_graphs:
                    overwrite = QMessageBox.question(
                        self,
                        "Graphe Existant",
                        "Un graphe avec ce nom existe déjà. Voulez-vous l'écraser ?",
                        QMessageBox.Yes | QMessageBox.No,
                    )
                    if overwrite == QMessageBox.Yes:
                        self._save_graph_data(name, user_data)
                    else:
                        new_name, ok = QInputDialog.getText(
                            self, "Nouveau Nom", "Entrez le nouveau nom du graphe:"
                        )
                        if ok and new_name:
                            self._save_graph_data(new_name, user_data)
                else:
                    self._save_graph_data(name, user_data)
                self.sauvegarderButton.setDisabled(True)

    def _save_graph_data(self, name, user_data):
        username = get_current_user()
        graph_data = {
            "nodes": list(self.G.nodes()),
            "edges": list(self.G.edges(data=True)),
            "positions": {node: (float(pos[0]), float(pos[1])) for node, pos in self.pos.items()},
        }
        user_data[username]["graphs"][name] = graph_data
        save_user_data(user_data)
        QMessageBox.information(self, "Succès", "Graphe sauvegardé avec succès.")
        
    def load_graph(self, name):
        username = get_current_user()
        user_data = load_user_data()
        if username in user_data and name in user_data[username]["graphs"]:
            graph_data = user_data[username]["graphs"][name]
            self.G.clear()
            self.pos.clear()
            self.G.add_nodes_from(graph_data["nodes"])
            self.G.add_edges_from((u, v, d) for u, v, d in graph_data["edges"])
            self.pos = {node: (pos[0], pos[1]) for node, pos in graph_data["positions"].items()}
            self.redraw_graph()
        else:
            QMessageBox.warning(self, "Erreur", "Le graphe n'existe pas ou n'a pas été trouvé.")

    def reset_buttons_states(self):
        self.algorithmsButton.setEnabled(True)
        self.sauvegarderButton.setEnabled(True)
        self.deleteNodeButton.setEnabled(True)
        self.deleteEdgeButton.setEnabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Welsh-Powell").setEnabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Kruskal pour Le Max-st").setEnabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Kruskal pour Le Min-st").setEnabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Prim pour Le Max-st").setEnabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Prim pour Le Min-st").setEnabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Dijkstra").setEnabled(True)

    def animateWelshPowell(self):
        animation_window = AnimationWindow(self.G, self.pos, algorithm="welsh_powell")
        self.animation_windows.append(animation_window)
        animation_window.show()
        # self.stable_sets = self.get_stable_sets_from_colors(animation_window.color_map)
        # self.find_menu_action(self.algorithmsMenu, "Trouver ensemble stable maximal").setEnabled(True)

    def animateKruskal(self):
        animation_window = AnimationWindow(self.G, self.pos, algorithm="kruskal")
        self.animation_windows.append(animation_window)
        animation_window.show()

    def animateKruskalMax(self):
        animation_window = AnimationWindow(self.G, self.pos, algorithm="kruskalMax")
        self.animation_windows.append(animation_window)
        animation_window.show()

    def animatePrim(self):
        start_node = random.choice(list(self.G.nodes()))
        animation_window = AnimationWindow(
            self.G, self.pos, algorithm="prim", start_node=start_node
        )
        self.animation_windows.append(animation_window)
        animation_window.show()

    def animatePrimMax(self):
        start_node = random.choice(list(self.G.nodes()))
        animation_window = AnimationWindow(
            self.G, self.pos, algorithm="primMax", start_node=start_node
        )
        self.animation_windows.append(animation_window)
        animation_window.show()

    def animateDijkstra(self):
        animation_window = DijkstraWindow(self.G, self.pos)
        self.animation_windows.append(animation_window)
        animation_window.show()

    def animateBellmanFord(self):
        try:
            bellman_ford_window = BellmanFordWindow(self.G, self.pos)
            bellman_ford_window.show()
            self.animation_windows.append(bellman_ford_window)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite: {str(e)}")

    def on_click(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            if self.mode == "add_node":
                addNode(self.G, self.pos, x, y, self.ax, self.canvas)
                if len(self.G.nodes) > 0:
                    self.addEdgeButton.setEnabled(True)
                    self.deleteNodeButton.setEnabled(True)
                    self.deleteEdgeButton.setEnabled(True)
                    self.sauvegarderButton.setEnabled(True)
                    self.algorithmsButton.setEnabled(True)
            elif self.mode == "add_edge":
                self.handle_edge_creation(x, y)
            elif self.mode == "deleting_nodes":
                self.handle_node_deletion(x, y)
            elif self.mode == "deleting_edges":
                self.handle_edge_deletion(x, y)


    def handle_edge_creation(self, x, y):
        node_id = self.get_closest_node(x, y)
        if self.selected_node_for_edge_creation is None:
            self.selected_node_for_edge_creation = node_id
        else:
            if self.selected_node_for_edge_creation == node_id:
                weight, ok = QInputDialog.getInt(
                    self, "Poids de la boucle", "Entrez le poids de la boucle:", min=1
                )
                if ok:
                    self.G.add_edge(node_id, node_id, weight=weight)
                    self.draw_loop(self.ax, self.pos, node_id, weight, self.canvas)
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

    def handle_node_deletion(self, x, y):
        node_id = self.get_closest_node(x, y)
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Do you confirm you want to delete node {node_id}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.G.remove_node(node_id)
            del self.pos[node_id]
            redrawGraph(self.ax, self.G, self.pos, [], self.canvas)
            self.sauvegarderButton.setEnabled(True)
            self.mode = None
            self.update_button_styles()


    def handle_edge_deletion(self, x, y):
        closest_edge = self.get_closest_edge(x, y)
        if closest_edge is not None:
            confirm = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Do you confirm you want to delete edge {closest_edge}?",
                QMessageBox.Yes | QMessageBox.No,
            )
            if confirm == QMessageBox.Yes:
                self.G.remove_edge(*closest_edge)
                redrawGraph(self.ax, self.G, self.pos, [], self.canvas)
                self.sauvegarderButton.setEnabled(True)
                self.mode = None
                self.update_button_styles()

    def get_closest_node(self, x, y):
        return min(
            self.G.nodes, key=lambda n: np.hypot(self.pos[n][0] - x, self.pos[n][1] - y)
        )

    def get_closest_edge(self, x, y):
        def distance_from_point_to_line(px, py, x1, y1, x2, y2):
            line_mag = np.hypot(x2 - x1, y2 - y1)
            u = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / (line_mag ** 2)
            if u < 0 or u > 1:
                return min(
                    np.hypot(px - x1, py - y1),
                    np.hypot(px - x2, py - y2)
                )
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
            return np.hypot(px - ix, py - iy)

        closest_edge = min(
            self.G.edges, 
            key=lambda e: distance_from_point_to_line(
                x, y, self.pos[e[0]][0], self.pos[e[0]][1], self.pos[e[1]][0], self.pos[e[1]][1]
            )
        )
        distance = distance_from_point_to_line(
            x, y, self.pos[closest_edge[0]][0], self.pos[closest_edge[0]][1], self.pos[closest_edge[1]][0], self.pos[closest_edge[1]][1]
        )
        if distance < 0.05:  # Adjust the threshold as needed
            return closest_edge
        return None

    def draw_loop(self, ax, pos, node_id, weight, canvas):
        x, y = pos[node_id]
        loop_radius = 0.05  # Augmenter le rayon pour plus de visibilité
        loop = plt.Circle(
            (x, y + loop_radius),
            loop_radius,
            color="black",
            fill=False,
            linestyle="-",
            linewidth=1,
        )
        ax.add_patch(loop)
        # Décaler le texte pour qu'il soit au-dessus de la boucle et non à l'intérieur
        ax.text(
            x,
            y + 2 * loop_radius,
            str(weight),
            color="darkblue",  # Changer la couleur pour une meilleure visibilité
            fontsize=10,  # Ajuster la taille du texte si nécessaire
            ha="center",
            va="center",
            bbox=dict(
                facecolor="white", edgecolor="none", pad=2
            ),  # Ajouter un fond pour le texte
        )
        canvas.draw()

    def redraw_graph(self):
        self.ax.clear()
        nx.draw(
            self.G,
            pos=self.pos,
            ax=self.ax,
            with_labels=True,
            node_color="lightblue",
            node_size=700,
            edge_color="gray",
        )
        for u, v, d in self.G.edges(data=True):
            if u == v:
                x, y = self.pos[u]
                loop_radius = 0.03
                loop = plt.Circle((x, y), loop_radius, color="black", fill=False)
                self.ax.add_patch(loop)
                self.ax.text(
                    x + loop_radius,
                    y + loop_radius,
                    str(d["weight"]),
                    color="red",
                    fontsize=12,
                    ha="center",
                    va="center",
                )
            else:
                self.ax.text(
                    (self.pos[u][0] + self.pos[v][0]) / 2,
                    (self.pos[u][1] + self.pos[v][1]) / 2,
                    str(d["weight"]),
                    color="red",
                    fontsize=12,
                    ha="center",
                    va="center",
                )
        self.canvas.draw()

    def animateBellmanFord(self):
        try:
            bellman_ford_window = BellmanFordWindow(self.G, self.pos)
            bellman_ford_window.show()
            self.animation_windows.append(
                bellman_ford_window
            )  # Gardez une référence pour éviter la fermeture prématurée
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite: {str(e)}")
