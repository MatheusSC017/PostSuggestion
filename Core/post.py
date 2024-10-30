import re

from Core.base import ChatGPT


class PostSuggestAssistant(ChatGPT):
    suggestions = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.messages[0]["content"] = (
            "You are a helpful assistant that suggests 3 examples of posts per request for "
            "social media-oriented posts based on user-provided characteristics, posts must"
            " be enclosed in double quotes."
        )

    def get_suggestions(self, product_characteristics="", **kwargs):
        for key, value in kwargs.items():
            if key in self.basic_configs.keys():
                self.basic_configs[key] = value
        if product_characteristics:
            self.send_request(product_characteristics)
        return self.suggestions

    def send_request(self, product_characteristics):
        post_suggestions = super().send_request(product_characteristics)
        post_suggestions = re.findall('"(.+)"', post_suggestions)
        self.suggestions.extend(post_suggestions)
        return post_suggestions
