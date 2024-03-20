from PyQt6.QtWidgets import QMainWindow, QLabel, QComboBox, QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout
from PyQt6.QtCore import Qt
from services.config_service import ConfigService

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

        # Adicionado layout vertical
        layout = QVBoxLayout()
        
        # Ajustando margens
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(0)

        # Adicionado titulo
        titulo = QLabel('Configurações')
        titulo.setStyleSheet('font-size: 20px; padding: 10px;')
        layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignTop)

        #Lendo drivers de áudio disponíveis
        self.lendo_drivers_audio()

        #Criando QHoxLayout para os ComboBox
        layout_combobox = QHBoxLayout()
        layout_combobox.setSpacing(15)
        layout_combobox.setContentsMargins(20, 0, 10, 10)

        # Titulo do microfone
        titulo_microfone = QLabel('Dispositivo de entrada - Microfone')
        titulo_microfone.setStyleSheet('font-size: 15px')
        layout_combobox.addWidget(titulo_microfone, alignment=Qt.AlignmentFlag.AlignTop)

        # Adicionado ComboBox
        self.combobox_microphone =  self.cria_combobox('drivers_microphone')
        layout_combobox.addWidget(self.combobox_microphone, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addLayout(layout_combobox)

        #Criando QHoxLayout para os ComboBox
        layout_combobox = QHBoxLayout()
        layout_combobox.setSpacing(15)
        layout_combobox.setContentsMargins(20, 0, 10, 10)

        # Titulo do audio
        titulo_audio = QLabel('Dispositivo de saída - Audio')
        titulo_audio.setStyleSheet('font-size: 15px')
        layout_combobox.addWidget(titulo_audio, alignment=Qt.AlignmentFlag.AlignTop)

        # Adicionado ComboBox
        self.combobox_audio =  self.cria_combobox('drivers_audio')
        layout_combobox.addWidget(self.combobox_audio, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addLayout(layout_combobox)


        # Cria um widget central e define o layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Adiciona um espaçador no final do layout
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(spacer)

    
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
