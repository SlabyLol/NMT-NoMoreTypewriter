import os, sys, requests, subprocess, time, shutil

def run_sync():
    repo = "https://raw.githubusercontent.com/SlabyLol/NMT-NoMoreTypewriter/main/"
    try:
        r = requests.get(repo + "p-nmt.uvt")
        if r.status_code == 200:
            for pkg in r.text.splitlines():
                if pkg.strip():
                    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg.strip()])
        
        for f in ["NMT.py", "nmt-u-c.py"]:
            req = requests.get(repo + f)
            with open(f, "wb") as file:
                file.write(req.content)
                
        subprocess.run(["pyinstaller", "--onefile", "--noconsole", "NMT.py"], check=True)
        if os.path.exists("NMT.exe"):
            try: os.rename("NMT.exe", "NMT.old.exe")
            except: pass
        shutil.copy("dist/NMT.exe", "NMT.exe")
        
        subprocess.run(["pyinstaller", "--onefile", "--noconsole", "nmt-u-c.py"], check=True)
        if os.path.exists("dist/nmt-u-c.exe"):
            bat = "u_bypass.bat"
            with open(bat, "w") as b:
                b.write('@echo off\ntimeout /t 2 /nobreak > NUL\nmove /y dist\\nmt-u-c.exe nmt-u-c.exe\nstart nmt-u-c.exe\ndel "%~f0"')
            os.startfile(bat)
            sys.exit()
    except:
        pass

if __name__ == "__main__":
    run_sync()
