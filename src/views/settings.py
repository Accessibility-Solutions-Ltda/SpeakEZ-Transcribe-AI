from PyQt6.QtWidgets import QMainWindow, QLabel

class Settings(QMainWindow):
    def __init__(self):
        super().__init__()

        #Teste
        label = QLabel('Configurações')
        label.setStyleSheet('font-size: 20px')
        self.setCentralWidget(label)