from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QApplication, QLabel, QHBoxLayout
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class Menu(QWidget):
    def __init__(self):
        
        super().__init__()

        # Define a cor de fundo do menu
        self.setStyleSheet("background-color: #B4CBD9")

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

        # Adiciona o QLabel ao layout
        h_layout.addWidget(image_label)

        # Adiciona outro espaçador no final do layout
        h_layout.addStretch()

        # Define o layout do widget
        image_widget.setLayout(h_layout)

        # Adiciona o widget ao layout principal
        layout.addWidget(image_widget)

        #Titulo de menu
        title = QLabel('Menu', self)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Adiciona botões ao layout
        button_home = QPushButton('Página Inicial')
        layout.addWidget(button_home)

        button_history = QPushButton('Histórico')
        layout.addWidget(button_history)

        button_settings = QPushButton('Configurações')
        layout.addWidget(button_settings)

        # Define o layout do widget
        self.setLayout(layout)