from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QSizePolicy, QTableWidget, QHeaderView, QTableWidgetItem
from PyQt6.QtWidgets import QTableWidget, QWidget
from services.config_service import ConfigService
import csv

class PalavraChave(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Configurações de palavra-chave')
        self.setMinimumSize(1024, 768)
        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Cria uma tabela com duas colunas
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(1)
        self.tabela.setHorizontalHeaderLabels(['Termos'])

        # Duas colunas no tamanho ajustado na toda tela
        self.tabela.horizontalHeader().setStretchLastSection(True)
        self.tabela.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        # Permite a edição dos itens da tabela
        self.tabela.setEditTriggers(QTableWidget.EditTrigger.DoubleClicked)
        self.lendo_tabela()
        self.preenchendo_tabela(self.lendo_tabela())
        layout.addWidget(self.tabela)

        # Botão para adicionar nova linha
        btn_adicionar = QPushButton('Adicionar Nova Linha')
        btn_adicionar.clicked.connect(self.adicionar_nova_linha)
        layout.addWidget(btn_adicionar)

        # Botão para salvar a tabela
        btn_salvar = QPushButton('Salvar')
        btn_salvar.clicked.connect(self.salvando_tabela)
        layout.addWidget(btn_salvar)
    
    def adicionar_nova_linha(self):
        row_count = self.tabela.rowCount()
        self.tabela.setRowCount(row_count + 1)
        self.tabela.setItem(row_count, 0, QTableWidgetItem(''))


    def abrir_janela_palavra_chave(self):
        """
        Abre a janela de configurações de palavra-chave.

        Retorna:
        Nenhum valor de retorno.
        """
        # Abrir uma janela de pyqt
        self.janela_palavra_chave = PalavraChave()
        self.janela_palavra_chave.show()
    
    def salvando_tabela(self):
        """
        Salva a tabela de palavra-chave em um arquivo CSV.

        Parâmetros:
        - filename: O nome do arquivo CSV para salvar os dados.

        Retorna:
        Nenhum valor de retorno.
        """
        filename = 'src/config/palavra_chave.csv'
        with open(filename, mode='w', newline='') as csvfile:
            fieldnames = ['termos']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for i in range(self.tabela.rowCount()):
                termo_original = self.tabela.item(i, 0).text()
                writer.writerow({'termos': termo_original})
    
    def lendo_tabela(self):
        """
        Lê a tabela de palavra-chave de um arquivo CSV.

        Parâmetros:
        - filename: O nome do arquivo CSV para ler os dados.

        Retorna:
        Uma lista de dicionários contendo os dados da tabela.
        """
        filename = 'src/config/palavra_chave.csv'
        with open(filename, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = []
            for row in reader:
                data.append(row)
        return data

    def preenchendo_tabela(self, data):
        """
        Preenche a tabela de palavra-chave com os dados lidos de um arquivo CSV.

        Retorna:
        Nenhum valor de retorno.
        """
        self.tabela.setRowCount(len(data))
        for i, row in enumerate(data):
            self.tabela.setItem(i, 0, QTableWidgetItem(row['termos']))



        