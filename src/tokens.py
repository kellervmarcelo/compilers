class Token:
    def __init__(self, token, ref_code, line):
        self.token = token
        self.ref_code = ref_code
        self.line = line


tokens = {
    1: "Program",
    2: "Label",
    3: "Const",
    4: "Var",
    5: "Procedure",
    6: "Begin",
    7: "End",
    8: "Integer",
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
    51: "$",
}

non_terminal_tokens = {
    52: "PROGRAMA",
    53: "BLOCO",
    54: "DCLROT",
    55: "LID",
    56: "REPIDENT",
    57: "DCLCONST",
    58: "LDCONST",
    59: "DCLVAR",
    60: "LDVAR",
    61: "TIPO",
    62: "DCLPROC",
    63: "DEFPAR",
    64: "CORPO",
    65: "REPCOMANDO",
    66: "COMANDO",
    67: "RCOMID",
    68: "RVAR",
    69: "PARAMETROS",
    70: "REPPAR",
    71: "ELSEPARTE",
    72: "VARIAVEL",
    73: "VARIAVEL1",
    74: "REPVARIAVEL",
    75: "ITEMSAIDA",
    76: "REPITEM",
    77: "EXPRESSAO",
    78: "REPEXPSIMP",
    79: "EXPSIMP",
    80: "REPEXP",
    81: "TERMO",
    82: "REPTERMO",
    83: "FATOR",
    84: "CONDCASE",
    85: "CONTCASE",
    86: "RPINTEIRO",
    87: "SEMEFEITO",
}

separators = [
    ":=",
    ">=",
    "<=",
    "<>",
    "+",
    "-",
    "*",
    "/",
    "[",
    "]",
    "(",
    ")",
    ":",
    "=",
    ">",
    "<",
    ",",
    ";",
    "..",
    ".",
    "$",
]

derivations = {
    "52,1": "PROGRAM|IDENTIFICADOR|;|BLOCO|.",
    "53,2": "DCLROT|DCLCONST|DCLVAR|DCLPROC|CORPO",
    "53,3": "DCLROT|DCLCONST|DCLVAR|DCLPROC|CORPO",
    "53,4": "DCLROT|DCLCONST|DCLVAR|DCLPROC|CORPO",
    "53,5": "DCLROT|DCLCONST|DCLVAR|DCLPROC|CORPO",
    "53,6": "DCLROT|DCLCONST|DCLVAR|DCLPROC|CORPO",
    "54,2": "LABEL|LID|;",
    "54,3": "NULL",
    "54,4": "NULL",
    "54,5": "NULL",
    "54,6": "NULL",
    "55,25": "IDENTIFICADOR|REPIDENT",
    "56,39": "NULL",
    "56,46": ",|IDENTIFICADOR|REPIDENT",
    "56,47": "NULL",
    "57,3": "CONST|IDENTIFICADOR|=|INTEIRO|;|LDCONST",
    "57,4": "NULL",
    "57,5": "NULL",
    "57,6": "NULL",
    "58,4": "NULL",
    "58,5": "NULL",
    "58,6": "NULL",
    "58,25": "IDENTIFICADOR|=|INTEIRO|;|LDCONST",
    "59,4": "VAR|LID|:|TIPO|;|LDVAR",
    "59,5": "NULL",
    "59,6": "NULL",
    "60,5": "NULL",
    "60,6": "NULL",
    "60,25": "LID|:|TIPO|;|LDVAR",
    "61,8": "INTEGER",
    "61,9": "ARRAY|[|INTEIRO|..|INTEIRO|]|OF|INTEGER",
    "62,5": "PROCEDURE|IDENTIFICADOR|DEFPAR|;|BLOCO|;|DCLPROC",
    "62,6": "NULL",
    "63,36": "(|LID|:|INTEGER|)",
    "63,39": "NULL",
    "64,6": "BEGIN|COMANDO|REPCOMANDO|END",
    "65,7": "NULL",
    "65,47": ";|COMANDO|REPCOMANDO",
    "66,6": "CORPO",
    "66,7": "NULL",
    "66,11": "CALL|IDENTIFICADOR|PARAMETROS",
    "66,12": "GOTO|IDENTIFICADOR",
    "66,13": "IF|EXPRESSAO|THEN|COMANDO|ELSEPARTE",
    "66,15": "NULL",
    "66,16": "WHILE|EXPRESSAO|DO|COMANDO",
    "66,18": "REPEAT|COMANDO|UNTIL|EXPRESSAO",
    "66,19": "NULL",
    "66,20": "READLN|(|VARIAVEL|REPVARIAVEL|)",
    "66,21": "WRITELN|(|ITEMSAIDA|REPITEM|)",
    "66,25": "IDENTIFICADOR|RCOMID",
    "66,27": "FOR|IDENTIFICADOR|:=|EXPRESSAO|TO|EXPRESSAO|DO|COMANDO",
    "66,29": "CASE|EXPRESSAO|OF|CONDCASE|END",
    "66,47": "NULL",
    "67,34": "RVAR|:=|EXPRESSAO",
    "67,38": "RVAR|:=|EXPRESSAO",
    "67,39": ":|COMANDO",
    "68,34": "[|EXPRESSAO|]",
    "68,38": "NULL",
    "69,7": "NULL",
    "69,15": "NULL",
    "69,19": "NULL",
    "69,36": "(|EXPRESSAO|REPPAR|)",
    "69,47": "NULL",
    "70,37": "NULL",
    "70,46": ",|EXPRESSAO|REPPAR",
    "71,7": "NULL",
    "71,15": "ELSE|COMANDO",
    "71,19": "NULL",
    "71,47": "NULL",
    "72,25": "IDENTIFICADOR|VARIAVEL1",
    "73,7": "NULL",
    "73,10": "NULL",
    "73,14": "NULL",
    "73,15": "NULL",
    "73,17": "NULL",
    "73,19": "NULL",
    "73,22": "NULL",
    "73,23": "NULL",
    "73,28": "NULL",
    "73,30": "NULL",
    "73,31": "NULL",
    "73,32": "NULL",
    "73,33": "NULL",
    "73,34": "[|EXPRESSAO|]",
    "73,35": "NULL",
    "73,37": "NULL",
    "73,40": "NULL",
    "73,41": "NULL",
    "73,42": "NULL",
    "73,43": "NULL",
    "73,44": "NULL",
    "73,45": "NULL",
    "73,46": "NULL",
    "73,47": "NULL",
    "74,37": "NULL",
    "74,46": ",|VARIAVEL|REPVARIAVEL",
    "75,24": "EXPRESSAO",
    "75,25": "EXPRESSAO",
    "75,26": "EXPRESSAO",
    "75,30": "EXPRESSAO",
    "75,31": "EXPRESSAO",
    "75,36": "EXPRESSAO",
    "75,48": "LITERAL",
    "76,37": "NULL",
    "76,46": ",|ITEMSAIDA|REPITEM",
    "77,24": "EXPSIMP|REPEXPSIMP",
    "77,25": "EXPSIMP|REPEXPSIMP",
    "77,26": "EXPSIMP|REPEXPSIMP",
    "77,30": "EXPSIMP|REPEXPSIMP",
    "77,31": "EXPSIMP|REPEXPSIMP",
    "77,36": "EXPSIMP|REPEXPSIMP",
    "78,7": "NULL",
    "78,10": "NULL",
    "78,14": "NULL",
    "78,15": "NULL",
    "78,17": "NULL",
    "78,19": "NULL",
    "78,28": "NULL",
    "78,35": "NULL",
    "78,37": "NULL",
    "78,40": "=|EXPSIMP",
    "78,41": ">|EXPSIMP",
    "78,42": ">=|EXPSIMP",
    "78,43": "<|EXPSIMP",
    "78,44": "<=|EXPSIMP",
    "78,45": "<>|EXPSIMP",
    "78,46": "NULL",
    "78,47": "NULL",
    "79,24": "TERMO|REPEXP",
    "79,25": "TERMO|REPEXP",
    "79,26": "TERMO|REPEXP",
    "79,30": "+|TERMO|REPEXP",
    "79,31": "-|TERMO|REPEXP",
    "79,36": "TERMO|REPEXP",
    "80,7": "NULL",
    "80,10": "NULL",
    "80,14": "NULL",
    "80,15": "NULL",
    "80,17": "NULL",
    "80,19": "NULL",
    "80,22": "OR|TERMO|REPEXP",
    "80,28": "NULL",
    "80,30": "+|TERMO|REPEXP",
    "80,31": "-|TERMO|REPEXP",
    "80,35": "NULL",
    "80,37": "NULL",
    "80,40": "NULL",
    "80,41": "NULL",
    "80,42": "NULL",
    "80,43": "NULL",
    "80,44": "NULL",
    "80,45": "NULL",
    "80,46": "NULL",
    "80,47": "NULL",
    "81,24": "FATOR|REPTERMO",
    "81,25": "FATOR|REPTERMO",
    "81,26": "FATOR|REPTERMO",
    "81,36": "FATOR|REPTERMO",
    "82,7": "NULL",
    "82,10": "NULL",
    "82,14": "NULL",
    "82,15": "NULL",
    "82,17": "NULL",
    "82,19": "NULL",
    "82,22": "NULL",
    "82,23": "AND|FATOR|REPTERMO",
    "82,28": "NULL",
    "82,30": "NULL",
    "82,31": "NULL",
    "82,32": "*|FATOR|REPTERMO",
    "82,33": "/|FATOR|REPTERMO",
    "82,35": "NULL",
    "82,37": "NULL",
    "82,40": "NULL",
    "82,41": "NULL",
    "82,42": "NULL",
    "82,43": "NULL",
    "82,44": "NULL",
    "82,45": "NULL",
    "82,46": "NULL",
    "82,47": "NULL",
    "83,24": "NOT|FATOR",
    "83,25": "VARIAVEL",
    "83,26": "INTEIRO",
    "83,36": "(|EXPRESSAO|)",
    "84,26": "INTEIRO|RPINTEIRO|:|COMANDO|CONTCASE",
    "85,7": "NULL",
    "85,47": ";|CONDCASE",
    "86,39": "NULL",
    "86,46": ",|INTEIRO|RPINTEIRO",
}
