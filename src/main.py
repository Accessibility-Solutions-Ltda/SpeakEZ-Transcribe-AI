from PyQt6.QtWidgets import QApplication
from views.speakez_transcribe_ai import SpeakezTranscribeAI

# Inicializa a aplicação
app = QApplication([])

# Cria a janela principal e chama a classe SpeakezTranscribeAI
window = SpeakezTranscribeAI()

# Executa a aplicação
app.exec()
