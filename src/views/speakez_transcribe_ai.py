from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QIcon

class SpeakezTranscribeAI(QMainWindow):
    def __init__(self):
        super().__init__()

        #Teste
        label = QLabel('SpeakezTranscribeAI')
        label.setStyleSheet('font-size: 20px')
        self.setCentralWidget(label)