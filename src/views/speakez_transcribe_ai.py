from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QIcon, QPixmap

class SpeakezTranscribeAI(QMainWindow):
    def __init__(self):
        super().__init__()

        #Titulo do aplicativo
        self.setWindowTitle('SpeakEZ Transcribe AI')

        #Icone do aplicativo
        self.setWindowIcon(QIcon('src/assets/icons/icon_ez-256x256.png'))

        #Texto de boas-vindas (Para teste de layout)
        text = QLabel('Bem-vindo ao SpeakEZ Transcribe AI', self)
        text.move(50, 50)
        text.adjustSize()

        #Tamanho da janela
        self.setGeometry(100, 100, 800, 600)
        
        #Exibir a janela
        self.show()

# Inicializa a aplicação (Para teste)
app = QApplication([])
# Cria a janela principal e chama a classe SpeakezTranscribeAI
window = SpeakezTranscribeAI()
# Executa a aplicação
app.exec()