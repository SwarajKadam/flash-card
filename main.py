import tkinter
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

#------------------------------ Create new flash cards -----------------------#

try:
    csv_file = pd.read_csv("data/words_to_learn.csv")
    
except FileNotFoundError:    
    csv_file =pd.read_csv("data/german_words.csv")
    list_csv =csv_file.to_dict(orient="records")
    
else:
    list_csv =csv_file.to_dict(orient="records")
    
known_words_list = []

def get_card():
    canvas.itemconfig(image_on_canvas,image=card_front_img)
    global word_dict,flip_timer
    window.after_cancel(flip_timer)
    word_dict=list_csv[random.randint(0,999)]
    word = word_dict.get("German")
    canvas.itemconfig(title_text,text="German",fill="black")
    canvas.itemconfig(word_text,text=word,fill="black")
    flip_timer=window.after(3000,translate)
    
def translate():
    canvas.itemconfig(image_on_canvas,image=card_back_img)
    word = word_dict.get("English")
    canvas.itemconfig(title_text,text="English",fill="white")
    canvas.itemconfig(word_text,text=word,fill="white")
    
def right():    
    known_words_list.append(word_dict)
    words_known = pd.DataFrame(known_words_list)
    words_known.to_csv("data/known_words.csv",index=False)
    list_csv.remove(word_dict)
    get_card()
    data = pd.DataFrame(list_csv)
    data.to_csv("data/words_to_learn.csv",index=False)
       
#------------------------------ UI Setup -------------------------------------#

window = tkinter.Tk()
window.title("Flashy")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)

canvas = tkinter.Canvas(width=800, height=526,bg= BACKGROUND_COLOR, highlightthickness=0)
card_front_img = tkinter.PhotoImage(file="./images/card_front.png")
card_back_img = tkinter.PhotoImage(file="./images/card_back.png")
image_on_canvas = canvas.create_image(400,263,image=card_front_img)
canvas.grid(column=0,row=0,columnspan=3,)

flip_timer = window.after(3000,translate)

title_text=canvas.create_text(400,150,text="",font=("Ariel",40,"italic"))
word_text=canvas.create_text(400,263,text="",font=("Ariel",60,"bold"))

correct_button_img = tkinter.PhotoImage(file="./images/right.png")
correct_button = tkinter.Button(image = correct_button_img,highlightthickness=0, command =right)
correct_button.grid(column=2,row=1)

wrong_button_img = tkinter.PhotoImage(file="./images/wrong.png")
wrong_button = tkinter.Button(image = wrong_button_img,highlightthickness=0, command =get_card)
wrong_button.grid(column=0,row=1)

get_card()

window.mainloop()