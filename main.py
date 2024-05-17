import sys
from PyQt5.QtWidgets import QApplication
from gui import LoginPage

def main():
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()