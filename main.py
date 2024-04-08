from openai import OpenAI
import copy
import json
import re

from utils.types import Emojis, Configs
from adjustment import AdjustmentPost


class PostSuggest:
    model = ""
    client = None
    basic_configs = {
        "Emojis": Emojis.LOW,
        "Size": 200,
        "Type": "Products offering",
        "Language": "Portuguese"
    }
    messages_post = []
    adjustment_post = {}
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
        self.messages_post.append(system_config)

    def next(self, product_characteristics):
        user_request = copy.deepcopy(self.basic_configs)
        user_request['Characteristics'] = product_characteristics
        self.messages_post.append({
            "role": "user",
            "content": "Rules: \n\n" + '\n'.join([': '.join((getattr(Configs, k.upper(), k), str(v)))
                                                  for k, v in user_request.items()])
        })
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages_post,
            temperature=0,
        )
        post_suggestions = json.loads(response.model_dump_json())["choices"][0]["message"]["content"]

        self.messages_post.append({"role": "assistant", "content": post_suggestions})
        post_suggestions = re.findall('\"(.+)\"', post_suggestions)
        self.suggestions.extend(post_suggestions)
        return post_suggestions

    def get_suggestion(self, product_characteristics=''):
        if product_characteristics:
            self.next(product_characteristics)
        return self.suggestions

    def new_adjustment(self, post):
        self.adjustment_post[post] = AdjustmentPost(self.client, self.model, self.suggestions[post], self.basic_configs)

    def end_adjustment(self, post):
        if post in self.adjustment_post.keys():
            post_suggestion = self.adjustment_post[post].messages[-1]["content"]
            del self.adjustment_post[post]
            return post_suggestion
        raise Exception("Post not found")

    def adjustment(self, post, adjustment_characteristics):
        if post not in self.adjustment_post.keys():
            self.new_adjustment(post)

        return self.adjustment_post[post].adjustment(adjustment_characteristics)


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

    print(post_suggest.adjustment(1, "Adicione ênfase a altitude de voo e adicione a informação sobre uma promoção "
                                     "com duração de 1 uma única semana"))

    print(post_suggest.adjustment(2, "Adicione ênfase a capacidade da bateria e adicione a informação sobre uma promoção "
                                     "com duração de 1 um único dia"))

    print("*" * 50)

    suggestions = post_suggest.get_suggestion(
        product_characteristics="The product is on sale until the weekend, pay attention to the durability of the "
                                "product and the good reviews received")
    for suggestion in suggestions:
        print(suggestion)

