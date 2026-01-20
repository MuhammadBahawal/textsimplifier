# 🚀 Phrase Simplifier - Setup Guide

## یہ کیا ہے؟
یہ **Windows Desktop Application** ہے جو PySide6 (Qt) سے بنی ہے۔
- ✅ Windows 10/11 پر چلتی ہے
- ✅ Mac/Linux پر بھی چل سکتی ہے

---

## 📋 Client Laptop پر Setup کرنے کا طریقہ

### Step 1: Python Install کریں
1. [python.org/downloads](https://www.python.org/downloads/) سے Python 3.11+ ڈاؤنلوڈ کریں
2. Install کرتے وقت **"Add Python to PATH"** ✅ ضرور چیک کریں

### Step 2: Project Folder Copy کریں
پورا `d:\phrase` فولڈر USB یا Google Drive سے client laptop میں copy کریں

### Step 3: Dependencies Install کریں
PowerShell یا CMD کھولیں اور:
```powershell
cd d:\phrase
pip install -r requirements.txt
```

### Step 4: Application چلائیں
```powershell
python main.py
```

---

## 🔧 EXE بنانے کا طریقہ (Optional)
اگر آپ `.exe` فائل بنانا چاہتے ہیں تاکہ Python install نہ کرنا پڑے:

```powershell
cd d:\phrase
python build.py
```

پھر `dist\PhraseSimplifier.exe` چلائیں۔

---

## ⚠️ ضروری باتیں
1. **Internet** ہونی چاہیے (Online mode کے لیے)
2. بغیر Internet کے **Offline mode** خود کام کرے گا
3. API Key پہلے سے config میں ہے، change کرنے کی ضرورت نہیں

---

## 🎯 استعمال
1. ایپ کھولیں
2. اپنا جملہ لکھیں (اردو، پنجابی، یا Roman Urdu)
3. Send دبائیں
4. آسان جملہ مل جائے گا!
