from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QIcon

class Introducao(QMainWindow):
    def __init__(self):
        super().__init__()

        #Teste
        label = QLabel('Introducao')
        self.setCentralWidget(label)