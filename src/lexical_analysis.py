import re
from src.tokens import Token, tokens, separators
from src.utils import is_a_number


def lexical_analysis(code):
    foundTokens = []

    comments_regex = re.compile(r"\(\*.*?\*\)", re.S)

    while True:
        match = re.search(comments_regex, code)
        if match == None:
            break

        new_comment = re.sub(r'[^\n]', '', match.group(0))
        code = code[:match.start()] + new_comment + code[match.end():]

    for idx, line in enumerate(code.split("\n")):
        for token in separate_tokens(line):
            checked_word = check_word(token)
            if checked_word is not None:
                foundTokens.append(
                    Token(checked_word[1], checked_word[0], idx + 1))

    return foundTokens


def separate_tokens(string):
    separator_regex = r'(\'.*\'|\ |\t|\n|\*|(?<![0-9])-[0-9]*|%s)' % ("|".join(
        "\\" + "\\".join(list(s)) for s in separators))

    separated_tokens = re.split(separator_regex, string)

    return filter(lambda x: x not in set(["", " ", "\t", "\n"]),
                  separated_tokens)


def check_word(word):
    for key, value in tokens.items():
        if value.casefold() == word.casefold():
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

    if (re.fullmatch(r'\(\*.*\*\)', word)):
        # Comment
        return

    if (re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_]{0,29}', word)):
        return 25, word

    if (re.fullmatch(r"End\.", word, re.IGNORECASE)):
        return 7, 'End'

    return -1, 'INVALID TOKEN: ' + word
