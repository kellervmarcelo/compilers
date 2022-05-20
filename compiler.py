from tkinter import *
from src.lexical_analysis import lexical_analysis
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

compiler = Tk()
compiler.title('Aula de Compiladores')

file_path = ''

lexical_analysis_result = []
syntactic_analysis_result = []
semantic_analysis_result = []

def run_lexical_analysis():
    code = editor.get("1.0",END)

    lexical_analysis_result = lexical_analysis(code)

    code_output.delete('1.0', END)
    for token in lexical_analysis_result:
        code_output.insert(END, f'Token: {token.token} | Ref. Code: {token.ref_code} | Line: {token.line}\n')

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
run_menu.add_command(label='Lexical analysis', command=run_lexical_analysis)

menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label='Run', menu=run_menu)

run_bar = Menu(menu_bar, tearoff=0)

compiler.config(menu=menu_bar)

editor = Text()
editor.pack()

code_output = Text(height=7)
code_output.pack()

compiler.mainloop()
