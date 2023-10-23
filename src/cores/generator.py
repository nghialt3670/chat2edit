import openai


class OpenAIGenerator:
    def __init__(self, model: str, api_key: str) -> None:
        self.model = model
        self.api_key = api_key

    def generate(self, prompt: str) -> str:
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that help create structured programs base on provided instructions."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
