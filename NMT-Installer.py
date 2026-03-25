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
        files = ["NMT.py", "nmt-u-c.py", "version.uvt"]
        for file in files:
            r = requests.get(repo_url + file)
            with open(file, "wb") as f: f.write(r.content)

        for script in ["NMT.py", "nmt-u-c.py"]:
            subprocess.run(["pyinstaller", "--onefile", "--noconsole", "--icon=icon.ico", script], check=True)
            exe_name = script.replace(".py", ".exe")
            if os.path.exists(f"dist/{exe_name}"):
                shutil.copy(f"dist/{exe_name}", exe_name)

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

        messagebox.showinfo("DarkFox Co.", "Full Suite Built & Pinned Successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("NMT - DEPLOYMENT")
root.geometry("400x300")
root.configure(bg="#050505")
tk.Label(root, text="NMT INSTALLER", fg="#00ffcc", bg="#050505", font=("Impact", 25)).pack(pady=30)
tk.Button(root, text="BUILD ALL FROM SOURCE", command=run_full_installation, bg="#00ffcc", font=("Arial", 12, "bold"), width=25).pack(pady=20)
root.mainloop()
