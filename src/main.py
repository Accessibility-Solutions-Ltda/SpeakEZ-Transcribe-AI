from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon, QResizeEvent
from views.speakez_transcribe_ai import SpeakezTranscribeAI
from views.menu import Menu
import ctypes

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        #Titulo do aplicativo
        self.setWindowTitle('SpeakEZ Transcribe AI')

        #Icone do aplicativo
        self.setWindowIcon(QIcon('src/assets/icons/icon_ez-256x256.png'))

        #Menu
        self.menu = Menu()
        self.setCentralWidget(self.menu)

        #Tamanho da janela
        self.setGeometry(100, 100, 800, 600)

        # Tamanho mínimo da janela
        self.setMinimumSize(800, 600)

        #Exibir a janela
        self.show()
    
    def resizeEvent(self, event):
        # Define a largura máxima do menu
        new_width = event.size().width()
        max_width = 300
        self.menu.setMaximumWidth(min(new_width, max_width))

        super().resizeEvent(event)
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