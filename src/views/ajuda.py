from PyQt6.QtWidgets import QMainWindow, QLabel, QComboBox, QWidget, QVBoxLayout, QSizePolicy, QGridLayout, QHBoxLayout, QLineEdit, QPushButton, QFrame, QSpacerItem, QScrollArea
from PyQt6.QtWidgets import QTabWidget, QMainWindow, QLabel, QComboBox, QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout, QLineEdit, QSpacerItem
from PyQt6.QtCore import Qt

from services.config_service import ConfigService


class Ajuda(QMainWindow):
    """
    Classe que representa a janela de ajuda.

    Esta classe herda da classe QMainWindow e é responsável por exibir a janela de ajuda
    do aplicativo SpeakEZ-Transcribe-AI.

    Atributos:
        Nenhum.

    Métodos:
        __init__(): Inicializa a janela de configurações.
    """
    def __init__(self):
        """
        Inicializa a classe de ajuda.

        Esta função é chamada quando um objeto da classe é criado.
        Ela configura a interface de ajuda, adicionando os elementos necessários,
        como títulos, comboboxes e layouts.

        Args:
            None

        Returns:
            None
        """
        super().__init__()

        self.config = ConfigService().lendo_configuracoes()
        self.font_padrao = self.config['font_size']
        self.topico_style = f"font-size: {str(self.font_padrao)}px; font-weight: bold;"
        self.explic_style = f'font-size: {str(self.font_padrao)}px; margin-bottom: 6px;'


        # Adicionado layout vertical
        central_widget = QWidget()
        central_widget.setMinimumSize(1024, 768)
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        
        # Ajustando margens
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)  # Adiciona um espaçamento vertical de 10 pixels

        # Adicionado titulo
        titulo = QLabel('Ajuda')
        titulo.setStyleSheet('font-size: 40px; font-weight: bold; font: segoe ui; margin-top: 20px; margin-bottom: 20px;')
        layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignTop)


        #Criando TabViewer para configurações
        bloco = QTabWidget()
        fonte_tab = bloco.font()
        fonte_tab.setFamily("Segoe UI")
        fonte_tab.setPointSize(14)
        bloco.setFont(fonte_tab)
        tab_front = QWidget()
        tab_hist = QWidget()
        tab_config = QWidget()
        bloco.addTab(tab_front, "Página Inicial")
        bloco.addTab(tab_hist,"Histórico")
        bloco.addTab(tab_config, "Configurações")
        layout.addWidget(bloco)

        # Criando QVBoxLayout para a aba de página inicial
        layout_front = self.create_layout(tab_front)

        # Criando QVBoxLayout para a aba de histórico
        layout_hist = self.create_layout(tab_hist)

        # Criando QVBoxLayout para a aba de configurações
        layout_config = self.create_layout(tab_config)

        #Botões da pagina inicial
        # Botão liga/desliga
        self.add_label(layout_front, 'Ligado/Desligado: ', 0, 0, self.topico_style)
        self.add_label(layout_front, "Controla o recurso de transcrição automática da reunião. Quando o botão está na posição 'Ligado', o programa começa a transcrever todas as falas da reunião em tempo real. Ao mudar para 'Desligado', o programa para de transcrever, interrompendo o registro das conversas.", 0, 1, self.explic_style)


        # Botão corrigir
        self.add_label(layout_front, 'Corrigir: ', 1, 0, self.topico_style)
        self.add_label(layout_front, 'Ferramenta que automaticamente aprimora o texto digitado. Ao acioná-lo, o programa irá ajustar a estrutura das frases, corrigir a pontuação e substituir palavras erradas para melhorar a clareza e a correção do texto.', 1, 1, self.explic_style)

        # Botão de conversão
        self.add_label(layout_front, 'Converter: ', 2, 0, self.topico_style)
        self.add_label(layout_front, 'Inicia a conversão do texto digitado em áudio. Ao clicar neste botão durante a reunião, o programa lerá em voz alta o texto inserido, permitindo que todos os participantes ouçam a informação sem necessidade de leitura visual.', 2, 1, self.explic_style)

        # combobox Data
        self.add_label(layout_hist, 'Data: ', 0, 0, self.topico_style)
        self.add_label(layout_hist, 'Permite escolher uma data específica para acessar o histórico de reuniões transcritas. Ao selecionar um dia no calendário, o programa exibirá todas as transcrições das reuniões que ocorreram no período, facilitando a busca e revisão de informações passadas.', 0, 1, self.explic_style)

        # Botão exportar transcrições
        self.add_label(layout_hist, 'Exportar Transcrições: ', 1, 0, self.topico_style)
        self.add_label(layout_hist, 'Permite que você salve ou envie as transcrições das reuniões em .TXT para outras plataformas. Ao clicar neste botão, você terá opções para exportar o documento.', 1, 1, self.explic_style)

        # Botão exportar transcrições
        self.add_label(layout_hist, 'Gerar Anotação Inteligente: ', 2, 0, self.topico_style)
        self.add_label(layout_hist, 'ativa um recurso que analisa e resume os pontos principais discutidos durante a reunião. Ao clicar neste botão, o programa identifica e organiza automaticamente as informações-chave, facilitando a compreensão e revisão dos tópicos abordados.', 2, 1, self.explic_style)

        # Botão de entrada
        self.add_label(layout_config, 'Dispositivo de entrada - Microfone: ', 0, 0, self.topico_style)
        self.add_label(layout_config, 'Permite selecionar o dispositivo de entrada de áudio que será usado para capturar o áudio durante a reunião. Ao clicar nele, você pode escolher entre os microfones disponíveis conectados ao sistema.', 0, 1, self.explic_style)

        # Botão de saída
        self.add_label(layout_config, 'Dispositivo de saída - Audio: ', 1, 0, self.topico_style)
        self.add_label(layout_config, 'Permite selecionar o dispositivo de saída de áudio que será configurado. Isso é importante para que o som convertido do texto para áudio seja emitido em um nível sonoro adequado para que o programa capte e as pessoas na reunião possam ouvir claramente.', 1, 1, self.explic_style)

        # entrada de Token
        self.add_label(layout_config, 'Token da OpenAI: ', 2, 0, self.topico_style)
        self.add_label(layout_config, 'Destinada para inserir o Token da OpenAI, que é uma chave de autenticação necessária para acessar os recursos e serviços da plataforma OpenAI. Ao inserir o Token fornecido pela OpenAI aqui, você poderá utilizar as funcionalidades e integrações oferecidas pela plataforma dentro do programa.', 2, 1, self.explic_style)

        # Botão configurações da palavra-chave
        self.add_label(layout_config, 'Configurações da palavra-chave: ', 3, 0, self.topico_style)
        self.add_label(layout_config, 'Permite a adição de termos específicos para aumentar a precisão da transcrição. É opcional.', 3, 1, self.explic_style)


    def create_layout(self, parent):
        widget = QWidget(parent=parent)
        layout = QGridLayout(widget)
        layout.setContentsMargins(10, 10, 0, 0)
        return layout
    
    def add_label(self, layout, text, row, column, style):
        label = QLabel(text)
        label.setWordWrap(True)  # Habilita a quebra de linha
        label.setStyleSheet(style)
        layout.addWidget(label, row, column)
