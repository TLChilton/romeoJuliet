import requests, colorama
colorama.init()
from pathlib import Path
res = requests.get('https://automatetheboringstuff.com/files/rj.txt')
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))
i = 0

# Beginning Minu
print("Welcome to Romeo and Juliet")
print("\033[093m0: Start from the beginning")
print("1: Start at a bookmark")
print("Please enter a selection: \033[0m", end='')
sel = input()

# Input validation
while sel != '1' and sel != '0':
    print("ERROR: Incorrect input detected")
    print("\033[093m0: Start from the beginning")
    print("1: Start at a bookmark")
    print("Please enter a selection: \033[0m", end='')
    sel = input()

# Bookmark Handler
if sel == '1':
    filePath = Path.cwd() / 'bookmark.txt'
    if filePath.exists():
        bookMarkFile = open(filePath, 'r')
        i = int(bookMarkFile.read())
        if (i < len(res.text) - 1):
            print("\033[092mStarting from position %s out of %s\033[0m" % (i, len(res.text)))
        else:
            print("ERROR: Bookmark is past length of text")
            print("\033[092mStarting from the beginning\033[0m")
    else:
        print ("It doesn't appear a bookmark exists")
        print ("\033[092mStarting from the beginning\033[0m")

# Main reading section
while(i < len(res.text) - 1):
    j = 0
    for k in range(i, len(res.text)):
        if res.text[k] == '\n':
            j += 1
        if j == 20:
            l = i
            i = k
            break
        elif k == (len(res.text) - 1):
            l = i
            i = k
    print(res.text[l:i])
    print("\033[093mPress enter to continue or \"X\" to exit: \033[0m", end='')
    inp = input()
    # Bookmark creation and program exit
    if inp.lower() == 'x':
        print("\033[093mCreate a bookmark? (y/n): \033[0m", end='')
        inp = input()
        if inp.lower() == 'y':
            print("\033[092mCreating a bookmark at position %s out of %s in bookmark.txt\033[0m" % (l, len(res.text)))
            bookMarkFile = open(Path.cwd() / 'bookmark.txt', 'w')
            bookMarkFile.write(str(l))
            bookMarkFile.close()
        break
