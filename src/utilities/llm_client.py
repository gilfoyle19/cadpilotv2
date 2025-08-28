import httpx
import json
import tenacity
from typing import List, Dict, Any, Optional
from httpx import ConnectError, ReadTimeout, HTTPStatusError
from loguru import logger

from src.config.settings import settings
from src.config.openrouter_models import OpenRouterModel

class OpenRouterClient:
    """A robust HTTPX-based client for OpenRouter API with retry logic."""
    
    def __init__(self):
        self.api_key = settings.openrouter_api_key
        self.base_url = settings.openrouter_base_url
        self.default_model = settings.default_model
        self.timeout = settings.request_timeout
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/gilfoyle19/cadpilotv2",
            "X-Title": "CAD Pilot v2 - Text to CAD Generator",
        }
        
        # Create async client with connection pooling
        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=20)
        )
    
    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=2, max=10),
        retry=(
            tenacity.retry_if_exception_type(ConnectError) |
            tenacity.retry_if_exception_type(ReadTimeout) |
            tenacity.retry_if_exception(
                lambda e: isinstance(e, HTTPStatusError) and 
                e.response.status_code in [429, 500, 502, 503, 504]
            )
        ),
        before_sleep=lambda retry_state: logger.warning(
            f"Retrying OpenRouter API call (attempt {retry_state.attempt_number}): "
            f"{type(retry_state.outcome.exception()).__name__}"
        ),
        reraise=True
    )
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[OpenRouterModel] = None,
        temperature: float = 0.1,
        max_tokens: int = 2000,
    ) -> str:
        """
        Send a chat completion request to OpenRouter API with robust error handling.
        """
        model_to_use = model or self.default_model
        
        payload = {
            "model": model_to_use,
            "messages": messages,
            "temperature": max(0.0, min(1.0, temperature)),  # Clamp to valid range
            "max_tokens": max_tokens,
        }
        
        try:
            logger.debug(f"Sending request to OpenRouter model: {model_to_use}")
            
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=self.headers,
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            # Extract content from response
            content = response_data["choices"][0]["message"]["content"].strip()
            
            # Log token usage for monitoring
            usage = response_data.get("usage", {})
            logger.debug(
                f"OpenRouter request successful. "
                f"Tokens: {usage.get('prompt_tokens', 'N/A')} prompt, "
                f"{usage.get('completion_tokens', 'N/A')} completion"
            )
            
            return content
            
        except httpx.HTTPStatusError as e:
            logger.error(f"OpenRouter API HTTP error {e.response.status_code}: {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"OpenRouter API request failed: {str(e)}")
            raise
        except KeyError as e:
            logger.error(f"Malformed response from OpenRouter: {response_data}")
            raise ValueError("Invalid response format from OpenRouter API") from e
    
    async def close(self):
        """Clean up the HTTP client gracefully."""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

# Global instance for easy access
llm_client = OpenRouterClient()