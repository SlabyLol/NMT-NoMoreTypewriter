import customtkinter as ctk
import pyautogui
import pytesseract
from PIL import ImageGrab
import threading
import time
import random
import pygetwindow as gw
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

KLO46 = "https://github.com/SlabyLol/NMT-NoMoreTypewriter/blob/main/update-log/KLO046/l-key.nmtk"
KEY_FILE = "nmt-lk.thnk"

class NMTApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        if not self.verify_access():
            self.destroy()
            return

        self.title("NMT - NoMoreTypewriter")
        self.geometry("550x700")

        self.label = ctk.CTkLabel(self, text="NoMoreTypewriter", font=("Orbitron", 30, "bold"), text_color="#00ffcc")
        self.label.pack(pady=(20, 5))

        self.win_label = ctk.CTkLabel(self, text="Select Target Window:", font=("Arial", 13, "bold"))
        self.win_label.pack(pady=(10, 0))
        self.windows = [w.title for w in gw.getAllWindows() if w.title != ""]
        self.window_selector = ctk.CTkOptionMenu(self, values=self.windows)
        self.window_selector.pack(pady=10)

        self.speed_label = ctk.CTkLabel(self, text="Typing Delay (Seconds):", font=("Arial", 13, "bold"))
        self.speed_label.pack()
        self.speed_slider = ctk.CTkSlider(self, from_=0.0, to=0.3)
        self.speed_slider.set(0.05)
        self.speed_slider.pack(pady=10)

        self.error_frame = ctk.CTkFrame(self)
        self.error_frame.pack(pady=15, padx=20, fill="x")
        self.error_check = ctk.CTkCheckBox(self.error_frame, text="Enable Human Errors (Stealth Mode)", command=self.toggle_error)
        self.error_check.pack(pady=10)
        self.error_entry = ctk.CTkEntry(self.error_frame, placeholder_text="Max errors", state="disabled")
        self.error_entry.pack(pady=5)

        self.counter_label = ctk.CTkLabel(self, text="Status: Ready", font=("Arial", 16, "bold"), text_color="#ffcc00")
        self.counter_label.pack(pady=15)

        self.start_btn = ctk.CTkButton(self, text="START NMT", command=self.start_thread, fg_color="#28a745", height=45)
        self.start_btn.pack(pady=5)
        self.stop_btn = ctk.CTkButton(self, text="EMERGENCY STOP", command=self.stop_bot, fg_color="#dc3545")
        self.stop_btn.pack(pady=5)

        self.footer = ctk.CTkLabel(self, text="©DarkFox Co. 2026 | Ultimate Stealth Edition", font=("Arial", 10), text_color="gray")
        self.footer.pack(side="bottom", pady=15)

        self.running = False

    def verify_access(self):
        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "r") as f:
                if f.read().strip() == "KLO046":
                    return True

        dialog = ctk.CTkInputDialog(text=f"Enter License Key found at GitHub:\n{KLO46}", title="Security Check")
        pw = dialog.get_input()
        
        if pw == "KLO046":
            with open(KEY_FILE, "w") as f:
                f.write("KLO046")
            return True
        return False

    def toggle_error(self):
        state = "normal" if self.error_check.get() else "disabled"
        self.error_entry.configure(state=state)

    def start_thread(self):
        if not self.running:
            threading.Thread(target=self.type_logic, daemon=True).start()

    def type_logic(self):
        self.running = True
        try:
            target_title = self.window_selector.get()
            win_list = gw.getWindowsWithTitle(target_title)
            if not win_list: return
            win = win_list[0]
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
                self.counter_label.configure(text=f"Keys left: {total - i}")

                if i in err_pos:
                    pyautogui.write(random.choice("asdfghjkl"))
                    time.sleep(delay + 0.1)
                    pyautogui.press('backspace')
                    time.sleep(delay)

                pyautogui.write(char)
                time.sleep(delay * random.uniform(0.8, 1.2))

            self.counter_label.configure(text="Finished!")
        except Exception:
            self.counter_label.configure(text="Error occurred.")
        self.running = False

    def stop_bot(self):
        self.running = False

if __name__ == "__main__":
    app = NMTApp()
    app.mainloop()
