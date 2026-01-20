
"""
Language detection for Urdu, Punjabi, and Roman Urdu.
"""
import re
from enum import Enum
from typing import Tuple

class Language(Enum):
    """Supported languages."""
    URDU = "urdu"
    PUNJABI = "punjabi"
    ROMAN_URDU = "roman_urdu"
    ENGLISH = "english"
    UNKNOWN = "unknown"

# Unicode ranges for Arabic script (used by Urdu and Punjabi)
ARABIC_SCRIPT_PATTERN = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]')

# Common Urdu-specific characters (not commonly in Punjabi)
URDU_SPECIFIC = set('ٹڈڑےۓ')

# Common Punjabi-specific characters (Shahmukhi)
PUNJABI_GURMUKHI_PATTERN = re.compile(r'[\u0A00-\u0A7F]')  # Gurmukhi script

# Common Roman Urdu patterns
ROMAN_URDU_WORDS = {
    'hai', 'hain', 'ho', 'tha', 'thi', 'the', 'tho',
    'kya', 'kia', 'kyun', 'kyon', 'kaisa', 'kaise',
    'mein', 'main', 'hum', 'tum', 'aap', 'ap',
    'acha', 'achchha', 'theek', 'thik',
    'nahi', 'nahin', 'na', 'mat',
    'aur', 'ya', 'lekin', 'magar', 'par',
    'se', 'ko', 'ka', 'ki', 'ke', 'ne', 'pe',
    'woh', 'wo', 'yeh', 'ye', 'is', 'us',
    'ab', 'jab', 'tab', 'kab', 'phir', 'fir',
    'bahut', 'bohot', 'bohat', 'zyada', 'ziada',
    'sab', 'kuch', 'koi', 'kaun', 'kon',
    'wala', 'wali', 'wale',
    'raha', 'rahi', 'rahe', 'rhe',
    'kar', 'karo', 'karna', 'karein',
    'jao', 'jana', 'chalo', 'chalna',
    'bolo', 'bolna', 'kaho', 'kehna',
    'dekho', 'dekhna', 'suno', 'sunna',
    'khaana', 'khana', 'peena', 'pina',
    'ghar', 'school', 'kaam', 'kam',
    'pyaar', 'pyar', 'mohabbat', 'dost',
    'bhai', 'behen', 'behan',
    'shukriya', 'meherbani', 'khuda', 'allah',
    'inshallah', 'mashallah', 'subhanallah',
    'assalam', 'walaikum', 'khudahafiz',
    'bilkul', 'zaroor', 'shayad',
}

# Common Punjabi Roman words (different from Urdu)
PUNJABI_WORDS = {
    'ki', 'kiven', 'kiddan', 'kithe', 'kithon',
    'hun', 'ohna', 'ehna', 'tuhada', 'sadda',
    'munda', 'kudi', 'kudiye',
    'chal', 'changa', 'changey', 'vadiya', 'wadiya',
    'paaji', 'paji', 'veere', 'veer',
    'bhaji', 'bhabhi', 'tayi', 'chacha',
    'sat', 'sri', 'akal', 'waheguru',
    'oye', 'yaar', 'yaara',
    'gaddi', 'gadi',
    'lassi', 'makki', 'roti',
    'jatt', 'jatti', 'gabru',
    'punjab', 'lahore', 'amritsar',
    'bhangra', 'gidda',
}

class LanguageDetector:
    """Detect language from text input."""
    
    def detect(self, text: str) -> Tuple[Language, float]:
        """
        Detect the language of the input text.
        Returns (Language, confidence_score).
        """
        if not text or not text.strip():
            return Language.UNKNOWN, 0.0
        
        text = text.strip()
        
        # Count Arabic script characters
        arabic_chars = len(ARABIC_SCRIPT_PATTERN.findall(text))
        total_chars = len(re.sub(r'\s', '', text))
        
        if total_chars == 0:
            return Language.UNKNOWN, 0.0
        
        arabic_ratio = arabic_chars / total_chars
        
        # If mostly Arabic script, it's Urdu or Punjabi (Shahmukhi)
        if arabic_ratio > 0.5:
            return self._detect_urdu_or_punjabi(text, arabic_ratio)
        
        # Check for Gurmukhi (Punjabi) script
        if PUNJABI_GURMUKHI_PATTERN.search(text):
            return Language.PUNJABI, 0.9
        
        # If Roman script, check for Roman Urdu or Punjabi patterns
        return self._detect_roman(text)
    
    def _detect_urdu_or_punjabi(self, text: str, arabic_ratio: float) -> Tuple[Language, float]:
        """Detect between Urdu and Punjabi written in Arabic script."""
        # Check for Urdu-specific characters
        urdu_specific_count = sum(1 for char in text if char in URDU_SPECIFIC)
        
        # Urdu is more common for Arabic script, default to Urdu
        if urdu_specific_count > 0:
            return Language.URDU, min(0.95, arabic_ratio + 0.1)
        
        # Default to Urdu for Arabic script (most common case)
        return Language.URDU, arabic_ratio
    
    def _detect_roman(self, text: str) -> Tuple[Language, float]:
        """Detect Roman Urdu or Roman Punjabi."""
        words = set(text.lower().split())
        
        # Count matching words
        urdu_matches = len(words & ROMAN_URDU_WORDS)
        punjabi_matches = len(words & PUNJABI_WORDS)
        
        total_words = len(words)
        if total_words == 0:
            return Language.UNKNOWN, 0.0
        
        urdu_ratio = urdu_matches / total_words
        punjabi_ratio = punjabi_matches / total_words
        
        # Determine language based on word matches
        if punjabi_ratio > urdu_ratio and punjabi_ratio > 0.1:
            return Language.PUNJABI, min(0.8, punjabi_ratio * 2)
        
        if urdu_ratio > 0.1 or urdu_matches >= 2:
            return Language.ROMAN_URDU, min(0.85, urdu_ratio * 2 + 0.3)
        
        # If some words match, assume Roman Urdu (more common)
        if urdu_matches > 0 or punjabi_matches > 0:
            return Language.ROMAN_URDU, 0.5
        
        # Default to English for unrecognized Roman text (pure English)
        return Language.ENGLISH, 0.7
    
    def get_language_name(self, lang: Language) -> str:
        """Get human-readable language name."""
        names = {
            Language.URDU: "اردو (Urdu)",
            Language.PUNJABI: "پنجابی (Punjabi)",
            Language.ROMAN_URDU: "Roman Urdu",
            Language.ENGLISH: "English",
            Language.UNKNOWN: "Unknown"
        }
        return names.get(lang, "Unknown")

# Global instance
_detector = LanguageDetector()

def detect_language(text: str) -> Tuple[Language, float]:
    """Detect language of the given text."""
    return _detector.detect(text)

def get_language_name(lang: Language) -> str:
    """Get human-readable language name."""
    return _detector.get_language_name(lang)
