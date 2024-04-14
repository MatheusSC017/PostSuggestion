import json
import copy

from ..utils.types import Configs


class AdjustmentPost:
    def __init__(self, client, model, post, basic_configs):
        self.client = client
        self.model = model
        self.post = post
        self.basic_configs = basic_configs

        system_config = {
            "role": "system",
            "content": f"You are a helpful assistant that improve posts for social media based in adjustments "
                       f"requested by the user. \n Post: {post} \n The response must contain only the post suggested"
        }
        self.messages = [system_config, ]

    def adjustment(self, adjustment_characteristics):
        user_request = copy.deepcopy(self.basic_configs)
        user_request['Adjustment requests'] = adjustment_characteristics

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
        post_suggestion = json.loads(response.model_dump_json())["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": post_suggestion})

        return post_suggestion
