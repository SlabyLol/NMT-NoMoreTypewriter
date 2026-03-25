import customtkinter as ctk
import pyautogui, threading, time, os, random, json, subprocess, sys
from flask import Flask, request
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app_bridge = Flask(__name__)
received_text = ""

@app_bridge.route('/inject', methods=['POST'])
def inject():
    global received_text
    data = request.get_json()
    received_text = data.get('text', '')
    return {"status": "success"}

class NMTApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NMT - TERMINATION HUB")
        self.geometry("600x850")
        self.running = False
        ctk.CTkLabel(self, text="NMT", font=("Impact", 60), text_color="#00ffcc").pack(pady=10)
        self.tabs = ctk.CTkTabview(self, width=550, height=550)
        self.tabs.pack(pady=10)
        self.tabs.add("Injector")
        self.tabs.add("Terminal")
        self.tabs.add("System")
        
        self.js = """(function(){const t=document.querySelector('.text-to-type')?.innerText||document.body.innerText;fetch('http://localhost:5000/inject',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t})}).then(()=>console.log('NMT Bridge Active'));})();"""
        self.txt = ctk.CTkTextbox(self.tabs.tab("Injector"), height=300, width=450)
        self.txt.insert("0.0", self.js)
        self.txt.pack(pady=10)
        ctk.CTkButton(self.tabs.tab("Injector"), text="COPY INJECT CODE", command=self.cp, fg_color="#ff003c").pack(pady=10)
        
        self.st = ctk.CTkLabel(self.tabs.tab("Terminal"), text="STATUS: WAITING", text_color="#ffcc00", font=("Arial", 14, "bold"))
        self.st.pack(pady=20)
        self.sp = ctk.CTkSlider(self.tabs.tab("Terminal"), from_=0.01, to=0.5)
        self.sp.set(0.08)
        self.sp.pack(pady=10)
        self.er = ctk.CTkSlider(self.tabs.tab("Terminal"), from_=0, to=15)
        self.er.set(3)
        self.er.pack(pady=10)
        ctk.CTkButton(self.tabs.tab("Terminal"), text="EXECUTE", command=self.start, fg_color="#28a745", height=50).pack(pady=20)
        
        ctk.CTkButton(self.tabs.tab("System"), text="RUN SELF-UPDATER", command=self.upd, fg_color="#555").pack(pady=50)
        
        threading.Thread(target=lambda: app_bridge.run(port=5000), daemon=True).start()

    def cp(self):
        import pyperclip
        pyperclip.copy(self.js)

    def upd(self):
        if os.path.exists("nmt-u-c.exe"):
            subprocess.Popen(["nmt-u-c.exe"])
            self.destroy()
            sys.exit()

    def start(self):
        if not self.running and received_text:
            self.running = True
            threading.Thread(target=self.run_engine, daemon=True).start()

    def run_engine(self):
        global received_text
        self.st.configure(text="STATUS: TERMINATING", text_color="#00ffcc")
        time.sleep(2)
        for c in list(received_text):
            if not self.running: break
            if random.random() < (self.er.get() / 100):
                pyautogui.write(random.choice("abcdefghijklmnopqrstuvwxyz"))
                time.sleep(self.sp.get())
                pyautogui.press("backspace")
            pyautogui.write(c)
            time.sleep(self.sp.get())
        self.running = False
        self.st.configure(text="STATUS: DONE", text_color="#00ffcc")

if __name__ == "__main__":
    app = NMTApp()
    app.mainloop()
