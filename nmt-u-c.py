import os
import time
import requests
import subprocess
import shutil

REPO_URL = "https://raw.githubusercontent.com/SlabyLol/NMT-NoMoreTypewriter/main/"

def refresh_shortcuts():
    try:
        import winshell
        from win32com.client import Dispatch
        path = os.path.join(winshell.desktop(), "NMT.lnk")
        shortcut = Dispatch('WScript.Shell').CreateShortCut(path)
        shortcut.Targetpath = os.path.abspath("NMT.exe")
        shortcut.WorkingDirectory = os.path.abspath("")
        shortcut.IconLocation = os.path.abspath("icon.ico")
        shortcut.save()
        
        vbs = "repin.vbs"
        with open(vbs, "w") as f:
            f.write(f'Set s = CreateObject("Shell.Application")\nSet f = s.Namespace("{os.path.abspath("")}")\nSet i = f.ParseName("NMT.exe")\ni.InvokeVerb("taskbarpin")')
        subprocess.run(["wscript.exe", vbs])
        os.remove(vbs)
    except: pass

def update_system():
    try:
        time.sleep(2)
        r_ver = requests.get(REPO_URL + "version.uvt", timeout=5)
        remote_v = r_ver.text.strip()
        local_v = "0.0.0"
        if os.path.exists("version.uvt"):
            with open("version.uvt", "r") as f: local_v = f.read().strip()
            
        if remote_v > local_v:
            r_py = requests.get(REPO_URL + "NMT.py")
            with open("NMT.py", "wb") as f: f.write(r_py.content)
            
            subprocess.run(["pyinstaller", "--onefile", "--noconsole", "--icon=icon.ico", "NMT.py"], check=True)
            if os.path.exists("NMT.exe"): os.remove("NMT.exe")
            shutil.copy("dist/NMT.exe", "NMT.exe")
            
            with open("version.uvt", "w") as f: f.write(remote_v)
            refresh_shortcuts()
            
            for folder in ["build", "dist"]:
                if os.path.exists(folder): shutil.rmtree(folder)
    except: pass
    if os.path.exists("NMT.exe"): subprocess.Popen(["NMT.exe"])

if __name__ == "__main__":
    update_system()
