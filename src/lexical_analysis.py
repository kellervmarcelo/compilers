from .utils import is_a_number

tokens = [
    "Program", "Label", "Const", "Var", "Procedure", "Begin", "End",
    "Integer", "Array", "Of", "Call", "Goto", "If", "Then", "Else", "While",
    "Do", "Repeat", "Until", "Readln", "Writeln", "Or", "And", "Not",
    "Identificador", "Inteiro", "For", "To", "Case", "+", "-", "*", "/", "[",
    "]", "(", ")", ":=", ":", "=", ">", ">=", "<", "<=", "<>", ",", ";",
    "literal", ".", ".."
]


def check_word(word):
    if is_a_number(word):
        return int(word), tokens.index("Inteiro")
    else:
        try:
            idx = tokens.index(word)
        except:
            # TODO: implement verification for "Identificador"
            idx = tokens.index("Identificador")

        if idx == -1:
            raise NameError("Invalid token!")

        return word, tokens[idx]
