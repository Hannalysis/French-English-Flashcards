from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image #to get the png to display
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    french_words_df = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    french_words_df = pandas.read_csv("french_words.csv")

french_words_dict = french_words_df.to_dict(orient = "records")

known_words = []

#------------------------------------------------------------------------------
#Functions#--------------------------------------------------------------------

def random_word():
    #rng French word
    global rng_dict
    rng_dict = random.choice(list(french_words_dict))
    rng_word = rng_dict["French"]
    global rng_translated
    rng_translated = rng_dict["English"] #Variable prepped for translation on screen
    canvas.itemconfig(nw_text, text = rng_word, fill = "black")
    canvas.itemconfig(locale_text, text = "French", fill = "black")
    canvas.itemconfig(card_display, image = card_front)
    window.after(3000, func = translated) #Interactable alternative to window.update and time.sleep


def translated():
    canvas.itemconfig(nw_text, text = rng_translated, fill = "white")
    canvas.itemconfig(locale_text, text = "English", fill = "white")
    canvas.itemconfig(card_display, image = card_back)


def wrong():
    random_word()

def right():
    random_word()
    known_words.append(rng_dict)
    french_words_dict.remove(rng_dict)
    unknown_words = [words for words in french_words_dict if words not in known_words]
    #List of Dict pairs to Dataframe to make csv ready
    unknown_words_csv = pandas.DataFrame(unknown_words)
    unknown_words_csv.to_csv("words_to_learn.csv", index = False)
    print(unknown_words_csv) #test
#------------------------------------------------------------------------------
#UI#---------------------------------------------------------------------------

window = Tk()
window.title("Flashy")
window.config(padx = 50, pady = 50, bg = BACKGROUND_COLOR)

#------------------------------------------------------------------------------
#Row 1

card_front = ImageTk.PhotoImage(Image.open("images\card_front.png"))
card_back = ImageTk.PhotoImage(Image.open("images\card_back.png"))
canvas = Canvas(width = 1000, height = 800, highlightthickness= 0, bg = BACKGROUND_COLOR)
card_display = canvas.create_image(500, 400, image = card_front)
locale_text = canvas.create_text(500, 250, text = "French", font = ("Light Calibri", 40, "italic"))
nw_text = canvas.create_text(500,400, text = "word", font = ("Arial", 60, "bold"))
canvas.grid(row = 0, column = 0, columnspan= 2)



#------------------------------------------------------------------------------
#Row 2

right_image = PhotoImage(file = R"images\right.png")
wrong_image = PhotoImage(file = "images\wrong.png")

wrong_button = Button (height = 95, width = 94, image = wrong_image, command = wrong, bg = BACKGROUND_COLOR)
wrong_button.grid (row = 1, column = 0)

correct_button = Button (height = 95, width = 94, image = right_image, command = right, bg = BACKGROUND_COLOR)
correct_button.grid(row = 1, column = 1)

#Calling func so rng_word is defined before canvas text is created
random_word()


window.mainloop()