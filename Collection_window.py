# collection_window.py
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QListWidget, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from gui import GraphDesigner
from gui import get_current_user, save_user_data, load_user_data

class CollectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Graph Collection")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #2c3e50; color: white;")

        widget = QWidget(self)
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        title = QLabel("Your Graph Collection", self)
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

        self.load_graph_list()

    def load_graph_list(self):
        self.graph_list.clear()
        username = get_current_user()
        user_data = load_user_data()
        if username in user_data:
            for graph_name in user_data[username]['graphs']:
                self.graph_list.addItem(graph_name)

    def load_graph(self):
        selected_graph = self.graph_list.currentItem().text()
        username = get_current_user()
        user_data = load_user_data()
        if selected_graph and username in user_data:
            graph_data = user_data[username]['graphs'][selected_graph]
            graph_designer = GraphDesigner()
            graph_designer.G = graph_data['G']
            graph_designer.pos = graph_data['pos']
            graph_designer.redraw_graph()
            graph_designer.show()
            self.close()

    def delete_graph(self):
        selected_graph = self.graph_list.currentItem().text()
        username = get_current_user()
        user_data = load_user_data()
        if selected_graph and username in user_data:
            del user_data[username]['graphs'][selected_graph]
            save_user_data(user_data)
            self.load_graph_list()
            QMessageBox.information(self, "Success", "Graph deleted successfully.")
