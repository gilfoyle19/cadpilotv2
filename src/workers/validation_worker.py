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
    """Validates and executes the generated CadQuery code."""

    async def execute(self, generated_code: str) -> Dict[str, Any]:
        """Execute the generated code and validate it produces a valid CadQuery object."""
        logger.info("Starting code validation...")

        try:
            with tempfile.NamedTemporaryFile(mode = 'w', suffix = '.py', delete = False) as f:

                f.write(generated_code)
                temp_file = f.name

            result = self._execute_code_safely(temp_file)

            os.unlink(temp_file)  # Clean up the temp file

            if result["success"]:
                logger.success("Code validation successful!")
                return{
                    "sucess": True,
                    "object": result["object"],
                    "message": "Valid CadQuery object generated."
                }
            else:
                logger.warning(f"Code validation failed: {result['error']}")
                return {
                    "success": False,
                    "error": result["error"],
                    "message": "Generated code failed to execute."
                }
        except Exception as e:
            logger.error(f"Validation process failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Unexpected error during validation."
            }
        
    def _execute_code_safely(self, file_path:str) -> Dict[str, Any]:
        """Execute the generated code in a restricted environment for safety."""

        safe_globals = {
            '__builtins__': {
                'range': range,
                'len': len,
                'float': float,
                'int': int,
                'str': str,
                'bool': bool,
                'list': list,
                'dict': dict,
            }
        }

        try:
            #Read and execute the code
            with open(file_path, 'r') as f:
                code_content = f.read()

            #execute the code
            exec(code_content, safe_globals)

            #Check if 'result'variable exists and is a Cadquery object
            if 'result' in safe_globals and hasattr(safe_globals['result'], 'val'):
                return {"success": True, "object": safe_globals['result']}
            else:
                return {"success": False, "error": "No valid 'result' object found."}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
        
