from PyQt6.QtWidgets import QTabWidget, QMainWindow, QLabel, QComboBox, QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout, QLineEdit, QPushButton, QSpacerItem
from PyQt6.QtCore import Qt
from services.config_service import ConfigService

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
        self.config_service = ConfigService()
        # Adicionado layout vertical
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        
        # Ajustando margens
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)

        # Adicionado titulo
        titulo = QLabel('Introdução')
        titulo.setStyleSheet('font-size: 40px; font-weight: bold; font: segoe ui; margin-top: 20px; margin-bottom: 20px;')
        layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignTop)
