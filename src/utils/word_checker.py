from is_a_number import isANumber
from is_reserved_word import isReservedWord
from is_reserved_word import tokens

output = open("output.txt", "w", encoding="utf-8")

def checkWord(word):
    numberToken = isANumber(word)
    if numberToken:
        output.write(f"{numberToken} --- {tokens.get(26)} \n")
    else:
        reservedWordToken = isReservedWord(word)
        output.write(f"{reservedWordToken[1]} --- {reservedWordToken[0]} \n")
    
