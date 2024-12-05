import syntax_analyzer
import lexemes as l

class Interpreter:  
    
    def __init__(self, root):
        self.root = root
        self.symbol_table = {}
        self.output = []
    
    def interpret(self):
        self.interpret_node(self.root)
        return self.output
    
    def interpret_node(self, node):
        for child in node.children:
            self.interpret_node(child)
            
        if node.type == 'VAR_DECL':
            self.declare_variable(node)
                
        elif node.type == 'EXPRESSION':
            node.value = node.children[0].value
            
        elif node.type in l.DATA_TYPES:
            node.value = self.evaluate_value(node, self.symbol_table)
            
        elif node.type == 'BIN_EXPR':
            operand1 = self.resolve_var(node.children[1].value)
            operand2 = self.resolve_var(node.children[3].value)
            node.value = self.perform_operation(node.children[0].value, operand1, operand2)
        
        elif node.type == 'INPUT_STMT':
            var_name = node.children[1].value
            self.gimmeh(var_name, self.symbol_table, '')
            
        elif node.type == 'PRINT_STMT':
            expr_nodes = []
            i = 1
            while i < len(node.children):
                expr_nodes.append(node.children[i])
                i += 2
            self.output.append(self.print_visible(expr_nodes)) 
            
        elif node.type == 'CONCAT_EXPR':
            node.value = str(self.resolve_var(node.children[1].value))
            i = 3
            while i < len(node.children):
                node.value += str(self.resolve_var(node.children[i].value))
                i += 2
        
    def evaluate_value(self, node, symbol_table):
        if node.type == 'NUMBR':
            return int(node.value)
        elif node.type == 'NUMBAR':
            return float(node.value)
        elif node.type == 'YARN':
            # remove quotes from string
            return node.value[1:-1]
        elif node.type == 'TROOF':
            return node.value == 'WIN'
        return node.value
    
    # takes a value and resolves it if it is a variable, otherwise returns the value
    # used when an operand may accept the value stored in a variable
    def resolve_var(self, var_name):
        if var_name in list(self.symbol_table.keys()):
            return self.symbol_table.get(var_name, 'NOOB')['value']
        else:
            return var_name

    def declare_variable(self, node):
        var_name = node.children[1].value
        
        if var_name in list(self.symbol_table.keys()):
            raise NameError("Variable " + var_name + " has already been declared")
        
        if len(node.children) >= 3:
            self.symbol_table[var_name] = {
                'value': self.resolve_var(node.children[3].value),
                'type': node.children[3].type
            }
        else:
            self.symbol_table[var_name] = {
                'value': 'NOOB',
                'type': 'NOOB'
            }
    
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
            print(str(e))
            raise TypeError("Invalid type: Cannot perform " + str(operator) + " on " + str(operand1) + " and " + str(operand2))
        
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
        output = ''
        for node in expr_nodes:
            value = node.value  
            output += str(self.resolve_var(value))
            # if value is None:
            #     output.append("NOOB")  
            # elif isinstance(value, bool):
            #     output.append("WIN" if value else "FAIL")  
            # elif isinstance(value, (int, float)):
            #     output.append(str(value))
            # elif isinstance(value, str):
            #     output.append(value)
            # else:
            #     output.append(f"UNKNOWN({value})")
        return output
    
    def gimmeh(self, variable_name, symbol_table, terminal_output):
        terminal_output += f"Enter value for {variable_name}:\n"

        user_input = input(f"Enter value for {variable_name}: ").strip()

        if variable_name in symbol_table:
            var_type = symbol_table[variable_name]['type']
            try:
                symbol_table[variable_name] = {
                    'value': int(user_input),
                    'type': var_type
                }
                terminal_output += f"{variable_name} set to {symbol_table[variable_name]['value']}\n"
            except ValueError:
                terminal_output += f"Error: Invalid value for {variable_name}.\n"
        else:
            terminal_output += f"Error: {variable_name} not found in symbol table.\n"
        return terminal_output  


