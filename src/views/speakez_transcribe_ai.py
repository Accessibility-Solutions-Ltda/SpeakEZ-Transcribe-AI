from PyQt6.QtWidgets import QMainWindow, QLabel

class SpeakezTranscribeAI(QMainWindow):
    """
    Classe responsável por representar a janela principal do aplicativo SpeakEZ Transcribe AI.

    Args:
        None

    Attributes:
        None

    Methods:
        __init__(): Construtor da classe.

    """

    def __init__(self):
        super().__init__()

        # Teste
        label = QLabel('SpeakezTranscribeAI')
        label.setStyleSheet('font-size: 20px')
        self.setCentralWidget(label)