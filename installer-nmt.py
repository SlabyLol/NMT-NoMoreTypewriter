import os
import subprocess
import shutil
import tkinter as tk
from tkinter import messagebox
import sys
import requests

def build_from_repo():
    try:
        packages = ["customtkinter", "pyautogui", "pytesseract", "pillow", "pygetwindow", "requests", "winshell", "pypiwin32", "pyinstaller"]
        for p in packages:
            subprocess.check_call([sys.executable, "-m", "pip", "install", p])

        from PIL import Image, ImageDraw
        img = Image.new('RGBA', (256, 256), color=(10, 10, 10, 255))
        draw = ImageDraw.Draw(img)
        draw.ellipse([10, 10, 246, 246], outline=(0, 255, 204), width=12)
        img.save("icon.ico", format="ICO", sizes=[(256, 256)])

        repo_base = "https://raw.githubusercontent.com/SlabyLol/NMT-NoMoreTypewriter/main/"
        
        files = ["NMT.py", "nmt-u-c.py"]
        for file in files:
            print(f"Downloading {file}...")
            r = requests.get(repo_base + file)
            with open(file, "wb") as f:
                f.write(r.content)

        for file in files:
            print(f"Compiling {file}...")
            subprocess.run(["pyinstaller", "--onefile", "--noconsole", "--icon=icon.ico", file], check=True)
            exe_name = file.replace(".py", ".exe")
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

        messagebox.showinfo("DarkFox Co.", "Download and EXE Generation Complete!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("NMT CLOUD INSTALLER")
root.geometry("400x250")
root.configure(bg="#050505")
tk.Label(root, text="NMT CLOUD FACTORY", fg="#00ffcc", bg="#050505", font=("Impact", 20)).pack(pady=20)
tk.Button(root, text="DOWNLOAD & BUILD FROM REPO", command=build_from_repo, bg="#00ffcc", font=("Arial", 10, "bold")).pack(pady=20)
root.mainloop()
