# 🚀 Phrase Simplifier - Client Setup Guide

## یہ کیا ہے؟
یہ **Windows Desktop Application** ہے جو اردو، پنجابی اور Roman Urdu کے جملوں کو آسان بناتی ہے۔

---

## 📋 Step-by-Step Setup

### Step 1: Python Install کریں
1. [python.org/downloads](https://www.python.org/downloads/) سے **Python 3.11+** ڈاؤنلوڈ کریں
2. Install کرتے وقت **"Add Python to PATH"** ✅ ضرور چیک کریں
3. Install مکمل ہونے کے بعد computer restart کریں

### Step 2: Project Folder Copy کریں
پورا `phrase` فولڈر USB یا Google Drive سے client laptop میں copy کریں
مثال: `D:\phrase`

### Step 3: Dependencies Install کریں
PowerShell یا CMD کھولیں اور یہ commands چلائیں:
```powershell
cd D:\phrase
pip install -r requirements.txt
```

### Step 4: Desktop Shortcut بنائیں
```powershell
python create_shortcut.py
```
اب Desktop پر **Phrase Simplifier** icon آ جائے گا!

### Step 5: Application چلائیں
Desktop پر **Phrase Simplifier** icon پر double-click کریں

یا command سے چلائیں:
```powershell
python main.py
```

---

## 🔧 EXE بنانا (Optional)
اگر آپ `.exe` فائل بنانا چاہتے ہیں تاکہ Python install نہ کرنا پڑے:

```powershell
cd D:\phrase
python build.py
```

پھر `dist\PhraseSimplifier.exe` directly چلائیں۔

---

## ✅ Test کرنے کے لیے
```powershell
python test_app.py
```
سب ٹیسٹ پاس ہونے چاہیئیں (17/17)

---

## 📁 Project Files

| فائل | کام |
|------|-----|
| `main.py` | ایپ چلانے کا main file |
| `requirements.txt` | Dependencies کی لسٹ |
| `create_shortcut.py` | Desktop shortcut بنانے کے لیے |
| `build.py` | EXE بنانے کے لیے |
| `test_app.py` | ٹیسٹ چلانے کے لیے |
| `config.py` | API key اور settings |

---

## ⚠️ مسائل حل کرنا

### Problem: `pip` command not found
**حل:** Python دوبارہ install کریں اور "Add to PATH" چیک کریں

### Problem: API کام نہیں کر رہی
**حل:** Offline mode خود کام کرے گا۔ نئی API key کے لیے [ai.google.dev](https://ai.google.dev) پر جائیں

### Problem: Unicode/Urdu نظر نہیں آ رہا
**حل:** Windows میں Urdu fonts install کریں (Jameel Noori Nastaleeq)

---

## 🎯 استعمال
1. ایپ کھولیں
2. اپنا جملہ لکھیں (اردو، پنجابی، یا Roman Urdu)
3. **Send** دبائیں
4. آسان جملہ مل جائے گا!

---

**Made with ❤️ for Urdu speakers**
