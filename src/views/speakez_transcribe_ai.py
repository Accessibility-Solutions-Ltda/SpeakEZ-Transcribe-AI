# speakez_transcribe_ai.py
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QTextEdit, QWidget, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import QThread
from services.transcribe_service import TranscribeService

class AudioGravadorStream(QThread):
    """
    Classe responsável por gravar e transcrever áudio em streaming.

    Atributos:
        transcribe_service (TranscribeService): Instância do serviço de transcrição.
        running (bool): Indica se a gravação está em andamento.

    Métodos:
        run(): Inicia a gravação e transcrição em streaming.
        stop(): Para a gravação em streaming.
    """

    def __init__(self):
        super().__init__()
        self.transcribe_service = TranscribeService()
        self.running = False

    def run(self):
        #Inicia a gravação e transcrição em streaming.
        self.running = True
        self.transcribe_service.captando_audio_streaming(lambda: self.running)

    def stop(self):
        #Para a gravação em streaming.
        self.running = False
        
class SpeakezTranscribeAI(QMainWindow):
    def __init__(self):
        super().__init__()

        font_20px = 'font-size: 20px'

        # Cria uma instância do serviço de transcrição
        self.audio_gravador_stream = AudioGravadorStream()
        
        # Conecta o sinal de transcrição do serviço de transcrição ao método
        self.audio_gravador_stream.transcribe_service.transcripton_signal.connect(self.receber_transcricao)


        # Configura a interface do usuário
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Adiciona um título à janela
        label = QLabel('SpeakezTranscribeAI')

        # Define o estilo do título
        label.setStyleSheet(font_20px)

        # Adiciona o título ao layout
        layout.addWidget(label)

        # Adiciona um layout horizontal para o botão de ligar/desligar
        layout_transcription = QHBoxLayout()

        # Criando texto de transcrição
        self.transcription_titulo = QLabel('Transcrição:')
        self.transcription_titulo.setStyleSheet(font_20px)
        layout_transcription.addWidget(self.transcription_titulo)

        # Adiciona um botão de ligar/desligar
        self.switch_button = QPushButton('OFF')
        self.switch_button.setCheckable(True)
        self.switch_button.setStyleSheet('background-color: red; padding: 10px;' + font_20px)

        # Define a política de tamanho do botão
        self.switch_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Conecta o sinal clicked do botão ao método on_switch_button_clicked
        self.switch_button.clicked.connect(self.on_switch_button_clicked)

        # Adiciona o botão ao layout horizontal
        layout_transcription.addWidget(self.switch_button)


        # Adiciona o layout horizontal ao layout principal
        layout.addLayout(layout_transcription)

        # Adiciona um campo de texto
        self.transcription_box = QTextEdit()
        self.transcription_box.setReadOnly(True)
        self.transcription_box.setStyleSheet(font_20px)
        layout.addWidget(self.transcription_box)

        # Define o widget central
        self.setCentralWidget(central_widget)

    def on_switch_button_clicked(self):
        """
        Função chamada quando o botão de alternância é clicado.

        Verifica se o botão está marcado ou desmarcado e realiza as ações correspondentes.
        Se o botão estiver marcado, altera o texto para 'ON', define o estilo do botão como verde e inicia a gravação de áudio.
        Se o botão estiver desmarcado, altera o texto para 'OFF', define o estilo do botão como vermelho e para a gravação de áudio.
        """
        if self.switch_button.isChecked():
            self.switch_button.setText('ON')
            self.switch_button.setStyleSheet('background-color: green; font-size: 30px; padding: 10px')

            # Inicia a gravação de áudio
            self.audio_gravador_stream.start()
        else:
            self.switch_button.setText('OFF')
            self.switch_button.setStyleSheet('background-color: red; font-size: 30px; padding: 10px')

            # Para a gravação de áudio
            self.audio_gravador_stream.stop()

    def receber_transcricao(self, transcription):
        """
        Adiciona a transcrição recebida à caixa de transcrição existente.

        Args:
            transcription (str): A transcrição a ser adicionada.

        Returns:
            None
        """
        texto_atual = self.transcription_box.toPlainText()
        self.transcription_box.setPlainText(f"{texto_atual}\n{transcription}")
