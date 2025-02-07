import random as rnd
import tkinter as tk

# --------------------------------------------------
# R O O T   F R A M E
# --------------------------------------------------
root = tk.Tk()
root.title("Zahlenratespiel")
root.geometry("320x240")
#root.minsize(320, 240)
#root.maxsize(320, 240)
root.resizable(False, False)
#root.state("zoomed")
#root.wm_attributes("-fullscreen", True)
root.configure(bg="gray0")

# --------------------------------------------------
# V A R I A B L E S
# --------------------------------------------------
rng = rnd.randrange(1, 100)
print(f"Zufallsgenerator erzeugt die Zahl {rng}")

message = tk.StringVar()
message.set("Drücke im Anschluss auf den OK Button")

# --------------------------------------------------
# F U N C T I O N S
# --------------------------------------------------
def update_message(this):
    message.set(this)

def check_number():
    input = int(main_entry.get())
    print(f"Eingegebene Zahl wurde ausgelesen: {input}")
    if input < 1 or input > 100:
    #if not (1 <= input <= 100):
        update_message("Bitte gib eine Zahl zwischen 1 und 100 ein")
    elif input < rng:
        update_message("Die gesuchte Zahl ist größer")
    elif input > rng:
        update_message("Die gesuchte Zahl ist kleiner")
    elif input == rng:
        update_message("Du hast die gesuchte Zahl erraten")  
    else:
        update_message("Gib eine gültige Zahl ein")  

# --------------------------------------------------
# H E A D E R   F R A M E
# --------------------------------------------------
header_frame = tk.Frame(root, bg="gray10")
header_frame.pack(side="top", fill="x")

header_label = tk.Label(header_frame, text="Zahlenratespiel", bg="gray10", fg="white")
header_label.pack(pady=5)

# --------------------------------------------------
# F O O T E R   F R A M E
# --------------------------------------------------
footer_frame = tk.Frame(root, bg="gray10")
footer_frame.pack(side="bottom", fill="x")

footer_label = tk.Label(footer_frame, text="©2025 Schmacht Games", bg="gray10", fg="white")
footer_label.pack(padx=5)

# --------------------------------------------------
# M A I N   F R A M E
# --------------------------------------------------
main_frame =tk.Frame(root, bg="gray5")
main_frame.pack(fill="both", padx=5, pady=5)

main_label = tk.Label(main_frame, bg="gray5", fg="white", text="Gib eine Zahl ein")
main_label.pack()

main_entry = tk.Entry(main_frame)
main_entry.pack()

main_label = tk.Label(main_frame, bg="gray5", fg="white", textvariable=message)
main_label.pack()

main_button = tk.Button(main_frame, text="OK" ,command=check_number)
main_button.pack()

root.mainloop()

# --------------------------------------------------
# P R O G R A M M A B L A U F
# --------------------------------------------------
root.mainloop()