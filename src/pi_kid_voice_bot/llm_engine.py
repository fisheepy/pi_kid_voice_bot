"""LLM-backed rule engines."""

from __future__ import annotations

import importlib
import importlib.util
import os


class LLMDependencyError(RuntimeError):
    """Raised when LLM optional dependencies are unavailable."""


class ChatGPTRuleEngine:
    """Rule engine backed by OpenAI ChatGPT API."""

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        system_prompt: str = "你是一个面向儿童的温柔语音助手，请用简短、友好的中文回答。",
    ) -> None:
        if importlib.util.find_spec("openai") is None:
            raise LLMDependencyError(
                "Missing optional dependency 'openai'. Install with: pip install -e .[llm]"
            )

        openai = importlib.import_module("openai")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise LLMDependencyError("OPENAI_API_KEY is not set.")

        self._client = openai.OpenAI(api_key=api_key)
        self._model = model
        self._system_prompt = system_prompt

    def reply(self, text: str) -> str:
        normalized = text.strip()
        if not normalized:
            return "我没听清楚，你可以再说一遍吗？"

        response = self._client.responses.create(
            model=self._model,
            input=[
                {"role": "system", "content": self._system_prompt},
                {"role": "user", "content": normalized},
            ],
        )
        output_text = getattr(response, "output_text", "")
        if not output_text:
            return "我刚刚有点走神了，我们再试一次好吗？"
        return output_text.strip()
