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
    if (category == Categories.begin.value):
        return False

    return True


def semantic_analysis(input_stack: list[Token]):
    category = 0
    scope_level = 0
    begin_level = 0
    start_of_scope = False
    scope_stack = []

    symbols = []

    def searchInTable(symbol):
        for table_symbol in symbols:
            if (table_symbol.symbol.lower() == symbol.symbol.lower()
                    and table_symbol.level == symbol.level):
                return table_symbol

    for idx, token in enumerate(input_stack):

        def isAssignment():
            return input_stack[idx + 1].ref_code == 38

        # Updates category for each of the keywords declared in the Categories Enum
        if (token.ref_code in Categories._value2member_map_):
            category = token.ref_code

        # Keeps track of beginning of new scopes
        if (token.ref_code
                in [Categories.procedure.value, Categories.program.value]):
            scope_level += 1
            start_of_scope = True

        # Keeps track of BEGIN keyword appearence to check against END keyword
        if (token.ref_code == Categories.begin.value):
            begin_level += 1

        # Keeps track of ending of new scopes
        if (isEndOfBlock(token)):
            if ((begin_level - 1) == scope_level):
                scope_level -= 1
                scope_stack.pop(-1)

            begin_level -= 1

        if (isIdentifier(token)):
            # Keeps track of beginning of new scopes
            if start_of_scope:
                scope_stack.append(token.token)
                start_of_scope = False

            symbol = SemanticSymbol(token.token, category, "", scope_level,
                                    scope_stack[-1])

            table_symbol = searchInTable(symbol)
            if (isDeclaration(category)):
                # Checks if variable is being declared for the second time
                if (table_symbol != None):
                    raise Exception(
                        f"Declaration not allowed. Line: {token.line}")

                # TODO Check for procedure parameters

                symbols.append(symbol)
            else:
                # Checks if variable was not declared
                if (table_symbol == None):
                    raise Exception(
                        f"Undeclared variable or procedure. Line: {token.line}"
                    )

                # Checks if const is being assigned a new value
                if (isAssignment()
                        and table_symbol.category == Categories.const.value):
                    raise Exception(
                        f"Const assignment is not allowed. Line: {token.line}")

                    # TODO Check if assignment is compatible with variable type

                # TODO Check if procedure calls are being called with the correct arguments

    return symbols
