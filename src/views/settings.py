from PyQt6.QtWidgets import QTabWidget, QMainWindow, QLabel, QComboBox, QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout, QLineEdit, QPushButton, QSpacerItem, QSlider
from PyQt6.QtCore import Qt
from services.config_service import ConfigService
from views.palavra_chave import PalavraChave

class Settings(QMainWindow):
    """
    Classe que representa a janela de configurações.

    Esta classe herda da classe QMainWindow e é responsável por exibir a janela de configurações
    do aplicativo SpeakEZ-Transcribe-AI.

    Atributos:
        Nenhum.

    Métodos:
        __init__(): Inicializa a janela de configurações.
    """
    def __init__(self):
        """
        Inicializa a classe de configurações.

        Esta função é chamada quando um objeto da classe é criado.
        Ela configura a interface de configurações, adicionando os elementos necessários,
        como títulos, comboboxes e layouts.

        Args:
            None

        Returns:
            None
        """
        super().__init__()
        self.config_service = ConfigService()
        self.config = self.config_service.lendo_configuracoes()
        self.font_size = self.config['font_size']

        # Adicionado layout vertical
        layout = QVBoxLayout()
        
        # Ajustando margens
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)

        # Adicionado titulo
        titulo = QLabel('Configurações')
        titulo.setStyleSheet('font-size: 40px; font-weight: bold; font: segoe ui; margin-top: 20px; margin-bottom: 20px;')
        layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignTop)

        #Lendo drivers de áudio disponíveis
        self.lendo_drivers_audio()

        #Criando TabViewer para configurações
        bloco = QTabWidget()
        fonte_tab = bloco.font()
        fonte_tab.setFamily("Segoe UI")
        bloco.setStyleSheet("QTabBar::tab {{ height: 50px; font-size: {}px; }}".format(self.font_size))
        bloco.setFont(fonte_tab)
        tab_geral = QWidget()
        tab_audio = QWidget()
        tab_token = QWidget()
        bloco.addTab(tab_geral,"Geral")
        bloco.addTab(tab_audio, "Gerenciamento de áudio")
        bloco.addTab(tab_token,"OpenAI")
        
        layout.addWidget(bloco)

        #Criando QVBoxLayout para a aba de áudio
        layout_audio_tab = QWidget(parent=tab_audio)      
        layout_audio = QVBoxLayout(layout_audio_tab)
        layout_audio.setContentsMargins(10,10,0,0)

       #Criando QVBoxLayout para a aba de token
        layout_openai_tab = QWidget(parent=tab_token)      
        layout_token = QVBoxLayout(layout_openai_tab)
        layout_token.setContentsMargins(10,10,0,0)

        #Criando QVBoxLayout para a aba de geral
        layout_geral_tab = QWidget(parent=tab_geral)      
        layout_geral = QVBoxLayout(layout_geral_tab)
        layout_geral.setContentsMargins(10,10,0,0)

        # Adicionando parametro de volume de áudio
        titulo_volume = QLabel('Volume de áudio')
        titulo_volume.setStyleSheet(f'font-size: {self.font_size}px')
        layout_geral.addWidget(titulo_volume, alignment=Qt.AlignmentFlag.AlignTop)

        # Adicionando deslizador de volume
        #Layout de deslizador de volume
        layout_volume = QHBoxLayout()
        self.deslizador_volume = QSlider(Qt.Orientation.Horizontal)
        self.deslizador_volume.setMinimum(0)
        self.deslizador_volume.setMaximum(100)
        self.deslizador_volume.setValue(int(round(self.config['volume_audio'] * 100, 2)))
        self.deslizador_volume.valueChanged.connect(lambda: self.atualiza_configuracao(self.deslizador_volume, 'volume_audio', '%', self.label_volume))
        self.deslizador_volume.setFixedSize(200, 20)
        layout_volume.addWidget(self.deslizador_volume)

        #Número de volume
        self.label_volume = QLabel(str(self.deslizador_volume.value()) + '%')
        self.label_volume.setStyleSheet(f'font-size: {self.font_size-4}px')
        layout_volume.addWidget(self.label_volume)
        layout_geral.addLayout(layout_volume)

        # Adicionando parâmetro de tamanho de fonte
        titulo_fonte = QLabel('Tamanho da fonte')
        titulo_fonte.setStyleSheet(f'font-size: {self.font_size}px')
        layout_geral.addWidget(titulo_fonte, alignment=Qt.AlignmentFlag.AlignTop)
        
        # Adicionando deslizador de tamanho de fonte
        # Layout de deslizador de tamanho de fonte
        layout_fonte = QHBoxLayout()
        self.deslizador_fonte = QSlider(Qt.Orientation.Horizontal)
        self.deslizador_fonte.setMinimum(10)  # mínimo tamanho de fonte
        self.deslizador_fonte.setMaximum(32)  # máximo tamanho de fonte
        self.deslizador_fonte.setValue(int(self.config['font_size']))
        self.deslizador_fonte.valueChanged.connect(lambda: self.atualiza_configuracao(self.deslizador_fonte, 'font_size', 'pt', self.label_fonte))
        self.deslizador_fonte.setFixedSize(200, 20)
        layout_fonte.addWidget(self.deslizador_fonte)
        
        # Número de tamanho de fonte
        self.label_fonte = QLabel(str(self.deslizador_fonte.value()) + 'pt')
        self.label_fonte.setStyleSheet(f'font-size: {self.font_size-4}px')
        layout_fonte.addWidget(self.label_fonte)
        layout_geral.addLayout(layout_fonte)



        # Titulo do microfone
        titulo_microfone = QLabel('Dispositivo de entrada - Microfone')
        titulo_microfone.setStyleSheet(f'font-size: {self.font_size}px')
        layout_audio.addWidget(titulo_microfone, alignment=Qt.AlignmentFlag.AlignTop)

        # Adicionado ComboBox
        self.combobox_microphone =  self.cria_combobox('drivers_microphone')
        self.combobox_microphone.setStyleSheet(f'font-size: {self.font_size-4}px; font: segoe ui')
        layout_audio.addWidget(self.combobox_microphone, alignment=Qt.AlignmentFlag.AlignTop)

        # Espaçador entre opções
        espacador = QSpacerItem(10,20,QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout_audio.addSpacerItem(espacador)

        # Titulo do audio
        titulo_audio = QLabel('Dispositivo de saída - Audio')
        titulo_audio.setStyleSheet(f'font-size: {self.font_size}px')
        layout_audio.addWidget(titulo_audio, alignment=Qt.AlignmentFlag.AlignTop)

        # Adicionado ComboBox
        self.combobox_audio =  self.cria_combobox('drivers_audio')
        self.combobox_audio.setStyleSheet(f'font-size: {self.font_size-4}px; font: segoe ui')
        layout_audio.addWidget(self.combobox_audio, alignment=Qt.AlignmentFlag.AlignTop)
        #layout.addLayout(layout_combobox)

        # Adiciona um título ao bloco de texto
        titulo_token = QLabel('Token da OpenAI:')

        # Ajusta o estilo do título
        titulo_token.setStyleSheet(f'font-size: {self.font_size}px')

        # Adiciona o título ao layout
        layout_token.addWidget(titulo_token, alignment=Qt.AlignmentFlag.AlignTop)

        # Cria um bloco de texto para inserir o token da OpenAI
        self.token = QLineEdit()

        # Expor o token se ele existir
        if 'openai_api_key' in self.config:
            self.token.setText(self.config['openai_api_key'])
        
        # Salvar o token da OpenAI
        self.token.textChanged.connect(lambda: self.config_service.salvando_configuracoes({'openai_api_key': self.token.text()}))
        self.token.setStyleSheet(f'font-size: {self.font_size}px')

        # Adiciona o bloco de texto ao layout
        layout_token.addWidget(self.token, alignment=Qt.AlignmentFlag.AlignTop)
        #layout.addLayout(layout_token)

        # Titulo de estilos de vozes
        titulo_vozes = QLabel('Estilos de voz')
        titulo_vozes.setStyleSheet(f'font-size: {self.font_size}px; margin-top: 20px; margin-bottom: 5px;')
        layout_token.addWidget(titulo_vozes, alignment=Qt.AlignmentFlag.AlignTop)

        # Adiciona a lista de estilos de vozes da TTS-HD da OpenAI
        self.voices = QComboBox()
        self.voices.addItems([ 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'])
        self.voices.setCurrentText(self.config['style_voice'])
        self.voices.currentIndexChanged.connect(lambda: self.config_service.salvando_configuracoes({'style_voice': self.voices.currentText()}))
        self.voices.setStyleSheet(f'font-size: {self.font_size-2}px; font: segoe ui')
        layout_token.addWidget(self.voices, alignment=Qt.AlignmentFlag.AlignTop)

        # Titulo de configurações de palavra-chave
        titulo_palavra_chave = QLabel('Configurações de palavra-chave')
        titulo_palavra_chave.setStyleSheet(f'font-size: {self.font_size-4}px; margin-top: 20px; margin-bottom: 5px;')
        layout.addWidget(titulo_palavra_chave, alignment=Qt.AlignmentFlag.AlignTop)

        # Abrir uma janela de palavra-chave
        abrir_janela_palavra_chave = QPushButton('Abrir janela de palavra-chave')
        abrir_janela_palavra_chave.setStyleSheet(f'font-size: {self.font_size-4}px; font: segoe ui')
        abrir_janela_palavra_chave.clicked.connect(lambda: self.abrir_janela_palavra_chave())
        layout.addWidget(abrir_janela_palavra_chave, alignment=Qt.AlignmentFlag.AlignTop)


        # Cria um widget central e define o layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Adiciona um espaçador no final do layout
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(spacer)
    
    def abrir_janela_palavra_chave(self):
        """
        Abre a janela de configurações de palavra-chave.

        Retorna:
        Nenhum valor de retorno.
        """
        #Abrir uma janela de pyqt
        self.janela_palavra_chave = PalavraChave()
        self.janela_palavra_chave.show()

    
    def lendo_drivers_audio(self):
            """
            Lê as configurações e retorna os drivers de áudio disponíveis.

            Returns:
                list: Uma lista contendo os drivers de áudio disponíveis.
            """
            self.config = self.config_service.lendo_configuracoes()

    def selecionando_driver(self, driver):
            """
            Seleciona o driver de áudio ou microfone especificado e atualiza a configuração correspondente.

            Parâmetros:
            - driver (str): O tipo de driver a ser selecionado. Pode ser 'drivers_audio' para o driver de áudio ou 'drivers_microphone' para o driver de microfone.

            Retorna:
            Nenhum.

            """
            if driver == 'drivers_audio':
                selected_driver_name = self.combobox_audio.currentText()

            elif driver == 'drivers_microphone':
                selected_driver_name = self.combobox_microphone.currentText()

            for driver_id, driver_name in self.config[driver].items():
                if driver_name == selected_driver_name:
                    self.config['selected_' + driver] = driver_id
                    self.config = self.config_service.salvando_configuracoes(self.config)
                    break
    
    def cria_combobox(self, text_audio):
            """
            Cria e retorna um objeto QComboBox preenchido com os valores do dicionário de configuração correspondente ao texto de áudio fornecido.

            Parâmetros:
            - text_audio (str): O texto de áudio para o qual o objeto QComboBox será criado.

            Retorna:
            - combobox (QComboBox): O objeto QComboBox preenchido com os valores do dicionário de configuração correspondente ao texto de áudio fornecido.
            """
            combobox = QComboBox()
            try:
                driver_atual = self.config['selected_' + text_audio]
                combobox.addItems(list(self.config[text_audio].values()))
                combobox.setCurrentText(self.config[text_audio][driver_atual])
                combobox.currentIndexChanged.connect(lambda: self.selecionando_driver(text_audio))
                return combobox
            except KeyError:
                combobox.addItems(list(self.config[text_audio].values()))
                combobox.currentIndexChanged.connect(lambda: self.selecionando_driver(text_audio))
                return combobox
    def atualiza_configuracao(self, deslizador, chave_config, sufixo, label):
        valor = deslizador.value()
        self.config_service.salvando_configuracoes({chave_config: valor})
        label.setText(f"{valor}{sufixo}")


