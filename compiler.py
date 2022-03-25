from tkinter import *
from src.lexical_analysis import check_word
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

f = open("test.txt")
foundTokens = []

for line in f:
    for word in line.split():
        foundTokens.append(word)

for token in foundTokens:
    print(check_word(token))

f.close()

compiler = Tk()
compiler.title('Aula de Compiladores')

file_path = ''


def set_file_path(path):
    global file_path
    file_path = path

def save_as():
    if file_path == '':
        path = asksaveasfilenam(filetypes=[('All Files', '*')])
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
run_menu.add_command(label='Lexical analysis')

menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label='Run', menu=run_menu)

run_bar = Menu(menu_bar, tearoff=0)

compiler.config(menu=menu_bar)

editor = Text()
editor.pack()

code_output = Text(height=7)
code_output.pack()

compiler.mainloop()
