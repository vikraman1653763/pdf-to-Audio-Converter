import PyPDF2
import pygame
import pyttsx3
import threading
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

paused = False  # Define paused globally

def convertAndPlay():
    text = text_box.get(0.0, tk.END)
    if len(text) <= 1:
        messagebox.showwarning('WARNING', 'FIRST ENTER SOME TEXT TO CONVERT INTO AUDIO')
        return
    
    voices = bot.getProperty('voices')
    bot.setProperty('voice', voices[voice_var.get()].id)
    bot.setProperty('rate', speed_scale.get())
    
    answer = messagebox.askyesno("WARNING", "YOU CANNOT PAUSE ONCE YOU STARTED THIS PROCESS. \nDO YOU WISH TO CONTINUE?")
    if answer == False:
        return
    
    bot.say(text)
    bot.runAndWait()

def saveAudio():
    text = text_box.get(0.0, tk.END).strip()
    if len(text) <= 1:
        messagebox.showwarning("WARNING", "FIRST ENTER SOME TEXT TO CONVERT INTO AUDIO")
        return
    
    filename = filedialog.asksaveasfilename(defaultextension=".wav")
    if filename:
        bot = pyttsx3.init()
        voices = bot.getProperty('voices')
        bot.setProperty('voice', voices[voice_var.get()].id)
        bot.setProperty('rate', speed_scale.get())
        bot.save_to_file(text, filename)
        bot.runAndWait()
        messagebox.showinfo('SUCCESSFUL', 'AUDIO IS SAVED')
        global song
        song = filename

def file():
    path = filedialog.askopenfilename()
    book = open(path, 'rb')
    pdfreader = PyPDF2.PdfReader(book)
    pages = len(pdfreader.pages)
    for i in range(int(startingpagenumber.get()), pages):
        page = pdfreader.pages[i - 1]
        txt = page.extract_text()
        text_box.insert(END, txt)

def play():
    text1 = text_box.get(0.0, tk.END)
    if song is None:
        messagebox.showwarning("WARNING", "FIRST SAVE THE TEXT AS AUDIO")
        return
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    global stopped
    stopped = False

def stop():
    pygame.mixer.music.stop()
    global stopped
    stopped = True

def pause(is_paused):
    global paused
    if song is None:
        return
    
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
        P.config(text="⏸ pause")
    else:
        pygame.mixer.music.pause()
        paused = True
        P.config(text="⏸ unpause")

def clear():
    text_box.delete(0.0, tk.END)
    global song
    song = None
    startingpagenumber.delete(0, END)

root = tk.Tk()
root.title("PDF FILE TEXT TO AUDIO SPEECH CONVERTER")
root.geometry("950x505+190+90")
root.configure(bg='#2D142C')
root.resizable(0, 0)

pygame.mixer.init()
bot = pyttsx3.init()
voice_var = tk.IntVar()

Label(root, text="TEXT AREA", bg='#2D142C', fg="#FFF", wraplength=1).place(x=5, y=170)
top = Label(root, text="PDF FILE TEXT TO AUDIO SPEECH CONVERTER", bg='#510A32', fg="#FFF", font=("sitka small", 8))
top.grid(padx=363, pady=0, sticky=N)
Label(root, text="CONTROLS", bg='#2D142C', fg="#FFF", wraplength=1).place(anchor=W, x=930, y=235)

text_box = ScrolledText(root, font=("sitka small", 11), bd=2, relief=tk.FLAT, wrap=tk.WORD, undo=True, bg='#ffffff', fg="#000000")
text_box.place(x=25, y=25, height=450, width=500)

frame = tk.Frame(root, bd=2, relief=tk.FLAT, bg='#510A32')
frame.place(x=545, y=25, height=450, width=380)

frame2 = tk.LabelFrame(frame, text='change speed', bg='#801336', relief=tk.FLAT)
frame2.grid(row=3, column=0, pady=5, padx=4)
speed_scale = tk.Scale(frame2, from_=100, to=300, orient=tk.HORIZONTAL, length=334, bg='#CC2A49', troughcolor='#CC2A49', highlightthickness=0)
speed_scale.set(200)
speed_scale.grid(row=2, columnspan=1, ipadx=5, ipady=5)

frame3 = tk.LabelFrame(frame, text='change voice', bg='#801336', relief=tk.FLAT)
frame3.grid(row=2, column=0, pady=5)
R1 = tk.Radiobutton(frame3, text='MALE', variable=voice_var, value=0, bg='#CC2A49')
R1.grid(row=0, column=0, ipadx=54, ipady=17)
R2 = tk.Radiobutton(frame3, text='FEMALE‍', variable=voice_var, value=1, bg='#CC2A49')
R2.grid(row=0, column=1, ipadx=54, ipady=17)

frame4 = tk.Frame(frame, bd=2, relief=tk.FLAT, width=25, bg='#801336')
frame4.grid(row=1, column=0, pady=10)
btn_1 = tk.Button(frame4, text='Direct Read', width=25, command=lambda: threading.Thread(target=convertAndPlay, daemon=True).start(), bg='#CC2A49', relief=tk.FLAT)
btn_1.grid(row=0, column=0, ipady=5, padx=4, pady=5)
btn_2 = tk.Button(frame4, text='Save as audio', width=25, command=saveAudio, bg='#CC2A49', relief=tk.FLAT)
btn_2.grid(row=1, column=0, ipady=5, padx=4, pady=5)
btn_3 = tk.Button(frame4, text='clear', width=19, command=clear, bg='#CC2A49', relief=tk.FLAT)
btn_3.grid(row=0, column=1, ipady=5, padx=4, pady=5)
btn_4 = tk.Button(frame4, text='Exit', width=19, command=root.destroy, bg='#CC2A49', relief=tk.FLAT)
btn_4.grid(row=1, column=1, ipady=5, padx=4, pady=5)

frame5 = tk.Frame(frame, bd=2, relief=tk.FLAT, bg='#801336')
frame5.grid(row=0, column=0, pady=10, padx=14)
page1 = Label(frame5, text=" Enter starting page number", bg="#CC2A49")
page1.grid(row=0, column=0, ipady=5, padx=4, pady=5)
startingpagenumber = Entry(frame5, bg="#CC2A49", relief=tk.FLAT)
startingpagenumber.grid(row=1, column=0, ipady=5, ipadx=15, padx=4, pady=5)
label = Label(frame5, text="Select the PDF you want to read.", bg="#CC2A49")
label.grid(row=0, column=1, ipady=5, padx=4, pady=5)
B = Button(frame5, text="Choose  the PDF", command=file, bg="#CC2A49", relief=tk.FLAT)
B.grid(row=1, column=1, ipady=1, padx=4, pady=5, ipadx=39)
S = Button(frame5, text="⏹ stop", command=stop, bg="#CC2A49", relief=tk.FLAT)
S.grid(row=2, column=0, ipady=5, sticky=W, padx=4, pady=5)
R = Button(frame5, text="▶ read ", command=play, bg="#CC2A49", relief=tk.FLAT)
R.grid(row=2, column=0, columnspan=2, ipady=5, padx=4, pady=5)
P = Button(frame5, text="⏸ pause", command=lambda: pause(paused), bg="#CC2A49", relief=tk.FLAT)
P.grid(row=2, column=1, ipady=5, padx=4, sticky=E, pady=5)

root.mainloop()
