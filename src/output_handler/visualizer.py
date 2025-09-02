#import pyvista as pv
from pathlib import Path
from loguru import logger
from typing import Optional
import tempfile
import os

class ModelVisualizer:
    """Visualizes CAD models using PyVista."""

    def __init__(self):
        self.plotter = None
    
    def visualize_model(self, cadquery_obj, screenshot_path: Optional[str] = None) -> Optional[str]:
        """
        Visualize a Cadquery object and optionall save a screenshot.
        
        Args: cadquery obj, optional screenshot path
        Returns: Path to screenshot if saved, else None
        """
        import pyvista as pv
        try:
            #Export to a temporary STEP file 
            with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as f:
                temp_stl = f.name 

            cadquery_obj.val().exportStl(temp_stl)

            #Load STEP file into PyVista
            mesh = pv.read(temp_stl)

            #create interactive plotter
            self.plotter = pv.Plotter()
            self.plotter.add_mesh(mesh, color="lightblue", show_edges=True, opacity=0.9)
            self.plotter.show_axes()
            self.plotter.add_title("CADpilotV2 - 3D Model Preview", font_size=14)

            #Save screenshot if requested
            screenshot_saved = None
            if screenshot_path:
                screenshot_dir = Path(screenshot_path)
                screenshot_dir.parent.mkdir(parents=True, exist_ok=True)
                self.plotter.screenshot(str(screenshot_path))
                screenshot_saved = str(screenshot_path)
                logger.success(f"Screenshot saved to {screenshot_path}")

            #Show interactive window
            logger.info("Opening 3D viewer...")
            self.plotter.show()

            #Clean up the temporary file
            os.unlink(temp_stl)

            return screenshot_saved
        
        except ImportError as e:
            #logger.error("PyVista is not installed. Please install it with 'pip install pyvista'.")
            logger.error(f"Pyvista import error:, {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to visualize model: {e}")
            return None
        
    def generate_thumbnail(self, cadquery_obj, output_path: str, size: tuple = (400, 300)) -> Optional[str]:
        """
        Generate a thumbnail image of the CAD model.
        
        Args:
            cadquery_obj: The CadQuery object to visualize.
            output_path (str): Path to save the thumbnail image.
            size (tuple): Size of the thumbnail (width, height).
            
        Returns:
            Optional[str]: Path to the saved thumbnail image, or None if failed.
        """
        try:
            with tempfile.NamedTemporaryFile(suffix=".step", delete=False) as f:
                temp_step = f.name

            cadquery_obj.val().exportStep(temp_step)
            mesh = pv.read(temp_step)

            #Offscreen rendering for thumbnails
            plotter = pv.Plotter(off_screen=True, window_size=size)
            plotter.add_mesh(mesh, color="lightblue", show_edges=True, opacity=0.9)
            plotter.show_axes()
            plotter.add_title("CADpilotV2 Thumbnail", font_size=10)
            plotter.camera_position = 'isometric'

            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plotter.screenshot(str(output_path))
            plotter.close()

            os.unlink(temp_step)
            logger.success(f"Thumbnail saved to {output_path}")
            return str(output_path)
        
        except Exception as e:
            logger.error(f"Failed to generate thumbnail: {e}")
            return None
        
visualizer = ModelVisualizer() 


            
