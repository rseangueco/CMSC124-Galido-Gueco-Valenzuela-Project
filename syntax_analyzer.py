import lexemes as l

class ParseTreeNode:
    def __init__(self, type, value, location):
        self.type = type
        self.value = value
        self.location = location
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        
    def print_tree(self, depth):
        print("type: " + self.type + 
              ", value: " + (str(self.value) if self.value is not None else "none") +
              (", children: " if self.children else ""))
        for child in self.children:
            for i in range(depth): print("\t", end = '')
            child.print_tree(depth+1)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = None
        self.index = -1
        self.symbol_table = {}  # dictionary to store variables and their values
        self.line = 1
        self.token_in_line = 1
        
        self.advance()
        
    # Increments token index
    def advance(self):
        self.index += 1
        self.current = self.tokens[self.index] if self.index < len(self.tokens) else None
    
    # adds the current token to a node as a child
    def add_current(self, node):
        type = self.current[1]
        value = self.current[0]
        node.add_child(ParseTreeNode(type, value, (str(self.line)+":"+str(self.token_in_line))))
        self.advance()
    
    # Stores the current token to add it to a new node as a child
    def store_current(self):
        type = self.current[1]
        value = self.current[0]
        self.advance()
        return ParseTreeNode(type, value, (str(self.line)+":"+str(self.token_in_line)))
    
    # Catches comments and linebreaks
    def next_token(self, node):
        while self.current and self.current[0] in ['BTW', 'OBTW', 'linebreak']:
            self.line += 1
            self.token_in_line = 1
            if self.current and self.current[0] in ['BTW', 'OBTW']:
                node.add_child(self.comment())
            elif self.current and self.current[0] == 'linebreak':
                self.advance()
                # uncomment to show linebreaks in parse tree
                # self.add_current(node)
        self.token_in_line += 1
        
    # Parses to the next token that is not a comment or line break
    def find_by_name(self, node, name, required):
        self.next_token(node)
        if self.current and (self.current[0] in list(name) or self.current[0] == name):
            return True
        else:
            if required:
                #print("Unexpected token: " + self.current[0] + "'." + 
                #      (" Expected '" + str(name) + "' " + str(self.index)))
                raise SyntaxError(str(self.line) + ":" + str(self.token_in_line) + " Unexpected token: '" + self.current[0] + "'." + 
                    (" Expected '" + str(name) + "'" if str(name) != None else None) )
            return False
        
        
    def find_by_type(self, node, type, required):
        self.next_token(node)
        if self.current and (self.current[1] in list(type) or self.current[1] == type):
            return True
        else:
            if required:
                #print("Unexpected token: " + self.current[0] + "'." + 
                #      (" Expected '" + str(type) + "' " + str(self.index)))
                raise SyntaxError(str(self.line) + ":" + str(self.token_in_line) + " Unexpected token: '" + self.current[0] + "'." + 
                    (" Expected '" + str(type) + "'" if str(type) != None else None) )
            return False
           
           
    def comment(self):
        node = ParseTreeNode('COMMENT', None, None)
        self.add_current(node)
        while self.current and self.current[1] == 'COMMENT': self.add_current(node)
        while self.current and self.current[0] == 'TLDR': self.add_current(node)

        return node
    
    
    def parse(self):
        return self.program()

    #start of parsing
    def program(self):
        node = ParseTreeNode('PROGRAM', None, None)
        if self.find_by_name(node, 'HAI', True): self.add_current(node)
        if self.find_by_name(node, 'WAZZUP', False):
            node.add_child(self.var_section())
        while self.find_by_name(node, 'HOW IZ I', False): node.add_child(self.func_decl_stmt())
        node.add_child(self.code_section())
        if self.find_by_name(node, 'KTHXBYE', True): self.add_current(node)
            
        return node
    
    #variable section: WAZZUP <var_decl>* BUHBYE
    def var_section(self):
        node = ParseTreeNode('VAR_SECTION', None, None)
        self.add_current(node) # WAZZUP
        while self.find_by_name(node, 'I HAS A', False):
            node.add_child(self.var_decl())
        if self.find_by_name(node, 'BUHBYE', True): self.add_current(node)
            
        return node
    
    #variable declaration: I HAS A identifier ITZ <expr>
    def var_decl(self):
        node = ParseTreeNode('VAR_DECL', None, None)
        self.add_current(node) # I HAS A
        if self.find_by_type(node, 'IDENTIFIER', True): self.add_current(node)
        if self.find_by_name(node, 'ITZ', False): 
            self.add_current(node)
            node.add_child(self.expr())
            
        return node
    
    #code section: statement
    def code_section(self):
        node = ParseTreeNode('CODE_SECTION', None, None)
        while (self.find_by_name(node, l.STMT_KEYWORDS, False) or 
               self.find_by_type(node, 'IDENTIFIER', False) or
               self.find_by_name(node, l.EXPR_KEYWORDS, False)): 
            node.add_child(self.stmt())
        
        return node

    #expressions: specifies expressions
    def expr(self):
        node = ParseTreeNode('EXPRESSION', None, None)
        #standalone identifiers and [DATA TYPES] is checked here
        if self.find_by_type(node, 'IDENTIFIER', False): self.add_current(node)
        elif self.find_by_type(node, l.DATA_TYPES, False): self.add_current(node)
        elif self.find_by_name(node, l.BIN_EXPR_KEYWORDS, False): node.add_child(self.bin_expr())
        elif self.find_by_name(node, l.INF_EXPR_KEYWORDS, False): node.add_child(self.inf_expr())
        elif self.find_by_name(node, "SMOOSH", False): node.add_child(self.concat_expr())
        elif self.find_by_name(node, "MAEK", False): node.add_child(self.type_expr())
        # NOT <expr>
        elif self.find_by_name(node, "NOT", False):
            self.add_current(node)
            node.add_child(self.expr())
        elif self.find_by_name(node, "I IZ", False):
            node.add_child(self.func_call_expr())
        else:
            raise SyntaxError(str(self.line) + ":" + str(self.token_in_line) + " Invalid Expression: " + self.current[0])
        
        return node
    
    #binary expression: [BINARY EXPRESSION KEYWORDS] <expr> AN <expr>
    def bin_expr(self):
        node = ParseTreeNode('BIN_EXPR', None, None)
        self.add_current(node)
        node.add_child(self.expr())
        if self.find_by_name(node, 'AN', True):
            self.add_current(node)
            node.add_child(self.expr())
        
        return node
    
    #infinite expression: [INF EXPRESSION KEYWORDS] <expr> (AN <expr>)+ MKAY
    def inf_expr(self):
        node = ParseTreeNode('INF_EXPR', None, None)
        self.add_current(node)
        node.add_child(self.expr())
        while self.find_by_name(node, 'AN', False):
            self.add_current(node)
            node.add_child(self.expr())
        if self.find_by_name(node, 'MKAY', True): self.add_current(node)
        
        return node
    
    #concat expression: SMOOSH <expr> (AN <expr>)+
    def concat_expr(self):
        node = ParseTreeNode('CONCAT_EXPR', None, None)
        self.add_current(node)
        node.add_child(self.expr())
        while self.find_by_name(node, 'AN', False):
            self.add_current(node)
            node.add_child(self.expr())
        
        return node
    
    #type expression: MAEK <expr> [DATA TYPES]
    def type_expr(self):
        node = ParseTreeNode('TYPE_EXPR', None, None)
        self.add_current(node)
        node.add_child(self.expr())
        if self.find_by_type(node, l.DATA_TYPES, True): self.add_current(node)
        
        return node
    
    #statements: [statement | expression]*
    def stmt(self):
        node = ParseTreeNode('STATEMENT', None, None)
        if self.find_by_name(node, 'VISIBLE', False): node.add_child(self.print_stmt())
        elif self.find_by_name(node, 'GIMMEH', False): node.add_child(self.input_stmt())
        elif self.find_by_type(node, 'IDENTIFIER', False): 
            identifier = self.store_current() # Store identifier before advancing
            # cases where an identifier is followed by assignment, type cast or switch statement
            if self.find_by_name(node, 'R', False): node.add_child(self.assign_stmt(identifier))
            elif self.find_by_name(node, 'IS NOW A', False): node.add_child(self.type_stmt(identifier))
            elif self.find_by_name(node, 'WTF?', False): node.add_child(self.switch_stmt(identifier))
        elif self.find_by_name(node, l.EXPR_KEYWORDS, False): 
            node.add_child(self.expr())
            # cases where expression is followed by an if-statement or switch statment
            if self.find_by_name(node, 'O RLY?', False):
                node.add_child(self.if_stmt())
            elif self.find_by_name(node, 'WTF?', False): node.add_child(self.switch_stmt())
        elif self.find_by_name(node, 'IM IN YR', False): node.add_child(self.loop_stmt())
        elif self.find_by_name(node, 'FOUND YR', False):
            node.add_child(self.return_stmt())
        elif self.find_by_name(node, 'GTFO', False):
            node.add_child(self.return_stmt())
        else:
            raise SyntaxError(str(self.line) + ":" + str(self.token_in_line) + " Invalid Statement: " + self.current[0])
        
        return node
    
    #print statement: VISIBLE <expr>
    def print_stmt(self):
        node = ParseTreeNode('PRINT_STMT', None, None)

        self.add_current(node)
        node.add_child(self.expr())
        # catch concatenation (+ <expr>)*
        while self.find_by_name(node, '+', False):
            self.add_current(node)
            node.add_child(self.expr())
        
        return node
    
    #input statement: GIMMEH identifier
    def input_stmt(self):
        node = ParseTreeNode('INPUT_STMT', None, None)
        self.add_current(node)
        if self.find_by_type(node, 'IDENTIFIER', True): self.add_current(node)
        
        return node
    
    #assignment statement: identifier R <expr>
    def assign_stmt(self, identifier):
        node = ParseTreeNode('ASSIGN_STMT', None, None)
        node.add_child(identifier)
        self.add_current(node)
        node.add_child(self.expr())
        
        return node
    
    #type statement: identifier IS NOW A [DATA TYPES]
    def type_stmt(self, identifier):
        node = ParseTreeNode('TYPE_STMT', None, None)
        node.add_child(identifier)
        self.add_current(node)
        if self.find_by_type(node, l.DATA_TYPES, True): self.add_current(node)

        return node
    
    #if statement
    def if_stmt(self):
        node = ParseTreeNode('IF_STATEMENT', None, None)

        self.add_current(node) #O RLY?
        if self.find_by_name(node, 'YA RLY', True): 
            self.add_current(node) #YA RLY
            node.add_child(self.code_section())
        while self.find_by_name(node, 'MEBBE', False):
            node.add_child(self.elif_stmt()) #checks for condition expression
            node.add_child(self.code_section()) #body
        if self.find_by_name(node, 'NO WAI', False):
            self.add_current(node)
            node.add_child(self.code_section()) #body
        if self.find_by_name(node, 'OIC', True): self.add_current(node)
        
        return node
    
    #MEBBE condition
    def elif_stmt(self):
        node = ParseTreeNode('ELIF_STATEMENT', None, None)
        self.add_current(node)
        node.add_child(self.expr())

        return node
    
    #switch statement
    def switch_stmt(self, identifier):
        node = ParseTreeNode('SWITCH_STATEMENT', None, None)
        node.add_child(ParseTreeNode('EXPRESSION', None, None))
        node.children[0].add_child(identifier)
        self.add_current(node)
        while self.find_by_name(node, 'OMG', False):
            node.add_child(self.switch_case())
            node.add_child(self.code_section())
            if self.find_by_name(node, 'GTFO', False): self.add_current(node)
        if self.find_by_name(node, 'OMGWTF', False): 
            self.add_current(node)
            node.add_child(self.code_section())
        if self.find_by_name(node, 'OIC', True): self.add_current(node)
        
        return node
    
    def switch_case(self):
        node = ParseTreeNode('SWITCH_CASE', None, None)
        self.add_current(node)
        node.add_child(self.expr())
        return node
    
    #loop statement: IM IN YR identifier operation YR <expr> condition <statement> IM OUTTA YR
    def loop_stmt(self):
        node = ParseTreeNode('LOOP_STMT', None, None)
        self.add_current(node)
        if self.find_by_type(node, 'IDENTIFIER', True): self.add_current(node)
        if self.find_by_name(node, ['UPPIN','NERFIN'], True): self.add_current(node) #operation
        if self.find_by_name(node, 'YR', True): self.add_current(node)
        node.add_child(self.expr())
        if self.find_by_name(node, ['TIL','WILE'], True): self.add_current(node) #condition
        node.add_child(self.expr())
        node.add_child(self.code_section()) #body
        if self.find_by_name(node, 'IM OUTTA YR', True): self.add_current(node)
        
        return node
    
    #function declaration: HOW IZ I identifier <parameter> <statement> IF YOU SAY SO
    def func_decl_stmt(self):
        node = ParseTreeNode('FUNC_DECL_STMT', None, None)
        self.add_current(node)
        if self.find_by_type(node, 'IDENTIFIER', True): self.add_current(node)
        if self.find_by_name(node, 'YR', False): node.add_child(self.parameter())
        node.add_child(self.code_section())
        if self.find_by_name(node, 'IF U SAY SO', True): self.add_current(node)
        
        return node
    
    #function call: I IZ identifier YR <expr> (AN <expr>)*
    def func_call_expr(self):
        node = ParseTreeNode('FUNC_CALL_STMT', None, None)
        self.add_current(node)
        if self.find_by_type(node, 'IDENTIFIER', True): self.add_current(node)
        if self.find_by_name(node, 'YR', False): 
            self.add_current(node)
            node.add_child(self.expr())
        while self.find_by_name(node, 'AN', False): 
            self.add_current(node)
            if self.find_by_name(node, 'YR', True): self.add_current(node)
            node.add_child(self.expr())
        
        return node
        
    #function return statement: GTFO | FOUND YR <expr>
    def return_stmt(self):
        node = ParseTreeNode('RETURN_STMT', None, None)
        if self.find_by_name(node, 'GTFO', False): self.add_current(node) #GTFO
        else: #FOUND YR
            self.add_current(node)
            node.add_child(self.expr())
        
        return node
    
    #function parameter: YR identifier (AN YR identifier)*
    def parameter(self):
        node = ParseTreeNode('PARAMETER', None, None)
        self.add_current(node)
        if self.find_by_type(node, 'IDENTIFIER', True): self.add_current(node)
        while self.find_by_name(node, 'AN', False): 
            self.add_current(node)
            if self.find_by_name(node, 'YR', True): self.add_current(node)
            if self.find_by_type(node, 'IDENTIFIER', True): self.add_current(node)
            
        return node