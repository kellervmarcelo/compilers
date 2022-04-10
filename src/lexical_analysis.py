import re
from .utils import is_a_number
from .tokens import tokens, separators


def separate_tokens(string):
    regex = r'(\ |\n|\*|%s)' % ("|".join("\\" + "\\".join(list(s))
                                         for s in separators))

    separated_tokens = re.split(regex, string)

    return filter(lambda x: x not in set(["", " "]), separated_tokens)


def check_word(word):
    for key, value in tokens.items():
        if value == word:
            return key, value

    if (is_a_number(word)):
        return 26, int(word)

    return 25, word
