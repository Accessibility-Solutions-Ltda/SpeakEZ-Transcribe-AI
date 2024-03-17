from PyQt6.QtWidgets import QMainWindow, QLabel

class Introducao(QMainWindow):
    def __init__(self):
        super().__init__()

        #Teste
        label = QLabel('Introducao')
        label.setStyleSheet('font-size: 20px')
        self.setCentralWidget(label)