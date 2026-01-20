"""
Build script for creating a Windows executable (.exe)
Uses PyInstaller to package the application.
"""
import subprocess
import sys
import os
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).parent
MAIN_SCRIPT = PROJECT_DIR / "main.py"
DIST_DIR = PROJECT_DIR / "dist"
BUILD_DIR = PROJECT_DIR / "build"
ICON_PATH = PROJECT_DIR / "assets" / "icon.ico"

# Application info
APP_NAME = "PhraseSimplifier"
APP_VERSION = "1.0.0"


def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
        return True
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        return True


def build_exe():
    """Build the Windows executable."""
    print("\n" + "=" * 50)
    print("  Phrase Simplifier - Build Script")
    print("=" * 50 + "\n")
    
    # Check dependencies
    check_pyinstaller()
    
    # Prepare PyInstaller arguments
    args = [
        sys.executable,
        "-m", "PyInstaller",
        "--name", APP_NAME,
        "--onefile",  # Single executable
        "--windowed",  # No console window
        "--clean",  # Clean build
        "--noconfirm",  # Overwrite without asking
    ]
    
    # Add icon if available
    if ICON_PATH.exists():
        args.extend(["--icon", str(ICON_PATH)])
        print(f"✓ Using icon: {ICON_PATH}")
    else:
        print("! No icon found, using default")
    
    # Add data files
    args.extend([
        "--add-data", f"{PROJECT_DIR / 'styles'};styles",
        "--add-data", f"{PROJECT_DIR / 'config.py'};.",
    ])
    
    # Add hidden imports (PySide6 plugins)
    hidden_imports = [
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "google.generativeai",
        "google.ai.generativelanguage",
    ]
    
    for imp in hidden_imports:
        args.extend(["--hidden-import", imp])
    
    # Add the main script
    args.append(str(MAIN_SCRIPT))
    
    print("\n📦 Building executable...\n")
    print(f"Command: {' '.join(args)}\n")
    
    # Run PyInstaller
    result = subprocess.run(args, cwd=str(PROJECT_DIR))
    
    if result.returncode == 0:
        exe_path = DIST_DIR / f"{APP_NAME}.exe"
        print("\n" + "=" * 50)
        print("  ✓ BUILD SUCCESSFUL!")
        print("=" * 50)
        print(f"\n📁 Executable location:")
        print(f"   {exe_path}")
        print(f"\n📊 Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        print("\n🚀 You can now run PhraseSimplifier.exe!")
        print("=" * 50 + "\n")
    else:
        print("\n❌ Build failed! Check the errors above.")
        sys.exit(1)


def clean():
    """Clean build artifacts."""
    import shutil
    
    print("🧹 Cleaning build artifacts...")
    
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        print(f"   Removed: {BUILD_DIR}")
    
    spec_file = PROJECT_DIR / f"{APP_NAME}.spec"
    if spec_file.exists():
        spec_file.unlink()
        print(f"   Removed: {spec_file}")
    
    print("✓ Clean complete!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean()
    else:
        build_exe()
