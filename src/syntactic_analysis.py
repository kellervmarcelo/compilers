from src.lexical_analysis import check_word
from src.tokens import derivations, non_terminal_tokens


def find_token_code(token):
    try:
        non_terminal = list(non_terminal_tokens.keys())[list(
            non_terminal_tokens.values()).index(token)]
        return non_terminal
    except:
        pass

    terminal = check_word(token)

    if terminal is not None:
        return terminal[0]

    raise Exception("Invalid token")


def syntactic_analysis(input_stack):
    derivation_stack = [52]

    while len(input_stack) > 0:
        if derivation_stack[0] < 52:
            if derivation_stack[0] == input_stack[0].ref_code:
                derivation_stack.pop(0)
                input_stack.pop(0)
                continue
            else:
                raise Exception(
                    f'Error on terminal analysis, line: {input_stack[0].line}')

        derivation_idx = f'{derivation_stack[0]},{input_stack[0].ref_code}'
        derivation = derivations.get(derivation_idx)

        if (derivation is None):
            raise Exception(
                f"Invalid derivation: {derivation_idx}, line: {input_stack[0].line}"
            )

        derivation_stack.pop(0)

        for item in reversed(derivation.split('|')):
            if item == "NULL":
                continue

            token_code = find_token_code(item)
            derivation_stack.insert(0, token_code)

    if len(derivation_stack) > 0:
       raise Exception("Derivations stack not empty")

    return

