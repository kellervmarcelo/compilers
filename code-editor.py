from word_checker import checkWord

f = open("test.txt")

for line in f:
    for word in line.split():
        checkWord(word)

f.close()

