from pathlib import Path
import requests
import colorama
colorama.init()

# Function for determining whether we are using a locally
#   stored book or the online book
def getBook():
    bookPath = Path.cwd() / 'romeoJuliet.txt'
    if bookPath.exists():
        print("Using locally stored book")
        bookFile = open(bookPath, 'r')
        book = bookFile.read()
        bookFile.close()
    else:
        print("Using online book")
        res = requests.get('https://automatetheboringstuff.com/files/rj.txt')
        res.raise_for_status()
        book = res.text
    return book

# Handles input for the beginning menu
def menu(flag):
    print("\033[093m1: Start from the beginning")
    print("2: Start at a bookmark")
    if (flag == 0): # Special case for if book has already been saved
        print("3: Save book locally")
    print("0: Exit")
    print("Please enter a selection: \033[0m", end='')
    sel = input()

    # Input validation
    if sel != '1' and sel != '2' and sel != '3' and sel != '0':
        print("\033[091mERROR: \033[0mIncorrect input detected")
        sel = menu(flag)
    elif sel == '3' and flag == 1: # Special case for if book has already been saved
        print("\033[091mERROR: \033[0mIncorrect input detected")
        sel = menu(flag)
    return sel


# Beginning Menu
print("\033[091mWelcome to Romeo and Juliet")
sel = menu(0)

# Download handler
if sel == '3':
    bookPath = Path.cwd() / 'romeoJuliet.txt'
    if bookPath.exists():
        print("\033[091mERROR: \033[0mromeoJuliet.txt already exists")
    else:
        res = requests.get('https://automatetheboringstuff.com/files/rj.txt')
        res.raise_for_status()
        bookFile = open('romeoJuliet.txt', 'wb')
        for chunk in res.iter_content(100000):
            bookFile.write(chunk)
        print("Book saved as romeoJuliet.txt")
    sel = menu(1)

# If sel == '0' quit program
if sel != '0':
    book = getBook()
    # Default is that our starting position is at the beginning
    i = 0
    # Bookmark Handler
    if sel == '2':
        filePath = Path.cwd() / 'bookmark.txt'
        if filePath.exists():
            bookMarkFile = open(filePath, 'r')
            i = int(bookMarkFile.read())
            if (i < len(book) - 1):
                print("\033[092mStarting from position %s out of %s\033[0m" %
                    (i, len(book)))
            else:
                print("\033[091mERROR: \033[0mBookmark is past length of text")
                print("\033[092mStarting from the beginning\033[0m")
                i = 0
        else:
            print("\033[091mERROR: \033[0mIt doesn't appear a bookmark exists")
            print("\033[092mStarting from the beginning\033[0m")

    # Main reading section
    inp = ''
    while inp.lower() != 'x':
        j = 0
        for k in range(i, len(book)):
            if book[k] == '\n':
                j += 1
            if j == 20:
                l = i
                i = k
                break
            elif k == (len(book) - 1):
                l = i
                i = k
        print ("\033[092mPosition %s out of %s\033[0m" % (l, len(book)))
        print(book[l:i])
        print("\033[093mPress enter to continue, \"B\" to go back a passage, or \"X\" to exit: \033[0m", end='')
        inp = input()

        # Error handler for end of text
        while i == len(book) - 1 and inp.lower() != 'x' and inp.lower() != 'b':
            print('\033[091mERROR: \033[0mYou are at the end')
            print("\033[093mEnter \"B\" to go back a passage, or \"X\" to exit: \033[0m", end='')
            inp = input()

        # Going backwards
        if inp.lower() == 'b':
            i = l
            while i == 0 and inp.lower() == 'b':
                print('\033[091mERROR: \033[0mYou are at the beginning')
                print("\033[093mPress enter to continue or \"X\" to exit: \033[0m", end='')
                inp = input()
            if i > 0:
                i = l
                j = 0
                for k in range(i, 0, -1):
                    if book[k] == '\n':
                        j += 1
                    if j == 20:
                        i = k
                        break
                    elif k == 1:
                        i = 0

        # Bookmark creation and program exit
        if inp.lower() == 'x':
            print("\033[093mCreate a bookmark? (y/n): \033[0m", end='')
            inp = input()
            if inp.lower() == 'y':
                print("\033[092mCreating a bookmark at position %s out of %s in bookmark.txt\033[0m" % (
                    l, len(book)))
                bookMarkFile = open(Path.cwd() / 'bookmark.txt', 'w')
                bookMarkFile.write(str(l))
                bookMarkFile.close()
            break
