"""
Create a desktop shortcut for Phrase Simplifier.
Run this script to add the app to your desktop.
"""
import os
import sys
from pathlib import Path

def create_desktop_shortcut():
    """Create a Windows desktop shortcut for the application."""
    
    # Get paths
    app_dir = Path(__file__).parent
    main_script = app_dir / "main.py"
    
    # Get desktop path
    desktop = Path(os.path.expanduser("~")) / "Desktop"
    shortcut_path = desktop / "Phrase Simplifier.lnk"
    
    # Get Python executable
    python_exe = sys.executable
    
    try:
        # Use PowerShell to create shortcut
        import subprocess
        
        # Icon path
        icon_path = app_dir / "assets" / "icon.ico"
        
        ps_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{python_exe}"
$Shortcut.Arguments = '"{main_script}"'
$Shortcut.WorkingDirectory = "{app_dir}"
$Shortcut.Description = "Phrase Simplifier - Simplify Urdu, Punjabi, Roman Urdu"
$Shortcut.IconLocation = "{icon_path}"
$Shortcut.WindowStyle = 1
$Shortcut.Save()
'''
        
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("=" * 50)
            print("SUCCESS: Desktop shortcut created!")
            print("=" * 50)
            print(f"Location: {shortcut_path}")
            print("You can now launch Phrase Simplifier from your desktop!")
            print("=" * 50)
            return True
        else:
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Failed to create shortcut: {e}")
        return False


def create_batch_launcher():
    """Create a batch file launcher as an alternative."""
    app_dir = Path(__file__).parent
    batch_path = app_dir / "PhraseSimplifier.bat"
    desktop = Path(os.path.expanduser("~")) / "Desktop"
    desktop_batch = desktop / "PhraseSimplifier.bat"
    
    batch_content = f'''@echo off
title Phrase Simplifier
cd /d "{app_dir}"
pythonw main.py
'''
    
    # Create in app directory
    with open(batch_path, 'w') as f:
        f.write(batch_content)
    
    # Copy to desktop
    with open(desktop_batch, 'w') as f:
        f.write(batch_content)
    
    print("=" * 50)
    print("SUCCESS: Batch launcher created!")
    print("=" * 50)
    print(f"App folder: {batch_path}")
    print(f"Desktop: {desktop_batch}")
    print("Double-click to launch!")
    print("=" * 50)
    return True


if __name__ == "__main__":
    print("")
    print("Creating Desktop Shortcut...")
    print("")
    
    success = create_desktop_shortcut()
    
    if not success:
        print("")
        print("Shortcut creation failed. Creating batch launcher instead...")
        print("")
        create_batch_launcher()
