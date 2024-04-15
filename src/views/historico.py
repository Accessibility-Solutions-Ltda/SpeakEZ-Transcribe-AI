from PyQt6.QtWidgets import QMainWindow, QLabel, QTabBar, QWidget, QVBoxLayout, QTableWidget, QHeaderView, QTableWidgetItem, QTabWidget, QPushButton, QHBoxLayout, QComboBox, QMessageBox, QTextEdit, QProgressBar
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSizePolicy
import qtawesome as qta
import csv
import threading

from services.openai_client import OpenaiClient

FONT_SIZE = 'font-size: 18px;'
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

        super().__init__()

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
        tab_widget.setStyleSheet("QTabBar::tab { height: 50px; font-size: 20px; }")
        
        layout_transcricao_tab = self.area_transcricao()

        layout_conversion_tab = self.area_conversion()

        tab_widget.addTab(layout_transcricao_tab, "Transcrição")
        tab_widget.addTab(layout_conversion_tab, "Conversão")

        # Adiciona o widget de abas ao layout
        layout.addWidget(tab_widget)
    
    def preenchendo_tabela(self):
        # Lendo o arquivo csv
        with open('src\config\historico.csv', 'r') as file:
            reader = csv.reader(file, delimiter='|')
            dados = list(reader)

        # Obtendo a data selecionada
        data_selecionada = self.combo_data.currentText()

        # Criando um iterador para os dados
        dados_iter = iter(dados)

        # Ignorando o cabeçalho
        next(dados_iter)

        # Limpando a tabela
        self.table.setRowCount(0)

        # Adicionando as transcrições à tabela
        for data in dados_iter:
            if data[0] == data_selecionada:
                row_count = self.table.rowCount()
                self.table.setRowCount(row_count + 1)
                self.table.setItem(row_count, 0, QTableWidgetItem(data[1]))
                self.table.setItem(row_count, 1, QTableWidgetItem(data[2]))

    def carregando_data(self):
        #Lendo o arquivo csv
        with open('src\config\historico.csv', 'r') as file:
            reader = csv.reader(file, delimiter='|')
            dados = list(reader)

        dados_iter = iter(dados)

        next(dados_iter)
        datas_unicas = set()
        for data in dados_iter:
        # Se a data ainda não foi adicionada, adicione-a
            if data[0] not in datas_unicas:
                self.combo_data.addItem(data[0])
                datas_unicas.add(data[0])

    def area_conversion(self):
        label_teste = QLabel('Teste')
        return label_teste

    def area_transcricao(self):

        # Cria novo layout para a aba de transcrição
        layout_transcricao_tab = QWidget()
        layout_vertical_transcricao = QVBoxLayout(layout_transcricao_tab)
        layout_vertical_transcricao.setContentsMargins(10, 10, 10, 10)

        #Criando layout para botões
        layout_botoes = QHBoxLayout()

        # Selecionando data
        label_data = QLabel('Data:')
        label_data.setStyleSheet(FONT_SIZE)
        layout_botoes.addWidget(label_data)
        

        # Caixa de seleção de data
        self.combo_data = QComboBox()
        self.combo_data.setStyleSheet(FONT_SIZE)
        self.combo_data.addItem('Selecione uma data')
        self.combo_data.setCurrentText('Selecione uma data')
        layout_botoes.addWidget(self.combo_data)
        self.carregando_data()
        # Aciona o método de carregar transcrições
        self.combo_data.currentIndexChanged.connect(self.preenchendo_tabela)

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
        self.table = QTableWidget()
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
        self.table.setStyleSheet("""
            QTableView {
                font-size: 16px;
            }
            QHeaderView {
                font-size: 20px;
            }
        """)

        # Adiciona a tabela ao layout
        layout_vertical_transcricao.addWidget(self.table)

        # Adiciona uma barra de progresso
        self.progress_bar = self.progress_bar()

        self.progress_bar.hide()

        layout_vertical_transcricao.addWidget(self.progress_bar)

        # Adiciona o campo de anotação
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText('Anotação')
        self.text_edit.setStyleSheet(FONT_SIZE)
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
        button.setStyleSheet('background-color: {}; color: {}; padding: 10px; border: none; border-style: none;border-radius: 10px;{}'.format(COLOR_PRIMARY, COLOR_TERTIARY, FONT_SIZE))
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        return button
    
    def exportar_transcricoes(self):
        try:
            # Lendo o arquivo csv
            with open('src\config\historico.csv', 'r') as file:
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
                nome_arquivo = f'{data_selecionada.replace("/", "_")}.txt'
                with open(nome_arquivo, 'w') as file:
                    # Adicionando as transcrições ao arquivo
                    for data in dados_iter:
                        if data[0] == data_selecionada:
                            file.write(f'{data[1]}: {data[2]}\n')
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
            with open('src\config\historico.csv', 'r') as file:
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
                nome_arquivo = f'{data_selecionada.replace("/", "_")}.txt'

                # Unificando as transcrições
                transcricoes = ''
                for data in dados_iter:
                    if data[0] == data_selecionada:
                        transcricoes += f'{data[2]}\n'
                
                #envia para a api da openai
                client = OpenaiClient().return_client()
                system_prompt = "{Crie uma anotação longa e detalhada} and {Gere To Do se for necessário}"
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
                # Mensagem de sucesso
                QMessageBox.information(self, "Mensagem de Informação", f"Transcrições exportadas com sucesso para o arquivo {nome_arquivo}.", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            
            else:
                #Mensagem de info Qt
                QMessageBox.information(self, "Mensagem de Informação", "Selecione uma data para exportar as transcrições.", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar transcrições: {e}", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
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


            
        






