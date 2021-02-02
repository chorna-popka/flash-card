from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FROM_LANGUAGE = "French"
TO_LANGUAGE = "English"
DELAY = 3

timer = None
current_pair = {}
# -------------------read csv------------------------------
try:
    df = pandas.read_csv("data/words_to_learn.csv")
    word_pairs = df.to_dict(orient="records")
except FileNotFoundError:
    try:
        df = pandas.read_csv("data/french_words.csv")
        word_pairs = df.to_dict(orient="records")
    except:
        print("Data file not found, shutting down...")
        exit(1)


def get_random_pair():
    global current_pair
    canvas.itemconfig(bg_img, image=img_card)
    current_pair = random.choice(word_pairs)
    canvas.itemconfig(lbl_title, text=FROM_LANGUAGE)
    canvas.itemconfig(lbl_word, text=current_pair[FROM_LANGUAGE])


# --------------flipping--------------------------
def flip():
    canvas.itemconfig(bg_img, image=img_back)
    canvas.itemconfig(lbl_title, text=TO_LANGUAGE)
    canvas.itemconfig(lbl_word, text=current_pair[TO_LANGUAGE])


def count_down():
    global timer
    timer = window.after(DELAY * 1000, flip)


def new_card():
    window.after_cancel(timer)
    get_random_pair()
    count_down()


def passed():
    new_card()
    word_pairs.remove(current_pair)
    to_csv = pandas.DataFrame(word_pairs)
    to_csv.to_csv("data/words_to_learn.csv", index=False)


def failed():
    new_card()

# -------------GUI--------------
window = Tk()
window.title("Flash cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
img_card = PhotoImage(file="images/card_front.png")
img_back = PhotoImage(file="images/card_back.png")
bg_img = canvas.create_image(400, 263, image=img_card)
lbl_title = canvas.create_text(400, 150, text="title", font=("Arial", 40, "italic"))
lbl_word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

img_fail = PhotoImage(file="images/wrong.png")
btn_fail = Button(image=img_fail, highlightthickness=0, command=failed)
btn_fail.grid(column=0, row=1)
img_pass = PhotoImage(file="images/right.png")
btn_pass = Button(image=img_pass, highlightthickness=0, command=passed)
btn_pass.grid(column=1, row=1)

get_random_pair()
count_down()


window.mainloop()
