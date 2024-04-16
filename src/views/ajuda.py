from PyQt6.QtWidgets import QMainWindow, QLabel, QComboBox, QWidget, QVBoxLayout, QSizePolicy, QGridLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtWidgets import QTabWidget, QMainWindow, QLabel, QComboBox, QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout, QLineEdit, QSpacerItem
from PyQt6.QtCore import Qt


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

        # Adicionado layout vertical
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        
        # Ajustando margens
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)

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

        #Criando QVBoxLayout para a aba de pagina inicial
        layout_front_tab = QWidget(parent=tab_front)      
        layout_front = QGridLayout(layout_front_tab)
        layout_front.setContentsMargins(10,10,0,0)

       #Criando QVBoxLayout para a aba de histórico
        layout_hist_tab = QWidget(parent=tab_hist)      
        layout_hist = QGridLayout(layout_hist_tab)
        layout_hist.setContentsMargins(10,10,0,0)

       #Criando QVBoxLayout para a aba de configurações
        layout_config_tab = QWidget(parent=tab_config)      
        layout_config = QGridLayout(layout_config_tab)
        layout_config.setContentsMargins(10,10,0,0)

        #Botões da pagina inicial
        
        # Botão liga/desliga
        topico_ligdes = QLabel('Ligado/Desligado: ')
        topico_ligdes.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout_front.addWidget(topico_ligdes, 0, 0)

        explic_ligdes = QLabel("controla o recurso de transcrição automática da reunião. Quando o botão está na posição 'Ligado', o programa começa a transcrever todas as falas da reunião em tempo real. Ao mudar para 'Desligado', o programa para de transcrever, interrompendo o registro das conversas.")
        explic_ligdes.setWordWrap(True)
        explic_ligdes.setStyleSheet('font-size: 18px; margin-bottom: 6px;')
        layout_front.addWidget(explic_ligdes, 0, 1)

        # Botão corrigir
        topico_varinha = QLabel('Corrigir: ')
        topico_varinha.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout_front.addWidget(topico_varinha, 1, 0)

        explic_varinha = QLabel('Ferramenta que automaticamente aprimora o texto digitado. Ao acioná-lo, o programa irá ajustar a estrutura das frases, corrigir a pontuação e substituir palavras erradas para melhorar a clareza e a correção do texto.')
        explic_varinha.setWordWrap(True)
        explic_varinha.setStyleSheet('font-size: 18px; margin-bottom: 6px;')
        layout_front.addWidget(explic_varinha, 1, 1)

        # Botão de conversão
        topico_convert = QLabel('Converter: ')
        topico_convert.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout_front.addWidget(topico_convert, 2, 0)

        explic_convert = QLabel('inicia a conversão do texto digitado em áudio. Ao clicar neste botão durante a reunião, o programa lerá em voz alta o texto inserido, permitindo que todos os participantes ouçam a informação sem necessidade de leitura visual.')
        explic_convert.setWordWrap(True)
        explic_convert.setStyleSheet('font-size: 18px; margin-bottom: 6px;')
        layout_front.addWidget(explic_convert, 2, 1)

        #Botões da tela de histórico
        
        # combobox Data
        topico_data = QLabel('Data: ')
        topico_data.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout_hist.addWidget(topico_data, 0, 0)

        explic_data = QLabel('Permite escolher uma data específica para acessar o histórico de reuniões transcritas. Ao selecionar um dia no calendário, o programa exibirá todas as transcrições das reuniões que ocorreram no período, facilitando a busca e revisão de informações passadas.')
        explic_data.setWordWrap(True)
        explic_data.setStyleSheet('font-size: 18px; margin-bottom: 6px;')
        layout_hist.addWidget(explic_data, 0, 1)

        # Botão exportar transcrições
        topico_export = QLabel('Exportar Transcrições: ')
        topico_export.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout_hist.addWidget(topico_export, 1, 0)
    
        explic_export = QLabel('Permite que você salve ou envie as transcrições das reuniões em .TXT para outras plataformas. Ao clicar neste botão, você terá opções para exportar o documento.')
        explic_export.setWordWrap(True)
        explic_export.setStyleSheet('font-size: 18px; margin-bottom: 6px;')
        layout_hist.addWidget(explic_export, 1, 1)

        # Botão exportar transcrições
        topico_anot = QLabel('Gerar Anotação Inteligente: ')
        topico_anot.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout_hist.addWidget(topico_anot, 2, 0)

        explic_anot = QLabel('ativa um recurso que analisa e resume os pontos principais discutidos durante a reunião. Ao clicar neste botão, o programa identifica e organiza automaticamente as informações-chave, facilitando a compreensão e revisão dos tópicos abordados.')
        explic_anot.setWordWrap(True)
        explic_anot.setStyleSheet('font-size: 18px; margin-bottom: 6px;')
        layout_hist.addWidget(explic_anot, 2, 1)

        # Botões da tela de configurações

        # Botão de entrada
        topico_entrada = QLabel('Dispositivo de entrada - Microfone: ')
        topico_entrada.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout_config.addWidget(topico_entrada, 0, 0)

        explic_entrada = QLabel('Permite selecionar o dispositivo de entrada de áudio que será usado para capturar o áudio durante a reunião. Ao clicar nele, você pode escolher entre os microfones disponíveis conectados ao sistema.')
        explic_entrada.setWordWrap(True)
        explic_entrada.setStyleSheet('font-size: 18px; margin-bottom: 6px;')
        layout_config.addWidget(explic_entrada, 0, 1)

        # Botão de saída
        topico_saida = QLabel('Dispositivo de saída - Audio: ')
        topico_saida.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout_config.addWidget(topico_saida, 1, 0)

        explic_saida = QLabel('Permite selecionar o dispositivo de saída de áudio que será configurado. Isso é importante para que o som convertido do texto para áudio seja emitido em um nível sonoro adequado para que o programa capte e as pessoas na reunião possam ouvir claramente.')
        explic_saida.setWordWrap(True)
        explic_saida.setStyleSheet('font-size: 18px; margin-bottom: 6px;')
        layout_config.addWidget(explic_saida, 1, 1)

        # entrada de Token
        topico_token = QLabel('Token da OpenAI: ')
        topico_token.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout_config.addWidget(topico_token, 2, 0)

        explic_token = QLabel('Destinada para inserir o Token da OpenAI, que é uma chave de autenticação necessária para acessar os recursos e serviços da plataforma OpenAI. Ao inserir o Token fornecido pela OpenAI aqui, você poderá utilizar as funcionalidades e integrações oferecidas pela plataforma dentro do programa.')
        explic_token.setWordWrap(True)
        explic_token.setStyleSheet('font-size: 18px; margin-bottom: 6px;')
        layout_config.addWidget(explic_token, 2, 1)

        # Botão configurações da palavra-chave
        topico_chave = QLabel('Configurações da palavra-chave: ')
        topico_chave.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout_config.addWidget(topico_chave, 3, 0)

        explic_chave = QLabel(' falta esse ')
        explic_chave.setWordWrap(True)
        explic_chave.setStyleSheet('font-size: 18px; margin-bottom: 6px;')
        layout_config.addWidget(explic_chave, 3, 1)
