import enum

from src.tokens import Token


class SemanticSymbol:

    def __init__(self, symbol, category, symbol_type, level, scope_name):
        self.symbol = symbol
        self.category = category
        self.symbol_type = symbol_type
        self.level = level
        self.scope_name = scope_name


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
    scope_level = 0
    begin_level = 0
    start_of_scope = False
    scope_stack = []

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

        if (not isDeclaration(token.ref_code)):
            if (token.ref_code != Categories.begin.value):
                scope_level += 1
                start_of_scope = True
            else:
                begin_level += 1

        if (isEndOfBlock(token)):
            if ((begin_level - 1) == scope_level):
                scope_level -= 1
                scope_stack.pop(-1)

            begin_level -= 1

        if (isIdentifier(token)):
            if start_of_scope:
                scope_stack.append(token.token)
                start_of_scope = False

            symbol = SemanticSymbol(token.token, category, "", scope_level, scope_stack[-1])

            if (isDeclaration(category)):
                if (isDeclared(symbol)):
                    raise Exception(
                        f"Declaration not allowed. Line: {token.line}")

                symbols.append(symbol)
