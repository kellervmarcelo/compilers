import tkinter as tk
from tkinter import ttk
from src.semantic_analysis import Categories, semantic_analysis
from src.lexical_analysis import lexical_analysis
from src.syntactic_analysis import syntactic_analysis
from tkinter.filedialog import asksaveasfilename, askopenfilename
from src.tokens import tokens, non_terminal_tokens

root = tk.Tk()
root.title('Aula de Compiladores')

file_path = ''

lexical_analysis_result = []
syntactic_analysis_result = []
semantic_analysis_result = []


def run_lexical_analysis():
    code = editor.get("1.0", tk.END)

    global lexical_analysis_result
    global syntactic_analysis_result
    global semantic_analysis_result

    lexical_analysis_result = []
    syntactic_analysis_result = []
    semantic_analysis_result = []

    lexical_output.delete(*lexical_output.get_children())
    semantic_output.delete(*semantic_output.get_children())

    syntactic_output.delete('1.0', tk.END)

    try:
        lexical_analysis_result = lexical_analysis(code)

        for token in lexical_analysis_result:
            lexical_output.insert('',
                                  tk.END,
                                  values=(token.ref_code, token.token,
                                          token.line))

        syntactic_output.insert(tk.END,
                                "Análise léxica: concluída com sucesso.\n")
    except Exception as e:
        syntactic_output.insert(tk.END, f"Análise léxica: {str(e)}.\n")


def run_syntactic_analysis():
    global syntactic_analysis_result
    global lexical_analysis_result

    run_lexical_analysis()

    try:
        syntactic_analysis_result = syntactic_analysis(
            lexical_analysis_result.copy())
        syntactic_output.insert(tk.END,
                                "Análise sintática: concluída com sucesso.\n")
    except Exception as e:
        syntactic_output.insert(tk.END, f'Análise sintática: {str(e)}.')


def run_semantic_analysis():
    global lexical_analysis_result
    global semantic_analysis_result

    run_syntactic_analysis()

    try:
        semantic_analysis_result = semantic_analysis(
            lexical_analysis_result.copy())
        for symbol in semantic_analysis_result:
            semantic_output.insert('',
                                   tk.END,
                                   values=(symbol.symbol,
                                           Categories(symbol.category).name,
                                           symbol.symbol_type, symbol.level,
                                           symbol.scope_name))
        syntactic_output.insert(tk.END,
                                f'Análise semântica: concluída com sucesso.')
    except Exception as e:
        syntactic_output.insert(tk.END, f'Análise semântica: {str(e)}.')


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
run_menu.add_command(label='Análise lexica', command=run_lexical_analysis)
run_menu.add_command(label='Análise sintática', command=run_syntactic_analysis)
run_menu.add_command(label='Análise semântica', command=run_semantic_analysis)

menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label='Run', menu=run_menu)

run_bar = tk.Menu(menu_bar, tearoff=0)

root.config(menu=menu_bar)

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill='both')

ref_table_columns = ('ref_code', 'description')
ref_table = ttk.Treeview(left_frame,
                         columns=ref_table_columns,
                         show='headings')
ref_table.heading('ref_code', text='Cód.')
ref_table.column('ref_code', width=50)
ref_table.heading('description', text='Descrição')
ref_table.column('description', width=130)

for key, value in tokens.items():
    ref_table.insert('', tk.END, values=(key, value))

for key, value in non_terminal_tokens.items():
    ref_table.insert('', tk.END, values=(key, value))

ref_table.pack(fill='y', expand=1)

mid_frame = tk.Frame(root)
mid_frame.pack(side=tk.LEFT, fill='both', expand=1)

editor = tk.Text(mid_frame)
editor.pack(fill='both', expand=1)

right_frame = tk.Frame(root, width=20)
right_frame.rowconfigure(0, weight=1)
right_frame.rowconfigure(1, weight=1)
right_frame.rowconfigure(2, weight=1)

right_frame.columnconfigure(0, weight=1)

right_frame.pack(side=tk.LEFT, fill='y')

lexical_output_columns = ('ref_code', 'token', 'line')
lexical_output = ttk.Treeview(right_frame,
                              columns=lexical_output_columns,
                              show='headings')

lexical_output.heading('ref_code', text='Cód.')
# lexical_output.column('ref_code', stretch=True)
lexical_output.heading('token', text='Token')
# lexical_output.column('token', stretch=True)
lexical_output.heading('line', text='Linha')
# lexical_output.column('line', stretch=True)

syntactic_output = tk.Text(right_frame)

semantic_output_columns = ('symbol', 'category', 'symbol_type', 'level',
                           'scope_name')
semantic_output = ttk.Treeview(right_frame,
                               columns=semantic_output_columns,
                               show='headings')

semantic_output.heading('symbol', text='Símbolo')
# semantic_output.column('symbol', stretch=True)
semantic_output.heading('category', text='Categoria')
# semantic_output.column('category', stretch=True)
semantic_output.heading('symbol_type', text='Tipo')
# semantic_output.column('symbol_type', stretch=True)
semantic_output.heading('level', text='Nível')
# semantic_output.column('level', stretch=True)
semantic_output.heading('scope_name', text='Escopo')
# semantic_output.column('scope_name', stretch=True)

lexical_output.grid(column=0, row=0)
syntactic_output.grid(column=0, row=1)
semantic_output.grid(column=0, row=2)

root.mainloop()
