from enum import StrEnum

class OpenRouterModel(StrEnum):
    """Enum of supported OpenRouter models with focus on free options."""
    
    # BEST FREE DEFAULT: Google's Gemini Pro - reliable and capable
    GOOGLE_GEMINI_FLASH = "google/gemini-2.5-flash-image-preview:free"
    
    # Excellent free alternatives:
    OPENAI_GPT_OSS = "openai/gpt-oss-20b:free"
    MISTRAL_7B_INSTRUCT = "mistralai/mistral-7b-instruct"  # Fast and capable
    LLAMA_3_405B_INSTRUCT = "meta-llama/llama-3.1-405b-instruct:free"  # Larger, more powerful
    DEEPSEEK_R1 = "deepseek/deepseek-r1:free"  # Great for code
    
    # Paid models (for when you need more power later)
    OPENAI_GPT4_TURBO = "openai/gpt-4-turbo"
    ANTHROPIC_CLAUDE_3_SONNET = "anthropic/claude-3-sonnet"
    
    @classmethod
    def get_default_free_model(cls):
        """Get the best default free model - Google Gemini Pro."""
        return cls.GOOGLE_GEMINI_FLASH
    
    @classmethod
    def get_free_models(cls):
        """Return all available free models."""
        return [
            cls.GOOGLE_GEMINI_FLASH,
            cls.OPENAI_GPT_OSS,
            cls.MISTRAL_7B_INSTRUCT,
            cls.LLAMA_3_405B_INSTRUCT,
            cls.DEEPSEEK_R1
        ]
    
    @classmethod
    def get_model_info(cls, model_enum) -> dict:
        """Get information about a model."""
        model_info = {
            cls.GOOGLE_GEMINI_FLASH: {
                "name": "Google Gemini Flash 2.5 Experimental",
                "free": True,
                "best_for": "General purpose - best default choice",
                "strength": "Reliable, good reasoning, free tier"
            },
            cls.OPENAI_GPT_OSS: {
                "name": "OpenAI GPT-OSS 20B", 
                "free": True,
                "best_for": "Code generation tasks",
                "strength": "Specialized for programming"
            },
            cls.MISTRAL_7B_INSTRUCT: {
                "name": "Mistral 7B Instruct",
                "free": True, 
                "best_for": "Fast responses, good balance",
                "strength": "Speed and efficiency"
            },
            cls.LLAMA_3_405B_INSTRUCT: {
                "name": "LLaMA 3.1 405B Instruct",
                "free": True,
                "best_for": "Complex reasoning tasks", 
                "strength": "Large model capacity"
            },
            cls.DEEPSEEK_R1: {
                "name": "DeepSeek R1",
                "free": True,
                "best_for": "Advanced code generation",
                "strength": "Large code-specific model"
            }
        }
        return model_info.get(model_enum, {"name": str(model_enum), "free": False})
    
