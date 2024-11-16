import json

from core.base import ChatGPT


class Chat(ChatGPT):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.messages[0]["content"] = (
            "You are a helpful assistant that will help with questions relationed to social media, example: posts, "
            "events, timelines and others"
        )

    def send_request(self, message):
        self.messages.append({"role": "user", "content": message})

        response = self.client.chat.completions.create(
            model=self.model, messages=self.messages, temperature=0
        )

        response = json.loads(response.model_dump_json())["choices"][0]["message"][
            "content"
        ]
        self.messages.append({"role": "assistant", "content": response})
        return response


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv()

    chat = Chat()

    print("Initializing Chat")
    while True:
        message = input()
        if message == "exit":
            break

        response = chat.send_request(message)
        print(f"\nAssistant: {response}\n")
