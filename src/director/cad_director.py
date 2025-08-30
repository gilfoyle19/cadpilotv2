from typing import Dict, Optional, Any
from loguru import logger
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.workers.spec_worker import SpecWorker
from src.workers.code_worker import CodeWorker
from src.workers.validation_worker import ValidationWorker
from src.workers.feedback_worker import FeedbackWorker

class CadDirector:
    """Orchestraters the complete CAD generation workflow."""

    def __init__(self):
        self.spec_worker = SpecWorker()
        self.code_worker = CodeWorker()
        self.validation_worker = ValidationWorker()
        self.feedback_worker = FeedbackWorker()
        self.max_iterations = 3  # Max feedback iterations

    async def generate_from_prompt(self, prompt: str) -> Dict[str, Any]:
            """
            Complete workflow.
            
            Args:
                prompt (str): Natural language description of the desired CAD model.
                
                Returns:
                Dict[str, Any]: Dictionary with status and outputs."""
            
            logger.info(f"Starting CAD generation for prompt: {prompt[:50]}...")

            try:
                #Step 1: Generate structured specification
                logger.info("Generating structured specification...")
                structured_spec = await self.spec_worker.execute(prompt)

                #Step 2-4: Code generation and validation loop
                result = await self._generate_and_validate(structured_spec)

                if result["status"] == "success":
                    logger.success("CAD generation completed successfully.")
                    return {
                        "status": "success",
                        "model": result["model"],
                        "specification": structured_spec,
                        "code": result["code"],
                        "iterations": result["iterations"]
                        
                 }
                
                else:
                    logger.error("CAD generation failed after maximum iterations.")
                    return {
                        "status": "error",
                        "message": result["message"],
                        "specification": structured_spec,
                    }
                
            except Exception as e:
                logger.error(f"CAD generation failed: {e}")
                return {
                    "status": "error",
                    "message": f"Generation process failed: {e}"
                }
        
    async def _generate_and_validate(self, specification: Dict[str, Any]) -> Dict[str, Any]:
        """Generate and validate code with retry loop"""

        feedback = None

        for iteration in range(self.max_iterations):
            logger.info(f"Code generation attempt {iteration + 1}...")

            try:
                #Generate code
                generated_code = await self.code_worker.execute(specification, feedback)

                #Validate code
                validation_result = await self.validation_worker.execute(generated_code)

                if validation_result["success"]:
                    return {
                        "status": "success",
                        "model": validation_result["object"],
                        "code": generated_code,
                        "iterations": iteration + 1
                    }
                else:

                    #Get the feedback for next iteration
                    feedback = await self.feedback_worker.execute(generated_code, validation_result, specification)
                    logger.info(f"Feedback for next iteration: {feedback}...")

            except Exception as e:
                logger.warning(f"Attempt {iteration + 1} failed: {e}")
                feedback = f"Previous attempt failed with error: {e}"

        return {
            "status": "error",
            "message": f"Failed to generate valid code after {self.max_iterations} attempts."
        }
            
