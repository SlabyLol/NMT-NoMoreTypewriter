import os
import subprocess
import shutil
import tkinter as tk
from tkinter import messagebox
import sys
import ctypes

def install_requirements():
    packages = ["customtkinter", "pyautogui", "pytesseract", "pillow", "pygetwindow", "requests", "winshell", "pypiwin32", "pyinstaller"]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def create_icon():
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGBA', (256, 256), color=(10, 10, 10, 255))
    draw = ImageDraw.Draw(img)
    draw.ellipse([10, 10, 246, 246], outline=(0, 255, 204), width=12)
    draw.text((50, 90), "NMT", fill=(0, 255, 204), font=None)
    img.save("icon.ico", format="ICO", sizes=[(256, 256)])

def create_shortcuts():
    import winshell
    from win32com.client import Dispatch
    
    desktop = winshell.desktop()
    path = os.path.join(desktop, "NMT - NoMoreTypewriter.lnk")
    target = os.path.abspath("NMT.exe")
    icon = os.path.abspath("icon.ico")
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = os.path.abspath("")
    shortcut.IconLocation = icon
    shortcut.save()
    
    vbs_path = "pin_to_taskbar.vbs"
    with open(vbs_path, "w") as f:
        f.write(f'Set objShell = CreateObject("Shell.Application")\n')
        f.write(f'Set objFolder = objShell.Namespace("{os.path.abspath("")}")\n')
        f.write(f'Set objFolderItem = objFolder.ParseName("NMT.exe")\n')
        f.write(f'objFolderItem.InvokeVerb("taskbarpin")')
    
    subprocess.run(["wscript.exe", vbs_path])
    os.remove(vbs_path)

def full_build():
    try:
        install_requirements()
        create_icon()
        
        if not os.path.exists("version.uvt"):
            with open("version.uvt", "w") as f: f.write("1.0.0")

        subprocess.run(["pyinstaller", "--onefile", "--noconsole", "--icon=icon.ico", "NMT.py"], check=True)
        if os.path.exists("dist/NMT.exe"): shutil.copy("dist/NMT.exe", "NMT.exe")

        subprocess.run(["pyinstaller", "--onefile", "--noconsole", "--icon=icon.ico", "nmt-u-c.py"], check=True)
        if os.path.exists("dist/nmt-u-c.exe"): shutil.copy("dist/nmt-u-c.exe", "nmt-u-c.exe")

        messagebox.showinfo("Success", "Build Complete! You can now create shortcuts.")
    except Exception as e:
        messagebox.showerror("Error", f"Build failed: {e}")

def run_shortcut_logic():
    try:
        create_shortcuts()
        messagebox.showinfo("Success", "Desktop and Taskbar shortcuts created!")
    except Exception as e:
        messagebox.showerror("Error", f"Shortcut failed: {e}")

def create_ui():
    root = tk.Tk()
    root.title("DARKFOX CO. - DEPLOYMENT TOOL")
    root.geometry("500x450")
    root.configure(bg="#050505")

    title = tk.Label(root, text="NMT INSTALLER", fg="#00ffcc", bg="#050505", font=("Impact", 30))
    title.pack(pady=30)

    build_btn = tk.Button(root, text="BUILD NMT & UPDATER (EXE)", command=full_build, bg="#00ffcc", fg="#000", font=("Arial", 12, "bold"), width=30)
    build_btn.pack(pady=10)

    shortcut_btn = tk.Button(root, text="CREATE SHORTCUTS & PIN", command=run_shortcut_logic, bg="#111", fg="#00ffcc", borderwidth=2, relief="flat", font=("Arial", 12, "bold"), width=30)
    shortcut_btn.pack(pady=10)

    exit_btn = tk.Button(root, text="EXIT", command=root.quit, bg="#333", fg="#fff", font=("Arial", 10), width=15)
    exit_btn.pack(pady=30)

    root.mainloop()

if __name__ == "__main__":
    create_ui()
