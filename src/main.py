from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from views.introducao import Introducao
from views.menu import Menu
from views.speakez_transcribe_ai import SpeakezTranscribeAI
from views.historico import Historico
from views.settings import Settings
import ctypes
from views.speakez_transcribe_ai import SpeakezTranscribeAI
from views.historico import Historico
from views.settings import Settings

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        #Titulo do aplicativo
        self.setWindowTitle('SpeakEZ Transcribe AI')

        #Icone do aplicativo
        self.setWindowIcon(QIcon('src/assets/icons/icon_ez-256x256.png'))

        #Menu
        self.menu = Menu()
        self.menu.change_page_signal.connect(self.mudando_pagina)
        self.speakez_transcribe_ai = Introducao()

        #Layout
        layout = QHBoxLayout()
        layout.addWidget(self.menu)
        layout.addWidget(self.speakez_transcribe_ai)

        #Widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        #Ajustando margens
        layout.setContentsMargins(0, 0, 0, 0)

        #Tamanho da janela
        self.setGeometry(100, 100, 800, 600)

        # Tamanho mínimo da janela
        self.setMinimumSize(1024, 768)

        # Definir a largura máxima do menu
        self.menu.setMaximumWidth(300)

        #Exibir a janela
        self.show()
    
    def mudando_pagina(self, page):
        # Cria um novo layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.menu)

        if page == 'speakez_transcribe_ai':
            # Cria o novo widget SpeakezTranscribeAI
            self.speakez_transcribe_ai = SpeakezTranscribeAI()

            # Cria um novo layout
            layout.addWidget(self.speakez_transcribe_ai)
        
        elif page == "history":
            # Cria o novo widget Historico
            self.historico = Historico()

            # Ajustando margens
            layout.setContentsMargins(0, 0, 0, 0)

            layout.addWidget(self.historico)
        
        elif page == "settings":
            # Cria o novo widget Settings
            self.settings = Settings()

            # Cria um novo layout
            layout.addWidget(self.settings)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        

def main():
    # Altere icone do aplicativo no Windows
    speakez_id = 'AcessibilitySolutions.SpeakezTranscribeAI.0.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(speakez_id)

    # Inicializa a aplicação
    app = QApplication([])

    # Cria a janela principal e chama a classe Main
    window = Main()

    # Executa a aplicação
    app.exec()

if __name__ == "__main__":
    main()