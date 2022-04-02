from tkinter import *
from src.lexical_analysis import check_word, separate_tokens
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess


compiler = Tk()
compiler.title('Aula de Compiladores')

file_path = ''

def lexycal_analisys():
    code = editor.get("1.0",END)
    foundTokens = []

    for line in code.split("\n"):
        for word in separate_tokens(line):
            foundTokens.append(word)

    code_output.delete('1.0', END)
    for token in foundTokens:
        code_output.insert(END, f'{check_word(token)}\n')

def set_file_path(path):
    global file_path
    file_path = path

def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('All Files', '*')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)


def open_file():
    path = askopenfilename(filetypes=[('All Files', '*')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)


menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open File', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)

run_menu = Menu(menu_bar, tearoff=0)
run_menu.add_command(label='Lexical analysis', command=lexycal_analisys)

menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label='Run', menu=run_menu)

run_bar = Menu(menu_bar, tearoff=0)

compiler.config(menu=menu_bar)

editor = Text()
editor.pack()

code_output = Text(height=7)
code_output.pack()

compiler.mainloop()
