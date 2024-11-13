from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import lexical_analyzer as lexer
root = Tk()

root.geometry("1400x800")
root.configure(bg="#A9A9A9")
root.resizable(False,False)
root.title("LOLCode")

title = Label(root, text="LOLCode Interpreter", font=('Arial', 20), anchor="w", bg="#A9A9A9", fg="#36454F")
title.place(x=710, y=5, height=30, width=300)

#code goes here
input_textbox = Text(root, font=('Arial bold', 12))
input_textbox.configure(bg="#E5E4E2", fg="#36454F", insertbackground="#00A7B5")
input_textbox.place(x=10, y=40, height=350, width=690)

#directory
dir_textbox = Text(root, font=('Arial'), bg="#A9A9A9", fg="#02066F", borderwidth=0, state="disabled")
dir_textbox.place(x=10, y=15, height=20, width=530)

#tokens
lexeme = scrolledtext.ScrolledText(root, font=('Consolas bold', 10))
lexeme.configure(bg="#E5E4E2", fg="#36454F", insertbackground="#00A7B5", state="disabled")
lexeme.place(x=710, y=80, height=310, width=335)

lexeme_label = Label(root, text="Lexemes", font=('Arial', 15), borderwidth=0, bg="#808080", fg="#36454F")
lexeme_label.place(x=710, y=40, height=40, width=335)

#symbol table
symbol_table = Text(root, font=('Arial'))
symbol_table.configure(bg="#E5E4E2", fg="#36454F", insertbackground="#00A7B5", state="disabled")
symbol_table.place(x=1055, y=80, height=310, width=335)

symbol_label = Label(root, text="Symbol Table", font=('Arial', 15), borderwidth=0, bg="#808080", fg="#36454F")
symbol_label.place(x=1055, y=40, height=40, width=335)

#button actions
file_path = ''
def openFile():
    global file_path
    path = filedialog.askopenfilename(filetypes=(("LOL Files", "*.lol"),))
    with open(path, 'r') as file:
        input = file.read()
        input_textbox.delete('1.0', END)
        input_textbox.insert('1.0', input)
        file_path = path
    print(file_path)
    dir_textbox.configure(state="normal")
    dir_textbox.delete('1.0', END)
    dir_textbox.insert('1.0', file_path)
    dir_textbox.configure(state="disabled")

def saveFile():
    global file_path
    if file_path == '':
        path = filedialog.asksaveasfilename(filetypes=(("LOL Files", "*.lol"),))
    else:
        path=file_path
    with open(path, 'w') as file:
        input = input_textbox.get('1.0', END)
        file.write(input)
        file_path = path
    print(file_path)
    dir_textbox.configure(state="normal")
    dir_textbox.delete('1.0', END)
    dir_textbox.insert('1.0', file_path)
    dir_textbox.configure(state="disabled")

def saveAsFile():
    global file_path
    path = filedialog.asksaveasfilename(filetypes=(("LOL Files", "*.lol"),))
    with open(path, 'w') as file:
        input = input_textbox.get('1.0', END)
        file.write(input)
        file_path = path
    dir_textbox.configure(state="normal")
    dir_textbox.delete('1.0', END)
    dir_textbox.insert('1.0', file_path)
    dir_textbox.configure(state="disabled")

def execFile():
    lexemes = lexer.lexer(file_path)
    lexeme.configure(state="normal")
    lexeme.delete('1.0', END)
    lexeme.insert('1.0', lexemes)
    lexeme.configure(state="disabled")

#BUTTONS
#save
save_button = Button(root,text='Save', command=saveFile, font=('Arial bold', 10), bg="#6082B6", fg="#36454F", activebackground="#7393B3", activeforeground="#36454F", borderwidth=0)
save_button.place(x=590, y=5, height=30, width=40)

#save as
saveas_button = Button(root,text='Save As', command=saveAsFile, font=('Arial bold', 10), bg="#6082B6", fg="#36454F", activebackground="#7393B3", activeforeground="#36454F",borderwidth=0)
saveas_button.place(x=640, y=5, height=30, width=60)

#open file
open_button = Button(root,text='Open', command=openFile, font=('Arial bold', 10), bg="#6082B6", fg="#36454F", activebackground="#7393B3", activeforeground="#36454F", borderwidth=0)
open_button.place(x=540, y=5, height=30, width=40)

#execute
exec_button = Button(root,text='Execute', command=execFile, font=('Arial bold', 15), bg="#6082B6", fg="#36454F", activebackground="#7393B3", activeforeground="#36454F", borderwidth=0)
exec_button.place(x=10, y=400, height=30, width=1380)

root.mainloop()