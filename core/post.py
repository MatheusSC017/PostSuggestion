import re

from core.base import ChatGPT
from utils.types import Emojis
from core.adjustment import AdjustmentPostAssitant
from core.translator import TranslatorAssistant

class PostSuggest(ChatGPT):
    adjustment_post = {}
    suggestions = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if len(self.basic_configs.keys()) == 0:
            self.basic_configs = {
                "Emojis": Emojis.LOW,
                "Size": 200,
                "Type": "Products offering",
                "Language": "Portuguese"
            }
        self.messages[0]['content'] = "You are a helpful assistant that suggests 3 examples of posts per request for " \
                                      "social media-oriented posts based on user-provided characteristics, posts must" \
                                      " be enclosed in double quotes."

        self.translate_assistant = TranslatorAssistant(basic_configs=self.basic_configs, model=self.model)

    def send_request(self, product_characteristics):
        post_suggestions = super().send_request(product_characteristics)
        post_suggestions = re.findall('\"(.+)\"', post_suggestions)
        self.suggestions.extend(post_suggestions)
        return post_suggestions

    def get_suggestion(self, product_characteristics=''):
        if product_characteristics:
            self.send_request(product_characteristics)
        return self.suggestions

    def new_adjustment(self, post):
        self.adjustment_post[post] = AdjustmentPostAssitant(post=self.suggestions[post],
                                                            basic_configs=self.basic_configs,
                                                            model=self.model)

    def translate_message(self, message):
        return self.translate_assistant.send_request(message)

    def end_adjustment(self, post):
        if post in self.adjustment_post.keys():
            post_suggestion = self.adjustment_post[post].messages[-1]["content"]
            del self.adjustment_post[post]
            return post_suggestion
        raise Exception("Post not found")

    def adjustment(self, post, adjustment_characteristics):
        if post not in self.adjustment_post.keys():
            self.new_adjustment(post)

        return self.adjustment_post[post].send_request(adjustment_characteristics)

    def reset(self):
        self.basic_configs = {
            "Emojis": Emojis.LOW,
            "Size": 200,
            "Type": "Products offering",
            "Language": "Portuguese"
        }
        self.messages_post = []
        self.adjustment_post = {}
        self.suggestions = []

    # Separate in a class ImageSuggest
    def generate_image(self):
        pass

    def improve_image(self):
        pass

    # Separate ina a Class to Translation
    def translate(self):
        pass

    # Separate in a class to suggestion not relationed to post, but social media and business
    def get_suggest(self):
        pass
