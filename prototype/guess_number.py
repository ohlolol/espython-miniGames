import random as rnd
import tkinter as tk

class Game:
    # --------------------------------------------------
    # B A S I C   E X E C U T I O N   C O N D I T I O N S
    # --------------------------------------------------
    def __init__(self, root):
        root.title("Zahlenratespiel")
        root.geometry("320x240")
        root.resizable(False, False)
        root.configure(bg="gray0")
        #root.wm_attributes("-fullscreen", True)

        self.rng = rnd.randrange(1, 100)
        print(f"Zufallsgenerator erzeugt die Zahl {self.rng}")

        self.message = tk.StringVar()
        self.message.set("Drücke im Anschluss auf den OK Button")

        self.setup_ui()

    # --------------------------------------------------
    # G R A P H I C A L   U S E R   I N T E R F A C E
    # --------------------------------------------------
    def setup_ui(self):
        # H E A D E R   F R A M E
        header_frame = tk.Frame(root, bg="gray10")
        header_frame.pack(side="top", fill="x")

        header_label = tk.Label(header_frame, text="Zahlenratespiel", bg="gray10", fg="white")
        header_label.pack(pady=5)

        # M A I N   F R A M E
        main_frame =tk.Frame(root, bg="gray5")
        main_frame.pack(fill="both", padx=5, pady=5)

        main_label = tk.Label(main_frame, bg="gray5", fg="white", text="Gib eine Zahl ein")
        main_label.pack()

        self.main_entry = tk.Entry(main_frame)
        self.main_entry.pack()

        main_label = tk.Label(main_frame, bg="gray5", fg="white", textvariable=self.message)
        main_label.pack()

        main_button = tk.Button(main_frame, text="OK" ,command=self.check_number)
        main_button.pack()

        # F O O T E R   F R A M E
        footer_frame = tk.Frame(root, bg="gray10")
        footer_frame.pack(side="bottom", fill="x")

        footer_label = tk.Label(footer_frame, text="©2025 Schmacht Games", bg="gray10", fg="white")
        footer_label.pack(padx=5)

    # --------------------------------------------------
    # G A M E P L A Y   M E C H A N I C S
    # --------------------------------------------------
    def check_number(self):
        input = int(self.main_entry.get())
        print(f"Eingegebene Zahl wurde ausgelesen: {input}")
        if input < 1 or input > 100:
        #if not (1 <= input <= 100):
            self.update_message("Bitte gib eine Zahl zwischen 1 und 100 ein")
        elif input < self.rng:
            self.update_message("Die gesuchte Zahl ist größer")
        elif input > self.rng:
            self.update_message("Die gesuchte Zahl ist kleiner")
        elif input == self.rng:
            self.update_message("Du hast die gesuchte Zahl erraten")  
        else:
            self.update_message("Gib eine gültige Zahl ein")  

    def update_message(self, text):
        self.message.set(text)
        
# --------------------------------------------------
# P R O C E S S   L O G I C
# --------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = Game(root)
    root.mainloop()