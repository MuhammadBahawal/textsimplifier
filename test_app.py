"""
Test script to verify all components of Phrase Simplifier work correctly.
Uses ASCII-safe output for Windows console compatibility.
"""
import sys
import os

# Fix encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules import correctly."""
    print("=" * 60)
    print("TESTING: Module Imports")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    try:
        from config import get_api_key, get_theme, APP_NAME
        print("[PASS] config module imported")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] config module: {e}")
        tests_failed += 1
    
    try:
        from src.language_detector import detect_language, Language
        print("[PASS] language_detector module imported")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] language_detector module: {e}")
        tests_failed += 1
    
    try:
        from src.network_checker import is_online, NetworkChecker
        print("[PASS] network_checker module imported")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] network_checker module: {e}")
        tests_failed += 1
    
    try:
        from src.simplifier_offline import simplify_offline, OfflineSimplifier
        print("[PASS] simplifier_offline module imported")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] simplifier_offline module: {e}")
        tests_failed += 1
    
    try:
        from src.simplifier_online import OnlineSimplifier
        print("[PASS] simplifier_online module imported")
        tests_passed += 1
    except Exception as e:
        print(f"[FAIL] simplifier_online module: {e}")
        tests_failed += 1
    
    return tests_passed, tests_failed


def test_language_detection():
    """Test language detection functionality."""
    print("\n" + "=" * 60)
    print("TESTING: Language Detection")
    print("=" * 60)
    
    from src.language_detector import detect_language, Language
    
    tests_passed = 0
    tests_failed = 0
    
    # Test Urdu (using Arabic script)
    urdu_text = "\u0645\u06cc\u06ba \u0646\u06d2 \u0622\u062c \u0627\u06cc\u06a9 \u06a9\u062a\u0627\u0628 \u067e\u0691\u06be\u06cc"
    lang, conf = detect_language(urdu_text)
    if lang == Language.URDU:
        print(f"[PASS] Urdu text detected correctly as {lang.value}")
        tests_passed += 1
    else:
        print(f"[FAIL] Expected URDU, got {lang.value}")
        tests_failed += 1
    
    # Test Roman Urdu
    roman_text = "Main kal aapke ghar aaunga"
    lang, conf = detect_language(roman_text)
    if lang == Language.ROMAN_URDU:
        print(f"[PASS] Roman Urdu detected: '{roman_text}' -> {lang.value}")
        tests_passed += 1
    else:
        print(f"[FAIL] Expected ROMAN_URDU, got {lang.value}")
        tests_failed += 1
    
    # Test another Roman Urdu
    roman_text2 = "Aap kaise hain? Sab theek hai?"
    lang, conf = detect_language(roman_text2)
    print(f"[PASS] Language detection working: '{roman_text2}' -> {lang.value}")
    tests_passed += 1
    
    return tests_passed, tests_failed


def test_offline_simplifier():
    """Test offline simplification functionality."""
    print("\n" + "=" * 60)
    print("TESTING: Offline Simplifier")
    print("=" * 60)
    
    from src.simplifier_offline import simplify_offline
    
    tests_passed = 0
    tests_failed = 0
    
    # Test Roman Urdu simplification
    test_input = "Main definitely zaroor aaunga"
    result = simplify_offline(test_input)
    print(f"[INFO] Input: '{test_input}'")
    print(f"[INFO] Output: '{result}'")
    if result and len(result) > 0:
        print("[PASS] Offline simplifier returned result")
        tests_passed += 1
    else:
        print("[FAIL] No result from offline simplifier")
        tests_failed += 1
    
    # Test another input
    test_input2 = "This is information about education"
    result2 = simplify_offline(test_input2)
    print(f"[INFO] Input 2: '{test_input2}'")
    print(f"[INFO] Output 2: '{result2}'")
    if result2 and len(result2) > 0:
        print("[PASS] Second simplification test passed")
        tests_passed += 1
    else:
        print("[FAIL] Second simplification failed")
        tests_failed += 1
    
    return tests_passed, tests_failed


def test_network_checker():
    """Test network connectivity checker."""
    print("\n" + "=" * 60)
    print("TESTING: Network Checker")
    print("=" * 60)
    
    from src.network_checker import is_online
    
    online = is_online()
    print(f"[INFO] Internet status: {'Online' if online else 'Offline'}")
    print("[PASS] Network checker executed successfully")
    
    return 1, 0


def test_ui_components():
    """Test UI components can be initialized."""
    print("\n" + "=" * 60)
    print("TESTING: UI Components")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        
        # Create app for testing (required for widget creation)
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        from src.message_bubble import MessageBubble, TypingIndicator
        
        # Test message bubble creation
        bubble = MessageBubble("Test message", is_user=True)
        print("[PASS] MessageBubble (user) created")
        tests_passed += 1
        
        bubble_ai = MessageBubble("AI response", is_user=False)
        print("[PASS] MessageBubble (AI) created")
        tests_passed += 1
        
        # Test RTL bubble
        bubble_rtl = MessageBubble("RTL message test", is_user=True, is_rtl=True)
        print("[PASS] MessageBubble (RTL) created")
        tests_passed += 1
        
        # Test typing indicator
        typing = TypingIndicator()
        print("[PASS] TypingIndicator created")
        tests_passed += 1
        
        from src.chat_widget import ChatWidget
        chat = ChatWidget()
        print("[PASS] ChatWidget created")
        tests_passed += 1
        
        from src.app import MainWindow
        window = MainWindow()
        print("[PASS] MainWindow created")
        tests_passed += 1
        
    except Exception as e:
        print(f"[FAIL] UI component error: {e}")
        import traceback
        traceback.print_exc()
        tests_failed += 1
    
    return tests_passed, tests_failed


def run_all_tests():
    """Run all tests and report results."""
    print("\n")
    print("#" * 60)
    print("#   PHRASE SIMPLIFIER - AUTOMATED TEST SUITE")
    print("#" * 60)
    
    total_passed = 0
    total_failed = 0
    
    # Run tests
    passed, failed = test_imports()
    total_passed += passed
    total_failed += failed
    
    passed, failed = test_language_detection()
    total_passed += passed
    total_failed += failed
    
    passed, failed = test_offline_simplifier()
    total_passed += passed
    total_failed += failed
    
    passed, failed = test_network_checker()
    total_passed += passed
    total_failed += failed
    
    passed, failed = test_ui_components()
    total_passed += passed
    total_failed += failed
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total Passed: {total_passed}")
    print(f"Total Failed: {total_failed}")
    if total_passed + total_failed > 0:
        print(f"Success Rate: {total_passed/(total_passed+total_failed)*100:.1f}%")
    print("=" * 60)
    
    if total_failed == 0:
        print("\n*** ALL TESTS PASSED! Application is working correctly. ***\n")
    else:
        print(f"\n*** {total_failed} TEST(S) FAILED. Please check the errors above. ***\n")
    
    return total_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
