import json
import re
from typing import Dict, Any
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.workers.base_worker import BaseWorker

from loguru import logger

class SpecWorker(BaseWorker):
    """Converts natural language to structured JSON specification."""
    
    async def execute(self, natural_language_prompt: str) -> Dict[str, Any]:
        """
        Convert natural language to structured JSON specification.
        The LLM will calculate all values - we just validate JSON structure.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": natural_language_prompt}
        ]
        
        llm_response = await self._call_llm(messages, temperature=0.1, max_tokens=1500)
        structured_spec = self._parse_json_response(llm_response)
        
        logger.success(f"Generated spec: {structured_spec.get('part_name', 'unknown')} "
                      f"with {len(structured_spec.get('parameters', {}))} parameters")
        
        return structured_spec
    
    def _parse_json_response(self, llm_response: str) -> Dict[str, Any]:
        """Parse and validate JSON response."""
        try:
            # Remove markdown code blocks and whitespace
            cleaned_response = re.sub(r'```(json)?\s*|\s*```', '', llm_response).strip()
            
            # Parse JSON
            spec_data = json.loads(cleaned_response)
            
            # Basic validation
            if not isinstance(spec_data, dict):
                raise ValueError("LLM response is not a JSON object")
                
            return spec_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {llm_response}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")