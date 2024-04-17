from PyQt6.QtWidgets import QMainWindow, QLabel, QTabBar, QWidget, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, QTabWidget, QPushButton, QHBoxLayout, QComboBox, QMessageBox, QTextEdit, QProgressBar
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSizePolicy
import qtawesome as qta
import csv
import threading

from services.openai_client import OpenaiClient
from services.config_service import ConfigService
from services.conversion_service import ConvertendoTextoEmAudio

COLOR_PRIMARY = '#4d608c'
COLOR_SECONDARY = '#b4cbd9'
COLOR_TERTIARY = 'white'

class Historico(QMainWindow):
    """
    Classe que representa a janela de histórico.

    Essa classe herda da classe QMainWindow e é responsável por exibir o histórico de transcrições.

    Atributos:
        Nenhum atributo definido.

    Métodos:
        __init__(): Construtor da classe Historico.
    """
    def __init__(self):
        super().__init__()

        self.config_service = ConfigService()
        self.config = self.config_service.lendo_configuracoes()
        self.font_size = self.config['font_size']
        self.font_size_constant = f'font-size: {str(self.font_size)}px;'

        self.table = QTableWidget()


        # Configura a interface do usuário
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        # Define o widget central
        self.setCentralWidget(central_widget)

        # Adiciona um título à janela
        label = QLabel('Histórico')
        # Define o estilo do título
        label.setStyleSheet("font-size: 36px; font-weight: bold; font: Segoe UI; color: {}; margin-top: 20px; margin-bottom: 20px;".format('black'))
        # Adiciona o título ao layout
        layout.addWidget(label)

        # Cria um novo QTabWidget
        tab_widget = QTabWidget()

        #Aumentando o tamanho das texto das abas
        tab_widget.setStyleSheet("QTabBar::tab {{ height: 50px; font-size: {}px; }}".format(self.font_size))
        
        layout_transcricao_tab = self.area_transcricao()

        layout_conversion_tab = self.area_conversion()

        tab_widget.addTab(layout_transcricao_tab, "Transcrição")
        tab_widget.addTab(layout_conversion_tab, "Conversão")

        # Adiciona o widget de abas ao layout
        layout.addWidget(tab_widget)
    
    def preenchendo_tabela_is_conversion(self, is_conversion_bool):
        # Lendo o arquivo csv
        with open('src\config\historico.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='|')
            dados = list(reader)

        # Obtendo a data selecionada
        if is_conversion_bool:
            data_selecionada = self.combo_data_conversion.currentText()
        else:
            data_selecionada = self.combo_data.currentText()

        # Limpando as tabelas
        self.table.setRowCount(0)
        self.table_conversion.setRowCount(0)

        # Adicionando as transcrições e conversões às tabelas
        for data in dados:
            # Se a conversão não está vazia, então é uma conversão

            if data['data'] == data_selecionada:
                if is_conversion_bool:
                    if data['conversion'] != '':  # Verifica se a conversão não está vazia
                        self.add_row_to_table(self.table_conversion, [data['hora'], data['conversion']], True)
                elif not is_conversion_bool:
                    if data['transcricao'] != '':  # Verifica se a transcrição não está vazia
                        self.add_row_to_table(self.table, [data['hora'], data['transcricao']], False)
    
    def add_row_to_table(self, table, row_data, is_conversion):
        if not is_conversion:
            row_count = table.rowCount()
            table.setRowCount(row_count + 1)
            for i, data in enumerate(row_data):
                table.setItem(row_count, i, QTableWidgetItem(data))
        else:
            row_count = table.rowCount()
            table.setRowCount(row_count + 1)
            for i, data in enumerate(row_data):
                table.setItem(row_count, i, QTableWidgetItem(data))
            # Adicionando botão para adicionar anotação
            btn = QPushButton('Reproduzir')
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet('background-color: {}; color: {};padding: 10px; border: none; border-style: none;border-radius: 10px;{}; margin:10px'.format(COLOR_PRIMARY, COLOR_TERTIARY, self.font_size_constant))
            btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            btn.clicked.connect(lambda: self.start_conversion_thread(row_data[1]))
            table.setCellWidget(row_count, 2, btn)
    def start_conversion_thread(self, text):
        self.conversion_thread = ConvertendoTextoEmAudio(text)
        self.conversion_thread.start()

    def carregando_data_is_conversion(self, is_conversion_bool):
        # Lendo o arquivo csv
        with open('src\config\historico.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='|')
            dados = list(reader)
    
        dados_iter = iter(dados)
    
        next(dados_iter)  # Ignorando o cabeçalho
    
        datas_unicas_transcription = set()
        datas_unicas_conversion = set()
        for data in dados_iter:
            # If the row has less than 4 elements, append empty strings until it has 4 elements
            while len(data) < 4:
                data.append('')
    
            # Se a conversão não está vazia, então é uma conversão
            is_conversion = data[3] != ''
    
            # Se a data ainda não foi adicionada, adicione-a ao combo box apropriado
            if not is_conversion_bool and not is_conversion:
                if data[0] not in datas_unicas_transcription:
                    self.combo_data.addItem(data[0])
                    datas_unicas_transcription.add(data[0])
            elif is_conversion_bool and is_conversion:
                if data[0] not in datas_unicas_conversion:
                    self.combo_data_conversion.addItem(data[0])
                    datas_unicas_conversion.add(data[0])

    def area_conversion(self):
        # Cria novo layout para a aba de transcrição
        layout_conversion_tab = QWidget()
        layout_vertical_conversion = QVBoxLayout(layout_conversion_tab)
        layout_vertical_conversion.setContentsMargins(10, 10, 10, 10)

        #Criando layout para botões
        layout_botoes_conversion = QHBoxLayout()

        # Selecionando data
        label_data_conversion = QLabel('Data:')
        label_data_conversion.setStyleSheet(self.font_size_constant)
        layout_botoes_conversion.addWidget(label_data_conversion)

        # Caixa de seleção de data
        self.combo_data_conversion = QComboBox()
        self.combo_data_conversion.setStyleSheet(self.font_size_constant)
        self.combo_data_conversion.addItem('Selecione uma data')
        self.combo_data_conversion.setCurrentText('Selecione uma data')
        layout_botoes_conversion.addWidget(self.combo_data_conversion)
        self.carregando_data_is_conversion(True)
        # Aciona o método de carregar transcrições
        self.combo_data_conversion.currentIndexChanged.connect(lambda: self.preenchendo_tabela_is_conversion(True))

        #Adicionando espaço entre os botões
        layout_botoes_conversion.addStretch()

        #Botão para exportar transcrições
        btn_exportar_conversion = self.criando_botoes('Exportar Conversões', 'fa5s.file-export', 'white')
        btn_exportar_conversion.clicked.connect(self.exportar_conversoes)
        layout_botoes_conversion.addWidget(btn_exportar_conversion)

        # Movendo os botões para a direita
        layout_botoes_conversion.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Adiciona o layout de botões ao layout da aba de transcrição
        layout_vertical_conversion.addLayout(layout_botoes_conversion)

        #Criando um QTableWidget
        self.table_conversion = QTableWidget()
        self.table_conversion.setColumnCount(3)
        self.table_conversion.setHorizontalHeaderLabels(['Hora', 'Conversão', 'Ação'])
        self.table_conversion.horizontalHeader().setStretchLastSection(True)
        self.table_conversion.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table_conversion.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_conversion.verticalHeader().setVisible(False)
        self.table_conversion.setAlternatingRowColors(True)
        self.table_conversion.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_conversion.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table_conversion.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        css_style = """QTableView {{font-size: {}px;}} QHeaderView {{font-size: {}px;}}""".format(self.font_size, self.font_size+2)
        self.table_conversion.setStyleSheet(css_style)

        # Adiciona a tabela ao layout
        layout_vertical_conversion.addWidget(self.table_conversion)


        # Adiciona o campo de anotação
        self.text_edit_conversion = QTextEdit()
        self.text_edit_conversion.setPlaceholderText('Anotação')
        self.text_edit_conversion.setStyleSheet(self.font_size_constant)
        self.text_edit_conversion.hide()

        layout_vertical_conversion.addWidget(self.text_edit_conversion)

        # Adiciona o layout da aba de transcrição ao tab_widget
        layout_conversion_tab.setLayout(layout_vertical_conversion)

        return layout_conversion_tab
    




    def area_transcricao(self):

        # Cria novo layout para a aba de transcrição
        layout_transcricao_tab = QWidget()
        layout_vertical_transcricao = QVBoxLayout(layout_transcricao_tab)
        layout_vertical_transcricao.setContentsMargins(10, 10, 10, 10)

        #Criando layout para botões
        layout_botoes = QHBoxLayout()

        # Selecionando data
        label_data = QLabel('Data:')
        label_data.setStyleSheet(self.font_size_constant)
        layout_botoes.addWidget(label_data)
        

        # Caixa de seleção de data
        self.combo_data = QComboBox()
        self.combo_data.setStyleSheet(self.font_size_constant)
        self.combo_data.addItem('Selecione uma data')
        self.combo_data.setCurrentText('Selecione uma data')
        layout_botoes.addWidget(self.combo_data)
        self.carregando_data_is_conversion(False)
        # Aciona o método de carregar transcrições
        self.combo_data.currentIndexChanged.connect(lambda: self.preenchendo_tabela_is_conversion(False))

        #Adicionando espaço entre os botões
        layout_botoes.addStretch()


        #Botão para exportar transcrições
        btn_exportar = self.criando_botoes('Exportar Transcrições', 'fa5s.file-export', 'white')
        btn_exportar.clicked.connect(self.exportar_transcricoes)
        layout_botoes.addWidget(btn_exportar)

        # Botão para gerar uma anotação inteligente
        btn_anotacao = self.criando_botoes('Gerar Anotação Inteligente', 'fa5s.sticky-note', 'white')
        btn_anotacao.clicked.connect(self.gerar_anotacao_inteligente)
        layout_botoes.addWidget(btn_anotacao)

        # Movendo os botões para a direita
        layout_botoes.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Adiciona o layout de botões ao layout da aba de transcrição
        layout_vertical_transcricao.addLayout(layout_botoes)

        #Criando um QTableWidget
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Hora', 'Transcrição'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setWordWrap(True)
        self.table.setWordWrap(True)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        css_style = """QTableView {{font-size: {}px;}} QHeaderView {{font-size: {}px;}}""".format(self.font_size, self.font_size+2)
        self.table.setStyleSheet(css_style)

        # Adiciona a tabela ao layout
        layout_vertical_transcricao.addWidget(self.table)

        # Adiciona uma barra de progresso
        self.progress_bar = self.progress_bar()

        self.progress_bar.hide()

        layout_vertical_transcricao.addWidget(self.progress_bar)

        # Adiciona o campo de anotação
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('Anotação')
        self.text_edit.setStyleSheet(self.font_size_constant)
        self.text_edit.hide()
        layout_vertical_transcricao.addWidget(self.text_edit)

        # Adiciona o layout da aba de transcrição ao tab_widget
        layout_transcricao_tab.setLayout(layout_vertical_transcricao)

        return layout_transcricao_tab


    def criando_botoes(self, text, icon_name, color, fixed_width=125):
        icon = qta.icon(icon_name, color=color)
        button = QPushButton(icon, text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setIcon(icon)
        button.setIconSize(QSize(18, 18))
        button.setStyleSheet('background-color: {}; color: {}; padding: 10px; border: none; border-style: none;border-radius: 10px;{}'.format(COLOR_PRIMARY, COLOR_TERTIARY, self.font_size_constant))
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        return button
    
    def exportar_transcricoes(self):
        try:
            # Lendo o arquivo csv
            with open('src\config\historico.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter='|')
                dados = list(reader)

            # Obtendo a data selecionada
            data_selecionada = self.combo_data.currentText()

            if data_selecionada != 'Selecione uma data':
                # Criando um iterador para os dados
                dados_iter = iter(dados)

                # Ignorando o cabeçalho
                next(dados_iter)

                # Criando um arquivo txt
                # Determinando o nome do arquivo
                nome_arquivo = f'{data_selecionada.replace("/", "_")}_transcricao.txt'
                with open(nome_arquivo, 'w') as file:
                    # Adicionando as transcrições ao arquivo
                    for data in dados_iter:
                        if data[0] == data_selecionada:
                            if data[2] != '':
                                file.write(f'{data[1]}: {data[2]}\n')
                # Mensagem de sucesso
                QMessageBox.information(self, "Mensagem de Informação", f"Transcrições exportadas com sucesso para o arquivo {nome_arquivo}.", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            
            else:
                #Mensagem de info Qt
                QMessageBox.information(self, "Mensagem de Informação", "Selecione uma data para exportar as transcrições.", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar transcrições: {e}", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
    
    def exportar_conversoes(self):
        try:
            # Lendo o arquivo csv
            with open('src\config\historico.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter='|')
                dados = list(reader)

            # Obtendo a data selecionada
            data_selecionada = self.combo_data_conversion.currentText()

            if data_selecionada != 'Selecione uma data':
                # Criando um iterador para os dados
                dados_iter = iter(dados)

                # Ignorando o cabeçalho
                next(dados_iter)

                # Criando um arquivo txt
                # Determinando o nome do arquivo
                nome_arquivo = f'{data_selecionada.replace("/", "_")}_conversion.txt'
                with open(nome_arquivo, 'w') as file:
                    # Adicionando as transcrições ao arquivo
                    for data in dados_iter:
                        if data[0] == data_selecionada:
                            if data[3] != '':
                                file.write(f'{data[1]}: {data[3]}\n')
                # Mensagem de sucesso
                QMessageBox.information(self, "Mensagem de Informação", f"Transcrições exportadas com sucesso para o arquivo {nome_arquivo}.", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            
            else:
                #Mensagem de info Qt
                QMessageBox.information(self, "Mensagem de Informação", "Selecione uma data para exportar as transcrições.", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar transcrições: {e}", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
    
    def gerar_anotacao_inteligente(self):
        try:
            self.progress_bar.show()
            # Lendo o arquivo csv
            with open('src\config\historico.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter='|')
                dados = list(reader)

            # Obtendo a data selecionada
            data_selecionada = self.combo_data.currentText()

            if data_selecionada != 'Selecione uma data':
                # Criando um iterador para os dados
                dados_iter = iter(dados)

                # Ignorando o cabeçalho
                next(dados_iter)

                # Criando um arquivo txt
                # Determinando o nome do arquivo
                nome_arquivo = f'{data_selecionada.replace("/", "_")}_anotação_inteligente.txt'

                # Unificando as transcrições
                transcricoes = ''
                for data in dados_iter:
                    if data[0] == data_selecionada:
                        transcricoes += f'{data[2]}\n'
                
                #envia para a api da openai
                client = OpenaiClient().return_client()
                system_prompt = "Gere uma anotação resumindo as transcrições do dia. E Gere To-Do's para as tarefas mencionadas."
                temperature = 0

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",
                    temperature=temperature,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": transcricoes
                        }
                    ]
                )
                aviso = "Anotação inteligente gerada com o auxílio do GPT da OpenAI.\n\n"
                self.text_edit.setPlainText(aviso + response.choices[0].message.content)
                self.text_edit.show()
                with open(nome_arquivo, 'w') as file:
                    file.write(aviso + response.choices[0].message.content)
                # Mensagem de sucesso
                QMessageBox.information(self, "Mensagem de Informação", f"Anotação inteligente foi gerada com sucesso! {nome_arquivo}.", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            
            else:
                #Mensagem de info Qt
                QMessageBox.information(self, "Mensagem de Informação", "Selecione uma data para exportar as transcrições.", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar anotação: {e}", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        finally:
            self.progress_bar.hide()
        
    def progress_bar(self):
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
        return self.conversion_progress


            
        






