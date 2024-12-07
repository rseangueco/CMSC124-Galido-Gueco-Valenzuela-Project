from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import scrolledtext
from tkinter import ttk
import lexer
# import syntax_analyzer_with_semnatics as parser
import syntax_analyzer as parser
import interpreter

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
# lexeme = scrolledtext.ScrolledText(root, font=('Consolas bold', 10))
# lexeme.configure(bg="#E5E4E2", fg="#36454F", insertbackground="#00A7B5", state="disabled")
# lexeme.place(x=710, y=80, height=310, width=335)
# style = ttk.Style()
# style.configure("Treeview",rowheight=40)
lexeme_frame = Frame(root, bg="#E5E4E2")
lexeme_frame.place(x=710, y=80, height=310, width=335)


lexeme_table = ttk.Treeview(lexeme_frame, columns=("Token", "Classification"), show="headings")
lexeme_table.heading("Token", text="Token")
lexeme_table.heading("Classification", text="Classification")
lexeme_table.column("Token", width=165, stretch=True)
lexeme_table.column("Classification", width=165, stretch=True)

lexeme_scrollbar = ttk.Scrollbar(lexeme_frame, orient=VERTICAL, command=lexeme_table.yview)
lexeme_table.configure(yscrollcommand=lexeme_scrollbar.set)
lexeme_scrollbar.pack(side=RIGHT, fill=Y)
lexeme_table.pack(side=LEFT, fill=BOTH, expand=True)

lexeme_label = Label(root, text="Lexemes", font=('Arial', 15), borderwidth=0, bg="#808080", fg="#36454F")
lexeme_label.place(x=710, y=40, height=40, width=335)

#symbol table using Treeview
symbol_frame = Frame(root, bg="#E5E4E2")
symbol_frame.place(x=1055, y=80, height=310, width=335)

symbol_table = ttk.Treeview(symbol_frame, columns=("Identifier", "Value"), show="headings")
symbol_table.heading("Identifier", text="Identifier")
symbol_table.heading("Value", text="Value")
symbol_table.column("Identifier", width=165)
symbol_table.column("Value", width=165)

#add scrollbar to symbol table
scrollbar = ttk.Scrollbar(symbol_frame, orient=VERTICAL, command=symbol_table.yview)
symbol_table.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
symbol_table.pack(side=LEFT, fill=BOTH, expand=True)

symbol_label = Label(root, text="Symbol Table", font=('Arial', 15), borderwidth=0, bg="#808080", fg="#36454F")
symbol_label.place(x=1055, y=40, height=40, width=335)

terminal = scrolledtext.ScrolledText(root, font=('Consolas', 10), bg="#E5E4E2", fg="#36454F", insertbackground="#00A7B5")
terminal.place(x=10, y=440, height=450, width=1380)

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
    
# def extract_value(expr_node, symbol_table):
#     if expr_node.type == 'NUMBR' or expr_node.type == 'NUMBAR':
#         return str(expr_node.value)
#     elif expr_node.type == 'YARN':
#         return expr_node.value.strip('"')  
#     elif expr_node.type == 'TROOF':
#         return "WIN" if expr_node.value else "FAIL"
#     elif expr_node.type == 'NOOB' or expr_node.value is None:
#         return "NOOB"
#     elif expr_node.type == 'IDENTIFIER':
#         return symbol_table.get(expr_node.value, "NOOB")
#     else:
#         return "UNKNOWN"

# def execFile():

#     for item in lexeme_table.get_children():
#         lexeme_table.delete(item)
#     #clear existing symbol table
#     for item in symbol_table.get_children():
#         symbol_table.delete(item)
        
#     #get tokens and formatted output
#     try:
#         tokens, formatted_output = lexer.lexer(file_path)
        
#         #update lexeme display
#         # lexeme.configure(state="normal")
#         # lexeme.delete('1.0', END)
#         # lexeme.insert('1.0', formatted_output)
#         # lexeme.configure(state="disabled")
        
#         for token, classification in tokens:
#             if token != "linebreak":
#                 lexeme_table.insert('', END, values=(token, classification))
#         #parse tokens and get symbol table
#         parser_instance = parser.Parser(tokens)
#         parse_tree = parser_instance.parse()
        
#         #update symbol table display with variables from parser
#         for var_name, var_value in parser_instance.symbol_table.items():
#             symbol_table.insert('', END, values=(var_name, var_value))
                
#         # except Exception as e:
#         #     #show error in lexeme display for debugging
#         #     lexeme.configure(state="normal")
#         #     lexeme.delete('1.0', END)
#         #     lexeme.insert('1.0', f"Error: {str(e)}")
#         #     lexeme.configure(state="disabled")
        
def execFile():
    for item in lexeme_table.get_children():
        lexeme_table.delete(item)
    for item in symbol_table.get_children():
        symbol_table.delete(item)
        terminal.delete('1.0', END)

    try:
        tokens, formatted_output = lexer.lexer(file_path)
        for token, classification in tokens:
            if token != "linebreak":
                lexeme_table.insert('', END, values=(token, classification))
                
        parser_instance = parser.Parser(tokens)
        parse_tree = parser_instance.parse()
        
        interpreter_instance = interpreter.Interpreter(parse_tree)
        output = interpreter_instance.interpret()
        
        for var_name, var_value in interpreter_instance.symbol_table.items():
            symbol_table.insert('', END, values=(var_name, var_value['value']))

        for line in output:
            terminal.insert(END, str(line) + '\n')
            print(line)
        
        # for child in parse_tree.children:
        #     if child.type == 'CODE_SECTION':
        #         for stmt in child.children:
        #             if stmt.type == 'STATEMENT':
        #                 for inner_child in stmt.children:
        #                     if inner_child.type == 'PRINT_STMT':
        #                         for expr in inner_child.children:
        #                             if expr.type == 'EXPRESSION':
        #                                 # print(expr.value)
        #                                 # terminal.insert(END, str(extract_value(expr, parser_instance.symbol_table)) + "\n")
        #                                 terminal.insert(END, str(expr.value) + "\n")
        #                                 terminal.see(END)
        #                     # elif inner_child.type == 'INPUT_STMT':
        #                     #     #update symbol table after processing GIMMEH
        #                     #     parser_instance.input_stmt()
        #                     #     #refresh symbol table in the GUI
        #                     #     symbol_table.delete(*symbol_table.get_children())
        #                     #     for var_name, var_value in interpreter_instance.symbol_table.items():
        #                     #         symbol_table.insert('', END, values=(var_name, var_value['value']))

    except Exception as e:
                        terminal.insert(END, f"Error: {str(e)}\n")
                        terminal.see(END)
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
