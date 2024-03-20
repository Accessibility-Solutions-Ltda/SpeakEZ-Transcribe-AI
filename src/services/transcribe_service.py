import pyaudio
import wave
from services.config_service import ConfigService
import openai
import threading
from PyQt6.QtCore import pyqtSignal, QObject
import timeit


class TranscribeService(QObject):
    transcripton_signal = pyqtSignal(str)
    class TranscribeService:
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

    def captando_audio_streaming(self, running):
            tempo_todo_metodo_start = timeit.default_timer()
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
            RATE = 44100
            RECORD_SECONDS = 5
            WAVE_OUTPUT_FILENAME1 = "output1.wav"
            WAVE_OUTPUT_FILENAME2 = "output2.wav"

            # Inicializando o serviço de configuração
            self.config_service = ConfigService()

            # Inicializando o PyAudio
            p = pyaudio.PyAudio()

            # Definindo o arquivo de saída
            output_file = WAVE_OUTPUT_FILENAME1

            # Inicializando a captura de áudio
            try:
                # Repetindo a captura de áudio enquanto a função running() retornar True
                while running():

                    # Selecionando o driver de áudio
                    stream = p.open(format=FORMAT,
                                    channels=CHANNELS,
                                    rate=RATE,
                                    input=True,
                                    frames_per_buffer=CHUNK)
                    
                    # Inicializando a lista de frames
                    frames = []

                    print("Recording audio...")

                    # Capturando áudio
                    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                        data = stream.read(CHUNK)
                        # Adicionando os frames capturados à lista de frames
                        frames.append(data)

                    print("Finished recording.")

                    # Parando a captura de áudio
                    stream.stop_stream()
                    stream.close()
                    tempo_salvando_arquivo_start = timeit.default_timer()
                    # Salvando o arquivo de áudio
                    wf = wave.open(output_file, 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))
                    wf.close()
                    tempo_salvando_arquivo_stop = timeit.default_timer()


                    # Enviando o arquivo de áudio para a API da OpenAI
                    threading.Thread(target=self.envia_para_openai, args=(output_file,)).start()

                    # Alterne entre os dois arquivos
                    if output_file == WAVE_OUTPUT_FILENAME1:
                        output_file = WAVE_OUTPUT_FILENAME2
                    else:
                        output_file = WAVE_OUTPUT_FILENAME1
                    tempo_todo_metodo_stop = timeit.default_timer()
                    print(f"Tempo de salvamento do arquivo: {tempo_salvando_arquivo_stop - tempo_salvando_arquivo_start}")
                    print(f"Tempo total do método: {tempo_todo_metodo_stop - tempo_todo_metodo_start}")

            # Lidando com exceções   
            except Exception as e:
                print(f"Erro: {e}")
            finally:
                print("Gravação de áudio é interrompida.")
                p.terminate()
    
    def envia_para_openai(self, filename):
        """
        Envia um arquivo de áudio para a API da OpenAI para transcrição.

        Parâmetros:
        - filename: O caminho do arquivo de áudio a ser enviado.

        Retorna:
        Nenhum valor de retorno.

        Lança:
        Nenhum erro é lançado explicitamente.

        """
        #Debugando
        print(f"Enviando {filename} para OpenAI...")

        tempo_todo_metodo_start = timeit.default_timer()

        # Lendo o arquivo de configuração
        config = self.config_service.lendo_configuracoes()
        openai.api_key = config['openai_api_key']

        # Enviando o arquivo de áudio para a API da OpenAI
        audio_file = open(filename, "rb")
        client = openai.Client(api_key=openai.api_key)
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file)
        tempo_todo_metodo_stop = timeit.default_timer()
        print(f"Tempo de envio para OpenAI: {tempo_todo_metodo_stop - tempo_todo_metodo_start}")
        # Enviando a transcrição para o sinal de transcrição
        self.envia_transcricao(transcription.text)


    def envia_transcricao(self, transcription):
            """
            Envia a transcrição para o sinal de transcrição.

            Args:
                transcription (str): A transcrição a ser enviada.

            Returns:
                None
            """
            self.transcripton_signal.emit(transcription)

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
