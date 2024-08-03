from Core.base import ChatGPT
from Utils.types import Configs
import copy
import json


class AdjustmentPostAssitant(ChatGPT):
    undo_history = []
    adjusted_post = []

    def __init__(self, post, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.adjusted_post.append(post)
        self.messages[0]['content'] = f"You are a helpful assistant that improve posts for social media based in " \
                                      f"adjustments requested by the user. \n Post: {post} \n The response must " \
                                      f"contain only the post suggested"

    def send_request(self, message):
        new_post = super().send_request(message)
        self.undo_history = []
        self.adjusted_post.append(new_post)
        return new_post

    def undo(self):
        if len(self.adjusted_post) > 1 and len(self.messages) > 1:
            self.adjusted_post.pop()
            for _ in range(2):
                self.undo_history.append(self.messages.pop())

    def redo(self):
        if len(self.adjusted_post) and len(self.undo_history):
            for _ in range(2):
                self.messages.append(self.undo_history.pop())
            self.adjusted_post.append(self.messages[-1]["content"])


class AdjustmentPostAssitantWithoutHistory(ChatGPT):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages[0]['content'] = f"You are a helpful assistant that improve posts for social media based in " \
                                      f"adjustments requested by the user. The response must contain only the post " \
                                      f"suggested"

    def send_request(self, message):
        pass

    def adjust_post(self, post, adjustments, **kwargs):
        for key, value in kwargs.items():
            self.basic_configs[key] = value
        user_request = copy.deepcopy(self.basic_configs)
        user_request['Original post'] = post
        user_request['Adjustments'] = adjustments
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
        response = json.loads(response.model_dump_json())["choices"][0]["message"]["content"]

        self.messages.append({"role": "assistant", "content": response})
        return response
