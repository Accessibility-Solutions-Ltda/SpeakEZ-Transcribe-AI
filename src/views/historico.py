from PyQt6.QtWidgets import QMainWindow, QLabel

class Historico(QMainWindow):
    def __init__(self):
        super().__init__()

        #Teste
        label = QLabel('Historico')
        label.setStyleSheet('font-size: 20px')
        self.setCentralWidget(label)