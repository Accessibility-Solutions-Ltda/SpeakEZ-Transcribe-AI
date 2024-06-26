from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QTextEdit, QWidget, QHBoxLayout, QSizePolicy, QProgressBar, QStackedWidget, QMessageBox
from PyQt6.QtCore import QThread, QSize, Qt
from PyQt6.QtGui import QTextCursor
from services.conversion_service import ConvertendoTextoEmAudio
from services.transcribe_service import TranscribeService
from services.config_service import ConfigService
from services.corrigindo_texto import CorrigindoTexto
import qtawesome as qta
import re


COLOR_PRIMARY = '#4d608c'
COLOR_SECONDARY = '#b4cbd9'
COLOR_TERTIARY = 'white'


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

        # Inicializa o serviço de configuração
        self.config = ConfigService().lendo_configuracoes()
        self.key = self.config['openai_api_key']
        self.font_size = self.config['font_size']
        self.font_size_constant = f'font-size: {str(self.font_size)}px;'

        # Cria uma instância do serviço de transcrição
        self.audio_gravador_stream = AudioGravadorStream()
        # Conecta o sinal de transcrição do serviço de transcrição ao método
        self.audio_gravador_stream.transcribe_service.transcripton_signal.connect(self.receber_transcricao)

        # Configura a interface do usuário
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        # Define o widget central
        self.setCentralWidget(central_widget)

        # Adiciona um título à janela
        label = QLabel('Página Inicial')
        # Define o estilo do título
        label.setStyleSheet("font-size: 36px; font-weight: bold; font: Segoe UI; color: {}; margin-top: 20px; margin-bottom: 20px;".format('black'))
        # Adiciona o título ao layout
        layout.addWidget(label)

        # Adiciona um layout vertical para todos os elementos da interface do usuário exceto titulo.
        layout_label = QVBoxLayout()
        layout_label.setContentsMargins(10, 10, 10, 10)

        # Chamando a função de interface da area de transcrição
        self.interface_transcricao(layout_label)


        # Chamando a função de interface de conversão de texto em áudio
        self.interface_conversao_texto_audio(layout_label)

        # Adiciona o layout ao layout principal
        layout.addLayout(layout_label)
    
    def interface_transcricao(self, layout_label):
        # Adiciona um layout horizontal para o botão de ligar/desligar e titulo de transcrição
        layout_transcription = QHBoxLayout()

        # Criando texto de transcrição
        self.transcription_titulo = QLabel('Transcrição')
        self.transcription_titulo.setStyleSheet(f"font-size: {self.font_size}px; font: Segoe UI;")
        layout_transcription.addWidget(self.transcription_titulo)

        # Adiciona um botão de ligar/desligar
        self.switch_button = QPushButton('Desligado')
        self.switch_button.setCheckable(True)
        self.switch_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.switch_button.setStyleSheet('background-color: {}; padding: 10px; border: 2px solid {}; border-radius: 10px; {};'.format(COLOR_SECONDARY, COLOR_PRIMARY, self.font_size_constant))
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
        self.transcription_box.setStyleSheet("border: 2px solid {}; border-radius: 10px; background-color: palette(base); {}".format(COLOR_PRIMARY, self.font_size_constant))
        layout_label.addWidget(self.transcription_box)
    
    def interface_conversao_texto_audio(self, layout_label):
        # Titulo de conversão
        self.transcription_titulo = QLabel('Conversão para áudio')
        self.transcription_titulo.setStyleSheet(f"font-size: {self.font_size}px; margin-top: 50px; font: Segoe UI; margin-bottom: 0px; ")
        layout_label.addWidget(self.transcription_titulo)

        #Criando layout horizontal para a conversão de texto em áudio
        layout_conversion = QHBoxLayout()
        
        # Adicionando um widget empilhado para ocultar a barra de progresso
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Chamando a função de interface da barra de progresso
        self.interface_barra_progresso(layout_label)

        # Adicionando um campo de texto como entrada
        self.conversion_text = QTextEdit()
        self.conversion_text.setPlaceholderText('Digite o texto aqui...')
        self.conversion_text.setStyleSheet("border: 2px solid {}; border-radius: 10px; background-color: palette(base); {}".format(COLOR_PRIMARY, self.font_size_constant))
        layout_conversion.addWidget(self.conversion_text)

        #Criando layout vertical para os botões
        layout_buttons = QVBoxLayout()
        # Adicionando um botão para corrigir texto
        self.correct_button = self.criando_botoes_conversion('Corrigir', 'fa5s.magic', 'white')
        self.correct_button.clicked.connect(self.corrigir_texto)
        layout_buttons.addWidget(self.correct_button)
        # Adicionando um botão para converter texto em áudio
        # Adicionando um iconé ao botão
        self.convert_button = self.criando_botoes_conversion('Converter', 'fa5s.play', 'white')
        self.convert_button.clicked.connect(self.converter_texto_em_audio)


        layout_buttons.addWidget(self.convert_button)
        # Adicionando um layout de botões ao layout de conversão
        layout_conversion.addLayout(layout_buttons)
        layout_label.addLayout(layout_conversion)
    
    def interface_barra_progresso(self, layout_label):
        # Adicionando uma barra de progresso
        self.conversion_progress = QProgressBar()
        self.conversion_progress.setStyleSheet("""
            QProgressBar {{
                border: 1px solid {};                              
                border-radius: 5px;
                text-align: center;
                background-color: #f0f0f0;
                margin-bottom: 0px;
            }}

            QProgressBar::chunk {{
                background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0.5, y2:0, stop:0 #f0f0f0, stop:1 {});
            }}
        """.format(COLOR_PRIMARY, COLOR_PRIMARY))
        self.conversion_progress.setFixedHeight(10)
        self.conversion_progress.setRange(0,0)

        # Adiciona um widget vazio ao QStackedWidget
        self.vazio_widget = QWidget()
        self.stacked_widget.addWidget(self.vazio_widget)

        self.stacked_widget.addWidget(self.conversion_progress)

        # Adiciona o QStackedWidget ao layout
        layout_label.addWidget(self.stacked_widget)
    
    def criando_botoes_conversion(self, text, icon_name, color, fixed_width=125):
        icon = qta.icon(icon_name, color=color)
        button = QPushButton(icon, text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setIcon(icon)
        button.setIconSize(QSize(18, 18))
        button.setStyleSheet('background-color: {}; color: {}; padding: 10px; border: none; border-style: none;border-radius: 10px;{}'.format(COLOR_PRIMARY, COLOR_TERTIARY, self.font_size_constant))
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        button.setFixedWidth(fixed_width)
        return button

    def on_switch_button_clicked(self):
        """
        Função chamada quando o botão de alternância é clicado.

        Verifica se o botão está marcado ou desmarcado e realiza as ações correspondentes.
        Se o botão estiver marcado, altera o texto para 'ON', define o estilo do botão como verde e inicia a gravação de áudio.
        Se o botão estiver desmarcado, altera o texto para 'OFF', define o estilo do botão como vermelho e para a gravação de áudio.
        """
        if self.switch_button.isChecked():
            self.switch_button.setText('Ligado')
            self.switch_button.setStyleSheet('background-color: {}; padding: 10px; border: 2px solid {}; border-radius: 10px; color: {}; {}'.format(COLOR_PRIMARY, COLOR_TERTIARY, COLOR_TERTIARY, self.font_size_constant))

            if self.key == '':
                QMessageBox.critical(self, 'Erro', 'Por favor, insira sua chave de API da OpenAI nas configurações.', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
                self.switch_button.setText('Desligado')
                self.switch_button.setStyleSheet('background-color: {}; padding: 10px; border: 2px solid {}; border-radius: 10px; {}'.format(COLOR_SECONDARY, COLOR_PRIMARY, self.font_size_constant))

            else:
                # Inicia a gravação de áudio
                self.audio_gravador_stream.start()
        else:
            self.switch_button.setText('Desligado')
            self.switch_button.setStyleSheet('background-color: {}; padding: 10px; border: 2px solid {}; border-radius: 10px; {}'.format(COLOR_SECONDARY, COLOR_PRIMARY, self.font_size_constant))

            # Para a gravação de áudio
            self.audio_gravador_stream.stop()


    def converter_texto_em_audio(self):
        """
        Inicia a conversão de texto em áudio.
        """
        text = self.conversion_text.toPlainText()
        if text:
            # Atualiza a interface do usuário para exibir a barra de progresso
            self.stacked_widget.setCurrentIndex(1)

            if self.key == '':
                QMessageBox.critical(self, 'Erro', 'Por favor, insira sua chave de API da OpenAI nas configurações.', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
                self.switch_button.setText('Desligado')
                self.switch_button.setStyleSheet('background-color: {}; padding: 10px; border: 2px solid {}; border-radius: 10px; {}'.format(COLOR_SECONDARY, COLOR_PRIMARY, self.font_size_constant))
                self.conversion_progress.hide()
            
            else:
        
                # Inicia a conversão de texto em áudio em uma nova thread
                self.conversion_thread = ConvertendoTextoEmAudio(text)
                self.conversion_thread.finished.connect(self.conversao_concluida)
                self.conversion_thread.start()
        else:
            QMessageBox.critical(self, 'Erro', 'Por favor, insira o texto que deseja converter.', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            self.conversion_progress.hide()

    def conversao_concluida(self):
        """
        Função chamada quando a conversão de texto em áudio é concluída.
        """
        # Atualiza a interface do usuário para exibir o campo de texto de conversão
        self.stacked_widget.setCurrentIndex(0)


    def receber_transcricao(self, transcription, is_corrigido, texto_a_remover):
        """
        Adiciona a transcrição recebida à caixa de transcrição existente.

        Args:
            transcription (str): A transcrição a ser adicionada.

        Returns:
            None
        """

        if is_corrigido:
            texto_atual = self.transcription_box.toHtml()
            texto_atual = self.remover_html(texto_atual)
            texto_atualizado = texto_atual.replace(texto_a_remover, transcription)
            self.transcription_box.setHtml(f'<span style="color:black;">{texto_atualizado}</span>')
            self.transcription_box.moveCursor(QTextCursor.End)
        elif not is_corrigido:
            self.transcription_box.append(f'<span style="color:#7d7d7d;">{transcription}</span>')
            

    def remover_html(self,texto_atual):
        texto_atual = re.sub(r'<[^>]*>|p,\s*li\s*{[^}]*}|hr\s*{[^}]*}|li\.unchecked::marker\s*{[^}]*}|li\.checked::marker\s*{[^}]*}', '', texto_atual)
        return texto_atual
    
    def corrigir_texto(self):
        """
        Corrige o texto na caixa de transcrição.
        """
        texto = self.conversion_text.toPlainText()
        self.stacked_widget.setCurrentIndex(1)
        
        if texto:
            if self.key == '':
                QMessageBox.critical(self, 'Erro', 'Por favor, insira sua chave de API da OpenAI nas configurações.', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
                self.conversion_progress.hide()
            else:
                # Inicia a correção do texto em uma nova thread
                self.correction_thread = CorrigindoTexto(texto)
                self.correction_thread.finished.connect(self.correcao_concluida)
                self.correction_thread.start()
        else:
            QMessageBox.critical(self, 'Erro', 'Por favor, insira o texto que deseja corrigir.', QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            self.conversion_progress.hide()

    def correcao_concluida(self):
        """
        Função chamada quando a correção do texto é concluída.
        """
        # Atualiza a interface do usuário para exibir o campo de texto de conversão
        self.stacked_widget.setCurrentIndex(0)
        self.conversion_text.setPlainText(self.correction_thread.resultado)


