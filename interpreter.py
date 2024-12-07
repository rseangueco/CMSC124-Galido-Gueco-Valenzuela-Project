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
        if node.type == 'SWITCH_STATEMENT':
            self.interpret_node(node.children[0])
            switch_value = self.symbol_table.get('IT', 'NOOB')['value']
            i = 2
            while i < len(node.children):
                if node.children[i].type == 'SWITCH_CASE':
                    self.interpret_node(node.children[i])
                    if node.children[i].value == switch_value:
                        self.interpret_node(node.children[i+1])
                        return
                elif node.children[i].value == 'OMGWTF':
                    self.interpret_node(node.children[i+1])
                elif node.children[i].value == 'OIC':
                    return
                i+=2
        else:
            for child in node.children:
                self.interpret_node(child)
            
        if node.type == 'VAR_DECL':
            self.declare_variable(node)
                
        elif node.type == 'EXPRESSION':
            node.value = node.children[0].value
            if node.children[0].value == 'NOT':
                node.value = 'FAIL' if self.resolve_var(node.children[1].value) and  self.resolve_var(node.children[1].value) != 'FAIL'  else 'WIN'
            self.symbol_table['IT'] = {
                'value': self.resolve_var(node.value),
                'type': node.children[0].type
            }
            
        elif node.type in l.DATA_TYPES:
            node.value = self.evaluate_value(node, self.symbol_table)
            
        elif node.type == 'BIN_EXPR':
            operand1 = self.resolve_var(node.children[1].value)
            operand2 = self.resolve_var(node.children[3].value)
            node.value = self.perform_bin_op(node.children[0].value, operand1, operand2)

        elif node.type == 'INF_EXPR':
            operands = []
            i = 1
            while i < len(node.children):
                operands.append(self.resolve_var(node.children[i].value))
                i += 2
            node.value = self.perform_inf_op(node.children[0].value, operands)
        
        elif node.type == 'ASSIGN_STMT':
            var_name = node.children[0].value
            new_value = node.children[2].value
            self.symbol_table[var_name] = {
                'value': new_value
            }
        
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
                
        elif node.type == 'TYPE_EXPR':
            original_value = self.resolve_var(node.children[1].value)
            target_type = node.children[2].type
            node.value = self.type_cast(original_value, target_type)
            
        elif node.type == 'SWITCH_CASE':
            node.value = node.children[1].value
       
            
        
    def evaluate_value(self, node, symbol_table):
        if node.type == 'NUMBR':
            return int(node.value)
        elif node.type == 'NUMBAR':
            return float(node.value)
        elif node.type == 'YARN':
            # remove quotes from string
            return node.value[1:-1]
        elif node.type == 'TROOF':
            return 'WIN' if node.value == 'WIN' else 'FAIL'
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
    
    def perform_bin_op(self, operator, operand1, operand2):
        if operand1 == 'FAIL': operand1 = False
        if operand2 == 'FAIL': operand2 = False
        
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
            elif operator == 'BOTH OF':
                return 'WIN' if (operand1 and operand2) else 'FAIL'
            elif operator == 'EITHER OF':
                return 'WIN' if (operand1 or operand2) else 'FAIL'
            elif operator == 'WON OF':
                return 'WIN' if (operand1 or operand2) and not (operand1 and operand2) else 'FAIL'
            elif operator == 'BOTH SAEM':
                return 'WIN' if (operand1 == operand2) else 'FAIL'
            elif operator == 'DIFFRINT':
                return 'WIN' if (operand1 != operand2) else 'FAIL'
        except Exception as e:
            print(str(e))
            raise TypeError("Invalid type: Cannot perform " + str(operator) + " on " + str(operand1) + " and " + str(operand2))
        
        return None
    
    def perform_inf_op(self, operator, operands):
        if operator == 'ALL OF':
            for operand in operands:
                if bool(operand) and operand != 'WIN':
                    return 'FAIL'
            return 'WIN'
        
        elif operator == 'ANY OF':
            for operand in operands:
                if not bool(operand) and operand != 'FAIL':
                    return 'WIN'
            return 'FAIL'
        
        return

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

    def type_cast(self, original_value, target_type):
        try:
            if target_type == "NUMBR":
                casted_value = int(original_value)
            elif target_type == "NUMBAR":
                casted_value = float(original_value)
            elif target_type == "YARN":
                casted_value = str(original_value)
            elif target_type == "TROOF":
                if isinstance(original_value, bool):
                    casted_value = 'WIN' if original_value else 'FAIL'
                elif isinstance(original_value, (int, float)):
                    casted_value = 'WIN' if original_value != 0 else 'FAIL'
                elif isinstance(original_value, str):
                    casted_value = 'WIN' if len(original_value) > 0 else 'FAIL'
                else:
                    casted_value = False
            else:
                casted_value = "NOOB"  # unsupported type results in NOOB
        except (ValueError, TypeError):
            casted_value = "NOOB"  # conversion failed
                
        return casted_value
