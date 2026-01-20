"""
Offline text simplifier using rule-based NLP.
Works without internet connection - provides real simplification.
"""
import re
from typing import Optional, Dict, List, Tuple
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.language_detector import Language, detect_language

# Extended synonym mappings for better simplification
URDU_SIMPLIFICATIONS: Dict[str, str] = {
    # Complex words -> Simple words
    'استعمال': 'استعمال',
    'مستعمل': 'استعمال شدہ',
    'دستیاب': 'ملتا ہے',
    'بہترین': 'اچھا',
    'شاندار': 'اچھا',
    'عمدہ': 'اچھا',
    'لاجواب': 'بہت اچھا',
    'ممتاز': 'اچھا',
    'اہم': 'ضروری',
    'ضروری': 'ضروری',
    'مشکل': 'مشکل',
    'دشوار': 'مشکل',
    'صعوبت': 'مشکل',
    'آسان': 'آسان',
    'سہل': 'آسان',
    'تصور': 'خیال',
    'خیال': 'خیال',
    'تعلیم': 'پڑھائی',
    'مطالعہ': 'پڑھنا',
    'معلومات': 'جانکاری',
    'واضح': 'صاف',
    'مکمل': 'پورا',
    'لہٰذا': 'اس لیے',
    'بنابریں': 'اس لیے',
    'تاہم': 'مگر',
    'البتہ': 'مگر',
    'حالانکہ': 'جبکہ',
    'باوجود': 'پھر بھی',
    'اگرچہ': 'اگر',
    'مستقبل': 'آگے',
    'ماضی': 'پہلے',
    'فوری': 'ابھی',
    'تقریباً': 'لگ بھگ',
    'بالکل': 'بالکل',
    'یقیناً': 'ضرور',
    'شائد': 'شاید',
    'ممکن': 'ہو سکتا',
    'ناممکن': 'نہیں ہو سکتا',
    'انتہائی': 'بہت',
    'غیر معمولی': 'عجیب',
    'خصوصی': 'خاص',
    'عمومی': 'عام',
    'مخصوص': 'خاص',
    'متعلق': 'کے بارے میں',
    'حاصل': 'ملنا',
    'فراہم': 'دینا',
    'موجود': 'ہے',
    'غائب': 'نہیں ہے',
    'مقام': 'جگہ',
    'علاقہ': 'جگہ',
    'خوبصورت': 'پیاری',
    'حسین': 'پیاری',
    'دلکش': 'اچھی',
}

ROMAN_URDU_SIMPLIFICATIONS: Dict[str, str] = {
    # Complex -> Simple (expanded)
    'definitely': 'zaroor',
    'absolutely': 'bilkul',
    'approximately': 'lagbhag',
    'taqreeban': 'lagbhag',
    'however': 'lekin',
    'moreover': 'aur',
    'furthermore': 'aur bhi',
    'nevertheless': 'phir bhi',
    'consequently': 'is liye',
    'therefore': 'is liye',
    'lehaza': 'is liye',
    'although': 'halankeh',
    'impossible': 'namumkin',
    'namumkin': 'nahi ho sakta',
    'excellent': 'bohat acha',
    'shandar': 'bohat acha',
    'behtareen': 'bohat acha',
    'wonderful': 'acha',
    'information': 'jaankari',
    'maloomat': 'jaankari',
    'education': 'parhai',
    'taleem': 'parhai',
    'immediately': 'abhi',
    'foran': 'abhi',
    'perhaps': 'shayad',
    'probably': 'shayad',
    'mumkin': 'ho sakta hai',
    'difficult': 'mushkil',
    'dushwar': 'mushkil',
    'utilize': 'istemal karo',
    'istemal': 'use',
    'purchase': 'khareedna',
    'kharidna': 'lena',
    'beautiful': 'khubsurat',
    'khubsurat': 'pyari',
    'extremely': 'bohat',
    'intehai': 'bohat',
    'regarding': 'ke baare mein',
    'mutaaliq': 'ke baare mein',
    'available': 'milta hai',
    'dastiyab': 'milta hai',
    'understand': 'samajhna',
    'comprehend': 'samajhna',
    'significant': 'ahem',
    'important': 'zaroori',
    'essential': 'zaroori',
    'lazmi': 'zaroori',
    'communicate': 'baat karna',
    'conversation': 'baat cheet',
    'guftagu': 'baat cheet',
    'circumstances': 'halaat',
    'situation': 'haalat',
    'surat-e-haal': 'haalat',
    'opportunity': 'mauka',
    'moqa': 'mauka',
    'accomplish': 'karna',
    'achieve': 'paana',
    'obtain': 'lena',
    'haasil': 'milna',
    'acquire': 'lena',
    'sufficient': 'kaafi',
    'adequate': 'kaafi',
    'kaafi': 'theek',
    'previously': 'pehle',
    'subsequently': 'baad mein',
    'currently': 'abhi',
    'filhaal': 'abhi',
    'assist': 'madad karna',
    'assistance': 'madad',
    'require': 'chahiye',
    'zaroorat': 'chahiye',
    'necessary': 'zaroori',
    'darkar': 'chahiye',
    'additional': 'aur',
    'mazeed': 'aur',
    'various': 'mukhtalif',
    'different': 'alag',
    'mukhtalif': 'alag alag',
    'particular': 'khaas',
    'specific': 'khaas',
    'makhsoos': 'khaas',
    'consider': 'sochna',
    'contemplate': 'sochna',
    'ghour': 'sochna',
}

PUNJABI_SIMPLIFICATIONS: Dict[str, str] = {
    # Punjabi complex -> simple
    'بالکل': 'ہاں',
    'ضرور': 'ہاں جی',
    'شاندار': 'ودیا',
    'مشکل': 'اوکھا',
    'آسان': 'سوکھا',
    'ضروری': 'لازمی',
    'خوبصورت': 'سوہنا',
    'بہت': 'بوہت',
}


class OfflineSimplifier:
    """Rule-based text simplifier for offline use."""
    
    def __init__(self):
        pass
    
    def simplify(self, text: str) -> str:
        """
        Simplify the given text using comprehensive rule-based approach.
        """
        if not text or not text.strip():
            return text
        
        # Detect language
        language, _ = detect_language(text)
        print(f"[Offline] Processing text in {language.value}")
        
        # Apply language-specific simplification
        if language == Language.URDU:
            return self._simplify_urdu(text)
        elif language == Language.PUNJABI:
            return self._simplify_punjabi(text)
        else:  # Roman Urdu or unknown
            return self._simplify_roman_urdu(text)
    
    def _simplify_urdu(self, text: str) -> str:
        """Simplify Urdu text."""
        result = text
        
        # Apply word replacements
        for complex_word, simple_word in URDU_SIMPLIFICATIONS.items():
            if complex_word in result:
                result = result.replace(complex_word, simple_word)
                print(f"[Urdu] Replaced '{complex_word}' with '{simple_word}'")
        
        # Split very long sentences (at punctuation)
        result = self._split_long_sentences(result, ['۔', '،', '؛'])
        
        return result.strip()
    
    def _simplify_punjabi(self, text: str) -> str:
        """Simplify Punjabi text."""
        result = text
        
        # Apply Punjabi-specific replacements
        for complex_word, simple_word in PUNJABI_SIMPLIFICATIONS.items():
            if complex_word in result:
                result = result.replace(complex_word, simple_word)
        
        # Apply Urdu simplifications too (shared vocabulary)
        for complex_word, simple_word in URDU_SIMPLIFICATIONS.items():
            if complex_word in result:
                result = result.replace(complex_word, simple_word)
        
        result = self._split_long_sentences(result, ['۔', '،', '؛'])
        
        return result.strip()
    
    def _simplify_roman_urdu(self, text: str) -> str:
        """Simplify Roman Urdu text with comprehensive rules."""
        # Work with lowercase for matching
        words = text.split()
        simplified_words = []
        changes_made = 0
        
        for word in words:
            # Clean the word for lookup (remove punctuation at end)
            clean_word = word.lower().rstrip('.,!?;:')
            suffix = word[len(clean_word):] if len(word) > len(clean_word) else ''
            
            # Check for simplification
            if clean_word in ROMAN_URDU_SIMPLIFICATIONS:
                replacement = ROMAN_URDU_SIMPLIFICATIONS[clean_word]
                # Preserve original capitalization
                if word[0].isupper():
                    replacement = replacement.capitalize()
                simplified_words.append(replacement + suffix)
                changes_made += 1
                print(f"[Roman] Replaced '{clean_word}' with '{replacement}'")
            else:
                simplified_words.append(word)
        
        result = ' '.join(simplified_words)
        
        # If we made changes, capitalize first letter properly
        if result and changes_made > 0:
            result = result[0].upper() + result[1:]
        
        # Split long sentences
        result = self._split_long_sentences_roman(result)
        
        print(f"[Offline] Made {changes_made} word replacements")
        return result.strip()
    
    def _split_long_sentences(self, text: str, delimiters: List[str]) -> str:
        """Split sentences that are too long (for Arabic script)."""
        # If text is short, return as is
        if len(text) < 150:
            return text
        
        # Find potential split points at commas
        for delim in delimiters[1:]:  # Skip full stop, use comma etc
            if delim in text:
                parts = text.split(delim)
                if len(parts) > 1 and all(len(p.strip()) > 10 for p in parts):
                    # Rejoin with full stop
                    result = []
                    for part in parts:
                        part = part.strip()
                        if part:
                            result.append(part)
                    return f' {delimiters[0]} '.join(result) + delimiters[0]
        
        return text
    
    def _split_long_sentences_roman(self, text: str) -> str:
        """Split long Roman Urdu sentences at commas."""
        if len(text) < 120:
            return text
        
        # Split on commas if sentence is long
        if ', ' in text or ',' in text:
            parts = re.split(r',\s*', text)
            if len(parts) > 1:
                result = []
                for part in parts:
                    part = part.strip()
                    if part and len(part) > 5:
                        # Capitalize first letter
                        part = part[0].upper() + part[1:] if part else part
                        result.append(part)
                if result:
                    return '. '.join(result) + '.'
        
        return text
    
    def is_available(self) -> bool:
        """Offline simplifier is always available."""
        return True


# Module-level function for convenience
_simplifier: Optional[OfflineSimplifier] = None

def get_offline_simplifier() -> OfflineSimplifier:
    """Get the global offline simplifier instance."""
    global _simplifier
    if _simplifier is None:
        _simplifier = OfflineSimplifier()
    return _simplifier

def simplify_offline(text: str) -> str:
    """Simplify text using offline rules."""
    return get_offline_simplifier().simplify(text)
