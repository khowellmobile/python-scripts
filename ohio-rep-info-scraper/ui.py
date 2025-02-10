import tkinter as tk

import queue
import threading
import time

from ohioHouseScraper import run_scraper

print_queue = queue.Queue()
scraper_is_running = False


def update_text_box():
    while True:
        try:
            # Try to get text from the queue
            text = print_queue.get_nowait()
            text_box.insert(tk.END, text)
            text_box.yview(tk.END)

            if text == "Finished Processing":
                break
        except queue.Empty:
            pass

        time.sleep(0.1)


def run_scraper_click():
    threading.Thread(target=run_scraper, args=(add_to_ui_queue,), daemon=True).start()
    threading.Thread(target=update_text_box, daemon=True).start()


def add_to_ui_queue(text):
    print_queue.put(text + "\n")
    print(text)


window_width = 800
window_height = 400
window_padding = 10

run_button_width = 100
run_button_height = 35
""" save_button_width = 100
save_button_height = 35 """

text_box_width = window_width - window_padding * 2 - 15
text_box_height = window_height - window_padding * 2 - run_button_height - 4
scroll_place_x = text_box_width

root = tk.Tk()
root.geometry("800x400")
root.title("Ohio Representative Scraper v0.8")
root.config(bg="white", padx=10, pady=10)

text_box = tk.Text(
    root,
    wrap="word",
    width=40,
    height=10,
    font=("Arial", 10),
    bg="#f0f0f0",
    fg="black",
    relief="solid",
    padx=5,
    pady=5,
)

scrollbar = tk.Scrollbar(root, command=text_box.yview, relief="flat")
text_box.config(yscrollcommand=scrollbar.set)

text_box.place(x=0, y=41, width=text_box_width, height=text_box_height)
scrollbar.place(x=scroll_place_x, y=41, width=15, height=text_box_height)

run_button = tk.Button(
    root,
    text="Run Scraper",
    font=("Arial", 10, "bold"),
    fg="white",
    bg="#c73852",
    padx=10,
    pady=5,
    relief="solid",
    command=run_scraper_click,
)
run_button.place(x=0, y=0, width=run_button_width, height=run_button_height)

save_button = tk.Button(
    root,
    text="Save Output",
    font=("Arial", 10, "bold"),
    fg="white",
    bg="#c73852",
    padx=10,
    pady=5,
    relief="solid",
    command=run_scraper_click,
)
save_button.place(
    x=run_button_width + 5, y=0, width=run_button_width, height=run_button_height
)

# Start the UI loop
root.mainloop()
