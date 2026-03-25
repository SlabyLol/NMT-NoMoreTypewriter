import os, subprocess, sys, requests, shutil, time

def update():
    repo = "https://raw.githubusercontent.com/SlabyLol/NMT-NoMoreTypewriter/main/"
    try:
        local_v = "0.0.0"
        if os.path.exists("version.uvt"):
            with open("version.uvt", "r") as f: local_v = f.read().strip()
        
        rv = requests.get(repo + "version.uvt").text.strip()
        
        if rv != local_v:
            r_req = requests.get(repo + "p-nmt.uvt")
            with open("p-nmt.uvt", "w") as f: f.write(r_req.text)
            
            for p in r_req.text.splitlines():
                if p.strip(): subprocess.check_call([sys.executable, "-m", "pip", "install", p.strip()])
            
            for f in ["NMT.py", "version.uvt"]:
                res = requests.get(repo + f)
                with open(f, "wb") as file: file.write(res.content)
            
            os.system("taskkill /f /im NMT.exe")
            time.sleep(1)
            
            subprocess.run(["pyinstaller", "--onefile", "--noconsole", "NMT.py"], check=True)
            
            if os.path.exists("NMT.exe"): os.remove("NMT.exe")
            shutil.copy("dist/NMT.exe", "NMT.exe")
            
            subprocess.Popen(["NMT.exe"])
    except:
        pass

if __name__ == "__main__":
    update()
