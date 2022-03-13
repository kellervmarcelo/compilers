def isANumber(word):
    """Essa função avalia a palavra recebida e determina se ela é um número ou não"""
    if type(word) is int:
        return True
    else:
        try:
            int(word)
            return word
        except:
            return False