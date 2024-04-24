from core.base import ChatGPT


class AdjustmentPostAssitant(ChatGPT):
    def __init__(self, post, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.post = post
        self.messages[0]['content'] = f"You are a helpful assistant that improve posts for social media based in " \
                                      f"adjustments requested by the user. \n Post: {post} \n The response must " \
                                      f"contain only the post suggested"

    def send_request(self, message):
        return super().send_request(message)
