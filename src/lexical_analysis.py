import re
from .utils import is_a_number
from .tokens import tokens, separators


def separate_tokens(string):
    regex = r'(\'.*\'|\*.*\*|\ |\n|\*|%s)' % ("|".join(
        "\\" + "\\".join(list(s)) for s in separators))

    separated_tokens = re.split(regex, string)

    return filter(lambda x: x not in set(["", " "]), separated_tokens)


def check_word(word):
    for key, value in tokens.items():
        if value == word:
            return key, value

    if (is_a_number(word)):
        return 26, int(word)

    if (re.fullmatch(r'\'.*\'', word)):
        # Possible string
        if (re.fullmatch(r'\'.{0,255}\'', word)):
            # Valid string
            return 48, word
        else:
            raise Exception(
                "String with lenght over 255 characters not allowed")

    if (re.fullmatch(r'\*.*\*', word)):
        # Comment
        return

    if (re.fullmatch(r'[a-zA-Z][a-zA-Z0-9]{0,29}', word)):
        return 25, word

    if (re.fullmatch(r"End\.", word, re.IGNORECASE)):
        return 7, 'End'

    raise Exception("Invalid tokens")
