from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QWidget,
    QMessageBox,
)
import pickle
import os

from gui import save_user_data


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

        self.load_button = QPushButton("Charger le graphe", self)
        self.load_button.clicked.connect(self.load_selected_graph)
        layout.addWidget(self.load_button)

        self.back_button = QPushButton("retour au Main Menu", self)
        self.back_button.clicked.connect(self.back_to_main_menu)
        layout.addWidget(self.back_button)

        self.delete_button = QPushButton("Supprimer graphe", self)
        self.delete_button.clicked.connect(self.delete_selected_graph)
        layout.addWidget(self.delete_button)

        self.load_graphs()

    def load_graphs(self):
        self.graph_list.clear()  # Nettoyer la liste avant de la remplir
        username = get_current_user()
        user_data = load_user_data()
        if username in user_data:
            graphs = user_data[username].get("graphs", {})
            if graphs:
                for graph_name in graphs:
                    self.graph_list.addItem(graph_name)
            else:
                # S'il n'y a pas de graphes à charger, informer l'utilisateur
                QMessageBox.information(self, "Pas de graphes", "Vous n'avez aucun graphe enregistrer !")
                self.back_to_main_menu()

    def load_selected_graph(self):
        selected_items = self.graph_list.selectedItems()
        if selected_items:
            graph_name = selected_items[0].text()
            from gui import GraphDesigner

            self.graph_designer = GraphDesigner()
            self.graph_designer.load_graph(graph_name)
            self.graph_designer.reset_buttons_states()
            self.graph_designer.show()
            self.close()

    def back_to_main_menu(self):
        from gui import MainMenu

        self.main_menu = MainMenu()
        self.main_menu.show()
        self.close()

    def delete_selected_graph(self):
        selected_items = self.graph_list.selectedItems()
        if selected_items:
            graph_name = selected_items[0].text()
            confirm = QMessageBox.question(
                self,
                "Confirmer la supression",
                f"Etes vous sur de suprimer le graphe : '{graph_name}'?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if confirm == QMessageBox.Yes:
                username = get_current_user()
                user_data = load_user_data()
                if username in user_data:
                    # Supprime le graphe de la liste des graphes de l'utilisateur
                    del user_data[username]["graphs"][graph_name]
                    save_user_data(user_data)
                    self.load_graphs()  # Mettre à jour la liste des graphes après suppression

                    # Si la liste des graphes est vide après suppression, retour au menu principal
                    if not user_data[username]["graphs"]:
                        QMessageBox.information(
                            self,
                            "Collection vide",
                            "Aucun graphe restant dans votre collection. Retour au menu principal.",
                        )
                        self.back_to_main_menu()
