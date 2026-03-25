import os
import time
import requests
import subprocess
import sys

GITHUB_VERSION_URL = "https://raw.githubusercontent.com/SlabyLol/NMT-NoMoreTypewriter/main/version.uvt"
GITHUB_EXE_URL = "https://github.com/SlabyLol/NMT-NoMoreTypewriter/releases/latest/download/NMT.exe"

def get_local_version():
    if os.path.exists("version.uvt"):
        with open("version.uvt", "r") as f: return f.read().strip()
    return "0.0.0"

def run_update():
    local_v = get_local_version()
    try:
        r_ver = requests.get(GITHUB_VERSION_URL, timeout=5)
        remote_v = r_ver.text.strip()
        if remote_v > local_v:
            if os.path.exists("NMT.exe"): os.remove("NMT.exe")
            r_exe = requests.get(GITHUB_EXE_URL, stream=True)
            with open("NMT.exe", "wb") as f:
                for chunk in r_exe.iter_content(chunk_size=8192): f.write(chunk)
            with open("version.uvt", "w") as f: f.write(remote_v)
            with open("nmt-lk.thnk", "w") as f: f.write("UNLOCKED")
    except: pass
    if os.path.exists("NMT.exe"): subprocess.Popen(["NMT.exe"])

if __name__ == "__main__":
    time.sleep(2)
    run_update()
