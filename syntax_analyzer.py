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

        self.advance()
        
    def advance(self):
        self.index += 1
        self.current = self.tokens[self.index] if self.index < len(self.tokens) else None
    
    def add_current(self, node):
        type = self.current[1]
        value = self.current[0]
        node.add_child(ParseTreeNode(type, value))
        self.advance()

    def evaluate_value(self, value_token):
        if value_token[1] == 'NUMBR':
            return int(value_token[0])
        elif value_token[1] == 'NUMBAR':
            return float(value_token[0])
        elif value_token[1] == 'YARN':
            #remove quotes from string
            return value_token[0][1:-1]
        elif value_token[1] == 'TROOF':
            return value_token[0] == 'WIN'
        elif value_token[1] == 'IDENTIFIER':
            return self.symbol_table.get(value_token[0], 'NOOB')
        return value_token[0]

    def perform_operation(self, operator, operand1, operand2):
        try:
            if operator == 'SUM OF':
                return operand1 + operand2
            elif operator == 'DIFF OF':
                return operand1 - operand2
            elif operator == 'PRODUKT OF':
                return operand1 * operand2
            elif operator == 'QUOSHUNT OF':
                return operand1 / operand2
            elif operator == 'MOD OF':
                return operand1 % operand2
            elif operator == 'BIGGR OF':
                return max(operand1, operand2)
            elif operator == 'SMALLR OF':
                return min(operand1, operand2)
        except Exception as e:
            return f"ERROR: {str(e)}"
        return None
    
    def parse(self):
        return self.program()


    def program(self):
        node = ParseTreeNode('PROGRAM', None)
        
        while self.current and self.current[0] != 'HAI':
            self.linebreak(node)

        self.add_current(node)

        while self.current and self.current[0] != 'WAZZUP':
            self.linebreak(node)

        node.add_child(self.var_section())
            
        node.add_child(self.code_section())
            
        while self.current and self.current[0] == 'KTHXBYE':
            self.add_current(node)
            
        return node
    
    def var_section(self):
        node = ParseTreeNode('VAR_SECTION', None)
        self.add_current(node)
        
        while self.current and self.current[0] in ['BTW', 'OBTW']:
            node.add_child(self.comment())

        # while self.current and self.current[0] == 'linebreak':
        #     self.add_current(node)

        while self.current and self.current[0] != 'BUHBYE':
            self.linebreak(node)
            if self.current and self.current[0] == 'I HAS A':
                node.add_child(self.var_decl())
            
        self.add_current(node)
        
        return node
    
    def var_decl(self):
        node = ParseTreeNode('VAR_DECL', None)

        self.add_current(node)  #consume 'I HAS A'
        
        #get variable name
        var_name = None
        if self.current and self.current[1] == 'IDENTIFIER':
            var_name = self.current[0]
            self.add_current(node)
        
        #check for initialization
        if self.current and self.current[0] == 'ITZ':
            self.add_current(node)  #consume 'ITZ'
            expr_node = self.expr()
            node.add_child(expr_node)
            
            #evaluate the expression and store in symbol table
            if var_name is not None:
                self.symbol_table[var_name] = expr_node.value
        else:
            #initialize with NOOB if no value provided
            if var_name is not None:
                self.symbol_table[var_name] = 'NOOB'
        return node
    
    def code_section(self):
        node = ParseTreeNode('CODE_SECTION', None)
        
        self.linebreak(node)
        self.add_current(node)
        
        while self.current and self.current[0] != 'KTHXBYE':
            self.linebreak(node)
            
            # for testing, this can be removed in finished implementations
            while self.current and self.current[0] in ['linebreak', 'BTW', 'OBTW']:
                self.linebreak(node)
                
            if self.current and (self.current[0] in ['VISIBLE', 'GIMMEH'] or
                                 self.current[1] == 'IDENTIFIER'):
                node.add_child(self.statement())
            else:
                print("Unexpected token: " + self.current[0] + " at index " + str(self.index))
                break
                
        return node

    def comment(self):
        node = ParseTreeNode('COMMENT', None)

        self.add_current(node)
        
        while self.current and self.current[1] == 'COMMENT':
            self.add_current(node)
        
        return node
    
    def linebreak(self, node):
        if self.current and self.current[0] in ['BTW', 'OBTW']:
            node.add_child(self.comment())
        elif self.current and self.current[0] == 'linebreak':
            self.add_current(node)

    def expr(self):
        node = ParseTreeNode('EXPRESSION', None)
        

        if self.current and (
            self.current[1] in ['IDENTIFIER', 'NUMBR', 'NUMBAR', 'YARN', 'TROOF']
        ):
            #simple expression (identifier or literal)
            node.value = self.evaluate_value(self.current)
            self.add_current(node)
        
        elif self.current and self.current[0] in [
            'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF',
            'MOD OF', 'BIGGR OF', 'SMALLR OF'
        ]:
            #operation
            operator = self.current[0]
            self.add_current(node)
            
            #get first operand
            operand1_node = self.expr()
            operand1 = operand1_node.value
            node.add_child(operand1_node)
            
            #get AN keyword
            if self.current and self.current[0] == 'AN':
                self.add_current(node)
                
                #get second operand
                operand2_node = self.expr()
                operand2 = operand2_node.value
                node.add_child(operand2_node)
                
                #perform the operation
                node.value = self.perform_operation(operator, operand1, operand2)
        if self.current and self.current[0] in ['BOTH OF', 'EITHER OF', 'WON OF']:
            self.add_current(node)
            node.add_child(self.expr())
            if self.current and self.current[0] == 'AN':
                self.add_current(node)
                node.add_child(self.expr())
        
        if self.current and self.current[0] in ['NOT']:
            self.add_current(node)
            node.add_child(self.expr())
        
        if self.current and self.current[0] in ['ALL OF', 'ANY OF']:
            self.add_current(node)
            node.add_child(self.infexpr())
            while self.current and self.current[0] not in ['MKAY']:
                if self.current and self.current[0] == 'AN':
                    self.add_current(node)
                    node.add_child(self.infexpr())
            self.add_current(node)
            
        if self.current and self.current[0] in ['SMOOSH']:
            self.add_current(node)
            node.add_child(self.concat_expr())
            
        if self.current and self.current[0] in ['MAEK']:
            self.add_current(node)
            node.add_child(self.type_expr())
        
        return node
    

    #for all of and any of
    def infexpr(self):
        node = ParseTreeNode('EXPRESSION', None)
        

        if self.current and (
            self.current[1] in ['IDENTIFIER', 'NUMBR', 'NUMBAR', 'YARN', 'TROOF']
        ):
            #simple expression (identifier or literal)
            node.value = self.evaluate_value(self.current)
            self.add_current(node)
        
        elif self.current and self.current[0] in [
            'SUM OF', 'DIFF OF', 'PRODUKT OF', 'QUOSHUNT OF',
            'MOD OF', 'BIGGR OF', 'SMALLR OF'
        ]:
            #operation
            operator = self.current[0]
            self.add_current(node)
            
            #get first operand
            operand1_node = self.infexpr()
            operand1 = operand1_node.value
            node.add_child(operand1_node)
            
            #get AN keyword
            if self.current and self.current[0] == 'AN':
                self.add_current(node)
                
                #get second operand
                operand2_node = self.infexpr()
                operand2 = operand2_node.value
                node.add_child(operand2_node)
                
                #perform the operation
                node.value = self.perform_operation(operator, operand1, operand2)
        if self.current and self.current[0] in ['BOTH OF', 'EITHER OF', 'WON OF']:
            self.add_current(node)
            node.add_child(self.infexpr())
            if self.current and self.current[0] == 'AN':
                self.add_current(node)
                node.add_child(self.infexpr())
        
        if self.current and self.current[0] in ['NOT']:
            self.add_current(node)
            node.add_child(self.infexpr())
        
        return node
    
    def concat_expr(self):
        node = ParseTreeNode('CONCAT', None)
        
        node.add_child(self.expr())
        
        while self.current and self.current[0] == 'AN':
            self.add_current(node)
            node.add_child(self.expr())
        
        return node
    
    def type_expr(self):
        node = ParseTreeNode('TYPE_EXPR', None)
        
        if self.current and self.current[1] == 'IDENTIFIER':
            self.add_current(node)
            
        if self.current and self.current[1] in ['NUMBR', 'NUMBAR', 'YARN', 'TROOF']:
            self.add_current(node)
            
        return node
    
    def logic_expr(self):
        node = ParseTreeNode('LOGIC_EXPR', None)
        
        
        
        return node
    
    def statement(self):
        node = ParseTreeNode('STATEMENT', None)
        
        if self.current and self.current[0] == 'VISIBLE':
            self.add_current(node)
            print_node = self.print_statement()
            node.add_child(print_node)
            #store the evaluated expression value
            node.value = print_node.value
            
        if self.current and self.current[0] == 'GIMMEH':
            self.add_current(node)
            input_node = self.input_statement()
            node.add_child(input_node)
            #store the evaluated expression value
            node.value = input_node.value
            
        if self.current and self.current[1] == 'IDENTIFIER':
            self.add_current(node)
            if self.current and self.current[0] == 'R':
                node.add_child(self.assignment_statement())
            if self.current and self.current[0] == 'IS NOW A':
                node.add_child(self.type_statement())
            
        return node
            
    def print_statement(self):
        node = ParseTreeNode('PRINT_STMT', None)
        
        expr_node = self.expr()
        node.add_child(expr_node)
        node.value = expr_node.value
        
        while self.current and self.current[0] == '+':
            self.add_current(node)
            expr_node = self.expr()
            node.add_child(expr_node)
            node.value = expr_node.value
        
        return node
    
    def input_statement(self):
        node = ParseTreeNode('INPUT_STMT', None)
        
        expr_node = self.expr()
        node.add_child(expr_node)
        node.value = expr_node.value
        
        return node
    
    def assignment_statement(self):
        node = ParseTreeNode('ASSIGNMENT', None)
        
        self.add_current(node)
        node.add_child(self.expr())
        
        return node
    
    def type_statement(self):
        node = ParseTreeNode('TYPE_STMT', None)
        
        self.add_current(node)
        if self.current and self.current[1] in ['NUMBR', 'NUMBAR', 'YARN', 'TROOF']:
            self.add_current(node)
        
        return node
    