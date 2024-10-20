from Core.adjustment import AdjustmentPostAssitant
from Core.post import PostSuggestAssistant
from Core.translator import TranslatorAssistant
from Utils.types import Emojis


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
                "Language": "Portuguese",
            }

        self.post_assistant = PostSuggestAssistant(
            basic_configs=self.basic_configs, model=self.model
        )
        self.translate_assistant = TranslatorAssistant(
            basic_configs=self.basic_configs, model=self.model
        )

    def get_suggestion(self, product_characteristics="", **kwargs):
        for key, value in kwargs.items():
            self.basic_configs[key] = value
        self.post_assistant.basic_configs = self.basic_configs
        if product_characteristics:
            self.post_assistant.send_request(product_characteristics)
        return self.post_assistant.suggestions

    def adjustment(self, post, adjustment_characteristics, **kwargs):
        if post not in self.adjustment_post.keys():
            self.new_adjustment(post, **kwargs)

        return self.adjustment_post[post].send_request(adjustment_characteristics)

    def new_adjustment(self, post, **kwargs):
        for key, value in kwargs.items():
            self.basic_configs[key] = value

        self.adjustment_post[post] = AdjustmentPostAssitant(
            post=self.post_assistant.suggestions[post],
            basic_configs=self.basic_configs,
            model=self.model,
        )

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
            "Language": "Portuguese",
        }
        self.adjustment_post = {}
        self.post_assistant = PostSuggestAssistant(
            basic_configs=self.basic_configs, model=self.model
        )
        self.translate_assistant = TranslatorAssistant(
            basic_configs=self.basic_configs, model=self.model
        )

    # Separate in a class ImageSuggest
    def generate_image(self):
        pass

    def improve_image(self):
        pass

    # Separate in a class to suggestion not relationed to post, but social media and business
    def get_suggest(self):
        pass
