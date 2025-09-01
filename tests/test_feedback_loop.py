#!/usr/bin/env python3
import asyncio
from dotenv import load_dotenv

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.director.cad_director import CadDirector
from src.workers.feedback_worker import FeedbackWorker
from src.workers.code_worker import CodeWorker
from loguru import logger

async def test_feedback_flow():
    """Test that feedback is properly generated and used."""
    print("🧪 Testing Feedback Loop...")
    print("=" * 50)
    
    feedback_worker = FeedbackWorker()
    code_worker = CodeWorker()
    
    # Create a deliberately bad code example that will fail validation
    bad_code = """
import cadquery as cq

# This code will fail - missing parameter and wrong method
result = cq.Workplane("XY").box(length, width, height)  # undefined variables
"""

    # Create a mock validation failure
    validation_result = {
        "success": False,
        "error": "NameError: name 'length' is not defined",
        "message": "Code execution failed"
    }

    # Create a simple specification
    spec = {
        "part_name": "test_cube",
        "parameters": {"size": 50.0},
        "features": [{"type": "extrude", "geometry": [{"primitive": "rectangle"}]}]
    }

    print("1. Generating feedback for bad code...")
    feedback = await feedback_worker.execute(bad_code, validation_result, spec)
    print(f"✅ Feedback generated: {feedback[:100]}...")

    print("\n2. Testing if feedback improves code generation...")
    
    # First, generate code without feedback
    print("   Generating code WITHOUT feedback:")
    code_no_feedback = await code_worker.execute(spec)
    print(f"   Code length: {len(code_no_feedback)} chars")
    print(f"   Preview: {code_no_feedback[:150]}...")

    # Then generate code WITH feedback
    print("\n   Generating code WITH feedback:")
    code_with_feedback = await code_worker.execute(spec, feedback)
    print(f"   Code length: {len(code_with_feedback)} chars")
    print(f"   Preview: {code_with_feedback[:150]}...")

    # Compare the two
    print("\n3. Comparison:")
    print(f"   Without feedback: {len(code_no_feedback)} chars")
    print(f"   With feedback:    {len(code_with_feedback)} chars")
    
    # Check if feedback actually caused changes
    if code_no_feedback != code_with_feedback:
        print("✅ SUCCESS: Feedback influenced code generation!")
        
        # Show specific differences
        lines_no_fb = code_no_feedback.split('\n')
        lines_with_fb = code_with_feedback.split('\n')
        
        print("\n   Differences found:")
        for i, (line1, line2) in enumerate(zip(lines_no_fb, lines_with_fb)):
            if line1 != line2:
                print(f"   Line {i}:")
                print(f"      Without: {line1[:50]}...")
                print(f"      With:    {line2[:50]}...")
                break
    else:
        print("❌ No differences found - feedback may not be working")

async def test_director_feedback_loop():
    """Test the complete feedback loop in the director."""
    print("\n" + "="*50)
    print("🧪 Testing Complete Director Feedback Loop")
    print("="*50)
    
    director = CadDirector()
    
    # Create a specification that might need multiple attempts
    # (e.g., something complex that might fail first try)
    complex_spec = {
        "part_name": "complex_bracket",
        "parameters": {
            "width": 100.0,
            "height": 50.0, 
            "thickness": 10.0,
            "hole_diameter": 8.0
        },
        "features": [
            {
                "name": "base",
                "type": "extrude",
                "plane": "XY",
                "geometry": [{"primitive": "rectangle", "width": 100.0, "height": 50.0}],
                "height": 10.0
            },
            {
                "name": "mounting_holes",
                "type": "hole",
                "plane": "XY",
                "position": [20.0, 20.0, 0.0],
                "geometry": [{"primitive": "circle", "radius": 4.0}],
                "height": 10.0
            }
        ]
    }
    
    print("Testing with complex specification that might require feedback...")
    result = await director.generate_from_prompt("complex bracket with mounting holes")
    
    if result["status"] == "success":
        print(f"✅ Success in {result['iterations']} iterations")
        if result["iterations"] > 1:
            print("   Feedback loop was used successfully!")
        else:
            print("   Succeeded on first try (no feedback needed)")
    else:
        print("❌ Failed after all attempts")

if __name__ == "__main__":
    load_dotenv()
    
    # Test basic feedback generation
    asyncio.run(test_feedback_flow())
    
    # Test complete loop (optional - might take longer)
    # asyncio.run(test_director_feedback_loop())