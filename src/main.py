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
from src.output_handler.exporter import export_model, export_model_with_name

async def main():
    configure_logging()
    
    parser = argparse.ArgumentParser(description="Generate CAD models from text prompts")
    parser.add_argument("prompt", help="Text description of the CAD model to generate")
    parser.add_argument("-o", "--output", default="outputs/models/", help="Output directory for generated files")
    parser.add_argument("-f", "--format", choices=["step", "stl"], default="step", help="Output file format")
    parser.add_argument("-n", "--name", help="Custom filename (without extension)")
    parser.add_argument("--no-export", action="store_true", help="Skip file export")
    
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
        
        # Export the model unless disabled
        if not args.no_export:
            try:
                if args.name:
                    export_path = export_model_with_name(
                        result["model"],
                        args.output,
                        args.name,
                        format=args.format
                    )
                else:
                    export_path = export_model(
                        result["model"],
                        args.output,
                        format=args.format
                    )
                print(f"   Exported to: {export_path}")
            except Exception as e:
                print(f"❌ Failed to export model: {e}")

        else:
            print("   Export skipped as per user request.")
    else:
        print("CAD generation failed.")
        print(f" Error: {result['message']}")
                    

if __name__ == "__main__":
    asyncio.run(main())