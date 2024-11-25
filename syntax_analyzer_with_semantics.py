import lexemes as l

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
            
class Semantics:       
    def evaluate_value(self, value_token, symbol_table):
        if value_token[1] == 'NUMBR':
            return int(value_token[0])
        elif value_token[1] == 'NUMBAR':
            return float(value_token[0])
        elif value_token[1] == 'YARN':
            # remove quotes from string
            return value_token[0][1:-1]
        elif value_token[1] == 'TROOF':
            return value_token[0] == 'WIN'
        elif value_token[1] == 'IDENTIFIER':
            return symbol_table.get(value_token[0], 'NOOB')
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
    
    # Adds the current token to a node as a child
    def add_current(self, node):
        type = self.current[1]
        value = self.current[0]
        node.add_child(ParseTreeNode(type, value))
        self.advance()
            
    
    def next_token(self, node):
        while self.current and self.current[0] in ['BTW', 'OBTW', 'linebreak']:
            if self.current and self.current[0] in ['BTW', 'OBTW']:
                node.add_child(self.comment())
            elif self.current and self.current[0] == 'linebreak':
                self.advance()
                # uncomment to show linebreaks in parse tree
                # self.add_current(node)
        
    # Parses to the next token that is not a comment or line break
    def find_by_name(self, node, name, required):
        self.next_token(node)
        if self.current and self.current[0] in name:
            return True
        else:
            if required:
                print("Unexpected token: " + self.current[0] + "'." + 
                      (" Expected '" + str(name) + "' " + str(self.index)))
                #raise SyntaxError("Unexpected token: '" + self.current[0] + "'." + 
                #    (" Expected '" + str(name) + "'" if str(name) != None else None) )
            return False
        
        
    def find_by_type(self, node, type, required):
        self.next_token(node)
        if self.current and self.current[1] in type:
            return True
        else:
            if required:
                print("Unexpected token: " + self.current[0] + "'." + 
                      (" Expected '" + str(type) + "' " + str(self.index)))
                # raise SyntaxError("Unexpected token: '" + self.current[0] + "'." + 
                #     (" Expected '" + str(type) + "'" if str(type) != None else None) )
            return False
           
           
    def comment(self):
        node = ParseTreeNode('COMMENT', None)
        self.add_current(node)
        while self.current and self.current[1] == 'COMMENT': self.add_current(node)
        while self.current and self.current[0] == 'TLDR': self.add_current(node)

        return node
    
    
    def parse(self):
        return self.program()


    def program(self):
        node = ParseTreeNode('PROGRAM', None)
        if self.find_by_name(node, 'HAI', True): self.add_current(node)
        if self.find_by_name(node, 'WAZZUP', False):
            node.add_child(self.var_section())
        while self.find_by_name(node, 'HOW IZ I', False): node.add_child(self.func_decl_stmt())
        node.add_child(self.code_section())
        if self.find_by_name(node, 'KTHXBYE', True): self.add_current(node)
            
        return node
    
    
    def var_section(self):
        node = ParseTreeNode('VAR_SECTION', None)
        self.add_current(node)
        while self.find_by_name(node, 'I HAS A', False):
            node.add_child(self.var_decl())
        if self.find_by_name(node, 'BUHBYE', True): self.add_current(node)
            
        return node
    
    
    def var_decl(self):
        node = ParseTreeNode('VAR_DECL', None)
        self.add_current(node)
        
        var_name = None
        if self.find_by_type(node, 'IDENTIFIER', True): 
            var_name = self.current[0]
            self.add_current(node)
        if self.find_by_name(node, 'ITZ', False): 
            self.add_current(node)
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
        while (self.find_by_name(node, l.STMT_KEYWORDS, False) or 
               self.find_by_type(node, 'IDENTIFIER', False) or
               self.find_by_name(node, l.EXPR_KEYWORDS, False)): 
            node.add_child(self.stmt())
        
        return node


    def expr(self):
        node = ParseTreeNode('EXPRESSION', None)
        if self.find_by_type(node, 'IDENTIFIER', False): 
            node.value = Semantics().evaluate_value(self.current, self.symbol_table)
            self.add_current(node)
        elif self.find_by_type(node, l.DATA_TYPES, False):
            node.value = Semantics().evaluate_value(self.current, self.symbol_table)
            self.add_current(node)
        elif self.find_by_name(node, l.BIN_EXPR_KEYWORDS, False): node.add_child(self.bin_expr())
        elif self.find_by_name(node, l.INF_EXPR_KEYWORDS, False): node.add_child(self.inf_expr())
        elif self.find_by_name(node, "SMOOSH", False): node.add_child(self.concat_expr())
        elif self.find_by_name(node, "MAEK", False): node.add_child(self.type_expr())
        elif self.find_by_name(node, "NOT", False):
            self.add_current(node)
            node.add_child(self.expr())
        else:
            print("Invalid Expression: " + self.current[0])
            return
        
        return node
    
    
    def bin_expr(self):
        node = ParseTreeNode('BIN_EXPR', None)
        
        operator = self.current[0]
        self.add_current(node)
        
        operand1_node = self.expr()
        operand1 = operand1_node.value
        if operand1 is None and operand1_node.type == 'BIN_EXPR':
            operand1 = operand1_node.value  # resolve the nested expression's value
            node.add_child(operand1_node)
        
        if self.find_by_name(node, 'AN', True):
            self.add_current(node)
        
            operand2_node = self.expr()
            operand2 = operand2_node.value
            if operand2 is None and operand2_node.type == 'BIN_EXPR':
                operand2 = operand2_node.value
                node.add_child(operand2_node)
                
            #perform the operation
            node.value = Semantics().perform_operation(operator, operand1, operand2)
        
        print("Operator:", operator)
        print("Operand1:", operand1)
        print("Operand2:", operand2)
                
        return node
    

    def inf_expr(self):
        node = ParseTreeNode('INF_EXPR', None)
        self.add_current(node)
        node.add_child(self.expr())
        while self.find_by_name(node, 'AN', False):
            self.add_current(node)
            node.add_child(self.expr())
        if self.find_by_name(node, 'MKAY', True): self.add_current(node)
        
        return node
    
    
    def concat_expr(self):
        node = ParseTreeNode('CONCAT_EXPR', None)
        self.add_current(node)
        node.add_child(self.expr())
        while self.find_by_name(node, 'AN', False):
            self.add_current(node)
            node.add_child(self.expr())
        
        return node
    
    
    def type_expr(self):
        node = ParseTreeNode('TYPE_EXPR', None)
        self.add_current(node)
        node.add_child(self.expr())
        if self.find_by_type(node, l.DATA_TYPES, True): self.add_current(node)
        
        return node
    
    
    def stmt(self):
        node = ParseTreeNode('STATEMENT', None)
        if self.find_by_name(node, 'VISIBLE', False): node.add_child(self.print_stmt())
        elif self.find_by_name(node, 'GIMMEH', False): node.add_child(self.input_stmt())
        elif self.find_by_type(node, 'IDENTIFIER', False): 
            self.add_current(node)
            if self.find_by_name(node, 'R', False): node.add_child(self.assign_stmt())
            elif self.find_by_name(node, 'IS NOW A', False): node.add_child(self.type_stmt())
            elif self.find_by_name(node, 'WTF?', False): node.add_child(self.switch_stmt())
        elif self.find_by_name(node, l.EXPR_KEYWORDS, False): 
            node.add_child(self.expr())
            if self.find_by_name(node, 'O RLY?', False): node.add_child(self.if_stmt())
            elif self.find_by_name(node, 'WTF?', False): node.add_child(self.switch_stmt())
        elif self.find_by_name(node, 'IM IN YR', False): node.add_child(self.loop_stmt())
        elif self.find_by_name(node, "I IZ", False):
            node.add_child(self.func_call_stmt())
        elif self.find_by_name(node, 'FOUND YR', False):
            node.add_child(self.return_stmt())
        elif self.find_by_name(node, 'GTFO', False):
            node.add_child(self.return_stmt())
        
        return node
    
    
    def print_stmt(self):
        node = ParseTreeNode('PRINT_STMT', None)

        self.add_current(node)
        node.add_child(self.expr())
        while self.find_by_name(node, '+', False):
            self.add_current(node)
            node.add_child(self.expr())
        
        return node
    
    
    def input_stmt(self):
        node = ParseTreeNode('INPUT_STMT', None)
        self.add_current(node)
        expr_node = self.expr()
        node.add_child(expr_node)
        node.value = expr_node.value
        
        return node
    
    
    def assign_stmt(self):
        node = ParseTreeNode('ASSIGN_STMT', None)
        
        self.add_current(node)
        node.add_child(self.expr())
        
        return node
    
    
    def type_stmt(self):
        node = ParseTreeNode('TYPE_STMT', None)
        self.add_current(node)
        if self.find_by_type(node, l.DATA_TYPES, True): self.add_current(node)

        return node
    

    def if_stmt(self):
        node = ParseTreeNode('IF_STATEMENT', None)
        self.add_current(node)
        if self.find_by_name(node, 'YA RLY', True): 
            self.add_current(node)
            node.add_child(self.code_section())
        while self.find_by_name(node, 'MEBBE', False):
            self.add_current(node)
            node.add_child(self.expr())
            node.add_child(self.code_section())
        if self.find_by_name(node, 'NO WAI', False):
            self.add_current(node)
            node.add_child(self.code_section())
        if self.find_by_name(node, 'OIC', True): self.add_current(node)
        
        return node 
    
    
    def switch_stmt(self):
        node = ParseTreeNode('SWITCH_STATEMENT', None)
        self.add_current(node)
        while self.find_by_name(node, 'OMG', False):
            self.add_current(node)
            node.add_child(self.expr())
            node.add_child(self.code_section())
            if self.find_by_name(node, 'GTFO', False): self.add_current(node)
        if self.find_by_name(node, 'OMGWTF', False): 
            self.add_current(node)
            node.add_child(self.code_section())
        if self.find_by_name(node, 'OIC', True): self.add_current(node)
        
        return node
    
    
    def loop_stmt(self):
        node = ParseTreeNode('LOOP_STMT', None)
        self.add_current(node)
        if self.find_by_type(node, 'IDENTIFIER', True): self.add_current(node)
        if self.find_by_name(node, ['UPPIN','NERFIN'], True): self.add_current(node)
        if self.find_by_name(node, 'YR', True): self.add_current(node)
        if self.find_by_type(node, 'IDENTIFIER', True): self.add_current(node)
        if self.find_by_name(node, ['TIL','WILE'], True): self.add_current(node)
        node.add_child(self.expr())
        node.add_child(self.code_section())
        if self.find_by_name(node, 'IM OUTTA YR', True): self.add_current(node)
        
        return node
    
    
    def func_decl_stmt(self):
        node = ParseTreeNode('FUNC_DECL_STMT', None)
        self.add_current(node)
        if self.find_by_type(node, 'IDENTIFIER', True): self.add_current(node)
        if self.find_by_name(node, 'YR', False): node.add_child(self.parameter())
        node.add_child(self.code_section())
        if self.find_by_name(node, 'IF U SAY SO', True): self.add_current(node)
        
        return node
    
    
    def func_call_stmt(self):
        node = ParseTreeNode('FUNC_CALL_STMT', None)
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
        
        
    def return_stmt(self):
        node = ParseTreeNode('RETURN_STMT', None)
        if self.find_by_name(node, 'GTFO', False): self.add_current(node)
        else:
            self.add_current(node)
            node.add_child(self.expr())
        
        return node
    
    
    def parameter(self):
        node = ParseTreeNode('PARAMETER', None)
        self.add_current(node)
        if self.find_by_type(node, 'IDENTIFIER', True): self.add_current(node)
        while self.find_by_name(node, 'AN', False): 
            self.add_current(node)
            if self.find_by_name(node, 'YR', True): node.add_child(self.parameter())
            
        return node