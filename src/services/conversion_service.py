from PyQt6.QtCore import QThread
from services.openai_client import OpenaiClient
from services.config_service import ConfigService
from openai import OpenAI
import pygame
import os
from pathlib import Path
import time
import threading
import datetime
class ConvertendoTextoEmAudio(QThread):
    """
    Classe responsável por converter texto em áudio.

    Métodos:
        run(): Executa a conversão de texto em áudio.
    """
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.config = ConfigService().lendo_configuracoes()

    def run(self):
        try:
            # Inicializando o cliente da OpenAI
            client = OpenaiClient().return_client()

            threading.Thread(target=self.salvar_no_csv, args=(self.text,)).start()

            voice = self.config['style_voice']

            # Faz a solicitação para a API OpenAI para gerar o áudio a partir do texto
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=self.text
            )

            # Obtém o diretório do script
            script_dir = Path(__file__).resolve().parent

            # Define o caminho completo do arquivo temporário
            temp_audio_path = script_dir / "temp_audio.mp3"

            # Salva o áudio no arquivo temporário
            with open(temp_audio_path, "wb") as f:
                f.write(response.content)

            # Reproduz o áudio usando pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.music.load(temp_audio_path)
            pygame.mixer.music.set_volume(float(self.config['volume_audio']))
            pygame.mixer.music.play()

            # Aguarda a reprodução do áudio terminar
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            # Encerra o Pygame
            pygame.mixer.quit()

            # Remove o arquivo temporário após a reprodução
            os.remove(temp_audio_path)

        except Exception as e:
            print("Erro ao reproduzir áudio:", e)

    def salvar_no_csv(self, text):
        data_hora_atual = datetime.datetime.now()
        text = text.replace('\n', ' ')
        with open('src/config/historico.csv', 'a', encoding='utf-8') as file:
            # data, hora, transcrição
            file.write(f"{data_hora_atual.date().strftime('%d/%m/%Y')}|{data_hora_atual.time().strftime('%H:%M:%S')}||{text}\n")

