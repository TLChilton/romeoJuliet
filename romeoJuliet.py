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


# Beginning Menu
print("\033[091mWelcome to Romeo and Juliet")
print("\033[093m0: Start from the beginning")
print("1: Start at a bookmark")
print("2: Save book locally")
print("3: Exit")
print("Please enter a selection: \033[0m", end='')
sel = input()

# Input validation
while sel != '0' and sel != '1' and sel != '2' and sel != '3':
    print("\033[091mERROR: \033[0mIncorrect input detected")
    print("\033[093m0: Start from the beginning")
    print("1: Start at a bookmark")
    print("2: Save book locally")
    print("3: Exit")
    print("Please enter a selection: \033[0m", end='')
    sel = input()

# Download handler
if sel == '2':
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
    print("\033[093m0: Start from the beginning")
    print("1: Start at a bookmark")
    print("3: Exit")
    print("Please enter a selection: \033[0m", end='')
    sel = input()
    while sel != '0' and sel != '1' and sel != '3':
        print("\033[091mERROR: \033[0mIncorrect input detected")
        print("\033[093m0: Start from the beginning")
        print("1: Start at a bookmark")
        print("3: Exit")
        print("Please enter a selection: \033[0m", end='')
        sel = input()

if sel != '3':
    book = getBook()
    # Default is that our starting position is at the beginning
    i = 0
    # Bookmark Handler
    if sel == '1':
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
    while(i < len(book) - 1):
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
        print(book[l:i])
        print("\033[093mPress enter to continue or \"X\" to exit: \033[0m", end='')
        inp = input()
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
