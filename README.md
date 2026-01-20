# Phrase Simplifier

A Windows desktop chatbot application that simplifies text in **Urdu**, **Punjabi**, and **Roman Urdu**.

![Phrase Simplifier](assets/screenshot.png)

## ✨ Features

- **Chatbot Interface**: Modern, conversational UI design
- **Multi-Language Support**: Urdu, Punjabi, and Roman Urdu
- **Online Mode**: Uses Google Gemini AI for intelligent simplification
- **Offline Mode**: Works without internet using local NLP rules
- **Auto Language Detection**: Automatically detects the input language
- **RTL Support**: Proper right-to-left text rendering for Urdu/Punjabi
- **Dark & Light Themes**: Toggle between themes with one click
- **Windows Compatible**: Runs on Windows 10 and 11

## 🚀 Quick Start

### Option 1: Run from Source

1. **Install Python 3.11+** from [python.org](https://www.python.org/)

2. **Install dependencies**:
   ```powershell
   cd d:\phrase
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```powershell
   python main.py
   ```

### Option 2: Build Executable

1. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Build the .exe**:
   ```powershell
   python build.py
   ```

3. **Run the executable**:
   ```powershell
   .\dist\PhraseSimplifier.exe
   ```

## 🔧 Configuration

### API Key (Optional)

For best results, get a free Google Gemini API key:

1. Visit [ai.google.dev](https://ai.google.dev)
2. Create a new API key
3. Set it in the app via **Settings ⚙️** or as an environment variable:
   ```powershell
   $env:GEMINI_API_KEY = "your-api-key-here"
   ```

### Without API Key

The app works without an API key using **offline mode**, which uses rule-based simplification.

## 📁 Project Structure

```
d:\phrase\
├── main.py                    # Application entry point
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── build.py                   # Build script for .exe
├── README.md                  # This file
│
├── src/
│   ├── __init__.py
│   ├── app.py                 # Main window
│   ├── chat_widget.py         # Chat UI component
│   ├── message_bubble.py      # Message bubble widget
│   ├── language_detector.py   # Language detection
│   ├── simplifier_online.py   # Gemini API integration
│   ├── simplifier_offline.py  # Offline NLP rules
│   └── network_checker.py     # Internet connectivity
│
├── styles/
│   ├── dark_theme.qss         # Dark mode styles
│   └── light_theme.qss        # Light mode styles
│
├── assets/
│   └── icon.ico               # App icon
│
└── dist/                      # Built executable
    └── PhraseSimplifier.exe
```

## 🌐 Online vs Offline Mode

### Online Mode (Gemini AI)
- Uses Google's Gemini 1.5 Flash model
- Best quality simplification results
- Requires internet connection
- Requires API key (free tier available)

### Offline Mode
- Works completely without internet
- Uses rule-based NLP techniques
- Synonym replacement
- Sentence structure simplification
- Instant response time

The app automatically switches between modes based on internet availability.

## 🎨 Themes

Toggle between **Dark** and **Light** themes using the 🌙/☀️ button in the toolbar.

## 📝 Usage Examples

### Urdu Input:
```
میں نے آج ایک انتہائی شاندار اور لاجواب کتاب کا مطالعہ کیا
↓
میں نے آج ایک بہت اچھی کتاب پڑھی
```

### Roman Urdu Input:
```
Main kal definitely zaroor aapke ghar aaunga
↓
Main kal zaroor aapke ghar aaunga
```

### Punjabi Input:
```
ایہ کم بہت شاندار طریقے نال ہویا
↓
ایہ کم بہت ودیا طریقے نال ہویا
```

## 🛠️ Development

### Running Tests
```powershell
python -m pytest tests/
```

### Building a New Release
```powershell
python build.py
```

### Cleaning Build Artifacts
```powershell
python build.py clean
```

## 📄 License

MIT License - Feel free to use and modify.

## 🙏 Credits

- Built with [PySide6](https://www.qt.io/qt-for-python) (Qt for Python)
- Powered by [Google Gemini AI](https://ai.google.dev)
- Urdu/Punjabi font support via system fonts

---

Made with ❤️ for Urdu, Punjabi, and Roman Urdu speakers
