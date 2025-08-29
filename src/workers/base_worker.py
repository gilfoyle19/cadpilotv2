from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional
from loguru import logger
import sys

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utilities.llm_client import llm_client
from src.config.openrouter_models import OpenRouterModel

class BaseWorker(ABC):
    """Abstract base class for workers."""

    def __init__(self, model: Optional[OpenRouterModel] = None):
        self.model = model
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        "Load system prompt from a txt file."
        prompt_name = self.__class__.__name__.replace("Worker", "").lower()
        prompt_path = Path(__file__).parent.parent / "utilities"/ "prompts"/ f"{prompt_name}_worker_prompt.txt"
        return prompt_path.read_text(encoding="utf-8")
    
    @abstractmethod
    async def execute(self, input_data: Any) -> Any:
        """Main Execution method. Shall be implemented by subclasses."""
        pass

    async def _call_llm(self, messages:list, **kwargs) -> str:
        "Helper method to call the llm client with error handling."
        try:
            return await llm_client.chat_completion(
                messages,
                model = self.model,
                **kwargs
            )
        except Exception as e:
            logger.error(f"{self.__class__.__name__} LLM call failed: {e}")
            raise
        