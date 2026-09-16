from mlx_lm import load, generate


class LocalModel:
    def __init__(self, model_name: str):
        self.model_name = model_name
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