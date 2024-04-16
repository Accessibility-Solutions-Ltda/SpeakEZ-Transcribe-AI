from PyQt6.QtCore import QThread
from services.openai_client import OpenaiClient
from openai import OpenAI
import pygame
import os
from pathlib import Path
import time

class ConvertendoTextoEmAudio(QThread):
    """
    Classe responsável por converter texto em áudio.

    Métodos:
        run(): Executa a conversão de texto em áudio.
    """
    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        try:
            # Inicializando o cliente da OpenAI
            client = OpenaiClient().return_client()

            # Faz a solicitação para a API OpenAI para gerar o áudio a partir do texto
            response = client.audio.speech.create(
                model="tts-1",
                voice="onyx",
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
