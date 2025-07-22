import os
import yaml
from typing import Optional, Dict, Any

from jinja2 import Template, TemplateError


class PromptKeyError(Exception):
    """Raised when prompt key is not found in YAML file."""


class PromptEngineError(Exception):
    """Base Exception class for prompt engine errors."""


class PromptEngine:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, prompt_dir: Optional[str] = None):

        if not hasattr(self, "_initialized") or not self._initialized:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.prompt_dir = prompt_dir or os.path.join(script_dir, "prompts")

            self._initialized = True

    def _file_path(self, filename: str, extension: str = "yaml") -> str:
        return os.path.join(self.prompt_dir, f"{filename.strip()}.{extension}")

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        if not filename or not filename.strip():
            raise ValueError("Filename cannot be empty")

        filepath = self._file_path(filename)

        with open(filepath) as f:
            data = yaml.safe_load(f)
        return data

    async def get_prompt(
        self, filename: str, prompt_key: str, **prompt_variables: Any
    ) -> str:
        prompt_data = self._load_yaml(filename=filename)

        if prompt_key not in prompt_data:
            raise PromptKeyError(
                f"Prompt key {prompt_key} not found in {filename}.yaml"
            )

        template = Template(prompt_data[prompt_key])
        try:
            return template.render(**prompt_variables)
        except KeyError:
            raise ValueError(f"Missing required Variables in Template")
        except TemplateError:
            raise ValueError("Template rendering Error")


prompt_engine = PromptEngine()
