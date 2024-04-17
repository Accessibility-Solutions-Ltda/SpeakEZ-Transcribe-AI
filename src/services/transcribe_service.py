import pyaudio
import wave
from services.config_service import ConfigService
from services.openai_client import OpenaiClient
import openai
import threading
from PyQt6.QtCore import pyqtSignal, QObject
import timeit
from datetime import datetime


class TranscribeService(QObject):
    transcripton_signal = pyqtSignal(str, bool, str)
    def __init__(self):
        """
        Inicializa uma nova instância da classe TranscribeService.

        Atributos:
        - transcribe (bool): Indica se a transcrição está ativada ou desativada.
        - config_service (ConfigService): Instância do serviço de configuração.
        - driver_select_audio: Resultado da função lendo_driver_select().

        """
        super().__init__()
        self.transcribe = False
        self.contador_transcricao = 0
        self.transcricao_original = ""
        self.palavra_chave = self.process_csv()
        self.lock = threading.Lock()
        self.config_service = ConfigService()
        #print(self.palavra_chave)

    def process_csv(self):
        """
        Processa o arquivo csv de palavra_chave.

        Este método processa o arquivo csv de palavra_chave e retorna uma lista de palavras-chave.
        """
        with open('src/config/palavra_chave.csv', 'r', encoding='utf-8') as file:
            #desconsiderando cabeçalho
            next(file)
            lines = file.read().splitlines()

        lista = ', '.join([word for line in lines for word in line.split(',')])
        return lista



    def captando_audio_streaming(self, running):
            """
            Função responsável por capturar áudio em streaming.

            Parâmetros:
            - running: uma função que retorna um valor booleano indicando se a captura de áudio deve continuar ou não.

            Retorna:
            Nenhum valor de retorno.
            """
            # Definindo as configurações de gravação de áudio
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 48000
            RECORD_SECONDS = 6
            WAVE_OUTPUT_FILENAME1 = "output1.wav"
            WAVE_OUTPUT_FILENAME2 = "output2.wav"

            # Inicializando o PyAudio
            p = pyaudio.PyAudio()

            # Definindo o arquivo de saída
            output_file = WAVE_OUTPUT_FILENAME1

            # Inicializando a lista de frames
            frames = []

            # Inicializando o cliente da OpenAI
            client = OpenaiClient().return_client()
            
            try:
                # Repetindo a captura de áudio enquanto a função running() retornar True
                while running():
                    data_hora_atual = datetime.now()
                    # Selecionando o driver de áudio
                    stream = p.open(format=FORMAT,
                                    channels=CHANNELS,
                                    rate=RATE,
                                    input=True,
                                    frames_per_buffer=CHUNK)

                    # Capturando áudio
                    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                        data = stream.read(CHUNK)
                        # Adicionando os frames capturados à lista de frames
                        frames.append(data)

                    # Enviando o arquivo de áudio para a API da OpenAI
                    threading.Thread(target=self.envia_audio_para_openai, args=(output_file, CHANNELS, FORMAT, RATE, frames, p, client, data_hora_atual)).start()

                    # Parando a captura de áudio
                    stream.stop_stream()
                    stream.close()

                    # Alterne entre os dois arquivos
                    if output_file == WAVE_OUTPUT_FILENAME1:
                        output_file = WAVE_OUTPUT_FILENAME2
                    else:
                        output_file = WAVE_OUTPUT_FILENAME1
                    frames = []

            # Lidando com exceções   
            except Exception as e:
                #print(f"Erro: {e}")
                pass
            finally:
                #print("Gravação de áudio é interrompida.")
                stream.stop_stream()
                stream.close()
                p.terminate()
    
    def envia_audio_para_openai(self, filename, channels, format, rate, frames, p, client, data_hora_atual):
        """
        Envia um arquivo de áudio para a API da OpenAI para transcrição.

        Parâmetros:
        - filename: O caminho do arquivo de áudio a ser enviado.

        Retorna:
        Nenhum valor de retorno.

        Lança:
        Nenhum erro é lançado explicitamente.

        """        
        # Salvando o arquivo de áudio
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

        # Enviando o arquivo de áudio para a API da OpenAI
        audio_file = open(filename, "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            prompt=self.palavra_chave
            )
        # Enviando a transcrição para o sinal de transcrição
        threading.Thread(target=self.envia_transcricao, args=(transcription.text, filename, client, data_hora_atual)).start()
        wf.close()
    
    def envia_openai_corrigir(self, texto, audio_file, client):

        #print(texto)

        system_prompt = "Corrige e melhore o texto especialmente em termos de palavra-chave.\n\nPalavras-chave: {}".format(self.palavra_chave)
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
                    "content": texto
                }
            ]
        )
        return response.choices[0].message.content

    def envia_transcricao(self, transcription, filename, client, data_hora_atual):
        """
        Envia a transcrição para o sinal de transcrição.
    
        Args:
            transcription (str): A transcrição a ser enviada.
    
        Returns:
            None
        """
        transcription = transcription.replace("...", " ")
        self.transcricao_original += transcription
    
        with self.lock:
            if self.contador_transcricao == 5:
                self.transcripton_signal.emit(transcription, False, "")
                transcription = self.envia_openai_corrigir(self.transcricao_original, filename, client)
                self.transcripton_signal.emit(transcription, True, self.transcricao_original)
                threading.Thread(target=self.salva_historico, args=(transcription, data_hora_atual)).start()
                self.transcricao_original = ""
                self.contador_transcricao = 0
            else:
                self.transcripton_signal.emit(transcription, False, "")
    
            self.contador_transcricao += 1
    
        #print(self.contador_transcricao)
    def lendo_driver_select(self):
            """
            Método responsável por ler o arquivo de configuração e selecionar o driver de áudio.

            Este método lê o arquivo de configuração e seleciona o driver de áudio
            para captura do áudio do microfone.

            Parâmetros:
                Nenhum parâmetro é necessário.

            Retorno:
                O ID do dispositivo selecionado.
            """
            # Lendo o arquivo de configuração
            config = self.config_service.lendo_configuracoes()
            select = config['selected_drivers_microphone']
            device_id = int(select)
            return device_id
    def salva_historico(self, transcription, data_hora_atual):
        """
        Salva a transcrição no arquivo de histórico.

        Este método salva a transcrição no arquivo de histórico, juntamente com a data e a hora da transcrição.

        Parâmetros: transcription (str): A transcrição a ser salva. data_hora_atual (float): A data e a hora da transcrição."""
        # Salvando a transcrição no arquivo csv de histórico
        with open('src/config/historico.csv', 'a', encoding='utf-8') as file:
            # data, hora, transcrição
            file.write(f"{data_hora_atual.date().strftime('%d/%m/%Y')}|{data_hora_atual.time().strftime('%H:%M:%S')}|{transcription}|\n")
