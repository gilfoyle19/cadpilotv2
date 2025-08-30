#!/usr/bin/env python3
import asyncio
import argparse
from pathlib import Path

import sys

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.director.cad_director import CadDirector
from src.utilities.logging_config import configure_logging
from src.config.settings import settings

async def main():
    configure_logging()
    
    parser = argparse.ArgumentParser(description="Generate CAD models from text prompts")
    parser.add_argument("prompt", help="Text description of the CAD model to generate")
    parser.add_argument("-o", "--output", default="outputs/models/", help="Output directory for generated files")
    parser.add_argument("-f", "--format", choices=["step", "stl"], default="step", help="Output file format")
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    Path(args.output).mkdir(parents=True, exist_ok=True)
    
    director = CadDirector()
    result = await director.generate_from_prompt(args.prompt)
    
    if result["status"] == "success":
        print("✅ CAD model generated successfully!")
        print(f"   Part: {result['specification']['part_name']}")
        print(f"   Iterations: {result['iterations']}")
        print(f"   Model ready for export to {args.output}")
        
        # Basic export (we'll enhance this later)
        try:
            from src.output_handler.exporter import export_model
            export_path = export_model(result["model"], args.output, args.format)
            print(f"   ✅ Exported to: {export_path}")
        except ImportError:
            print("   ⚠️  Export functionality not implemented yet")
        except Exception as e:
            print(f"   ❌ Export failed: {e}")
            
    else:
        print("❌ CAD generation failed")
        print(f"   Error: {result['message']}")

if __name__ == "__main__":
    asyncio.run(main())