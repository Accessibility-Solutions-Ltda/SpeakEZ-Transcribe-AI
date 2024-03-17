from PyQt6.QtWidgets import QMainWindow, QLabel

class Introducao(QMainWindow):
    """
    Classe responsável por exibir a introdução do programa.

    Esta classe herda da classe QMainWindow e é utilizada para criar uma janela
    principal que exibe a introdução do programa SpeakEZ-Transcribe-AI.

    Atributos:
        Nenhum atributo definido.

    Métodos:
        __init__(): Construtor da classe Introducao.
    """
    def __init__(self):
        super().__init__()

        #Teste
        label = QLabel('Introducao')
        label.setStyleSheet('font-size: 20px')
        self.setCentralWidget(label)