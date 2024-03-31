from openai import OpenAI
import copy
import json
import re


class Emojis:
    NO = "Zero emojis"
    LOW = "1 to 5 emojis"
    MEDIUM = "6 to 10 emojis"
    HIGH = "More 10 emojis"


class Configs:
    EMOJIS = "Number de emojis by Post"
    SIZE = "Size of the Post in characters"
    TYPE = "Main Post Topic"


class PostSuggest:
    model = ""
    client = None
    basic_configs = {
        "Emojis": Emojis.LOW,
        "Size": 200,
        "Type": "Products offering"
    }
    messages = []
    suggestions = []

    def __init__(self, api_key, model="gpt-3.5-turbo", basic_configs={}):
        self.model = model
        self.client = OpenAI(api_key=api_key)

        for key, value in basic_configs.items():
            self.basic_configs[key] = value

        system_config = {
            "role": "system",
            "content": "You are a helpful assistant that suggests 3 examples of posts per request for social "
                       "media-oriented posts based on user-provided characteristics, posts must be enclosed in double "
                       "quotes."
        }
        self.messages.append(system_config)

    def next(self, product_characteristics):
        user_request = copy.deepcopy(self.basic_configs)
        user_request['Characteristics'] = product_characteristics
        self.messages.append({
            "role": "user",
            "content": "Rules: \n\n" + '\n'.join([': '.join((getattr(Configs, k.upper(), k), str(v)))
                                                  for k, v in user_request.items()])
        })
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0,
        )
        post_suggestions = json.loads(response.model_dump_json())["choices"][0]["message"]["content"]
        
        self.messages.append({"role": "assistant", "content": post_suggestions})
        post_suggestions = re.findall('\"(.+)\"', post_suggestions)
        self.suggestions.extend(post_suggestions)
        return post_suggestions

    def get_suggestion(self, product_characteristics=''):
        if product_characteristics:
            self.next(product_characteristics)
        return self.suggestions


if __name__ == "__main__":
    import dotenv
    import os

    dotenv.load_dotenv()

    api_key = os.environ.get('OPENAI_KEY')

    post_suggest = PostSuggest(api_key=api_key)

    suggestions = post_suggest.get_suggestion(
        product_characteristics="Drone 20x20cms, com capacidade de voo de até 100 metro de altitude, bateria com "
                                "duração de 15 minutos, kit acompanhado 3 baterias, equipamento de manutenção, helices "
                                "reservas e equipamentos de limpeza")
    for suggestion in suggestions:
        print("-" * 25)
        print(suggestion)

    print("*" * 50)
    #
    # suggestions = post_suggest.get_suggestion(
    #     product_characteristics="The product is on sale until the weekend, pay attention to the durability of the "
    #                             "product and the good reviews received")
    # for suggestion in suggestions:
    #     print(suggestion)

