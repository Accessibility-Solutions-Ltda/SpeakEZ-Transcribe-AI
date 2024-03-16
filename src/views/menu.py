from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QApplication, QLabel, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
import qtawesome as qta

from PyQt6.QtWidgets import QSpacerItem, QSizePolicy

class HoverButton(QPushButton):
    def __init__(self, *args, type_icon, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_icon = qta.icon(type_icon, color='black')
        self.hover_icon = qta.icon(type_icon, color='white')
        self.setIcon(self.default_icon)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.setIcon(self.hover_icon)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.setIcon(self.default_icon)

class Menu(QWidget):
    def __init__(self):
        
        super().__init__()

        # Define a cor de fundo do menu
        color_background = "background-color: #B4CBD9"
        self.setStyleSheet(color_background)

        # Cria um QVBoxLayout
        layout = QVBoxLayout()

        # Define as margens e espaçamento do layout
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Cria um widget para a imagem
        image_widget = QWidget()

        # Cria um QHBoxLayout para o widget da imagem
        h_layout = QHBoxLayout(image_widget)

        # Adiciona um espaçador no início do layout
        h_layout.addStretch()

        # Cria um QLabel para a imagem
        image_label = QLabel()

        # Carrega a imagem
        pixmap = QPixmap('src/assets/icons/icon_ez-256x256.png')

        #Ajustando o tamanho da imagem
        pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Define o pixmap do QLabel para a imagem
        image_label.setPixmap(pixmap)

        image_label.setStyleSheet("padding: 100")

        # Adiciona o QLabel ao layout
        h_layout.addWidget(image_label)

        # Adiciona outro espaçador no final do layout
        h_layout.addStretch()

        # Define o layout do widget
        image_widget.setLayout(h_layout)

        # Adiciona o widget ao layout principal
        layout.addWidget(image_widget, alignment=Qt.AlignmentFlag.AlignTop)

        # Titulo de menu
        titulo_menu = QLabel('Menu')
        titulo_menu.setStyleSheet("border-style: none; padding: 10; text-align: left; font-size: 30px; font-weight: bold; font-style: italic;")
        layout.addWidget(titulo_menu, alignment=Qt.AlignmentFlag.AlignTop)

        CSS_STYLE = "QPushButton { border: none; border-style: none; padding: 10; text-align: left; font-size: 18px; border-radius: 10px;}"\
                "QPushButton:hover { background-color: #4d608c; color: white; font-weight: bold;}"
        
        #Cria um novo QWidgets para os botões
        button_widget = QWidget()
        button_widget.setStyleSheet(color_background)

        # Cria um layout vertical para o widget dos botões
        button_layout = QVBoxLayout(button_widget)



        # Adiciona botões ao layout
        button_home = HoverButton('Página Inicial', type_icon='fa5s.home')
        button_home.setCursor(Qt.CursorShape.PointingHandCursor)  # Define o cursor para a mãozinha
        button_home.setStyleSheet(CSS_STYLE)  # Define a cor de fundo quando o cursor passa acima
        
        button_layout.addWidget(button_home, alignment=Qt.AlignmentFlag.AlignTop)

        button_history = HoverButton('Histórico', type_icon='fa5s.history')
        button_history.setCursor(Qt.CursorShape.PointingHandCursor)  # Define o cursor para a mãozinha
        button_history.setStyleSheet(CSS_STYLE)  # Define a cor de fundo quando o cursor passa acima
        button_layout.addWidget(button_history, alignment=Qt.AlignmentFlag.AlignTop)

        button_settings = HoverButton('Configurações', type_icon='fa5s.cog')
        button_settings.setCursor(Qt.CursorShape.PointingHandCursor)  # Define o cursor para a mãozinha
        button_settings.setStyleSheet(CSS_STYLE)  # Define a cor de fundo quando o cursor passa acima
        button_layout.addWidget(button_settings, alignment=Qt.AlignmentFlag.AlignTop)

        # Adiciona o layout dos botões ao widget
        layout.addWidget(button_widget, alignment=Qt.AlignmentFlag.AlignTop)

        # Adiciona um espaçador no final do layout
        spacer = QWidget()
        spacer.setStyleSheet(color_background)
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(spacer)

        # Define o layout do widget
        self.setLayout(layout)