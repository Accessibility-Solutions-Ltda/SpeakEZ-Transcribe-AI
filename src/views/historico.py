from PyQt6.QtWidgets import QMainWindow, QLabel

class Historico(QMainWindow):
    """
    Classe que representa a janela de histórico.

    Essa classe herda da classe QMainWindow e é responsável por exibir o histórico de transcrições.

    Atributos:
        Nenhum atributo definido.

    Métodos:
        __init__(): Construtor da classe Historico.
    """
    def __init__(self):
        super().__init__()

        #Teste
        label = QLabel('Historico')
        label.setStyleSheet('font-size: 20px')
        self.setCentralWidget(label)