import os, subprocess, shutil, sys, requests
import tkinter as tk
from tkinter import messagebox

def forge():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "pyinstaller"])
        repo = "https://raw.githubusercontent.com/SlabyLol/NMT-NoMoreTypewriter/main/"
        
        for f in ["NMT.py", "nmt-u-c.py", "p-nmt.uvt"]:
            r = requests.get(repo + f)
            with open(f, "wb") as file: file.write(r.content)
            
        with open("p-nmt.uvt", "r") as f:
            for p in f.read().splitlines():
                if p.strip():
                    subprocess.check_call([sys.executable, "-m", "pip", "install", p.strip()])
                    
        for s in ["NMT.py", "nmt-u-c.py"]:
            subprocess.run(["pyinstaller", "--onefile", "--noconsole", s], check=True)
            exe = s.replace(".py", ".exe")
            shutil.copy(f"dist/{exe}", exe)
            
        messagebox.showinfo("DARKFOX", "SYSTEM FORGED")
    except Exception as e:
        messagebox.showerror("ERR", str(e))

root = tk.Tk()
root.title("NMT FORGE")
root.geometry("300x150")
root.configure(bg="#050505")
tk.Button(root, text="FORGE NMT SYSTEM", command=forge, bg="#00ffcc", font=("Arial", 12, "bold")).pack(pady=50)
root.mainloop()
