import re
from tabulate import tabulate
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
        idx +=1
        token = ""
        for i in range(len(line)):
            char = line[i]
            token += char
            #ignore whitespace
            if token == " " or token == "\t":
                token = ""
            #handle multi-line comments
            if in_multiline_comment:
                if token.strip() == "TLDR":
                    in_multiline_comment = False
                    tokens.append((multiline_comment.strip(), "COMMENT"))
                    multiline_comment = ""
                    tokens.append((token.strip(), "KEYWORD"))
                    break
                else:
                    multiline_comment += char
                    continue
            #single-line comments
            if token.strip() == "BTW":
                tokens.append((token.strip(), "KEYWORD"))
                comment = "".join(line[i + 1:]).strip()
                tokens.append((comment, "COMMENT"))
                break
            #multi-line comments start
            if token.strip() == "OBTW":
                tokens.append((token.strip(), "KEYWORD"))
                in_multiline_comment = True
                multiline_comment = ""
                break
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
    
    return tokens

def format_tokens(tokens):
    return tabulate(tokens, headers=["Lexeme", "Type"], tablefmt="fancy_grid")
            
def lexer(input):
    text = extract(input)
    tokens = tokenize(text)
    formatted_output = format_tokens(tokens)
    return tokens, formatted_output