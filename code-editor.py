from numpy import number

f = open("test.txt")
output = open("output.txt", "w", encoding="utf-8")

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


def isANumber(word):
    if type(word) is int:
        return True
    else:
        try:
            int(word)
            return word
        except:
            return False


def isReservedWord(word):
    for key, value in tokens.items():
        if value == word:
            return value, key
    return tokens.get(25), word


def checkWord(word):
    numberToken = isANumber(word)
    if numberToken:
        output.write(f"{numberToken} --- {tokens.get(26)} \n")
    else:
        reservedWordToken = isReservedWord(word)
        output.write(f"{reservedWordToken[1]} --- {reservedWordToken[0]} \n")


for line in f:
    for word in line.split():
        checkWord(word)
        # output.write(f"{word} --- {key}\n")

f.close()
output.close()
