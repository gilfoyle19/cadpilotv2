from typing import Dict, Any, Optional
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.workers.base_worker import BaseWorker

from loguru import logger

class CodeWorker(BaseWorker):
    """Generates CadQuery code from evaluated specifications."""
    
    async def execute(self, specification: Dict[str, Any], feedback: Optional[str] = None) -> str:
        """
        Generate CadQuery code from specification with pre-calculated values.
        """
        # Build the user-specific part of the prompt
        user_prompt = self._build_user_prompt(specification, feedback)
        
        # Use the system prompt that was loaded from file by BaseWorker
        messages = [
            {"role": "system", "content": self.system_prompt},  #FROM code_worker_prompt.txt
            {"role": "user", "content": user_prompt}            #SPECIFIC REQUEST
        ]
        
        generated_code = await self._call_llm(messages, temperature=0.3, max_tokens=5000)
        self._validate_code_structure(generated_code)
        
        logger.success(f"Generated code ({len(generated_code)} characters)")
        return generated_code
    
    def _build_user_prompt(self, spec: Dict[str, Any], feedback: Optional[str]) -> str:
        """Build the user part of the prompt (specific to this request)."""
        import json
        
        base_prompt = f"Generate CadQuery code for this specification:\n\n{json.dumps(spec, indent=2)}"
        
        if feedback:
            base_prompt += f"\n\nINCORPORATE THIS FEEDBACK:\n{feedback}"
        
        return base_prompt
    
    def _validate_code_structure(self, code: str):
        """Basic validation of generated code."""
        if 'import cadquery' not in code:
            logger.warning("Generated code may be missing cadquery import")
        if 'result =' not in code:
            logger.warning("Generated code may be missing 'result' variable")