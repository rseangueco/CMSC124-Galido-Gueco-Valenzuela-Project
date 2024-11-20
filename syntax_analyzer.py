import lexical_analyzer as lexer

class ParseTreeNode:
    def __init__(self, type):
        self.type = type
        self.value = None
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        
    def print_tree(self):
        print("type: " + self.type + ", value: " + (self.value if self.value else "none") + ", children: [", end = '')
        for child in self.children:
            print("\n\t", end = '')
            child.print_tree()
        print("]", end ='')

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
        node = ParseTreeNode('PROGRAM')
        # <comment> <program>
        while self.current and self.current[0] == 'BTW' or self.current[0] == 'OBTW':
            self.advance()
            node.add_child(self.comment())
            
        # HAI <var_section> <code_section> KTHXBYE
        while self.current and self.current[0] == 'HAI':
            self.advance()
            newNode = ParseTreeNode('KEYWORD')
            newNode.value = self.current[0]
            node.add_child(newNode)
            
        while self.current and self.current[0] == 'KTHXBYE':
            self.advance()
            node.add_child(ParseTreeNode('KTHXBYE'))
            
        # <program> <comment>
        return node
    
    def var_section(self):
        result = {'type': 'var_section', 'children':['WAZZUP', self.var_decl(), 'BUHBYE']}
        return result
    
    def var_decl(self):
        result = {}
        return result
    
    def code_section(self):
        result = {'type':'code_section', 'children':[]}
        return result
    
    def comment(self):
        result = ParseTreeNode('COMMENT')
        return result