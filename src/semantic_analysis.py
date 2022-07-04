import enum

from src.tokens import Token


class SemanticSymbol:

    def __init__(self, symbol, category, symbol_type, level):
        self.symbol = symbol
        self.category = category
        self.symbol_type = symbol_type
        self.level = level


class Categories(enum.Enum):
    program = 1
    label = 2
    const = 3
    var = 4
    procedure = 5
    begin = 6


def isIdentifier(token: Token):
    return token.ref_code == 25


def isEndOfBlock(token: Token):
    return token.ref_code == 7


def isDeclaration(category):
    if (category == Categories.program.value
            or category == Categories.procedure.value
            or category == Categories.begin.value):
        return False

    return True


def semantic_analysis(input_stack: list[Token]):
    category = 0
    level = 0

    symbols = []

    def isDeclared(symbol):
        for table_symbol in symbols:
            if (table_symbol.symbol == symbol.symbol
                    and table_symbol.level == symbol.level):
                return True

        return False

    for token in input_stack:
        if (token.ref_code in Categories._value2member_map_):
            category = token.ref_code

        if (token.ref_code == Categories.procedure.value
                or token.ref_code == Categories.program.value):
            level += 1

        if (isEndOfBlock(token)):
            level -= 1

        if (isIdentifier(token)):
            symbol = SemanticSymbol(token.token, category, "", level)

            if (isDeclaration(category)):
                if (isDeclared(symbol)):
                    raise Exception(
                        f"Declaration not allowed. Line: {token.line}")

                symbols.append(symbol)
