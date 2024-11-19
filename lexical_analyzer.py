import re
from tabulate import tabulate
import syntax_analyzer as parser
import lexemes as l

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
        #print("line "+str(idx))
        idx +=1
        token = ""
        for i in range(len(line)):
            token += line[i]
            #ignore whitespace
            if token == " " or token == "\t":
                token = ""
            #ignore line after comment
            if token == "BTW" or token == "OBTW":
                #print(token+": KEYWORD")
                tokens.append((token, "KEYWORD"))
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
