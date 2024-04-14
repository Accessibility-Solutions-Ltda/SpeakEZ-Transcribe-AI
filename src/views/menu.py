from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal, QSize
import qtawesome as qta

# Defina constantes para os nomes das páginas
SPEAKEZ_PAGE = 'speakez_transcribe_ai'
HISTORY_PAGE = 'history'
SETTINGS_PAGE = 'settings'
INTRODUCAO_PAGE = 'introducao'

class HoverButton(QPushButton):
    def __init__(self, *args, type_icon, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_icon = qta.icon(type_icon, color='black')
        self.hover_icon = qta.icon(type_icon, color='white')
        self.setIcon(self.default_icon)
        self.setIconSize(QSize(18, 18))

    def enterEvent(self, event):
        super().enterEvent(event)
        self.setIcon(self.hover_icon)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.setIcon(self.default_icon)

class Menu(QWidget):
    """
    Classe que representa o menu da aplicação.

    O menu contém uma imagem, um título e botões para navegação.

    Atributos:
    - change_page_signal (pyqtSignal): Sinal emitido quando um botão é clicado para mudar de página.

    Métodos:
    - __init__(): Construtor da classe Menu.
    - cria_botao(texto, page, icon_type): Cria um botão para a navegação no menu.
    """
    change_page_signal = pyqtSignal(str)
    
    def __init__(self):
        """
        Construtor da classe Menu.

        Inicializa o menu com uma cor de fundo, uma imagem, um título e botões de navegação.
        """
        super().__init__()

        # Define a cor de fundo do menu
        color_background = "background-color: #B4CBD9"
        self.setStyleSheet(color_background)

        # Cria um QVBoxLayout
        layout = QVBoxLayout()

        # Define as margens e espaçamento do layout
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Cria um QHBoxLayout para o widget da imagem
        h_layout = QHBoxLayout()
        layout.addLayout(h_layout)

        # Cria um QLabel para a imagem
        image_label = QLabel()

        # Carrega a imagem
        pixmap = QPixmap(r'src\assets\icons\256x256.png')

        # Ajustando o tamanho da imagem
        pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Define o pixmap do QLabel para a imagem
        image_label.setPixmap(pixmap)

        image_label.setStyleSheet("padding: 118")
        h_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter) 


        # Titulo de menu
        titulo_menu = QLabel('Menu')
        titulo_menu.setStyleSheet("border-style: none; padding: 10; text-align: left; font-size: 30px; font-weight: bold; font-style: italic;")
        layout.addWidget(titulo_menu, alignment=Qt.AlignmentFlag.AlignTop)
        
        # Cria um novo QWidgets para os botões
        button_widget = QWidget()
        button_widget.setStyleSheet(color_background)

        # Cria um layout vertical para o widget dos botões
        button_layout = QVBoxLayout(button_widget)

        # Adiciona botões ao layout
        button_home = self.cria_botao('Página Inicial', SPEAKEZ_PAGE, 'fa5s.home')
        button_layout.addWidget(button_home, alignment=Qt.AlignmentFlag.AlignTop)

        button_history = self.cria_botao('Histórico', HISTORY_PAGE, 'fa5s.history')
        button_layout.addWidget(button_history, alignment=Qt.AlignmentFlag.AlignTop)

        button_settings = self.cria_botao('Configurações', SETTINGS_PAGE, 'fa5s.cog')
        button_layout.addWidget(button_settings, alignment=Qt.AlignmentFlag.AlignTop)

        button_help = self.cria_botao('Ajuda', INTRODUCAO_PAGE, 'fa5s.question')
        button_layout.addWidget(button_help, alignment=Qt.AlignmentFlag.AlignTop)

        # Adiciona o layout dos botões ao widget
        layout.addWidget(button_widget, alignment=Qt.AlignmentFlag.AlignTop)

        # Adiciona um espaçador no final do layout
        spacer = QWidget()
        spacer.setStyleSheet(color_background)
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(spacer)

        # Define o layout do widget
        self.setLayout(layout)
    
    def cria_botao(self, texto, page, icon_type):
        """
        Cria um botão para a navegação no menu.

        Parâmetros:
        - texto (str): Texto exibido no botão.
        - page (str): Página para a qual o botão irá navegar.
        - icon_type (str): Tipo de ícone a ser exibido no botão.

        Retorna:
        - button (HoverButton): Botão de navegação criado.
        """
        button = HoverButton(texto, type_icon=icon_type)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        css_style = "QPushButton { border: none; border-style: none; padding: 10; text-align: left; font-size: 18px; border-radius: 10px;}"\
                "QPushButton:hover { background-color: #4d608c; color: white; font-weight: bold;}"
        button.setStyleSheet(css_style)

        # Conecta o sinal clicked do botão ao método mudar_pagina
        # Muda a página para a página especificada
        button.clicked.connect(lambda: self.change_page_signal.emit(page))
        return button
