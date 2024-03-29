from openai import OpenAI
import os
import json
import re


class PostSuggest:
    model = ""
    client = None
    messages = []
    suggestions = []

    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.model = model
        self.client = OpenAI(api_key=api_key)
        system_config = "You are a helpful assistant that suggests 3 examples per request for social media-oriented " \
                        "product posts with a justify based on user-provided characteristics."
        self.messages.append({"role": "system", "content": system_config})

    def next(self, product_characteristics):
        self.messages.append({"role": "user", "content": product_characteristics})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0,
        )
        suggestions = json.loads(response.model_dump_json())["choices"][0]["message"]["content"]

        self.messages.append({"role": "assistant", "content": suggestions})

        suggestions = re.findall('\"(.+)\": \"(.+)\"', suggestions)
        self.suggestions.extend(suggestions)
        return suggestions

    def get_suggestion(self, product_characteristics=''):
        if product_characteristics:
            self.next(product_characteristics)
        return self.suggestions


if __name__ == "__main__":
    import dotenv
    import os

    dotenv.load_dotenv()

    api_key = os.environ.get('OPENAI_KEY')

    post_suggest = PostSuggest(api_key='')

    suggestions = post_suggest.get_suggestion(
        product_characteristics="Drone 20x20cms, com capacidade de voo de até 100 metro de altitude, bateria com "
                                "duração de 15 minutos, kit acompanhado 3 baterias, equipamento de manutenção, helices "
                                "reservas e equipamentos de limpeza")
    for suggestion in suggestions:
        print(suggestion)

    suggestions = post_suggest.get_suggestion(
        product_characteristics="The product is on sale until the weekend, pay attention to the durability of the "
                                "product and the good reviews received")
    for suggestion in suggestions:
        print(suggestion)
