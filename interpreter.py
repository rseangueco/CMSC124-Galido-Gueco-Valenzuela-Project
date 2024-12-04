import syntax_analyzer
import lexemes as l

class Interpreter:  
    
    def __init__(self, root):
        self.root = root
        self.symbol_table = {}
    
    def interpret(self):
        return self.interpret_node(self.root)
    
    def interpret_node(self, node):
        
        for child in node.children:
            self.interpret_node(child)
            
        if node.type == 'VAR_DECL':
            self.declare_variable(node)
                
        elif node.type == 'EXPRESSION':
            node.value = node.children[0].value
            
        elif node.type in l.DATA_TYPES:
            node.value = self.evaluate_value(node, self.symbol_table)
            
        elif node.type == 'IDENTIFIER':
            if node.value in self.symbol_table.keys():
                node.value = self.evaluate_value(node, self.symbol_table)
            
        elif node.type == 'BIN_EXPR':
            operand1 = self.resolve_var(node.children[1].value)
            operand2 = self.resolve_var(node.children[3].value)
            node.value = self.perform_operation(node.children[0].value, operand1, operand2)
        
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
        elif node.type == 'IDENTIFIER':
            return symbol_table.get(node.value, 'NOOB')['value']
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
            print("Variable " + var_name + " has already been declared")
        
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


