from concurrent.futures import process
from click import command
from word_checker import checkWord
import os.path
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

f = open("test.txt")
foundTokens = []

for line in f:
    for word in line.split():
        foundTokens.append(word)

for token in foundTokens:
    checkWord(token)

f.close()

compiler = Tk()
compiler.title('Aula de Compiladores')

file_path = ''

def set_file_path(path):
    global file_path 
    file_path = path

def run ():
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text="You have to save your code before running it")
        text.pack()
        return
    command = f'python {file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.insert(END, output)
    code_output.insert(END, error)

def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else: 
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)

def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
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
menu_bar.add_cascade(label='File', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

compiler.config(menu=menu_bar)

editor = Text()
editor.pack()

code_output = Text(height=7)
code_output.pack()

compiler.mainloop()
