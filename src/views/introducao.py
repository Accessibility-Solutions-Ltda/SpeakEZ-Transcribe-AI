from PyQt6.QtWidgets import QTabWidget, QMainWindow, QLabel, QComboBox, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
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
        self.config = self.config_service.lendo_configuracoes()
        self.font_padrao = self.config['font_size']
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

        # Adicionado texto de introdução
        introducao = QLabel('Bem-vindo ao SpeakEZ Transcribe AI!')
        introducao.setStyleSheet(f'font-size: {self.font_padrao + 2}px; margin-bottom: 20px;margin-left: 20px;')
        layout.addWidget(introducao, alignment=Qt.AlignmentFlag.AlignTop)

        # Adicionado imagem de icone
        imagem = QLabel()
        imagem.setPixmap(QPixmap(r'src\assets\icons\256x256.png').scaled(96, 96, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        layout.addWidget(imagem, alignment=Qt.AlignmentFlag.AlignCenter)

        # Adicionado texto de introdução

        introducao = QLabel("""Bem-vindo ao SpeakEZ Transcribe AI, uma poderosa ferramenta desenvolvida pelos talentosos estudantes da UFABC: Arthur Osakawa, Gabriel Hagui, Gabriel Rameh, Fernanda Simone e Renan Henrique. Este aplicativo foi cuidadosamente projetado para atender às necessidades das pessoas com deficiências auditivas, mas também é ideal para qualquer pessoa que busque uma transcrição e conversão de áudio de alta qualidade em suas reuniões online.
Com o SpeakEZ, você tem acesso a um conjunto completo de ferramentas essenciais para aprimorar suas reuniões virtuais. A precisão da transcrição é garantida pelo nosso corretor inteligente baseado na tecnologia GPT da OpenAI, que utiliza termos específicos de forma precisa, eliminando os erros comuns em outras soluções. Você também pode inserir manualmente termos específicos para uma transcrição ainda mais precisa.
Além da transcrição, o SpeakEZ oferece uma conversão de texto em áudio inteligente, produzindo uma voz natural e humanizada. Para agilizar ainda mais suas interações, nosso aplicativo conta com um corretor inteligente para facilitar a digitação.
Não se preocupe em perder informações importantes. O histórico do SpeakEZ registra todas as transcrições, gerando automaticamente anotações e tarefas para melhorar a organização e compreensão. Além disso, você pode acessar facilmente o histórico de conversões para revisitar transcrições anteriores.
Experimente o SpeakEZ Transcribe AI hoje e transforme a maneira como você realiza suas reuniões online!""")
        introducao.setWordWrap(True)
        
        introducao.setStyleSheet(f'font-size: {self.font_padrao + 2}px; margin-bottom: 20px;margin-left: 20px;margin-top: 20px;')
        layout.addWidget(introducao, alignment=Qt.AlignmentFlag.AlignTop)
        
        # Adicionado texto de introdução
        introducao = QLabel('Para começar, selecione uma das opções no menu à esquerda.')
        introducao.setStyleSheet(f'font-size: {self.font_padrao + 2}px; margin-bottom: 20px;margin-left: 20px;')
        layout.addWidget(introducao, alignment=Qt.AlignmentFlag.AlignTop)


