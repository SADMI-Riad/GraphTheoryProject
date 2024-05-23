from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QListWidget, QPushButton, QWidget
from PyQt5.QtCore import Qt
import pickle
import os

def load_user_data():
    if not os.path.exists("user_data.pkl"):
        return {}
    with open("user_data.pkl", "rb") as file:
        data = pickle.load(file)
        return data

def get_current_user():
    if os.path.exists("current_user.txt"):
        with open("current_user.txt", "r") as file:
            return file.read().strip()
    return None

class CollectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Collection")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #2c3e50; color: white;")

        widget = QWidget(self)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.graph_list = QListWidget(self)
        layout.addWidget(self.graph_list)

        self.load_button = QPushButton("Load Graph", self)
        self.load_button.clicked.connect(self.load_selected_graph)
        layout.addWidget(self.load_button)

        self.back_button = QPushButton("Back to Main Menu", self)
        self.back_button.clicked.connect(self.back_to_main_menu)
        layout.addWidget(self.back_button)

        self.load_graphs()

    def load_graphs(self):
        username = get_current_user()
        user_data = load_user_data()
        if username in user_data:
            graphs = user_data[username].get("graphs", {})
            for graph_name in graphs:
                self.graph_list.addItem(graph_name)

    def load_selected_graph(self):
        selected_items = self.graph_list.selectedItems()
        if selected_items:
            graph_name = selected_items[0].text()
            from gui import GraphDesigner
            self.graph_designer = GraphDesigner()
            self.graph_designer.load_graph(graph_name)
            self.graph_designer.show()
            self.close()

    def back_to_main_menu(self):
        from gui import MainMenu
        self.main_menu = MainMenu()
        self.main_menu.show()
        self.close()