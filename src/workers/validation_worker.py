import tempfile
import os
from typing import Any, Dict
from loguru import logger

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.workers.base_worker import BaseWorker


class ValidationWorker(BaseWorker):
    """Executes and validates generated CadQuery code."""
    
    async def execute(self, generated_code: str) -> Dict[str, Any]:
        """
        Execute the generated code and validate it produces a valid CadQuery object.
        """
        logger.info("Validating generated code...")
        
        try:
            # Create a temporary file with the generated code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(generated_code)
                temp_file = f.name
            
            # Execute the code in a controlled environment
            result = self._execute_code_safely(temp_file)
            
            # Clean up
            os.unlink(temp_file)
            
            if result["success"]:
                logger.success("Code validation successful!")
                return {
                    "success": True,
                    "object": result["object"],
                    "message": "Valid CadQuery object generated"
                }
            else:
                logger.warning(f"Code validation failed: {result['error']}")
                return {
                    "success": False,
                    "error": result["error"],
                    "message": "Generated code failed to execute"
                }
                
        except Exception as e:
            logger.error(f"Validation process failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Validation process error"
            }
    
    def _execute_code_safely(self, file_path: str) -> Dict[str, Any]:
        """
        Simpler execution - just import what we need and run the code.
        """
        try:
            # Import cadquery here so it's available
            import cadquery as cq
            
            # Create a namespace with cadquery available
            local_vars = {'cq': cq, 'show_object': lambda x: None}
            
            # Read and execute the code
            with open(file_path, 'r') as f:
                code_content = f.read()
            
            # Execute the code with cadquery available
            exec(code_content, {}, local_vars)
            
            # Check if 'result' variable exists
            if 'result' in local_vars and hasattr(local_vars['result'], 'val'):
                return {"success": True, "object": local_vars['result']}
            else:
                return {"success": False, "error": "No valid 'result' object found"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}