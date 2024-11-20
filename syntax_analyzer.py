import lexical_analyzer as lexer

class ParseTreeNode:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        
    def print_tree(self, depth):
        print("type: " + self.type + 
              ", value: " + (self.value if self.value else "none") + 
              (", children: " if self.children else ""))
        for child in self.children:
            for i in range(depth): print("\t", end = '')
            child.print_tree(depth+1)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = None
        self.index = -1
        self.advance()
        
    def advance(self):
        self.index += 1
        self.current = self.tokens[self.index] if self.index < len(self.tokens) else None
    
    def add_current(self,node):
        type = self.current[1]
        value = self.current[0]
        node.add_child( ParseTreeNode(type, value))
        self.advance()
        
    def parse(self):
        return self.program()
    
    def program(self):
        node = ParseTreeNode('PROGRAM', None)
        # <comment> <program>
        while self.current and self.current[0] == 'BTW' or self.current[0] == 'OBTW':
            node.add_child(self.comment())
            
        # HAI <var_section> <code_section> KTHXBYE
        while self.current and self.current[0] == 'HAI':
            self.add_current(node)
            
        while self.current and self.current[0] == 'WAZZUP':
            node.add_child(self.var_section())
            
        node.add_child(self.code_section())
            
        while self.current and self.current[0] == 'KTHXBYE':
            self.add_current(node)
            
        # <program> <comment>
        return node
    
    def var_section(self):
        node = ParseTreeNode('VAR_SECTION', None)
        self.add_current(node)
        
        # comment
        while self.current and self.current[0] == 'BTW' or self.current[0] == 'OBTW':
            node.add_child(self.comment())
            
        # var_decl
        while self.current and self.current[0] == 'I HAS A':
            node.add_child(self.var_decl())
            
        while self.current and self.current[0] == 'BUHBYE':
            self.add_current(node)
        
        return node
    
    def var_decl(self):
        node = ParseTreeNode('VAR_DECL', None)
        self.add_current(node)
        
        while self.current and self.current[1] == 'IDENTIFIER':
            self.add_current(node)
            
        while self.current and self.current[0] == 'ITZ':
            self.add_current(node)
            node.add_child(self.expr())
        
        while self.current and self.current[0] == 'BTW' or self.current[0] == 'OBTW':
            node.add_child(self.comment())
        
        return node
    
    def code_section(self):
        node = ParseTreeNode('CODE_SECTION', None)
        
        while self.current and self.current[0] == 'BTW' or self.current[0] == 'OBTW':
            node.add_child(self.comment())
            
        # this should eventually have all keywords that can start a statement
        while self.current and self.current[0] == 'VISIBLE':
            node.add_child(self.statement())
            
        return node
    
    def comment(self):
        node = ParseTreeNode('COMMENT', None)
        
        self.add_current(node)
        
        while self.current and self.current[1] == 'COMMENT':
            self.add_current(node)
            
        return node
    
    def expr(self):
        node = ParseTreeNode('EXPRESSION', None)
        
        # identifier or literal
        while self.current and (
        self.current[1] == 'IDENTIFIER' or
        self.current[1] == 'NUMBR' or
        self.current[1] == 'NUMBAR' or
        self.current[1] == 'YARN' or
        self.current[1] == 'TROOF' ):
            self.add_current(node)
        
        # operation
        while self.current and (
        self.current[0] == 'SUM OF' or
        self.current[0] == 'DIFF OF' or
        self.current[0] == 'PRODUKT OF' or
        self.current[0] == 'QUOSHUNT OF' or
        self.current[0] == 'MOD OF' or
        self.current[0] == 'BIGGR OF' or
        self.current[0] == 'SMALLR OF'):
            self.add_current(node)
            node.add_child(self.arith_expr())
        
        return node
    
    def arith_expr(self):
        node = ParseTreeNode('ARITH_EXPR', None)
        
        node.add_child(self.expr())
        
        while self.current and self.current[0] == 'AN':
            self.add_current(node)
            node.add_child(self.expr())
            
        return node
    
    def statement(self):
        node = ParseTreeNode('STATEMENT', None)
        
        while self.current and self.current[0] == 'VISIBLE':
            self.add_current(node)
            node.add_child(self.print_statement())
            
        while self.current and self.current[0] == 'BTW' or self.current[0] == 'OBTW':
            node.add_child(self.comment())
            
        return node
        
    def print_statement(self):
        node = ParseTreeNode('PRINT_STMT', None)
        
        node.add_child(self.expr())
        
        return node