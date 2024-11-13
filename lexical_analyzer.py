import re
from tabulate import tabulate

keywords = ["HAI", "KTHXBYE", "WAZZUP", "BUHBYE", "BTW", "OBTW", "TLDR", "I HAS A", "ITZ", "R", "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH OF", "EITHER OF", "WON OF", "NOT", "ANY OF", "ALL OF", "BOTH SAEM", "DIFFRINT", "SMOOSH", "MAEK", "A", "IS NOW A", "VISIBLE", "GIMMEH", "O RLY?", "YA RLY", "MEBBE", "NO WAI", "OIC", "WTF?", "OMG", "OMGWTF", "IM IN YR", "UPPIN", "NERFIN", "YR", "TIL", "WILE", "IM OUTTA YR", "HOW IZ I", "GTFO", "IF U SAY SO", "FOUND YR", "I IZ", "MKAY", "AN", "+"]
NUMBR = "^-?\d+$"
NUMBAR = "^-?\d+\.\d+$"
YARN = "^\".*\"$"
TROOF = "^(WIN|FAIL)$"
TYPE = "^(NUMBR|NUMBAR|YARN|TROOF|NOOB)$"
IDENTIFIER = "^[a-zA-Z][_a-zA-Z\d]*$"
separatedkeywords = ["I", "HAS", "A", "SUM", "DIFF", "PRODUKT", "QUOSHUNT", "MOD", "BIGGR", "SMALLR", "BOTH", "ANY", "ALL", "EITHER", "WON", "OF", "SAEM", "NOW", "O", "RLY", "YA", "RLY?", "NO", "WAI", "IM", "IN", "OUTTA", "YR", "HOW", "IF", "U", "SAY", "SO", "FOUND", "IZ"]

#separates the text by characters
def extract(input):
    input = open(input, 'r')
    #create array of line string
    text = input.readlines()

    #separate each character per line
    for i in range(len(text)):
        text[i] = list(text[i])
    return text  

def tokenize(text):
    idx = 1
    tokens = []
    for line in text:
        print("line "+str(idx))
        idx +=1
        token = ""
        for i in range(len(line)):
            token += line[i]
            #ignore whitespace
            if token == " ":
                token = ""
            #ignore line after comment
            if token == "BTW" or token == "OBTW":
                print(token+": KEYWORD")
                tokens.append((token, "KEYWORD"))
                break
            #keywords
            elif token in keywords:
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    print(token+": KEYWORD")
                    tokens.append((token, "KEYWORD"))
                    token = ""
            #NUMBR literal
            elif bool(re.search(NUMBR, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    print(token+": NUMBR")
                    tokens.append((token, "NUMBR"))
                    token = ""
            #NUMBAR literal
            elif bool(re.search(NUMBAR, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    print(token+": NUMBAR")
                    tokens.append((token, "NUMBAR"))
                    token = ""
            #YARN literal
            elif bool(re.search(YARN, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    print(token+": YARN")
                    tokens.append((token, "YARN"))
                    token = ""
            #TROOF literal
            elif bool(re.search(TROOF, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    print(token+": TROOF")
                    tokens.append((token, "TROOF"))
                    token = ""
            #TYPE literal
            elif bool(re.search(TYPE, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    print(token+": TYPE")
                    tokens.append((token, "TROOF"))
                    token = ""
            #identifiers
            elif bool(re.search(IDENTIFIER, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    if token not in separatedkeywords:
                        print(token+": IDENTIFIER")
                        tokens.append((token, "IDENTIFIER"))
                        token = ""
    head = ["Lexeme", "Type"]
    return tabulate(tokens, headers=head, tablefmt="fancy_grid")
            
def lexer(input):
    text = extract(input)
    return tokenize(text)
