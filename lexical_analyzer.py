import re
from tabulate import tabulate
import syntax_analyzer as parser
import lexemes as l

#separates the text by characters
def extract(input):
    with open(input, 'r') as file:
        text = file.readlines()

    for i in range(len(text)):
        text[i] = list(text[i])
    return text

# Tokenize input
def tokenize(text):
    idx = 1
    tokens = []
    token = ""
    in_multiline_comment = False
    multiline_comment = ""

    for line in text:
        #print("line "+str(idx))
        idx +=1
        token = ""
        for i in range(len(line)):
            char = line[i]
            token += char
            #ignore whitespace
            if token == " " or token == "\t":
                token = ""
<<<<<<< HEAD
            #handle multi-line comments
            if in_multiline_comment:
                if token.strip() == "TLDR":
                    in_multiline_comment = False
                    print(multiline_comment.strip() + ": COMMENT")
                    tokens.append((multiline_comment.strip(), "COMMENT"))
                    multiline_comment = ""
                    print(token.strip() + ": KEYWORD")
                    tokens.append((token.strip(), "KEYWORD"))
                    break
                else:
                    multiline_comment += char
                    continue
            #single-line comments
            if token.strip() == "BTW":
                print(token.strip() + ": KEYWORD")
                tokens.append((token.strip(), "KEYWORD"))
                comment = "".join(line[i + 1:]).strip()
                print(comment + ": COMMENT")
                tokens.append((comment, "COMMENT"))
                break
            #multi-line comments start
            if token.strip() == "OBTW":
                print(token.strip() + ": KEYWORD")
                tokens.append((token.strip(), "KEYWORD"))
                in_multiline_comment = True
                multiline_comment = ""
=======
            #ignore line after comment
            if token == "BTW" or token == "OBTW":
                #print(token+": KEYWORD")
                tokens.append((token, "KEYWORD"))
>>>>>>> 2300d12 (feat: added syntax_analyzer, moved lexemes)
                break
            #keywords
            elif token in l.keywords:
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    #print(token+": KEYWORD")
                    tokens.append((token, token))
                    token = ""
            #NUMBR literal
            elif bool(re.search(l.NUMBR, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    #print(token+": NUMBR")
                    tokens.append((token, "NUMBR"))
                    token = ""
            #NUMBAR literal
            elif bool(re.search(l.NUMBAR, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    #print(token+": NUMBAR")
                    tokens.append((token, "NUMBAR"))
                    token = ""
            #YARN literal
            elif bool(re.search(l.YARN, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    #print(token+": YARN")
                    tokens.append((token, "YARN"))
                    token = ""
            #TROOF literal
            elif bool(re.search(l.TROOF, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    #print(token+": TROOF")
                    tokens.append((token, "TROOF"))
                    token = ""
            #TYPE literal
            elif bool(re.search(l.TYPE, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    #print(token+": TYPE")
                    tokens.append((token, "TROOF"))
                    token = ""
            #identifiers
            elif bool(re.search(l.IDENTIFIER, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    if token not in l.separatedkeywords:
                        #print(token+": IDENTIFIER")
                        tokens.append((token, "IDENTIFIER"))
                        token = ""
    head = ["Lexeme", "Type"]
    
    # debug code
    print(tokens)
    p = parser.Parser(tokens)
    print(p.parse())
    
    return tabulate(tokens, headers=head, tablefmt="fancy_grid")
            
def lexer(input):
    text = extract(input)
    return tokenize(text)
