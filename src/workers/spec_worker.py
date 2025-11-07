import json
from ast import literal_eval
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
        
        llm_response = await self._call_llm(messages, temperature=0, max_tokens=5000)
        structured_spec = self._parse_json_response(llm_response)
        
        logger.success(f"Generated spec: {structured_spec.get('part_name', 'unknown')} "
                      )
        
        #logger.success(f"Generated spec: {structured_spec.get('part_name', 'unknown')} "
                     # f"with {len(structured_spec.get('parameters', {}))} parameters")
        
        return structured_spec

    def _parse_json_response(self, llm_response: str) -> Dict[str, Any]:
        """
        Parses LLM response by first cleaning the output and then robustly converting 
        Python-like dictionary strings (unquoted keys, single quotes) into valid JSON
        using ast.literal_eval, followed by structural validation.
        """
        
        # 1. Aggressively clean the response of markdown code blocks and whitespace.
        # We use re.IGNORECASE to catch variants like ```JSON, ```json, etc.
        cleaned_response = re.sub(r'```(json)?\s*|\s*```', '', llm_response, flags=re.IGNORECASE).strip()

        # 2. Check for empty response (handles "Expecting value: line 1 column 1" error)
        if not cleaned_response:
            raise ValueError("CAD generation failed: Received an empty or purely whitespace response.")
        
        spec_data: Dict[str, Any] = {}
        
        try:
            # Attempt 1: Try standard, strict JSON parse first (fastest path).
            spec_data = json.loads(cleaned_response)
            
        except json.JSONDecodeError:
            # Attempt 2: If strict JSON fails, try converting from Python-like dictionary syntax.
            # This step handles unquoted keys, single quotes, and missing commas 
            # (which caused the errors "Expecting property name" and "Expecting ',' delimiter").
            try:
                # Safely evaluate the Python-like string into a Python dictionary.
                python_dict = literal_eval(cleaned_response)
                
                # Strictly serialize the dictionary back to valid JSON. 
                # This fixes quotes and comma issues automatically.
                valid_json_string = json.dumps(python_dict)
                
                # Load the now strictly valid JSON string.
                spec_data = json.loads(valid_json_string)

            except (SyntaxError, ValueError, TypeError) as eval_error:
                # If literal_eval also fails, the response is fundamentally unusable.
                raise ValueError(f"Invalid JSON structure/syntax from LLM: The response was not a valid Python literal or JSON: {eval_error}")

        # 3. Perform Final Structural Validation (Ensures the data is useful)
        
        # Must be a dictionary.
        if not isinstance(spec_data, dict):
            raise ValueError("JSON structural validation failed: Top-level object is not a dictionary.")
            
        # Check for required top-level keys.
        required_keys = ["part_name", "description", "cad_operations"]
        for key in required_keys:
            if key not in spec_data:
                raise ValueError(f"JSON structural validation failed: Missing required key: '{key}'.")
        
        # Validate the 'cad_operations' array.
        cad_ops = spec_data.get("cad_operations")
        if not isinstance(cad_ops, list) or not cad_ops:
            raise ValueError("'cad_operations' must be a non-empty JSON array (list).")
            
        return spec_data