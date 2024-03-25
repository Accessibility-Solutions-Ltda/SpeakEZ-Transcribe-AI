# speakez_transcribe_ai.py
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QTextEdit, QWidget, QHBoxLayout, QSizePolicy, QProgressBar
from PyQt6.QtCore import QThread, QSize
from services.transcribe_service import TranscribeService
import qtawesome as qta

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

        layout_label = QVBoxLayout()
        layout_label.setContentsMargins(10, 10, 10, 10)

        # Adiciona um título à janela
        label = QLabel('SpeakezTranscribeAI')
        

        # Define o estilo do título
        label.setStyleSheet("font-size: 30px; font-weight: bold; color: #4d608c; margin-top: 20px; margin-bottom: 20px;")

        # Adiciona o título ao layout
        layout.addWidget(label)


        # Adiciona um layout horizontal para o botão de ligar/desligar
        layout_transcription = QHBoxLayout()

        # Criando texto de transcrição
        self.transcription_titulo = QLabel('Transcrição')
        self.transcription_titulo.setStyleSheet(font_20px)
        layout_transcription.addWidget(self.transcription_titulo)

        # Adiciona um botão de ligar/desligar
        self.switch_button = QPushButton('Desligado')
        self.switch_button.setCheckable(True)
        self.switch_button.setStyleSheet('background-color: white; padding: 10px; border: 2px solid #4d608c; border-radius: 10px; ' + font_20px)
        self.switch_button.setFixedWidth(125)

        # Define a política de tamanho do botão
        self.switch_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Conecta o sinal clicked do botão ao método on_switch_button_clicked
        self.switch_button.clicked.connect(self.on_switch_button_clicked)

        # Adiciona o botão ao layout horizontal
        layout_transcription.addWidget(self.switch_button)


        # Adiciona o layout horizontal ao layout principal
        layout_label.addLayout(layout_transcription)

        # Adiciona um campo de texto
        self.transcription_box = QTextEdit()
        self.transcription_box.setReadOnly(True)
        self.transcription_box.setStyleSheet(font_20px + "; border: 2px solid #4d608c; border-radius: 10px; background-color: palette(base);")
        layout_label.addWidget(self.transcription_box)

        # Define o widget central
        self.setCentralWidget(central_widget)

        # Titulo de conversão
        self.transcription_titulo = QLabel('Convertendo em áudio')
        self.transcription_titulo.setStyleSheet(font_20px)
        layout_label.addWidget(self.transcription_titulo)

        #Criando layout horizontal para a conversão de texto em áudio
        layout_conversion = QHBoxLayout()


        # Adicionando uma barra de progresso
        self.conversion_progress = QProgressBar()
        self.conversion_progress.setStyleSheet("""
    QProgressBar {
        border: 1px solid #4d608c;                              
        border-radius: 5px;
        text-align: center;
        background-color: #f0f0f0;
    }

    QProgressBar::chunk {
        background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0.5, y2:0, stop:0 #f0f0f0, stop:1 #4d608c); 
    }
""")
        self.conversion_progress.setFixedHeight(10)
        self.conversion_progress.setRange(0,0)
        layout_label.addWidget(self.conversion_progress)

        # Adicionando um campo de texto como entrada
        self.conversion_text = QTextEdit()
        self.conversion_text.setPlaceholderText('Digite o texto aqui...')
        self.conversion_text.setStyleSheet(font_20px + "; border: 2px solid #4d608c; border-radius: 10px; background-color: palette(base);")
        layout_conversion.addWidget(self.conversion_text)

        #Criando layout vertical para os botões
        layout_buttons = QVBoxLayout()

        # Adicionando um botão para corrigir texto
        icon_magic = qta.icon('fa5s.magic', color='white')
        self.correct_button = QPushButton('Corrigir')
        self.correct_button.setIcon(icon_magic)
        self.correct_button.setIconSize(QSize(18, 18))
        self.correct_button.setStyleSheet('background-color: #4d608c; color: white; padding: 10px; border: none; border-style: none;border-radius: 10px;' + font_20px)
        self.correct_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.correct_button.setFixedWidth(125)  # Definindo uma largura fixa
        layout_buttons.addWidget(self.correct_button)

        # Adicionando um botão para converter texto em áudio

        # Adicionando um iconé ao botão
        icon_play = qta.icon('fa5s.play', color='white')
        self.convert_button = QPushButton(icon_play, 'Converter')
        self.convert_button.setIcon(icon_play)
        self.convert_button.setIconSize(QSize(18, 18))
        self.convert_button.setStyleSheet('background-color: #4d608c; color: white; padding: 10px; border: none; border-style: none;border-radius: 10px;' + font_20px)
        self.convert_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.convert_button.setFixedWidth(125)  # Definindo uma largura fixa
        layout_buttons.addWidget(self.convert_button)

        layout_conversion.addLayout(layout_buttons)
        layout_label.addLayout(layout_conversion)

        # Adiciona o layout ao layout principal
        layout.addLayout(layout_label)

    def on_switch_button_clicked(self):
        """
        Função chamada quando o botão de alternância é clicado.

        Verifica se o botão está marcado ou desmarcado e realiza as ações correspondentes.
        Se o botão estiver marcado, altera o texto para 'ON', define o estilo do botão como verde e inicia a gravação de áudio.
        Se o botão estiver desmarcado, altera o texto para 'OFF', define o estilo do botão como vermelho e para a gravação de áudio.
        """
        if self.switch_button.isChecked():
            self.switch_button.setText('Ligado')
            self.switch_button.setStyleSheet('background-color: #4d608c; font-size: 20px; padding: 10px; border: 2px solid white; border-radius: 10px; color: white;')

            # Inicia a gravação de áudio
            #self.audio_gravador_stream.start()
        else:
            self.switch_button.setText('Desligado')
            self.switch_button.setStyleSheet('background-color: white; padding: 10px; border: 2px solid #4d608c; border-radius: 10px; font-size: 20px')

            # Para a gravação de áudio
            #self.audio_gravador_stream.stop()

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
