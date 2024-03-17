from PyQt6.QtWidgets import QMainWindow, QLabel

class Settings(QMainWindow):
    """
    Classe que representa a janela de configurações.

    Esta classe herda da classe QMainWindow e é responsável por exibir a janela de configurações
    do aplicativo SpeakEZ-Transcribe-AI.

    Atributos:
        Nenhum.

    Métodos:
        __init__(): Inicializa a janela de configurações.
    """
    def __init__(self):
        super().__init__()

        #Teste
        label = QLabel('Configurações')
        label.setStyleSheet('font-size: 20px')
        self.setCentralWidget(label)