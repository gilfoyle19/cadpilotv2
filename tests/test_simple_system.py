#!/usr/bin/env python3
import asyncio
from dotenv import load_dotenv

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.workers.spec_worker import SpecWorker
from src.workers.code_worker import CodeWorker

async def test_simple_system():
    """Test the simplified system."""
    print("🧪 Testing Simplified System...")
    
    spec_worker = SpecWorker()
    code_gen = CodeWorker()
    
    test_prompts = [
        "a cylindrical spacer, 20mm long, 8mm diameter",
        "a hexagonal nut, M10 size, 5mm thick",
        "a simple cube with 50mm sides",
    ]
    
    for prompt in test_prompts:
        try:
            print(f"\n📝 Prompt: {prompt[:60]}...")
            
            # Generate specification
            spec = await spec_worker.execute(prompt)
            print(f"✅ Generated spec: {spec['part_name']}")
            print(f"   Parameters: {list(spec['parameters'].keys())}")
            
            # Show that values are already calculated
            if 'parameters' in spec:
                for param, value in list(spec['parameters'].items())[:3]:  # Show first 3
                    print(f"     {param}: {value}")
            
            # Generate code
            code = await code_gen.execute(spec)
            print(f"✅ Generated code ({len(code)} characters)")
            print(f"   Preview: {code}...")
            
        except Exception as e:
            print(f"❌ Failed: {e}")

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(test_simple_system())