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
    return current_user

def set_current_user(username):
    global current_user
    current_user = username

mock_database = load_user_data()

class CollectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.graph_designer = None  # Initialize the GraphDesigner attribute
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Graph Collection")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2c3e50; color: white;")

        widget = QWidget(self)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        title = QLabel("Your Graphs Collection", self)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.graph_list = QListWidget(self)
        self.graph_list.setFont(QFont("Arial", 12))
        layout.addWidget(self.graph_list)

        load_button = QPushButton("Load Graph", self)
        load_button.setFont(QFont("Arial", 12))
        load_button.setStyleSheet("background-color: #3498db; color: white;")
        load_button.clicked.connect(self.load_graph)
        layout.addWidget(load_button)

        delete_button = QPushButton("Delete Graph", self)
        delete_button.setFont(QFont("Arial", 12))
        delete_button.setStyleSheet("background-color: #e74c3c; color: white;")
        delete_button.clicked.connect(self.delete_graph)
        layout.addWidget(delete_button)

        back_button = QPushButton("Back to Main Menu", self)
        back_button.setFont(QFont("Arial", 12))
        back_button.setStyleSheet("background-color: #95a5a6; color: white;")
        back_button.clicked.connect(self.back_to_main_menu)
        layout.addWidget(back_button)

        self.load_graph_list()

    def load_graph_list(self):
        username = get_current_user()
        print(f"Current user for loading graphs: {username}")  # Debug print
        user_data = load_user_data()
        if username in user_data:
            self.graph_list.clear()
            for graph_name in user_data[username]['graphs']:
                print(f"Found graph: {graph_name}")  # Debug print
                self.graph_list.addItem(graph_name)
        else:
            print("User not found in user data.")  # Debug print

    def load_graph(self):
        selected_graph = self.graph_list.currentItem()
        if selected_graph:
            graph_name = selected_graph.text()
            username = get_current_user()
            user_data = load_user_data()
            if username in user_data and graph_name in user_data[username]['graphs']:
                graph_data = user_data[username]['graphs'][graph_name]
                from gui import GraphDesigner  # Local import to avoid circular dependency
                self.graph_designer = GraphDesigner()
                self.graph_designer.G = graph_data['G']
                self.graph_designer.pos = graph_data['pos']
                self.graph_designer.redraw_graph()
                self.graph_designer.show()
                self.close()

    def delete_graph(self):
        selected_graph = self.graph_list.currentItem()
        if selected_graph:
            graph_name = selected_graph.text()
            confirm = QMessageBox.question(self, "Confirm Deletion", f"Do you confirm you want to delete the graph {graph_name}?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                username = get_current_user()
                user_data = load_user_data()
                if username in user_data and graph_name in user_data[username]['graphs']:
                    del user_data[username]['graphs'][graph_name]
                    save_user_data(user_data)
                    self.load_graph_list()

    def back_to_main_menu(self):
        from gui import MainMenu  # Local import to avoid circular dependency
        self.main_menu = MainMenu()
        self.main_menu.show()
        self.close()
