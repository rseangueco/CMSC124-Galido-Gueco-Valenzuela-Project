import lexical_analyzer as lexer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = None
        self.index = -1
        self.advance()
        
    def advance(self):
        self.index += 1
        self.current = self.tokens[self.index] if self.index < len(self.tokens) else None
        
    def parse(self):
        return self.program()
    
    def program(self):
        result = {'type': 'program', 'children': ['HAI', self.var_section(), self.code_section(), 'KTHXBYE']}
        return result
    
    def var_section(self):
        result = {'type': 'var_section', 'children':['WAZZUP', self.var_decl(), 'BUHBYE']}
        return result
    
    def var_decl(self):
        result = {}
        return result
    
    def code_section(self):
        result = {'type':'code_section', 'children':[]}
        return result