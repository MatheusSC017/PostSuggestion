from Utils.types import Emojis
from Core.post import PostSuggestAssistant
from Core.adjustment import AdjustmentPostAssitant
from Core.translator import TranslatorAssistant


class OpenAIAssistants:
    adjustment_post = {}

    def __init__(self, model="gpt-3.5-turbo", basic_configs={}):
        self.model = model
        self.basic_configs = basic_configs

        if len(self.basic_configs.keys()) == 0:
            self.basic_configs = {
                "Emojis": Emojis.LOW,
                "Size": 200,
                "Type": "Products offering",
                "Language": "Portuguese"
            }

        self.post_assistant = PostSuggestAssistant(basic_configs=self.basic_configs, model=self.model)
        self.translate_assistant = TranslatorAssistant(basic_configs=self.basic_configs, model=self.model)

    def get_suggestion(self, product_characteristics='', **kwargs):
        for key, value in kwargs.items():
            self.basic_configs[key] = value
        self.post_assistant.basic_configs = self.basic_configs
        if product_characteristics:
            self.post_assistant.send_request(product_characteristics)
        return self.post_assistant.suggestions

    def adjustment(self, post, adjustment_characteristics):
        if post not in self.adjustment_post.keys():
            self.new_adjustment(post)

        return self.adjustment_post[post].send_request(adjustment_characteristics)

    def new_adjustment(self, post):
        self.adjustment_post[post] = AdjustmentPostAssitant(post=self.post_assistant.suggestions[post],
                                                            basic_configs=self.basic_configs,
                                                            model=self.model)

    def end_adjustment(self, post):
        if post in self.adjustment_post.keys():
            post_suggestion = self.adjustment_post[post].messages[-1]["content"]
            del self.adjustment_post[post]
            return post_suggestion
        raise Exception("Post not found")

    def translate_message(self, message):
        return self.translate_assistant.send_request(message)

    def reset(self):
        self.basic_configs = {
            "Emojis": Emojis.LOW,
            "Size": 200,
            "Type": "Products offering",
            "Language": "Portuguese"
        }
        self.adjustment_post = {}
        self.post_assistant = PostSuggestAssistant(basic_configs=self.basic_configs, model=self.model)
        self.translate_assistant = TranslatorAssistant(basic_configs=self.basic_configs, model=self.model)

    # Separate in a class ImageSuggest
    def generate_image(self):
        pass

    def improve_image(self):
        pass

    # Separate in a class to suggestion not relationed to post, but social media and business
    def get_suggest(self):
        pass


if __name__ == "__main__":
    assistants = OpenAIAssistants()

    # Drone 20x20cms, com capacidade de voo de até 100 metro de altitude, bateria com duração de 15 minutos, kit acompanhado 3 baterias, equipamento de manutenção, helices reservas e equipamentos de limpeza
    # Adicione ênfase a altitude de voo e adicione a informação sobre uma promoção com duração de 1 uma única semana
    # Adicione ênfase a capacidade da bateria e adicione a informação sobre uma promoção com duração de 1 um único dia
    # The product is on sale until the weekend, pay attention to the durability of the product and the good reviews received

    option = 0
    while option != 4:
        try:
            print("Choice an option:\n"
                  "1 - Get suggestions to post;\n"
                  "2 - Improve a suggested post;\n"
                  "3 - Translate a suggested post;\n"
                  "4 - Close;")
            option = int(input())

            if option == 1:
                print("Enter with the product/service characteristics: ")
                product = input()
                suggestions = assistants.get_suggestion(product_characteristics=product)
                for suggestion in suggestions:
                    print(f"\n{suggestion}")

            elif option == 2:
                print("Enter with the index of the suggestion: ")
                product = int(input())
                print("Enter with the adjustments requireds: ")
                adjustments = input()
                print(assistants.adjustment(1, adjustments))

            elif option == 3:
                print("Enter with the message that you want translate: ")
                message = input()
                print(assistants.translate_message(message))

            print("\n\n")

        except ValueError:
            print("Enter with a valid option!")
