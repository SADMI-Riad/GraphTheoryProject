import sys
from PyQt5.QtWidgets import QApplication
from gui import MainMenu

def main():
    app = QApplication(sys.argv)
    main_menu = MainMenu()
    main_menu.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()