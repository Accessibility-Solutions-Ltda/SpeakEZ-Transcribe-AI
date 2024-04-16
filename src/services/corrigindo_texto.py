import openai
from services.openai_client import OpenaiClient
from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QMessageBox

class CorrigindoTexto(QThread):
    def __init__(self, texto):
        QThread.__init__(self)
        self.texto = texto
        self.resultado = ""

    def run(self):
        try:
            client = OpenaiClient().return_client()
            system_prompt = "Corrige e melhore o texto."
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
                        "content": self.texto
                    }
                ]
            )
            self.resultado = response.choices[0].message.content
        except Exception as e:
            # Exibe uma mensagem de erro pyqt
            QMessageBox.information(None, 'Erro', f"Erro ao corrigir texto: {e}")