import lexemes as l
from tkinter import simpledialog

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
            if value_token[0] not in symbol_table:
                raise NameError(f"Undeclared variable: {value_token[0]}.")
            else:
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
    
    def all_of(self, operands):
        for operand in operands:
            if not bool(operand):
                return False
        return True

    def any_of(self, operands):
        for operand in operands:
            if bool(operand):
                return True
        return False
    
    def print_visible(self, expr_nodes):
        output = []
        for node in expr_nodes:
            value = node.value  

            if value is None:
                output.append("NOOB")  
            elif isinstance(value, bool):
                output.append("WIN" if value else "FAIL")  
            elif isinstance(value, (int, float)):
                output.append(str(value))
            elif isinstance(value, str):
                output.append(value)
            else:
                output.append(f"UNKNOWN({value})")

        return " ".join(output)
    
    def gimmeh(self, variable_name, symbol_table, terminal_output):
        terminal_output += f"Enter value for {variable_name}:\n"

        user_input = input(f"Enter value for {variable_name}: ").strip()

        if variable_name in symbol_table:
            var_type = type(symbol_table[variable_name])
            try:
                if var_type == int:
                    symbol_table[variable_name] = int(user_input)
                elif var_type == float:
                    symbol_table[variable_name] = float(user_input)
                else: 
                    symbol_table[variable_name] = user_input
                terminal_output += f"{variable_name} set to {symbol_table[variable_name]}\n"
            except ValueError:
                terminal_output += f"Error: Invalid value for {variable_name}.\n"
        else:
            terminal_output += f"Error: {variable_name} not found in symbol table.\n"
        return terminal_output  



class Parser:
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = None
        self.index = -1
        self.symbol_table = {}  # dictionary to store variables and their values
        self.terminal_output = ""

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
        else: 
            raise SyntaxError("Identifier not foud")
        
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
            Semantics().evaluate_value(self.current, self.symbol_table)
            node.add_child(self.stmt())
        
        return node


    def expr(self):
        node = ParseTreeNode('EXPRESSION', None)
        if self.find_by_type(node, 'IDENTIFIER', False): 
            value = Semantics().evaluate_value(self.current, self.symbol_table)
            node.value = value
            self.add_current(node)
        elif self.find_by_type(node, l.DATA_TYPES, False):
            value = Semantics().evaluate_value(self.current, self.symbol_table)
            node.value = value
            self.add_current(node)
        elif self.find_by_name(node, l.BIN_EXPR_KEYWORDS, False): 
            bin_expr_node = self.bin_expr()
            node.value = bin_expr_node.value
            node.add_child(bin_expr_node)
        elif self.find_by_name(node, l.INF_EXPR_KEYWORDS, False): 
            inf_expr_node = self.inf_expr()
            node.value = inf_expr_node.value
            node.add_child(inf_expr_node)
        elif self.find_by_name(node, "SMOOSH", False): 
            concat_expr_node = self.concat_expr()
            node.value = concat_expr_node.value
            node.add_child(concat_expr_node)
        elif self.find_by_name(node, "MAEK", False): 
            type_expr_node = self.type_expr()
            node.value = type_expr_node.value
            node.add_child(type_expr_node)
        elif self.find_by_name(node, "NOT", False):
            self.add_current(node)
            
            # Evaluate the operand
            not_expr_node = self.expr()
            node.add_child(not_expr_node)

            # Apply semantics for NOT
            operand_value = not_expr_node.value
            if isinstance(operand_value, bool):
                node.value = not operand_value  # Flip boolean
            elif isinstance(operand_value, (int, float)):
                node.value = operand_value == 0  # True if operand is zero
            elif isinstance(operand_value, str):
                node.value = len(operand_value) == 0  # True if string is empty
            else:
                node.value = True  # Treat NOOB as WIN (true when negated)
            
            node.type = "TROOF"  # Result of NOT is always TROOF
        else:
            raise SyntaxError("Invalid Expression: " + self.current[0])
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
        
        return node
    

    # def inf_expr(self):
    #     node = ParseTreeNode('INF_EXPR', None)
    #     self.add_current(node)
    #     node.add_child(self.expr())
    #     while self.find_by_name(node, 'AN', False):
    #         self.add_current(node)
    #         node.add_child(self.expr())
    #     if self.find_by_name(node, 'MKAY', True): self.add_current(node)
        
    #     return node
    
    def inf_expr(self):
        node = ParseTreeNode('INF_EXPR', None)
        self.add_current(node)

        operands = [self.expr()]
        while self.find_by_name(node, 'AN', False):
            self.add_current(node)
            operands.append(self.expr())

        if self.find_by_name(node, 'ALL OF', False):
            self.add_current(node)
            node.value = Semantics().all_of(operands)
        elif self.find_by_name(node, 'ANY OF', False):
            self.add_current(node)
            node.value = Semantics().any_of(operands)
        else:
            node.value = operands[-1]  #use last operand as the value

        if self.find_by_name(node, 'MKAY', True):
            self.add_current(node)

        return node    
    
    # def concat_expr(self):
    #     node = ParseTreeNode('CONCAT_EXPR', None)
    #     self.add_current(node)
    #     node.add_child(self.expr())
    #     while self.find_by_name(node, 'AN', False):
    #         self.add_current(node)
    #         node.add_child(self.expr())
        
    #     return node
    
    def concat_expr(self):
        node = ParseTreeNode('CONCAT_EXPR', None)
        self.add_current(node)

        # collect all expressions to be concatenated
        expr_nodes = [self.expr()]
        node.add_child(expr_nodes[0])

        while self.find_by_name(node, 'AN', False):
            self.add_current(node)
            next_expr = self.expr()
            expr_nodes.append(next_expr)
            node.add_child(next_expr)

        # perform concatenation
        concatenated_result = ''.join([str(expr_node.value) for expr_node in expr_nodes])
        node.value = concatenated_result
        node.type = "YARN"  # the result of SMOOSH is always YARN (string)

        return node
    
    
    # def type_expr(self):
    #     node = ParseTreeNode('TYPE_EXPR', None)
    #     self.add_current(node)
    #     node.add_child(self.expr())
    #     if self.find_by_type(node, l.DATA_TYPES, True): self.add_current(node)
        
    #     return node
    
    
    def type_expr(self):
        node = ParseTreeNode('TYPE_EXPR', None)
        self.add_current(node)

        # expression to be cast
        expr_node = self.expr()
        node.add_child(expr_node)

        # target data type
        if self.find_by_type(node, l.DATA_TYPES, True):
            target_type = self.current[0]
            self.add_current(node)

            # perform type casting
            original_value = expr_node.value
            try:
                if target_type == "NUMBR":
                    casted_value = int(original_value)
                elif target_type == "NUMBAR":
                    casted_value = float(original_value)
                elif target_type == "YARN":
                    casted_value = str(original_value)
                elif target_type == "TROOF":
                    if isinstance(original_value, bool):
                        casted_value = original_value
                    elif isinstance(original_value, (int, float)):
                        casted_value = original_value != 0
                    elif isinstance(original_value, str):
                        casted_value = len(original_value) > 0
                    else:
                        casted_value = False
                else:
                    casted_value = "NOOB"  # unsupported type results in NOOB
            except (ValueError, TypeError):
                casted_value = "NOOB"  # conversion failed

            node.value = casted_value
            node.type = target_type
        else:
            raise SyntaxError("MAEK requires a target data type.")

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
    
    # def print_stmt(self):
    #     node = ParseTreeNode('PRINT_STMT', None)

    #     self.add_current(node)
    #     node.add_child(self.expr())
    #     while self.find_by_name(node, '+', False):
    #         self.add_current(node)
    #         node.add_child(self.expr())
        
    #     return node
    
    def print_stmt(self):
        node = ParseTreeNode('PRINT_STMT', None)

        self.add_current(node)
        expr_nodes = [self.expr()]
        node.add_child(expr_nodes[0])
        
        while self.find_by_name(node, '+', False):
            self.add_current(node)
            next_expr = self.expr()
            expr_nodes.append(next_expr)
            node.add_child(next_expr)
        
        #add printable output as the node's value
        node.value = Semantics().print_visible(expr_nodes)
        
        return node
    
    
    # def input_stmt(self):
    #     node = ParseTreeNode('INPUT_STMT', None)
    #     self.add_current(node)
    #     expr_node = self.expr()
    #     node.add_child(expr_node)
    #     node.value = expr_node.value
        
    #     return node
    
    
    def input_stmt(self):
        node = ParseTreeNode("INPUT_STMT", None)

        self.add_current(node)

        if self.current[1] == "IDENTIFIER":
            variable_name = self.current[0]
            self.add_current(node)
            Semantics().gimmeh(variable_name, self.symbol_table, self.terminal_output)
        else:
            raise SyntaxError("Expected an identifier after GIMMEH.")
        
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