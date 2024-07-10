import random
from tkinter import *
import ctypes
from words import movies, lorem, wiki
import ttkbootstrap as ttk


# It makes the bare window look a lot better than the original tkinter one and the text looks less pixelated
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Create window, made it automatically full-screen
window = ttk.Window()
window.state("zoomed")
window.title("Typing Speed Test")


# Gets called when the button_restart from the results_page is clicked, clears the screen and starts the test again
def restart():
    label_time_passed.place_forget()
    frame_close_reset.place_forget()
    label_typing_speed.place_forget()
    bi_label_left.place_forget()
    bi_label_right.place_forget()
    label_average_wpm.place_forget()
    label_user_wpm.place_forget()
    frame_close_reset.place_forget()
    label_percentage.place_forget()
    drop.pack(anchor=E, pady=117, padx=25)

    start()


# styles all buttons that are made with ttkbootstrap
global my_style2
my_style2 = ttk.Style()
my_style2.configure('secondary.TButton', font=("Akzidenz Grotesk", 30), background='#FFD4D4', foreground='white',
                    borderwidth=0, focusthickness=3, focuscolor='none', bordercolor="#FFD4D4")

# created widgets that are tied to both pages, so it's easier to work with them
global label_typing_speed
label_typing_speed = ttk.Label(window, text="Typing Speed Test", font="Times 50 bold")

global frame_close_reset
frame_close_reset = ttk.Frame(window)

global button_close
button_close = ttk.Button(frame_close_reset, text="Close", style="secondary.TButton", command=window.destroy)
global button_restart
button_restart = ttk.Button(frame_close_reset, text="Restart", style="secondary.TButton", command=restart)

# Default text, in case the user doesn't choose an option from the OptionMenu, movies comes from words.py
global text
text = random.choice(movies).lower()


def main_screen():
    # --- GLOBAL ---
    global time_passed
    global label_time_passed
    global split
    global bi_label_right
    global bi_label_left
    global working

    # --- VARIABLES ---
    time_passed = 0
    split = 0
    working = True

    # --- CREATE ---

    label_time_passed = ttk.Label(window, text=f"Time: {time_passed}s", font=("Akzidenz Grotesk", 30, "bold"))
    bi_label_left = ttk.Label(window, text=text[0:split], font=("Akzidenz Grotesk", 35, "bold"), bootstyle="success")
    bi_label_right = ttk.Label(window, text=text[split:], font=("Akzidenz Grotesk", 35, "bold"), bootstyle="secondary")

    # --- PACK/PLACE - FORGET ---
    label_typing_speed.place(rely=0.1, relx=0.5, anchor=CENTER)
    label_time_passed.place(rely=0.3, relx=0.5, anchor=CENTER)
    frame_close_reset.place(rely=0.9, relx=0.5, anchor=CENTER)
    button_close.pack(side=LEFT, padx=4)
    bi_label_left.place(relx=0.5, rely=0.5, anchor=E)
    bi_label_right.place(relx=0.5, rely=0.5, anchor=W)

    button_start.place_forget()
    label_percentage.place_forget()
    drop.pack_forget()
    label_time_passed2.place_forget()

    # --- FUNCTION CALLING ---
    window.bind("<Key>", key_press)
    window.after(1000, addSecond)
    window.after(60000, stopTest)


def addSecond():
    global time_passed
    # It adds 1 to time_passed and configures the label to show the new value of it every 1 second,
    # only if the test is still going
    time_passed += 1
    label_time_passed.configure(text=f'Time: {time_passed}s')
    if working:
        window.after(1000, addSecond)


def stopTest():
    # after 60 seconds this function gets called.
    # --- GLOBAL ---
    global working
    global wpm

    # --- VARIABLES ---
    # working = False, so time_passed won't gain anything over 60
    working = False
    # calculates the user's words per minute by splitting each word when it meets a space and checking the len()
    wpm = int(len(bi_label_left.cget('text').split(" ")) - 1)

    # --- PACK/PLACE - FORGET ---
    # makes the widgets that are irrelevant for the result disappear and call the result page
    label_time_passed.place_forget()
    button_restart.pack(side=LEFT)
    bi_label_left.place_forget()
    bi_label_right.place_forget()

    # --- FUNCTION CALLING ---
    results_page()


def results_page():
    global label_average_wpm
    label_average_wpm = ttk.Label(window, text="Average typing speed: 41.4 words per minute", font=("Akzidenz Grotesk", 20, "bold"))
    label_average_wpm.place(relx=0.5, rely=0.3, anchor=CENTER)

    global label_user_wpm
    label_user_wpm = ttk.Label(window, text=f"Your typing speed: {wpm} wpm", font=("Akzidenz Grotesk", 40, "bold"))
    label_user_wpm.place(relx=0.5, rely=0.4, anchor=CENTER)
    frame_close_reset.place(relx=0.5, rely=0.7, anchor=CENTER)

    global perc
    perc = round((wpm / 41.4) * 100)
    global label_percentage
    label_percentage = ttk.Label(window, text=f"That's {perc}% of the average", font=("Akzidenz Grotesk", 20, "bold"))
    label_percentage.place(relx=0.5, rely=0.5, anchor=CENTER)


def start():
    # --- GLOBAL ---
    global button_start
    global label_time_passed2
    global label_percentage

    # --- PACK/PLACE - FORGET ---
    # start button triggers main_screen, the timer starts and the text appears
    button_start = ttk.Button(window, text="Start", style="secondary.TButton", command=main_screen)
    # Instructions that disappear after the start button is pressed
    label_percentage = ttk.Label(window, text="The timer will start, and the text will appear after you press Start", font=("Akzidenz Grotesk", 20, "bold"))
    # Showcases the Time label before the test starts, so the user knows where it's placed
    label_time_passed2 = ttk.Label(window, text=f"Time: 0s", font=("Akzidenz Grotesk", 30, "bold"))

    button_start.place(relx=0.5, rely=0.5, anchor=CENTER)
    label_percentage.place(relx=0.5, rely=0.4, anchor=CENTER)
    label_time_passed2.place(rely=0.3, relx=0.5, anchor=CENTER)
    label_typing_speed.place(rely=0.1, relx=0.5, anchor=CENTER)
    frame_close_reset.place(rely=0.9, relx=0.5, anchor=CENTER)
    button_close.pack(side=LEFT, padx=4)
    button_restart.pack_forget()


# OptionMenu configurations
def selected(event):
    global text
    if clicked.get() == "Movies":
        text = random.choice(movies).lower()
    elif clicked.get() == "Ipsums":
        text = random.choice(lorem).lower()
    elif clicked.get() == "Wikipedia articles":
        text = random.choice(wiki).lower()


options = [
    "Mode",
    "Movies",
    "Ipsums",
    "Wikipedia articles",
]

clicked = StringVar()

drop = ttk.OptionMenu(window, clicked, *options, style="secondary.TButton", command=selected)
drop.pack(anchor=E, pady=117, padx=25)


# Detects every key press, if the pressed key is the same as the required one, it removes it prom the right
# label and adds it to the left one
def key_press(event=None):
    try:
        if event.char.lower() == bi_label_right.cget('text')[0].lower():
            bi_label_right.configure(text=bi_label_right.cget('text')[1:])
            bi_label_left.configure(text=bi_label_left.cget('text') + event.char)

    except TclError:
        pass


# the start is called here instead of main_screen, so the test only starts after the start button is pressed.
start()


window.mainloop()
