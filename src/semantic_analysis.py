import enum
from src.tokens import Token
from src.utils import is_a_number


class SemanticSymbol:

    def __init__(self, symbol, category, symbol_type, level, scope_stack):
        self.symbol = symbol
        self.category = category
        self.symbol_type = symbol_type
        self.level = level
        self.scope_name = scope_stack[-1]
        self.scope_stack = scope_stack


class Categories(enum.Enum):
    program = 1
    label = 2
    const = 3
    var = 4
    procedure = 5
    begin = 6

    parameter = -1


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

    def isDeclared(symbol: SemanticSymbol):
        for table_symbol in symbols:
            if (table_symbol.symbol.lower() == symbol.symbol.lower()
                    and table_symbol.level == symbol.level):
                return True
        return False

    def searchInTable(symbol: str, level: int, scope_stack: list[str]):
        while level > 0:
            for table_symbol in symbols:
                if (table_symbol.symbol.lower() == symbol.lower()
                        and table_symbol.level == level
                        and table_symbol.scope_name == scope_stack[-1]):
                    return table_symbol

            level -= 1
            scope_stack.pop(-1)

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
                                    scope_stack.copy())

            if (isDeclaration(category)):
                # Checks if variable is being declared for the second time
                if (isDeclared(symbol)):
                    raise Exception(
                        f"Declaration not allowed. Line: {token.line}")

                symbol_type = ""

                # Checks for variable types
                if (symbol.category == Categories.const.value):
                    symbol_type = "Integer"

                if (symbol.category == Categories.var.value):
                    is_type_declaration = False

                    for _token in input_stack[idx:]:
                        # Token : detected, type declaration starts here
                        if _token.ref_code == 39:
                            is_type_declaration = True
                            continue

                        # Token ; detected, break out of loop
                        if _token.ref_code == 47:
                            break

                        if is_type_declaration:
                            # If keyword Of or Integer
                            if _token.ref_code == 10 or (_token.ref_code == 8
                                                         and
                                                         symbol_type != ""):
                                symbol_type = symbol_type + " "

                            symbol_type = symbol_type + str(_token.token)

                # Check for procedure parameters
                if (symbol.category == Categories.procedure.value):
                    if (symbols[-1].symbol == scope_stack[-1]):
                        symbol_type = "Integer"
                        symbol.category = Categories.parameter.value

                symbol.symbol_type = symbol_type
                symbols.append(symbol)
            else:
                table_symbol = searchInTable(symbol.symbol, symbol.level,
                                             symbol.scope_stack.copy())

                # Checks if variable was not declared
                if (table_symbol == None):
                    raise Exception(
                        f"Undeclared variable or procedure. Line: {token.line}"
                    )

                if (isAssignment()):
                    # Checks if const is being assigned a new value
                    if (table_symbol.category == Categories.const.value):
                        raise Exception(
                            f"Const assignment is not allowed. Line: {token.line}"
                        )

                    # Check if assignment is compatible with variable type
                    for _token in input_stack[idx:]:
                        # Token ; detected, break out of loop
                        if _token.ref_code == 47:
                            break

                        if (is_a_number(_token.token) and table_symbol.symbol_type != 'Integer'):
                            raise Exception(
                                f"Invalid assignment. Line: {token.line}")

                        if isIdentifier(_token):
                            _symbol = SemanticSymbol(_token.token, category,
                                                     "", scope_level,
                                                     scope_stack.copy())

                            _table_symbol = searchInTable(
                                _symbol.symbol, _symbol.level,
                                _symbol.scope_stack.copy())

                            if (_table_symbol == None):
                                break

                            # TODO Check for array

                            if (_table_symbol.symbol_type != table_symbol.symbol_type):
                                raise Exception(f"Invalid assignment. Line: {token.line}")

                    # TODO Check if array is being assigned within supported range

                # TODO Check if procedure calls are being called with the correct arguments

    return symbols
