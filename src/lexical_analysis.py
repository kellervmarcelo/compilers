from .utils import is_a_number

tokens = {
    1: "Program",
    2: "Label",
    3: "Const",
    4: "Var",
    5: "Procedure",
    6: "Begin",
    7: "End",
    8: "Interger",
    9: "Array",
    10: "Of",
    11: "Call",
    12: "Goto",
    13: "If",
    14: "Then",
    15: "Else",
    16: "While",
    17: "Do",
    18: "Repeat",
    19: "Until",
    20: "Readln",
    21: "Writeln",
    22: "Or",
    23: "And",
    24: "Not",
    25: "Identificador",
    26: "Inteiro",
    27: "For",
    28: "To",
    29: "Case",
    30: "+",
    31: "-",
    32: "*",
    33: "/",
    34: "[",
    35: "]",
    36: "(",
    37: ")",
    38: ":=",
    39: ":",
    40: "=",
    41: ">",
    42: ">=",
    43: "<",
    44: "<=",
    45: "<>",
    46: ",",
    47: ";",
    48: "literal",
    49: ".",
    50: "..",
}


def check_word(word):
    for key, value in tokens.items():
        if value == word:
            return key, value;

    if (is_a_number(word)):
        return 26, int(word)

    return 25, word
