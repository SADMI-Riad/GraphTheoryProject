import sys
import os
import heapq
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QMessageBox, QInputDialog, QLabel, QLineEdit, QApplication,
    QScrollArea, QListWidget, QToolButton, QMenu, QAction
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from graph_operations import redrawGraph, addNode, draw_edge
from algorithmes.coloration import welch_powell
from algorithmes.prim import prim_mst
from algorithmes.Dijkstra import dijkstra
from algorithmes.kruskal_min import kruskal_mst
from Animation_window import AnimationWindow
from dijkstra_window import DijkstraWindow
import pickle

button_style = """
QPushButton {
    background-color: white;
    color: black;
    border: 2px solid #555;
    border-radius: 5px;
    padding: 5px;
    font-size: 12px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #eeeeee;
}
QPushButton:pressed {
    background-color: #cccccc;
}
"""

current_user = None

USER_DATA_FILE = "user_data.pkl"
CURRENT_USER_FILE = "current_user.txt"

def save_current_user_to_file(username):
    with open(CURRENT_USER_FILE, "w") as file:
        file.write(username)

def load_current_user_from_file():
    if os.path.exists(CURRENT_USER_FILE):
        with open(CURRENT_USER_FILE, "r") as file:
            return file.read().strip()
    return None

def load_user_data():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    with open(USER_DATA_FILE, "rb") as file:
        data = pickle.load(file)
        return data

def save_user_data(data):
    with open(USER_DATA_FILE, "wb") as file:
        pickle.dump(data, file)

def get_current_user():
    global current_user
    if current_user is None:
        current_user = load_current_user_from_file()
    print(f"Getting current user: {current_user}")  # Debug print
    return current_user

def set_current_user(username):
    global current_user
    current_user = username
    save_current_user_to_file(username)
    print(f"Setting current user: {current_user}")  # Debug print




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
        from Collection_window import CollectionWindow  # Local import to avoid circular dependency
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
        self.mode = "creating_nodes"
        self.selected_node_for_edge_creation = None
        self.G = nx.DiGraph()
        self.pos = {}
        self.stable_sets = {}
        self.animation_steps = []
        self.animation_windows = []

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

        self.operationsButton = QToolButton(self)
        self.operationsButton.setStyleSheet(
            """
            QToolButton {
                border: none;
            }
            QToolButton::menu-indicator {
                image: none;
            }
            """
        )
        self.operationsButton.setText("Opérations")
        icon = QIcon("icons/menu1.png")
        self.operationsButton.setIcon(icon)
        self.operationsMenu = QMenu(self)
        self.operationsButton.setMenu(self.operationsMenu)
        self.operationsButton.setPopupMode(QToolButton.InstantPopup)
        button_layout.addWidget(self.operationsButton)

        self.algorithmsButton = QToolButton(self)
        self.algorithmsButton.setText("Algorithmes")
        self.algorithmsMenu = QMenu(self)
        self.algorithmsButton.setMenu(self.algorithmsMenu)
        self.algorithmsButton.setPopupMode(QToolButton.InstantPopup)
        button_layout.addWidget(self.algorithmsButton)

        self.add_action_to_menu(
            self.operationsMenu,
            "Fin création sommets",
            self.endNodesCreation,
        )
        self.add_action_to_menu(
            self.operationsMenu,
            "Fin création arcs",
            self.endEdgesCreation,
        )
        self.add_action_to_menu(
            self.algorithmsMenu,
            "Trouver ensemble stable maximal",
            self.findStableSet,
        )
        self.add_action_to_menu(
            self.algorithmsMenu,
            "Animer Welsh-Powell",
            self.animateWelshPowell,
        )
        self.add_action_to_menu(
            self.algorithmsMenu,
            "Animer Kruskal",
            self.animateKruskal,
        )
        self.add_action_to_menu(
            self.algorithmsMenu,
            "Animer Prim",
            self.animatePrim,
        )
        self.add_action_to_menu(
            self.algorithmsMenu,
            "Animer Dijkstra",
            self.animateDijkstra,
        )

        self.sauvegarderButton = QPushButton("Sauvegarder")
        self.sauvegarderButton.setFixedWidth(200)
        self.sauvegarderButton.setStyleSheet(button_style)
        self.sauvegarderButton.clicked.connect(self.save_graph)
        self.sauvegarderButton.setDisabled(True)
        button_layout.addWidget(self.sauvegarderButton)

        self.deleteNodeButton = QPushButton("Supprimer sommet")
        self.deleteNodeButton.setFixedWidth(200)
        self.deleteNodeButton.setStyleSheet(button_style)
        self.deleteNodeButton.clicked.connect(self.enableDeleteNodeMode)
        self.deleteNodeButton.setDisabled(True)
        button_layout.addWidget(self.deleteNodeButton)

        self.stopDeletionModeButton = QPushButton("Arrêter le mode suppression")
        self.stopDeletionModeButton.setFixedWidth(200)
        self.stopDeletionModeButton.setStyleSheet(button_style)
        self.stopDeletionModeButton.setDisabled(True)
        self.stopDeletionModeButton.clicked.connect(self.stopDeleteNodeMode)
        button_layout.addWidget(self.stopDeletionModeButton)

        self.canvas.mpl_connect("button_press_event", self.on_click)

        button_layout.addStretch()

        # Initially disable all buttons except "Fin création sommets"
        self.set_initial_button_states()

    def set_initial_button_states(self):
        self.operationsButton.setEnabled(True)
        self.algorithmsButton.setDisabled(True)
        self.sauvegarderButton.setDisabled(True)
        self.deleteNodeButton.setDisabled(True)
        self.stopDeletionModeButton.setDisabled(True)

        self.find_menu_action(self.operationsMenu, "Fin création sommets").setEnabled(True)
        self.find_menu_action(self.operationsMenu, "Fin création arcs").setDisabled(True)
        self.find_menu_action(self.algorithmsMenu, "Trouver ensemble stable maximal").setDisabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Welsh-Powell").setDisabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Kruskal").setDisabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Prim").setDisabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Dijkstra").setDisabled(True)

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
        name, ok = QInputDialog.getText(self, "Sauvegarder le graphe", "Entrez le nom du graphe:")
        if ok and name:
            username = get_current_user()
            user_data = load_user_data()
            if username in user_data:
                existing_graphs = user_data[username]['graphs']
                if name in existing_graphs:
                    overwrite = QMessageBox.question(
                        self,
                        "Graphe Existant",
                        "Un graphe avec ce nom existe déjà. Voulez-vous l'écraser ?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if overwrite == QMessageBox.Yes:
                        self._save_graph_data(name, user_data)
                    else:
                        new_name, ok = QInputDialog.getText(self, "Nouveau Nom", "Entrez le nouveau nom du graphe:")
                        if ok and new_name:
                            self._save_graph_data(new_name, user_data)
                else:
                    self._save_graph_data(name, user_data)
                self.sauvegarderButton.setDisabled(True)

    def _save_graph_data(self, name, user_data):
        username = get_current_user()
        user_data[username]['graphs'][name] = {
            'G': self.G,
            'pos': self.pos
        }
        save_user_data(user_data)
        QMessageBox.information(self, "Succès", "Graphe sauvegardé avec succès.")

    def endNodesCreation(self):
        self.mode = "creating_edges"
        QMessageBox.information(self, "Mode Change", "Switching to edge creation mode.")
        self.find_menu_action(self.operationsMenu, "Fin création sommets").setDisabled(True)
        self.find_menu_action(self.operationsMenu, "Fin création arcs").setEnabled(True)

    def endEdgesCreation(self):
        self.mode = "none"
        QMessageBox.information(self, "Mode Change", "Edge creation completed.")
        self.operationsButton.setEnabled(False)
        self.algorithmsButton.setEnabled(True)
        self.sauvegarderButton.setEnabled(True)
        self.deleteNodeButton.setEnabled(True)
        self.find_menu_action(self.operationsMenu, "Fin création arcs").setDisabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Welsh-Powell").setEnabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Kruskal").setEnabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Prim").setEnabled(True)
        self.find_menu_action(self.algorithmsMenu, "Animer Dijkstra").setEnabled(True)

    def animateWelshPowell(self):
        animation_window = AnimationWindow(self.G, self.pos, algorithm="welsh_powell")
        self.animation_windows.append(animation_window)
        animation_window.show()
        self.stable_sets = self.get_stable_sets_from_colors(animation_window.color_map)
        self.find_menu_action(self.algorithmsMenu, "Trouver ensemble stable maximal").setEnabled(True)

    def animateKruskal(self):
        animation_window = AnimationWindow(self.G, self.pos, algorithm="kruskal")
        self.animation_windows.append(animation_window)
        animation_window.show()

    def animatePrim(self):
        start_node = list(self.G.nodes())[0]
        animation_window = AnimationWindow(self.G, self.pos, algorithm="prim", start_node=start_node)
        self.animation_windows.append(animation_window)
        animation_window.show()

    def animateDijkstra(self):
        animation_window = DijkstraWindow(self.G, self.pos)
        self.animation_windows.append(animation_window)
        animation_window.show()

    def get_stable_sets_from_colors(self, color_map):
        stable_sets = {}
        for node, color in color_map.items():
            if color not in stable_sets:
                stable_sets[color] = []
            stable_sets[color].append(node)
        return stable_sets

    def findStableSet(self):
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

    def enableDeleteNodeMode(self):
        self.mode = "deleting_nodes"
        self.deleteNodeButton.setDisabled(True)
        self.stopDeletionModeButton.setEnabled(True)
        self.operationsButton.setDisabled(True)
        self.algorithmsButton.setDisabled(True)
        self.sauvegarderButton.setDisabled(True)
        QMessageBox.information(self, "Mode Change", "Delete node mode activated. Click on a node to delete it.")

    def stopDeleteNodeMode(self):
        self.mode = "none"
        self.deleteNodeButton.setEnabled(True)
        self.stopDeletionModeButton.setDisabled(True)
        self.operationsButton.setEnabled(False)
        self.algorithmsButton.setEnabled(True)
        self.sauvegarderButton.setEnabled(False)
        QMessageBox.information(self, "Mode Change", "Delete node mode deactivated.")

    def on_click(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            if self.mode == "creating_nodes":
                addNode(self.G, self.pos, x, y, self.ax, self.canvas)
                self.sauvegarderButton.setEnabled(True)
            elif self.mode == "creating_edges":
                self.handle_edge_creation(x, y)
                self.sauvegarderButton.setEnabled(True)
            elif self.mode == "deleting_nodes":
                self.handle_node_deletion(x, y)
                self.sauvegarderButton.setEnabled(True)

    def handle_edge_creation(self, x, y):
        node_id = self.get_closest_node(x, y)
        if self.selected_node_for_edge_creation is None:
            self.selected_node_for_edge_creation = node_id
        else:
            if self.selected_node_for_edge_creation == node_id:
                weight, ok = QInputDialog.getInt(self, "Poids de la boucle", "Entrez le poids de la boucle:", min=1)
                if ok:
                    self.G.add_edge(node_id, node_id, weight=weight)
                    self.draw_loop(self.ax, self.pos, node_id, weight, self.canvas)
            else:
                weight, ok = QInputDialog.getInt(self, "Poids de l'arc", "Entrez le poids de l'arc:", min=1)
                if ok:
                    self.G.add_edge(self.selected_node_for_edge_creation, node_id, weight=weight)
                    draw_edge(self.ax, self.pos, self.selected_node_for_edge_creation, node_id, weight, self.canvas)
            self.selected_node_for_edge_creation = None

    def handle_node_deletion(self, x, y):
        node_id = self.get_closest_node(x, y)
        confirm = QMessageBox.question(self, "Confirm Deletion", f"Do you confirm you want to delete node {node_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.G.remove_node(node_id)
            del self.pos[node_id]
            redrawGraph(self.ax, self.G, self.pos, [], self.canvas)
            self.sauvegarderButton.setEnabled(True)

    def get_closest_node(self, x, y):
        return min(
            self.G.nodes, key=lambda n: np.hypot(self.pos[n][0] - x, self.pos[n][1] - y)
        )

    def draw_loop(self, ax, pos, node_id, weight, canvas):
        x, y = pos[node_id]
        loop_radius = 0.03
        loop = plt.Circle((x, y), loop_radius, color='black', fill=False)
        ax.add_patch(loop)
        ax.text(x + loop_radius, y + loop_radius, str(weight), color='red', fontsize=12, ha='center', va='center')
        canvas.draw()

    def redraw_graph(self):
        self.ax.clear()
        nx.draw(self.G, pos=self.pos, ax=self.ax, with_labels=True, node_color='lightblue', node_size=700, edge_color='gray')
        for (u, v, d) in self.G.edges(data=True):
            if u == v:
                x, y = self.pos[u]
                loop_radius = 0.03
                loop = plt.Circle((x, y), loop_radius, color='black', fill=False)
                self.ax.add_patch(loop)
                self.ax.text(x + loop_radius, y + loop_radius, str(d['weight']), color='red', fontsize=12, ha='center', va='center')
            else:
                self.ax.text((self.pos[u][0] + self.pos[v][0]) / 2, (self.pos[u][1] + self.pos[v][1]) / 2, str(d['weight']), color='red', fontsize=12, ha='center', va='center')
        self.canvas.draw()
