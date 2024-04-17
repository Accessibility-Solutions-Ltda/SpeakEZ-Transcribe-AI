from services.config_service import ConfigService
import openai


class OpenaiClient:
    def return_client(self):
        config = ConfigService().lendo_configuracoes()
        openai.api_key = config['openai_api_key']
        client = openai.Client(api_key=openai.api_key)
        return client