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
        """Load the appropriate system prompt based on class name."""
        class_name = self.__class__.__name__
        
        # Map class names to prompt files
        prompt_mapping = {
            "SpecWorker": "spec_worker_prompt.txt",
            "CodeWorker": "code_worker_prompt.txt",
            "ValidationWorker": "validation_worker_prompt.txt",
            "FeedbackWorker": "feedback_worker_prompt.txt"
        }
        
        if class_name not in prompt_mapping:
            raise ValueError(f"No prompt mapping for class: {class_name}")
        
        prompt_file = prompt_mapping[class_name]
        prompt_path = Path(__file__).parent.parent / "utilities" / "prompts" / prompt_file
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
            
        return prompt_path.read_text(encoding='utf-8')

    
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
        