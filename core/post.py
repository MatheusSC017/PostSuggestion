import copy
import json

from core.base import ChatGPT
from utils.types import Configs


class PostSuggestAssistant(ChatGPT):
    suggestions = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.messages[0]["content"] = (
            "You are a helpful assistant that suggests 3 examples of posts per request for social media-oriented posts "
            "based on user-provided characteristics, posts must be returned in json format. You must follow the "
            "required number of characters (Size), language and number of emojis allowed"
        )

    def send_request(self, message, **kwargs):
        for key, value in kwargs.items():
            self.basic_configs[key] = value

        user_request = copy.deepcopy(self.basic_configs)
        user_request["Characteristics"] = message
        self.messages.append(
            {
                "role": "user",
                "content": "Rules: \n\n"
                + "\n".join(
                    [
                        ": ".join((getattr(Configs, k.upper(), k), str(v)))
                        for k, v in user_request.items()
                    ]
                ),
            }
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0,
            response_format={"type": "json_object"},
        )
        response = json.loads(response.model_dump_json())["choices"][0]["message"][
            "content"
        ]
        self.messages.append({"role": "assistant", "content": response})

        response = json.loads(response)
        post_suggestions = [list(post.values())[0] for post in response["posts"]]
        self.suggestions.extend(post_suggestions)
        return self.suggestions
