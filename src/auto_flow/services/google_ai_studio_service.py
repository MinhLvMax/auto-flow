from google import genai
from src.auto_flow.config import GOOGLE_API_KEY

class GoogleAIStudioService:
    def __init__(self, api_key=GOOGLE_API_KEY):
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)
        pass

    def get_list_model(self, supported_action='generateContent'):
        models = []
        for model in self.client.models.list():
            if supported_action in model.supported_actions:
                models.append(model)
        print(models)
        return models

    def single_chat(self, model_id: str, prompt: str, system_msg:str = ''):
        response = self.client.models.generate_content(
            model=model_id,
            config={"system_instruction": system_msg},
            contents=prompt
        )
        return response.text


if __name__ == '__main__':
    gass = GoogleAIStudioService(api_key=GOOGLE_API_KEY)
    # gass.get_list_model()
    gass.single_chat('models/gemini-2.5-flash', 'Xin chào, bạn là ai?')