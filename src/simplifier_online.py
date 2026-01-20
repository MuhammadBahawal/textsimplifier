"""
Online text simplifier using Google Gemini API.
Provides intelligent text simplification for Urdu, Punjabi, and Roman Urdu.
"""
from google import genai
from google.genai import types
from typing import Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_api_key
from src.language_detector import Language, detect_language

class OnlineSimplifier:
    """Simplify text using Google Gemini API."""
    
    def __init__(self):
        self._client = None
        self._configured = False
    
    def _ensure_configured(self) -> bool:
        """Ensure the API is configured."""
        if self._configured and self._client:
            return True
        
        api_key = get_api_key()
        if not api_key:
            print("No API key available")
            return False
        
        try:
            self._client = genai.Client(api_key=api_key)
            self._configured = True
            print(f"Gemini API configured successfully")
            return True
        except Exception as e:
            print(f"Failed to configure Gemini API: {e}")
            return False
    
    def _get_prompt(self, text: str) -> str:
        """Generate a unified multilingual prompt that auto-detects language and responds accordingly."""
        
        return f"""You are a multilingual text simplifier expert. Your task is to:

1. AUTOMATICALLY DETECT the language of the input text. It can be:
   - اردو (Urdu in Arabic script)
   - پنجابی (Punjabi in Shahmukhi/Arabic script)
   - English
   - Roman Urdu (Urdu written in Roman/Latin letters)

2. SIMPLIFY the text by:
   - Keeping the EXACT same meaning
   - Replacing difficult/complex words with simpler everyday words
   - Breaking long sentences into shorter, clearer ones
   - Using common, everyday vocabulary

3. RESPOND IN THE SAME LANGUAGE as the input:
   - If input is in Urdu → respond in Urdu (Arabic script)
   - If input is in Punjabi → respond in Punjabi (Shahmukhi script)  
   - If input is in English → respond in English
   - If input is in Roman Urdu → respond in Roman Urdu

CRITICAL RULES:
- Reply with ONLY the simplified text
- Do NOT add any explanations, labels, or quotes
- Do NOT mention what language you detected
- Do NOT add "Simplified:", "آسان جملہ:", or any prefix
- Just output the simplified sentence directly

Input text:
{text}

Simplified output:"""
    
    def simplify(self, text: str) -> Optional[str]:
        """
        Simplify the given text using Gemini API.
        Returns simplified text or None if failed.
        Tries multiple models for better reliability.
        """
        if not text or not text.strip():
            return None
        
        if not self._ensure_configured():
            print("API not configured, returning None")
            return None
        
        # List of models to try in order of preference
        models_to_try = [
            "gemini-3-flash-preview",
            "gemini-2.5-flash",
            "gemini-2.0-flash",
        ]
        
        try:
            # Generate prompt - Gemini will auto-detect language
            prompt = self._get_prompt(text)
            
            # Try each model
            for model_name in models_to_try:
                try:
                    print(f"Trying model: {model_name}...")
                    response = self._client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.3,
                            max_output_tokens=1000,
                        )
                    )
                    
                    if response and response.text:
                        # Clean up the response
                        result = response.text.strip()
                        
                        # Remove any quotes around the response
                        if result.startswith('"') and result.endswith('"'):
                            result = result[1:-1]
                        if result.startswith("'") and result.endswith("'"):
                            result = result[1:-1]
                        
                        # Remove common prefixes the model might add
                        prefixes_to_remove = [
                            "Simplified version:",
                            "Simplified:",
                            "آسان جملہ:",
                            "سوکھا جملہ:",
                            "Here is the simplified version:",
                            "Here's the simplified text:",
                        ]
                        for prefix in prefixes_to_remove:
                            if result.lower().startswith(prefix.lower()):
                                result = result[len(prefix):].strip()
                        
                        print(f"Success with {model_name}: {result[:100]}...")
                        return result
                        
                except Exception as model_error:
                    error_str = str(model_error)
                    if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                        print(f"Model {model_name} quota exhausted, trying next...")
                        continue
                    elif "503" in error_str or "UNAVAILABLE" in error_str:
                        print(f"Model {model_name} unavailable, trying next...")
                        continue
                    else:
                        print(f"Error with {model_name}: {model_error}")
                        continue
            
            print("All models failed")
            return None
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def is_available(self) -> bool:
        """Check if online simplification is available."""
        return self._ensure_configured()


# Module-level function for convenience
_simplifier: Optional[OnlineSimplifier] = None

def get_online_simplifier() -> OnlineSimplifier:
    """Get the global online simplifier instance."""
    global _simplifier
    if _simplifier is None:
        _simplifier = OnlineSimplifier()
    return _simplifier

def simplify_online(text: str) -> Optional[str]:
    """Simplify text using online API."""
    return get_online_simplifier().simplify(text)
