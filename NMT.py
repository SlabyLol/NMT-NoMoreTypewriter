import customtkinter as ctk
import pyautogui
import pytesseract
from PIL import ImageGrab
import threading
import time
import random
import pygetwindow as gw
import tkinter.messagebox as messagebox
import os
import subprocess

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NMTApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NMT - NoMoreTypewriter [FULL VERSION]")
        self.geometry("500x800")

        self.label = ctk.CTkLabel(self, text="NMT", font=("Orbitron", 40, "bold"), text_color="#00ffcc")
        self.label.pack(pady=(20, 0))
        
        self.status_tag = ctk.CTkLabel(self, text="STATUS: UNLOCKED", font=("Arial", 10, "bold"), text_color="#ffcc00")
        self.status_tag.pack(pady=(0, 20))

        self.win_label = ctk.CTkLabel(self, text="TARGET WINDOW:", font=("Arial", 12, "bold"))
        self.win_label.pack()
        self.windows = [w.title for w in gw.getAllWindows() if w.title != ""]
        self.window_selector = ctk.CTkOptionMenu(self, values=self.windows, fg_color="#1a1a1a", button_color="#00ffcc", button_hover_color="#00ccaa")
        self.window_selector.pack(pady=10)

        self.speed_label = ctk.CTkLabel(self, text="TYPING DELAY:", font=("Arial", 12, "bold"))
        self.speed_label.pack()
        self.speed_slider = ctk.CTkSlider(self, from_=0.0, to=0.3, progress_color="#00ffcc")
        self.speed_slider.set(0.05)
        self.speed_slider.pack(pady=10)

        self.error_frame = ctk.CTkFrame(self, fg_color="#111", border_width=1, border_color="#333")
        self.error_frame.pack(pady=20, padx=30, fill="x")
        
        self.error_check = ctk.CTkCheckBox(self.error_frame, text="HUMAN ERROR STEALTH", text_color="#00ffcc", command=self.toggle_error)
        self.error_check.pack(pady=10)
        self.error_entry = ctk.CTkEntry(self.error_frame, placeholder_text="Max errors", state="disabled", fg_color="#000")
        self.error_entry.pack(pady=10)

        self.start_btn = ctk.CTkButton(self, text="DESTROY TYPEWRITER", command=self.start_thread, fg_color="#28a745", hover_color="#218838", font=("Arial", 16, "bold"), height=50)
        self.start_btn.pack(pady=10, padx=50, fill="x")

        self.stop_btn = ctk.CTkButton(self, text="EMERGENCY STOP", command=self.stop_bot, fg_color="#dc3545", hover_color="#c82333")
        self.stop_btn.pack(pady=5)

        self.update_btn = ctk.CTkButton(self, text="CHECK FOR UPDATES", command=self.run_updater, fg_color="#555", font=("Arial", 12, "bold"))
        self.update_btn.pack(pady=10)

        self.feedback_btn = ctk.CTkButton(self, text="⭐ RATE & SUGGEST FEATURES", command=self.show_feedback, fg_color="#333", text_color="#fff")
        self.feedback_btn.pack(pady=10)

        self.footer = ctk.CTkLabel(self, text="©DARKFOX CO. 2026", font=("Arial", 10), text_color="gray")
        self.footer.pack(side="bottom", pady=10)

        self.running = False

    def run_updater(self):
        updater_exe = "nmt-u-c.exe"
        if os.path.exists(updater_exe):
            subprocess.Popen([updater_exe])
            self.destroy()
            exit()
        else:
            messagebox.showerror("Error", "Updater (nmt-u-c.exe) not found!")

    def show_feedback(self):
        messagebox.showinfo("Feedback & Suggestions", "Send your ratings and feature ideas to:\ndarkfox.tobias@outlook.com")

    def toggle_error(self):
        state = "normal" if self.error_check.get() else "disabled"
        self.error_entry.configure(state=state)

    def start_thread(self):
        if not self.running:
            threading.Thread(target=self.type_logic, daemon=True).start()

    def type_logic(self):
        self.running = True
        try:
            target = self.window_selector.get()
            win = gw.getWindowsWithTitle(target)[0]
            win.activate()
            time.sleep(2)
            screenshot = ImageGrab.grab(bbox=(win.left, win.top, win.right, win.bottom))
            text = pytesseract.image_to_string(screenshot).replace('\n', ' ').strip()
            total = len(text)
            delay = self.speed_slider.get()
            max_err = int(self.error_entry.get()) if self.error_check.get() and self.error_entry.get() else 0
            err_pos = random.sample(range(total), min(max_err, total))
            for i, char in enumerate(text):
                if not self.running: break
                if i in err_pos:
                    pyautogui.write(random.choice("asdfghjkl"))
                    time.sleep(delay + 0.1)
                    pyautogui.press('backspace')
                    time.sleep(delay)
                pyautogui.write(char)
                time.sleep(delay * random.uniform(0.8, 1.2))
        except: pass
        self.running = False

    def stop_bot(self):
        self.running = False

if __name__ == "__main__":
    app = NMTApp()
    app.mainloop()
