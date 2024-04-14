import pyaudio
import soundcard as sc
import wave
from services.config_service import ConfigService
import openai
import threading
from PyQt6.QtCore import pyqtSignal, QObject
import timeit
import numpy as np


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
        self.config_service = ConfigService()
        self.config = self.config_service.lendo_configuracoes()
        select_audio = self.config['selected_drivers_audio']
        speakers = sc.all_speakers()
        self.select_audio = next((m for m in speakers if m.id == select_audio), None)

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
        RATE = 44100
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME1 = "output1.wav"
        WAVE_OUTPUT_FILENAME2 = "output2.wav"

        # Inicializando o serviço de configuração
        self.config_service = ConfigService()

        # Definindo o arquivo de saída
        output_file = WAVE_OUTPUT_FILENAME1

        # Inicializando a lista de frames
        frames = []

        # Lendo o arquivo de configuração
        openai.api_key = self.config['openai_api_key']
        client = openai.Client(api_key=openai.api_key)

        try:
            # Repetindo a captura de áudio enquanto a função running() retornar True
            while running():
                # Capturando áudio
                with self.select_audio.recorder(samplerate=RATE) as recorder:
                    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                        data = recorder.record(numframes=CHUNK)
                        # Adicionando os frames capturados à lista de frames
                        frames.append(data)

                # Enviando o arquivo de áudio para a API da OpenAI
                threading.Thread(target=self.envia_audio_para_openai, args=(output_file, 1, np.int16, RATE, frames, client)).start()

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
    
    def envia_audio_para_openai(self, filename, channels, format, rate, frames, client):
        """
        Envia um arquivo de áudio para a API da OpenAI para transcrição.

        Parâmetros:
        - filename: O caminho do arquivo de áudio a ser enviado.

        Retorna:
        Nenhum valor de retorno.

        Lança:
        Nenhum erro é lançado explicitamente.

        """        
        # Convertendo os frames de numpy array para bytes
        frames_bytes = b''.join([np.int16(frame).tobytes() for frame in frames])

        # Salvando o arquivo de áudio
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(np.dtype(format).itemsize)  # get_sample_size is not needed as we're using numpy dtype
        wf.setframerate(rate)
        wf.writeframes(frames_bytes)

        # Enviando o arquivo de áudio para a API da OpenAI
        with open(filename, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file)
        # Enviando a transcrição para o sinal de transcrição
        threading.Thread(target=self.envia_transcricao, args=(transcription.text, filename, client)).start()
        wf.close()
    
    def envia_openai_corrigir(self, texto, audio_file, client):

        #print(texto)

        system_prompt = "Corrige o texto e remove uma palavra se não fizer sentido ou adiciona uma palavra se fizer sentido pelo contexto."
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

    def envia_transcricao(self, transcription, filename, client):
        """
        Envia a transcrição para o sinal de transcrição.
    
        Args:
            transcription (str): A transcrição a ser enviada.
    
        Returns:
            None
        """
        transcription = transcription.replace("...", " ")
        self.transcricao_original += transcription
        is_corrigido = False

        if self.contador_transcricao == 5:
            self.transcripton_signal.emit(transcription, is_corrigido, self.transcricao_original)
            transcription = self.envia_openai_corrigir(self.transcricao_original, filename, client)
            is_corrigido = True
            self.contador_transcricao = 0
    
        self.transcripton_signal.emit(transcription, is_corrigido, self.transcricao_original if is_corrigido else "")
        
        self.contador_transcricao += 1
        print(self.contador_transcricao)

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
