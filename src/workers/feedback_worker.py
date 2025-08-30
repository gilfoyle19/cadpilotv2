from typing import Dict, Any
from loguru import logger

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.workers.base_worker import BaseWorker

class FeedbackWorker(BaseWorker):
    """Analyzes validation errors and provides feedback for code improvement."""

    async def execute(self, generated_code: str, validation_result: Dict[str, Any], specification: Dict[str, Any]) -> str:
        """
        Generate feedback for improving the failed code generation."""
        
        logger.info("Generating feedback for failed validation...")

        error_message = validation_result.get("error", "Unknown error") # Extract error message

        messages = [
            {"role": "system", "content": self.system_prompt},  # FROM feedback_worker_prompt.txt
            {"role": "user", "content": self._build_prompt(generated_code, error_message, specification)}
        ]

        feedback = await self._call_llm(messages, temperature=0.5, max_tokens=500)
        logger.success(f"Generated feedback: {feedback[:100]}...")

        return feedback
    
    def _build_prompt(self, code: str, error: str, spec: Dict[str, Any]) -> str:
        """Build the feedback request prompt."""
        import json

        return f"""
Generated code failed validation. Please provide specific feedback to improve it.

ERROR: {error}

ORIGINAL SPECIFICATION:
{json.dumps(spec, indent=2)}

FAILED CODE:
```python
{code}

Please provide constructive feedback on how to fix the code to meet the specification. Focusing on:

1. Specific syntax errors.
2. CadQuery API usage issues.
3. Parameter handling problems.
4. Geomertic construction logic errors.
"""
