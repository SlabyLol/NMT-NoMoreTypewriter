import customtkinter as ctk
import pyautogui, threading, time, os, random, subprocess, sys
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
        self.configure(fg_color="#050505")
        self.running = False
        
        ctk.CTkLabel(self, text="NMT", font=("Impact", 80), text_color="#00ffcc").pack(pady=20)
        
        self.tabs = ctk.CTkTabview(self, width=550, height=580, fg_color="#0a0a0a", segmented_button_selected_color="#00ffcc", segmented_button_selected_hover_color="#00e6b8", segmented_button_unselected_color="#1a1a1a")
        self.tabs.pack(pady=10, padx=20)
        
        self.tabs.add("INJECTOR")
        self.tabs.add("TERMINAL")
        self.tabs.add("SYSTEM")
        
        self.js = """(function(){const t=document.querySelector('.text-to-type')?.innerText||document.body.innerText;fetch('http://localhost:5000/inject',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t})}).then(()=>console.log('NMT Bridge Active'));})();"""
        
        self.txt = ctk.CTkTextbox(self.tabs.tab("INJECTOR"), height=350, width=480, fg_color="#000", text_color="#00ffcc", font=("Consolas", 12), border_width=1, border_color="#1a1a1a")
        self.txt.insert("0.0", self.js)
        self.txt.pack(pady=15)
        
        ctk.CTkButton(self.tabs.tab("INJECTOR"), text="COPY BRIDGE CODE", command=self.cp, fg_color="#ff003c", hover_color="#cc0030", font=("Arial", 14, "bold"), height=40).pack(pady=10)
        
        self.st = ctk.CTkLabel(self.tabs.tab("TERMINAL"), text="STATUS: WAITING FOR DATA", text_color="#ffcc00", font=("Arial", 18, "bold"))
        self.st.pack(pady=30)
        
        ctk.CTkLabel(self.tabs.tab("TERMINAL"), text="TYPING SPEED (DELAY)", font=("Arial", 12)).pack()
        self.sp = ctk.CTkSlider(self.tabs.tab("TERMINAL"), from_=0.01, to=0.5, button_color="#00ffcc")
        self.sp.set(0.08)
        self.sp.pack(pady=15, padx=30, fill="x")
        
        ctk.CTkLabel(self.tabs.tab("TERMINAL"), text="HUMAN ERROR RATE (%)", font=("Arial", 12)).pack()
        self.er = ctk.CTkSlider(self.tabs.tab("TERMINAL"), from_=0, to=20, button_color="#ff003c")
        self.er.set(3)
        self.er.pack(pady=15, padx=30, fill="x")
        
        self.btn_run = ctk.CTkButton(self.tabs.tab("TERMINAL"), text="EXECUTE TERMINATION", command=self.start, fg_color="#28a745", hover_color="#218838", font=("Arial", 16, "bold"), height=60)
        self.btn_run.pack(pady=40, padx=50, fill="x")
        
        ctk.CTkButton(self.tabs.tab("SYSTEM"), text="FORCE SELF-UPDATE", command=self.upd, fg_color="#333", hover_color="#444").pack(pady=50, padx=50, fill="x")
        
        threading.Thread(target=lambda: app_bridge.run(port=5000), daemon=True).start()

    def cp(self):
        import pyperclip
        pyperclip.copy(self.js)
        self.txt.configure(border_color="#00ffcc")

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
        self.st.configure(text="STATUS: INJECTING...", text_color="#00ffcc")
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
        self.st.configure(text="STATUS: COMPLETE", text_color="#00ffcc")

if __name__ == "__main__":
    app = NMTApp()
    app.mainloop()
