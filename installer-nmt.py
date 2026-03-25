import os
import subprocess
import shutil
import tkinter as tk
from tkinter import messagebox
import sys
import requests

def run_full_installation():
    try:
        packages = ["customtkinter", "pyautogui", "pytesseract", "pillow", "pygetwindow", "requests", "winshell", "pypiwin32", "pyinstaller"]
        for p in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", p])

        from PIL import Image, ImageDraw
        img = Image.new('RGBA', (256, 256), color=(10, 10, 10, 255))
        draw = ImageDraw.Draw(img)
        draw.ellipse([10, 10, 246, 246], outline=(0, 255, 204), width=12)
        img.save("icon.ico", format="ICO", sizes=[(256, 256)])

        repo_url = "https://raw.githubusercontent.com/SlabyLol/NMT-NoMoreTypewriter/main/"
        
        for file in ["NMT.py", "nmt-u-c.py", "version.uvt"]:
            r = requests.get(repo_url + file)
            with open(file, "wb") as f:
                f.write(r.content)

        subprocess.run(["pyinstaller", "--onefile", "--noconsole", "--icon=icon.ico", "NMT.py"], check=True)
        shutil.copy("dist/NMT.exe", "NMT.exe")

        subprocess.run(["pyinstaller", "--onefile", "--noconsole", "--icon=icon.ico", "nmt-u-c.py"], check=True)
        shutil.copy("dist/nmt-u-c.exe", "nmt-u-c.exe")

        import winshell
        from win32com.client import Dispatch
        path = os.path.join(winshell.desktop(), "NMT.lnk")
        shortcut = Dispatch('WScript.Shell').CreateShortCut(path)
        shortcut.Targetpath = os.path.abspath("NMT.exe")
        shortcut.WorkingDirectory = os.path.abspath("")
        shortcut.IconLocation = os.path.abspath("icon.ico")
        shortcut.save()

        vbs = "pin.vbs"
        with open(vbs, "w") as f:
            f.write(f'Set s = CreateObject("Shell.Application")\nSet f = s.Namespace("{os.path.abspath("")}")\nSet i = f.ParseName("NMT.exe")\ni.InvokeVerb("taskbarpin")')
        subprocess.run(["wscript.exe", vbs])
        os.remove(vbs)

        for folder in ["build", "dist"]:
            if os.path.exists(folder): shutil.rmtree(folder)
        for file in ["NMT.spec", "nmt-u-c.spec"]:
            if os.path.exists(file): os.remove(file)

        messagebox.showinfo("DarkFox Co.", "Installation Success! App, Updater, and Version file synced.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("NMT - OFFICIAL INSTALLER")
root.geometry("400x300")
root.configure(bg="#050505")
tk.Label(root, text="NMT DEPLOYMENT", fg="#00ffcc", bg="#050505", font=("Impact", 25)).pack(pady=30)
tk.Button(root, text="FULL INSTALL & BUILD", command=run_full_installation, bg="#00ffcc", font=("Arial", 12, "bold"), width=25).pack(pady=20)
root.mainloop()
