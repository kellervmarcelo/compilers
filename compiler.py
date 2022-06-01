import tkinter as tk
from src.lexical_analysis import lexical_analysis
from src.syntactic_analysis import syntactic_analysis
from tkinter.filedialog import asksaveasfilename, askopenfilename

root = tk.Tk()
root.title('Aula de Compiladores')

file_path = ''

lexical_analysis_result = []
syntactic_analysis_result = []
semantic_analysis_result = []


def run_lexical_analysis():
    code = editor.get("1.0", tk.END)

    global lexical_analysis_result
    lexical_analysis_result = lexical_analysis(code)

    code_output.delete('1.0', tk.END)
    for token in lexical_analysis_result:
        code_output.insert(
            tk.END,
            f'Token: {token.token} | Ref. Code: {token.ref_code} | Line: {token.line}\n'
        )


def run_syntactic_analysis():
    global syntactic_analysis_result
    global lexical_analysis_result

    syntactic_analysis_result = syntactic_analysis(lexical_analysis_result)


def set_file_path(path):
    global file_path
    file_path = path


def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('All Files', '*')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', tk.END)
        file.write(code)
        set_file_path(path)


def open_file():
    path = askopenfilename(filetypes=[('All Files', '*')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', tk.END)
        editor.insert('1.0', code)
        set_file_path(path)


menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open File', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)

run_menu = tk.Menu(menu_bar, tearoff=0)
run_menu.add_command(label='Lexical analysis', command=run_lexical_analysis)
run_menu.add_command(label='Semantic  analysis',
                     command=run_syntactic_analysis)

menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label='Run', menu=run_menu)

run_bar = tk.Menu(menu_bar, tearoff=0)

root.config(menu=menu_bar)

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill='both')

reference_table = tk.Text(left_frame, width=40)
reference_table.pack(fill='y', expand=1)

mid_frame = tk.Frame(root)
mid_frame.pack(side=tk.LEFT, fill='both', expand=1)

editor = tk.Text(mid_frame)
editor.pack(fill='both', expand=1)

code_output = tk.Text(mid_frame, height=7)
code_output.pack(fill='both', expand=1)

right_frame = tk.Frame(root, width=50)
right_frame.pack(side=tk.LEFT, fill='y', expand=1)

upper_stack = tk.Text(right_frame)
upper_stack.pack(fill='y', expand=1)

bottom_stack = tk.Text(right_frame)
bottom_stack.pack(fill='y', expand=1)

root.mainloop()
