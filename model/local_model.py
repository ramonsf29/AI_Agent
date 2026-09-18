from mlx_lm import load, generate
import os

class LocalModel:
    def __init__(self, model_name: str):
        self.model_name = model_name
        os.environ["HF_HUB_OFFLINE"] = "1"
        self.model, self.tokenizer = load(model_name)

    def generate(self, messages: list[dict], max_tokens: int = 600) -> str:
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        response = generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
        )

        return response