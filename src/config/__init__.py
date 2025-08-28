# Make settings available at package level
from .settings import settings
from .openrouter_models import OpenRouterModel

__all__ = ['settings', 'OpenRouterModel']