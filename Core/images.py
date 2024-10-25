import os
import urllib

import dotenv

from Core.base import OpenAIUnique

dotenv.load_dotenv()


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

    def generate_image(self, prompt, name, size="1024x1024", quality="standard"):
        if size not in ("256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"):
            raise ValueError(
                'The size must be between the listed values: ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"], '
                "if a value is not provided the generated image will be of the proportions 1024x1024"
            )
        if quality not in ("standard", "hd"):
            raise ValueError(
                'The quality must be between the listed values: ["standard", "hd"], if a value is not provided the generated '
                "image will be of the quality standard"
            )

        model = "dall-e-3" if size not in ("256x256", "512x512") else "dall-e-2"

        response = self.client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
        )

        urllib.request.urlretrieve(response.data[0].url, f"../Images/{name}.jpg")
        return response.data[0].url

    def update_image(self, prompt, image, mask, size="1024x1024"):
        if size not in ("256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"):
            raise ValueError(
                'The size must be between the listed values: ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"], '
                "if a value is not provided the generated image will be of the proportions 1024x1024"
            )

        response = self.client.images.edit(
            model="dall-e-2",
            image=image,
            mask=mask,
            prompt=prompt,
            n=1,
            size=size,
        )

        return response.data[0].url


if __name__ == "__main__":
    instance = Dalle()

    print(
        instance.generate_image(
            "Logo para empresa de Energia Solar com as inicias NMV (Novo Mundo Verde), Utilize somente a sigla como texto",
            "NMV",
            size="256x256",
        )
    )
