#!/usr/bin/env python3
import asyncio
from dotenv import load_dotenv

# Use direct imports instead of through src package
from src.utilities.llm_client import llm_client
from src.config.openrouter_models import OpenRouterModel

async def test_all_free_models():
    """Test all available free models to compare performance."""
    print("🧪 Testing All Free OpenRouter Models...")
    print("=" * 50)
    
    test_prompt = """You are a CAD assistant. Please describe how you would convert 
    this text description into a CAD model: "a hexagonal nut, M10 size, 5mm thick"."""
    
    models_to_test = OpenRouterModel.get_free_models()
    
    for model in models_to_test:
        try:
            model_info = OpenRouterModel.get_model_info(model)
            print(f"\n🔧 Testing {model_info['name']} ({model.value})...")
            print(f"   Best for: {model_info['best_for']}")
            
            messages = [
                {"role": "system", "content": "You are an expert CAD engineering assistant."},
                {"role": "user", "content": test_prompt}
            ]
            
            response = await llm_client.chat_completion(
                messages, 
                model=model,
                temperature=0.1,
                max_tokens=150
            )
            
            print(f"✅ SUCCESS")
            print(f"   Response: {response[:120]}...")
            
        except Exception as e:
            print(f"❌ FAILED - {str(e)[:80]}...")
    
    print(f"\n🎯 Recommended default: {OpenRouterModel.GOOGLE_GEMINI_FLASH.value}")

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(test_all_free_models())