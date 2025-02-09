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
        tk.Label(header_frame, text="Zahlenratespiel", bg="gray10", fg="white").pack(pady=5)

        # M A I N   F R A M E
        main_frame = tk.Frame(root, bg="gray5")
        main_frame.pack(fill="both", padx=5, pady=5)
        tk.Label(main_frame, bg="gray5", fg="white", text="Gib eine Zahl ein").pack()

        self.main_entry = tk.Entry(main_frame)
        self.main_entry.pack()

        tk.Label(main_frame, bg="gray5", fg="white", textvariable=self.message).pack()
        tk.Button(main_frame, text="OK" ,command=self.check_number).pack()

        # B U T T O N   F R A M E
        button_frame = tk.Frame(root, bg="gray5")
        button_frame.pack()

        # B U T T O N S
        n0 = tk.Button(button_frame, width=2, height=1, text="0", command=lambda: self.add_numbers(0)) 
        n1 = tk.Button(button_frame, width=2, height=1, text="1", command=lambda: self.add_numbers(1))
        n2 = tk.Button(button_frame, width=2, height=1, text="2", command=lambda: self.add_numbers(2))
        n3 = tk.Button(button_frame, width=2, height=1, text="3", command=lambda: self.add_numbers(3))
        n4 = tk.Button(button_frame, width=2, height=1, text="4", command=lambda: self.add_numbers(4))
        n5 = tk.Button(button_frame, width=2, height=1, text="5", command=lambda: self.add_numbers(5))
        n6 = tk.Button(button_frame, width=2, height=1, text="6", command=lambda: self.add_numbers(6))
        n7 = tk.Button(button_frame, width=2, height=1, text="7", command=lambda: self.add_numbers(7))
        n8 = tk.Button(button_frame, width=2, height=1, text="8", command=lambda: self.add_numbers(8))
        n9 = tk.Button(button_frame, width=2, height=1, text="9", command=lambda: self.add_numbers(9))

        # B U T T O N S   G R I D
        n0.grid(column=0, row=0)
        n1.grid(column=1, row=0)
        n2.grid(column=2, row=0)
        n3.grid(column=3, row=0)
        n4.grid(column=4, row=0)
        n5.grid(column=0, row=1)
        n6.grid(column=1, row=1)
        n7.grid(column=2, row=1)
        n8.grid(column=3, row=1)
        n9.grid(column=4, row=1)

        # F O O T E R   F R A M E
        footer_frame = tk.Frame(root, bg="gray10")
        footer_frame.pack(side="bottom", fill="x")
        tk.Label(footer_frame, text="©2025 Schmacht Games", bg="gray10", fg="white").pack(padx=5)

    # --------------------------------------------------
    # G A M E P L A Y   M E C H A N I C S
    # --------------------------------------------------
    def add_numbers(self, number):
        current = self.main_entry.get()
        self.main_entry.delete(0, tk.END)
        self.main_entry.insert(0, current + str(number))
        

    def check_number(self):
        try:
            input = int(self.main_entry.get())
            self.main_entry.delete(0, tk.END)
            print(f"Eingegebene Zahl wurde ausgelesen: {input}")
            if input < 1 or input > 100:
            #if not (1 <= input <= 100):
                self.update_message("Bitte gib eine Zahl zwischen 1 und 100 ein")
            elif input < self.rng:
                self.update_message(f"Die gesuchte Zahl ist größer als {input}")
            elif input > self.rng:
                self.update_message(f"Die gesuchte Zahl ist kleiner als {input}")
            else:
                self.update_message(f"Du hast die gesuchte Zahl erraten: {input}")  
        except ValueError:
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