import cadquery as cq
from pathlib import Path
from datetime import datetime
from loguru import logger
from typing import Optional

def export_model(cadquery_obj, output_dir: str, format: str = "step") -> str:
    """
    Export a CadQuery object to a file.
    
    Args: 
    cadquery_obj: The CadQuery object to export.
    output_dir (str): Directory to save the exported file.
    format (str): File format, either "step" or "stl
    """
    try:
        # Ensure the output directory exists
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"model_{timestamp}.{format}"
        filepath = output_path / filename

        # Export based on format
        if format.lower() == "step":
            cadquery_obj.val().exportStep(str(filepath))
        elif format.lower() == "stl":
            cadquery_obj.val().exportStl(str(filepath))
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'step' or 'stl'.")
        
    except Exception as e:
        logger.error(f"Failed to export model: {e}")
        raise

def export_model_with_name(cadquery_obj, output_dir: str, filename: str, formart: str = "step") -> str:
    """
    Export a CadQuery object to a file with a specific filename.
    
    Args: 
    cadquery_obj: The CadQuery object to export.
    output_dir (str): Directory to save the exported file.
    filename (str): Desired filename without extension.
    format (str): File format, either "step" or "stl
    """
    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Ensure filename has correct extension
        if not filename.endswith(f".{format}"):
            filename = f"{filename}.{format}"

        filepath = output_path / filename

        if format.lower() == "step":
            cadquery_obj.val().exportStep(str(filepath))
        elif format.lower() == "stl":
            cadquery_obj.val().exportStl(str(filepath))
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'step' or 'stl'.")
        
        logger.success(f"Exported {format.upper()} model to {filepath}")
        return str(filepath)
    
    except Exception as e:
        logger.error(f"Failed to export model: {e}")
        raise

    