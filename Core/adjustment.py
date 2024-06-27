from Core.base import ChatGPT


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
