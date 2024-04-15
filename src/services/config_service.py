import toml
import pyaudio
import os

PATH_CONFIG = 'src/config/config.toml'
class ConfigService:
    def __init__(self):
        # Registrando drivers de áudio existentes
        self.audio = pyaudio.PyAudio()

    def verificando_arquivo_configuracao(self):
        """
        Verifica se o arquivo de configuração existe e cria um novo arquivo se não existir.
        Registra os drivers de áudio existentes.

        Parâmetros:
        - self: A instância do objeto.

        Retorna:
        Nenhum valor de retorno.
        """
        # Verificando se arquivo de configuração existe
        try:
            with open(PATH_CONFIG, 'r', encoding='iso-8859-1') as _:
                #print('Arquivo de configuração encontrado.')
                pass
        except FileNotFoundError:
            # Verificando se o diretório de configuração existe
            if not os.path.exists('src/config/'):
                # Criando diretório de configuração
                os.makedirs('src/config/')
            # Criando arquivo de configuração
            with open(PATH_CONFIG, 'w', encoding='iso-8859-1') as _:
                self.definir_default_drivers_openai()
            # Criando seção config['openai_api_key']
            config = toml.load(open(PATH_CONFIG, 'r', encoding='iso-8859-1'))
            config['openai_api_key'] = ''
            with open(PATH_CONFIG, 'w', encoding='iso-8859-1') as file:
                toml.dump(config, file)
        # Registrando drivers de áudio existentes
        self.registrando_drivers_audio()

        #Criando csv de palavra chave
        try:
            with open('src/config/palavra_chave.csv', 'r') as _:
                #print('Arquivo de palavra chave encontrado.')
                pass
        except FileNotFoundError:
            with open('src/config/palavra_chave.csv', 'w') as file:
                file.write('termo_original,termo_substituto\n')
                #print('Arquivo de palavra chave criado.')
        
        #Criando csv de histórico
        try:
            with open('src/config/historico.csv', 'r') as _:
                #print('Arquivo de histórico encontrado.')
                pass
        except FileNotFoundError:
            with open('src/config/historico.csv', 'w') as file:
                file.write('data|hora|transcricao\n')
                #print('Arquivo de histórico criado.')



    def registrando_drivers_audio(self):
        """
        Registra os drivers de áudio existentes.

        Este método registra os drivers de áudio disponíveis no sistema e os salva em um arquivo de configuração.
        Os drivers de microfone são salvos na seção 'drivers_microphone' e os drivers de áudio são salvos na seção 'drivers_audio'.

        Returns:
            None
        """

        # Carrega o arquivo de configuração existente
        config = toml.load(open(PATH_CONFIG, 'r', encoding='iso-8859-1'))

        # Cria uma nova seção para os drivers de microfone
        config['drivers_microphone'] = {}

        # Cria uma nova seção para os drivers de áudio
        config['drivers_audio'] = {}

        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                # Salvando drivers de microfone em arquivo de configuração
                config['drivers_microphone'][f"{i}"] = device_info['name']
            elif device_info['maxOutputChannels'] > 0:
                # Salvando drivers de áudio em arquivo de configuração
                config['drivers_audio'][f"{i}"] = device_info['name']

        # Salva o arquivo de configuração
        with open(PATH_CONFIG, 'w', encoding='iso-8859-1') as file:
            toml.dump(config, file)

        self.audio.terminate()
    
    def definir_default_drivers_openai(self):
        """
        Define os drivers de áudio e microfone padrão do sistema operacional.

        Este método define os drivers de áudio e microfone padrão do sistema operacional e os salva em um arquivo de configuração.

        Returns:
            None
        """
        # Carrega o arquivo de configuração existente
        config = toml.load(open(PATH_CONFIG, 'r', encoding='iso-8859-1'))

        # Verifica se os drivers padrão já estão definidos
        if 'selected_drivers_audio' not in config:
            config['selected_drivers_audio'] = self.audio.get_default_input_device_info()['index']
        if 'selected_drivers_microphone' not in config:
            config['selected_drivers_microphone'] = self.audio.get_default_output_device_info()['index']
        config['select_model_gpt_transcribe'] = 'gpt-3.5-turbo-0125'
        config['select_model_gpt_correct'] = 'gpt-3.5-turbo-0125'
        config['list_models'] = ['gpt-4-turbo', 'gpt-3.5-turbo-0125', "gpt-4-turbo-preview", "gpt-4"]

        # Salva o arquivo de configuração
        with open(PATH_CONFIG, 'w', encoding='iso-8859-1') as file:
            toml.dump(config, file)

    def lendo_configuracoes(self):
        """
        Lê as configurações do arquivo de configuração e retorna um dicionário com as configurações.

        Returns:
            dict: Um dicionário contendo as configurações lidas do arquivo de configuração.
        """
        config = toml.load(open(PATH_CONFIG, 'r', encoding='iso-8859-1'))
        return config
    
    def salvando_configuracoes(self, new_config):
        """
        Atualiza e salva as configurações em um arquivo.

        Args:
            new_config (dict): Um dicionário contendo as configurações a serem atualizadas.

        Returns:
            dict: As configurações atualizadas.

        """
        # Carrega as configurações existentes
        with open(PATH_CONFIG, 'r', encoding='iso-8859-1') as file:
            config = toml.load(file)

        # Atualiza as configurações
        config.update(new_config)

        # Salva as configurações atualizadas
        with open(PATH_CONFIG, 'w', encoding='iso-8859-1') as file:
            toml.dump(config, file)

        return config
