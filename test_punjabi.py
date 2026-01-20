
import sys
import os

# Fix encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.language_detector import detect_language, Language
from src.simplifier_online import simplify_online

def test_punjabi_detection():
    print("=" * 60)
    print("TESTING: Punjabi Language Detection")
    print("=" * 60)
    
    test_cases = [
        ("ਤੁਹਾਡਾ ਕੀ ਹਾਲ ਹੈ?", Language.PUNJABI, "Gurmukhi Punjabi"),
        ("Tuhada ki haal hai?", Language.PUNJABI, "Roman Punjabi"),
        ("Kiven ho paaji?", Language.PUNJABI, "Roman Punjabi 2"),
        ("Sadda kuta kuta, tuhada kuta Tommy", Language.PUNJABI, "Roman Punjabi 3"),
    ]
    
    passed = 0
    for text, expected, label in test_cases:
        lang, conf = detect_language(text)
        if lang == expected:
            print(f"[PASS] {label}: detected {lang.value} (conf: {conf:.2f})")
            passed += 1
        else:
            print(f"[FAIL] {label}: expected {expected.value}, got {lang.value} (conf: {conf:.2f})")
            
    # Shahmukhi test (currently likely to detect as URDU)
    shahmukhi_text = "تہاڈا کی حال اے؟"
    lang, conf = detect_language(shahmukhi_text)
    print(f"[INFO] Shahmukhi ('{shahmukhi_text}'): detected {lang.value} (conf: {conf:.2f})")
    
    return passed, len(test_cases)

def test_punjabi_simplification():
    print("\n" + "=" * 60)
    print("TESTING: Punjabi Simplification (Online)")
    print("=" * 60)
    
    # Gurmukhi
    text1 = "ਮੈਂ ਅੱਜ ਬਹੁਤ ਖੁਸ਼ ਹਾਂ ਕਿਉਂਕਿ ਮੇਰਾ ਕੰਮ ਖਤਮ ਹੋ ਗਿਆ ਹੈ।"
    print(f"[INFO] Input (Gurmukhi): {text1}")
    result1 = simplify_online(text1)
    if result1:
        print(f"[PASS] Output: {result1}")
    else:
        print("[FAIL] No result for Gurmukhi")
        
    # Roman Punjabi
    text2 = "Mainu lagda hai ke sanu eh kamm jaldi khatam karna chahida hai."
    print(f"\n[INFO] Input (Roman): {text2}")
    result2 = simplify_online(text2)
    if result2:
        print(f"[PASS] Output: {result2}")
    else:
        print("[FAIL] No result for Roman Punjabi")

    return 2 if (result1 and result2) else 1

if __name__ == "__main__":
    p_det, t_det = test_punjabi_detection()
    p_sim = test_punjabi_simplification()
    print("\n" + "=" * 60)
    print(f"PUNJABI TEST SUMMARY: {p_det}/{t_det} detection passed, {p_sim}/2 simplification passed")
    print("=" * 60)
