import os

import dotenv

from core.base import OpenAIUnique
from utils.patterns import singleton
from utils.validations import IMAGE_VALIDATIONS

dotenv.load_dotenv()


@singleton
class Dalle:
    _client = None

    @property
    def client(self):
        if self._client is None:
            self._set_client()
        return self._client

    def _set_client(self):
        api_key = os.environ.get("OPENAI_KEY")
        self._client = OpenAIUnique(api_key=api_key)

    def generate_image(self, prompt, size="1024x1024", quality="standard"):
        for field, value in zip(
                ["Prompt", "Size", "Quality"],
                [prompt, size, quality],
        ):
            if field in IMAGE_VALIDATIONS and IMAGE_VALIDATIONS[field][0](value):
                raise ValueError(IMAGE_VALIDATIONS[field][1])

        model = "dall-e-3" if size not in ("256x256", "512x512") else "dall-e-2"

        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
        )

        return response.data[0].url

    def update_image(self, prompt, image_byte, mask_byte, size="1024x1024"):
        for field, value in zip(
                ["Prompt", "Size"],
                [prompt, size],
        ):
            if field in IMAGE_VALIDATIONS and IMAGE_VALIDATIONS[field][0](value):
                raise ValueError(IMAGE_VALIDATIONS[field][1])

        response = self.client.images.edit(
            model="dall-e-2",
            image=image_byte,
            mask=mask_byte,
            prompt=prompt,
            n=1,
            size=size,
        )

        return response.data[0].url

    def generate_variations(self, prompt, image_byte, size="1024x1024"):
        for field, value in zip(
            ["Prompt", "Size"],
            [prompt, size],
        ):
            if field in IMAGE_VALIDATIONS and IMAGE_VALIDATIONS[field][0](value):
                raise ValueError(IMAGE_VALIDATIONS[field][1])

        response = self.client.images.create_variation(
            image=image_byte, n=2, model="dall-e-2", size=size
        )

        return response.data[0].url, response.data[1].url


if __name__ == "__main__":
    instance = Dalle()

    print(
        instance.generate_image(
            "Logo para empresa de Energia Solar com as inicias NMV (Novo Mundo Verde), Utilize somente a sigla como texto NMV",
            size="256x256",
        )
    )
