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

#tokenize input
def tokenize(text):
    idx = 1
    tokens = []
    token = ""
    in_multiline_comment = False
    multiline_comment = ""

    for line in text:
        idx +=1
        token = ""
        for i in range(len(line)):
            char = line[i]
            token += char
            #handle multi-line comments
            if in_multiline_comment:
                if token.strip() == "TLDR":
                    in_multiline_comment = False
                    tokens.append((multiline_comment.strip()[:-3], "COMMENT"))
                    multiline_comment = ""
                    tokens.append((token.strip(), "KEYWORD"))
                    break
                else:
                    multiline_comment += char
                    continue
            #ignore whitespace
            elif token == " " or token == "\t":
                token = ""
            elif token == "\n":
                tokens.append(("linebreak", "LINEBREAK"))
            #single-line comments
            elif token.strip() == "BTW":
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    tokens.append((token.strip(), "KEYWORD"))
                    comment = "".join(line[i + 1:]).strip()
                    tokens.append((comment, "COMMENT"))
                    break
            #multi-line comments start
            elif token.strip() == "OBTW":
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    tokens.append((token.strip(), "KEYWORD"))
                    in_multiline_comment = True
                    multiline_comment = ""
            #keywords
            elif token in l.keywords:
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    tokens.append((token, "KEYWORD"))
                    token = ""
            #NUMBR literal
            elif bool(re.search(l.NUMBR, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    tokens.append((token, "NUMBR"))
                    token = ""
            #NUMBAR literal
            elif bool(re.search(l.NUMBAR, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    tokens.append((token, "NUMBAR"))
                    token = ""
            #YARN literal
            elif bool(re.search(l.YARN, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    tokens.append((token, "YARN"))
                    token = ""
            #TROOF literal
            elif bool(re.search(l.TROOF, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    tokens.append((token, "TROOF"))
                    token = ""
            #TYPE literal
            elif bool(re.search(l.TYPE, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    tokens.append((token, "TROOF"))
                    token = ""
            #identifiers
            elif bool(re.search(l.IDENTIFIER, token)):
                if i == len(line)-1 or line[i+1] == " " or line[i+1] == "\n":
                    if token not in l.separatedkeywords:
                        tokens.append((token, "IDENTIFIER"))
                        token = ""
                    else:
                        startIndex = -1
                        tempLine = ''.join(line)
                        for j in l.keywords:
                            startIndex = tempLine.find(j)
                            if startIndex == tempLine.find(token):
                                break
                        if startIndex != tempLine.find(token):
                            tokens.append((token, 'IDENTIFIER'))
                            token = ""       
    print(tabulate(tokens, headers=["Lexeme", "Type"], tablefmt="fancy_grid"))
    return tokens

def format_tokens(tokens):
        # debug code
    p = parser.Parser(tokens)
    print(p.parse().print_tree(1))
    
    return tabulate(tokens, headers=["Lexeme", "Type"], tablefmt="fancy_grid")
            
def lexer(input):
    text = extract(input)
    tokens = tokenize(text)
    formatted_output = format_tokens(tokens)
    return tokens, formatted_output