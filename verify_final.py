
import sys
import os
import time

# Ensure output is UTF-8 for console
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.simplifier_online import simplify_online
from src.language_detector import detect_language, get_language_name

def test_simplification(text, label):
    print(f"\n--- Testing {label} ---")
    print(f"Input: {text}")
    
    lang, conf = detect_language(text)
    print(f"Detected: {get_language_name(lang)} (Confidence: {conf:.2f})")
    
    print("Simplifying...")
    start_time = time.time()
    result = simplify_online(text)
    end_time = time.time()
    
    if result:
        print(f"Output: {result}")
        print(f"Time taken: {end_time - start_time:.2f}s")
        return True
    else:
        print("FAILED: No result from simplification.")
        return False

def run_all_checks():
    print("=" * 60)
    print("PHRASE SIMPLIFIER - FINAL END-TO-END VERIFICATION")
    print("=" * 60)
    
    test_cases = [
        # Punjabi Gurmukhi
        ("ਤੁਹਾਡਾ ਕੀ ਹਾਲ ਹੈ? ਮੈਂ ਬਹੁਤ ਖੁਸ਼ ਹਾਂ ਕਿਉਂਕਿ ਮੈਂ ਅੱਜ ਕੰਮ ਮੁਕਾ ਲਿਆ ਹੈ।", "Punjabi Gurmukhi"),
        # Punjabi Shahmukhi
        ("تہاڈا کی حال اے؟ میں بہت خوش واں کیوں جے میرا کم مک گیا اے۔", "Punjabi Shahmukhi"),
        # Punjabi Roman
        ("Tuhada ki haal hai? Main te vadiya waan.", "Punjabi Roman"),
        # Urdu
        ("میں نہایت ہی مسرت محسوس کر رہا ہوں کہ میرا کام مکمل ہو چکا ہے۔", "Urdu Script"),
        # Roman Urdu
        ("Main bohat khush hoon kyun ke mera kaam khatam ho gaya hai.", "Roman Urdu")
    ]
    
    passed = 0
    for text, label in test_cases:
        if test_simplification(text, label):
            passed += 1
            
    print("\n" + "=" * 60)
    print(f"FINAL SUMMARY: {passed}/{len(test_cases)} tests passed.")
    print("=" * 60)
    
    return passed == len(test_cases)

if __name__ == "__main__":
    success = run_all_checks()
    sys.exit(0 if success else 1)
