import enum
import re
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

    def isArray(self):
        return re.search("Array", self.symbol_type, re.IGNORECASE)


class Categories(enum.Enum):
    program = 1
    label = 2
    const = 3
    var = 4
    procedure = 5
    begin = 6

    parameter = -1


class Operators(enum.Enum):
    sum = 30
    sub = 31
    mult = 32
    division = 33


def isIdentifier(token: Token):
    return token.ref_code == 25


def isEndOfBlock(token: Token):
    return token.ref_code == 7


def isDeclaration(category):
    if category == Categories.begin.value:
        return False

    return True


def semantic_analysis(input_stack: list[Token]):
    category = 0
    begin_level = 0
    start_of_scope = False
    scope_stack = []

    symbols = []

    def isDeclared(symbol: SemanticSymbol):
        for table_symbol in symbols:
            if (
                table_symbol.symbol.lower() == symbol.symbol.lower()
                and table_symbol.level == symbol.level
                and table_symbol.scope_name == symbol.scope_name
            ):
                return True
        return False

    def searchInTable(symbol: str, level: int, scope_stack: list[str]):
        while level > 0:
            for table_symbol in symbols:
                if (
                    table_symbol.symbol.lower() == symbol.lower()
                    and table_symbol.level == level
                    and table_symbol.scope_name == scope_stack[-1]
                ):
                    return table_symbol

            level -= 1
            scope_stack.pop(-1)

    for idx, token in enumerate(input_stack):

        def isRegularAssignment():
            return input_stack[idx + 1].ref_code == 38

        def isArrayAssignment():
            return (
                input_stack[idx + 1].ref_code == 34
                and input_stack[idx + 3].ref_code == 35
                and input_stack[idx + 4].ref_code == 38
            )

        # Updates category for each of the keywords declared in the Categories Enum
        if token.ref_code in Categories._value2member_map_:
            category = token.ref_code

        # Keeps track of beginning of new scopes
        if token.ref_code in [Categories.procedure.value, Categories.program.value]:
            start_of_scope = True

        # Keeps track of BEGIN keyword appearence to check against END keyword
        if token.ref_code == Categories.begin.value:
            begin_level += 1

        # Keeps track of ending of new scopes
        if isEndOfBlock(token):
            if (begin_level) == len(scope_stack) - 1:
                scope_stack.pop(-1)

            begin_level -= 1

        if isIdentifier(token):
            # Keeps track of beginning of new scopes
            if start_of_scope:
                scope_stack.append(token.token)
                start_of_scope = False

            symbol = SemanticSymbol(
                token.token, category, "", len(scope_stack), scope_stack.copy()
            )

            # Check for procedure parameters
            if category == Categories.procedure.value:
                if symbols[-1].symbol == scope_stack[-1]:
                    symbol_type = "Integer"
                    symbol.category = Categories.parameter.value
                else:
                    symbol.level -= 1
                    symbol.scope_stack.pop(-1)
                    symbol.scope_name = symbol.scope_stack[-1]

            if isDeclaration(category):
                # Checks if variable is being declared for the second time
                if isDeclared(symbol):
                    raise Exception(f"Declaration not allowed. Line: {token.line}")

                symbol_type = ""

                # Checks for variable types
                if symbol.category == Categories.const.value:
                    symbol_type = "Integer"

                if symbol.category == Categories.var.value:
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
                            if _token.ref_code == 10 or (
                                _token.ref_code == 8 and symbol_type != ""
                            ):
                                symbol_type = symbol_type + " "

                            symbol_type = symbol_type + str(_token.token)


                symbol.symbol_type = symbol_type
                symbols.append(symbol)
            else:
                table_symbol = searchInTable(
                    symbol.symbol, symbol.level, symbol.scope_stack.copy()
                )

                # Checks if variable was not declared
                if table_symbol == None:
                    raise Exception(
                        f"Undeclared variable or procedure. Line: {token.line}"
                    )

                # Check if for loop variables are in fact variables
                if input_stack[idx - 1].ref_code == 27:
                    if table_symbol.category != Categories.var.value:
                        raise Exception(
                            "FOR must receive a variable. Line: {token.line}"
                        )

                    if table_symbol.symbol_type != "Integer":
                        raise Exception(
                            "FOR must receive an integer variable. Line: {token.line}"
                        )
                elif isRegularAssignment():
                    # Checks if const is being assigned a new value
                    if table_symbol.category == Categories.const.value:
                        raise Exception(
                            f"Const assignment is not allowed. Line: {token.line}"
                        )

                    # Check if assignment is compatible with variable type
                    for _idx, _token in enumerate(input_stack[idx:]):
                        # Token ; detected, break out of loop
                        if _token.ref_code == 47:
                            break

                        if (
                            is_a_number(_token.token)
                            and table_symbol.symbol_type != "Integer"
                        ):
                            raise Exception(f"Invalid assignment. Line: {token.line}")

                        if isIdentifier(_token):
                            _symbol = SemanticSymbol(
                                _token.token,
                                category,
                                "",
                                len(scope_stack),
                                scope_stack.copy(),
                            )

                            _table_symbol = searchInTable(
                                _symbol.symbol,
                                _symbol.level,
                                _symbol.scope_stack.copy(),
                            )

                            if _table_symbol == None:
                                break

                            if _table_symbol.isArray():
                                i = idx + _idx + 1
                                if not (
                                    input_stack[i].ref_code == 34
                                    and is_a_number(input_stack[i + 1].token)
                                    and is_a_number(input_stack[i + 2].ref_code == 35)
                                ):
                                    raise Exception(
                                        f"Invalid assignment. Line: {token.line}"
                                    )

                                # array = [_table_symbol.symbol]
                                # bracket_count = 0
                                # for array_token in input_stack[_idx + idx + 1:]:
                                #     if array_token.ref_code == 34:
                                #         bracket_count += 1
                                #     elif array_token.ref_code == 35:
                                #         bracket_count -= 1
                                #     array.append(str(array_token.token))
                                #     if bracket_count == 0:
                                #         break

                            else:
                                if (
                                    _table_symbol.symbol_type
                                    != table_symbol.symbol_type
                                ):
                                    raise Exception(
                                        f"Invalid assignment. Line: {token.line}"
                                    )

                # Checks if array is being assigned a value and if variable is an integer
                if isArrayAssignment():
                    start_assignment = False

                    for _token in input_stack[idx:]:

                        if _token.ref_code == 38:
                            start_assignment = True
                            continue

                        # Token ; detected, break out of loop
                        if _token.ref_code == 47:
                            break

                        if start_assignment == False:
                            continue

                        if is_a_number(_token.token):
                            continue

                        _symbol = SemanticSymbol(
                            _token.token,
                            category,
                            "",
                            len(scope_stack),
                            scope_stack.copy(),
                        )

                        _table_symbol = searchInTable(
                            _symbol.symbol,
                            _symbol.level,
                            _symbol.scope_stack.copy(),
                        )

                        if _table_symbol == None:
                            continue

                        if _table_symbol.symbol_type != "Integer":
                            raise Exception(f"Invalid assignment. Line: {token.line}")

                # Check if procedure calls are being called with the correct arguments
                # TODO: Currently, it's assumed that the procedure will only have one integer param
                if table_symbol.category == Categories.procedure.value:
                    parenthesis_count = 0
                    for _token in input_stack[idx + 1 :]:
                        if _token.ref_code in Operators._value2member_map_:
                            continue

                        if is_a_number(_token.token):
                            continue

                        if _token.ref_code == 36:
                            parenthesis_count += 1
                            continue
                        elif _token.ref_code == 37:
                            parenthesis_count -= 1
                            continue

                        if parenthesis_count == 0:
                            break

                        _symbol = SemanticSymbol(
                            _token.token,
                            category,
                            "",
                            len(scope_stack),
                            scope_stack.copy(),
                        )

                        _table_symbol = searchInTable(
                            _symbol.symbol,
                            _symbol.level,
                            _symbol.scope_stack.copy(),
                        )

                        if _table_symbol == None:
                            raise Exception(f"Invalid parameter. Line: {_token.line}")

                        if _table_symbol.symbol_type != "Integer":
                            raise Exception(f"Invalid parameter. Line: {_token.line}")


    return symbols
