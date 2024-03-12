import openai
from openai import OpenAI
from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    def __call__(
        self, 
        prompt: str
    ) -> str:
        pass


class OpenAILLM(LLM):
    def __init__(
        self, 
        api_key: str,
    ) -> None:
        self.client = OpenAI(api_key=api_key)

    def __call__(
        self, 
        prompt: str
    ) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are going to write python code that satisfy the instruction"
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content
    


