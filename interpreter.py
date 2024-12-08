import syntax_analyzer
import tkinter as tk
from tkinter import *
import lexemes as l
import re

# handles the execution of various types of statements and expressions,
# interacts with the parse tree and maintains a symbol table for variable storage
class Interpreter:  
    
    def __init__(self, root, terminal):
        self.root = root
        self.symbol_table = {}
        self.return_val = ''
        self.output = []
        
        self.terminal = terminal
        self.input_ready = tk.StringVar()
        self.terminal.bind('<Return>', self.on_enter)
    
    # callback function triggered when the Enter key is pressed in the terminal
    # signals that input has been received
    def on_enter(self, event):
        self.input_ready.set("input received")
        
    # starts the interpretation process by visiting the root of the syntax tree
    # returns the final return value after interpretation
    def interpret(self):
        self.interpret_node(self.root)
        return self.return_val
    
    # interprets a given node in the syntax tree, handling various statement and expression types recursively
    def interpret_node(self, node): 
        
        if node.type == 'IF_STATEMENT': self.interpret_if_block(node)
        elif node.type == 'SWITCH_STATEMENT': self.interpret_switch_block(node)
        elif node.type == 'LOOP_STMT': self.interpret_loop_block(node)
        elif node.type == "FUNC_DECL_STMT": self.declare_function(node)
        else:
            for child in node.children:
                self.interpret_node(child)
        
        if node.type in l.DATA_TYPES:
            node.value = self.evaluate_value(node)
            
        elif node.type == 'EXPRESSION':
            node.value = node.children[0].value
            if node.children[0].value == 'NOT':
                node.value = 'FAIL' if self.resolve_var(node.children[1].value) and  self.resolve_var(node.children[1].value) != 'FAIL'  else 'WIN'
            self.symbol_table['IT'] = {
                'value': self.resolve_var(node.value),
                'type': node.children[0].type
            }            
        
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
            
        elif node.type == 'VAR_DECL':
            self.declare_variable(node)
        
        elif node.type == 'ASSIGN_STMT':
            var_name = node.children[0].value
            new_value = node.children[2].value
            self.symbol_table[var_name] = {
                'value': new_value
            }
        
        elif node.type == 'INPUT_STMT':
            var_name = node.children[1].value
            self.gimmeh(var_name, '')
            
        elif node.type == 'PRINT_STMT':
            expr_nodes = []
            i = 1
            while i < len(node.children):
                expr_nodes.append(node.children[i])
                i += 2
            self.output.append(self.print_visible(expr_nodes)) 
            
        elif node.type == 'TYPE_STMT':
            var_name = node.children[0].value
            target_type = node.children[2].type
            original_value = self.symbol_table.get(var_name, 'NOOB')['value']
            self.symbol_table[var_name] = {
                'value': self.type_cast(original_value, target_type),
                'type': target_type
            }

        elif node.type == 'SWITCH_CASE':
            node.value = node.children[1].value
            
        elif node.type == "FUNC_CALL_STMT":
            self.call_function(node)
            
        elif node.type == 'RETURN_STMT':
            self.return_val = self.symbol_table.get('IT', 'NOOB')['value'] if len(node.children) > 1 else 'NOOB'
    
    # interprets an IF block by evaluating the condition and executing the appropriate branch
    def interpret_if_block(self, node):
        if_value = self.symbol_table.get('IT', 'NOOB')['value']
        i = 1
        while i < len(node.children):
            if node.children[i].value == 'YA RLY':
                if if_value == 'WIN':
                    self.interpret_node(node.children[i+1])
                    return
            elif node.children[i].type == 'ELIF_STATEMENT':
                self.interpret_node(node.children[i].children[1])
                elif_value = self.symbol_table.get('IT', 'NOOB')['value']
                if elif_value == 'WIN':
                    self.interpret_node(node.children[i+1])
                    return
            elif node.children[i].value == 'NO WAI':
                self.interpret_node(node.children[i+1])
                return
            elif node.children[i].value == 'OIC':
                return
            i += 2   
    
    # interprets a SWITCH block by evaluating cases and executing the matching case block
    def interpret_switch_block(self, node):
        self.interpret_node(node.children[0])
        switch_value = self.symbol_table.get('IT', 'NOOB')['value']
        i = 2
        while i < len(node.children):
            if node.children[i].type == 'SWITCH_CASE':
                self.interpret_node(node.children[i])
                if self.type_cast(node.children[i].value, 'YARN') == switch_value:
                    self.interpret_node(node.children[i+1])
                    return
            elif node.children[i].value == 'OMGWTF':
                self.interpret_node(node.children[i+1])
            elif node.children[i].value == 'OIC':
                return
            i+=2
    
    # interprets a LOOP block, handling variable incrementation and termination conditions
    def interpret_loop_block(self, node):
        self.interpret_node(node.children[4])
        self.interpret_node(node.children[6])
        inc = node.children[2].value
        term = node.children[5].value
        var = node.children[4].value
        condition = self.resolve_var(node.children[6].value)
        
        if (term == 'WILE' and condition == 'WIN') or (term == 'TIL' and condition == 'FAIL'):
            self.interpret_node(node.children[7])
            if inc == 'UPPIN':
                self.symbol_table[var] = {
                    'value': self.perform_bin_op('SUM OF', self.resolve_var(var), 1),
                    'type': 'NUMBR'
                }
            elif inc == 'NERFIN':
                self.symbol_table[var] = {
                    'value': self.perform_bin_op('DIFF OF', self.resolve_var(var), 1),
                    'type': 'NUMBR'
                }
            self.interpret_node(node)
    
    # declares a function by storing its parameters and body in the symbol table
    def declare_function(self, node):
        for i in range(0,2):
            self.interpret_node(node.children[i])
        func_name = node.children[1].value
        parameters = []
        for parameter in node.children[2].children:
            if parameter.type == 'IDENTIFIER':
                parameters.append(parameter.value)
                
        self.symbol_table[func_name] = {
            'value': func_name,
            'type': 'FUNCTION',
            'body': node.children[3],
            'parameters': parameters
        }
    
    # calls a function by setting up a new interpreter for its body and passing arguments
    def call_function(self, node):
        func_name = node.children[1].value
        in_parameters = []
        i = 3
        while i < len(node.children):
            in_parameters.append(self.resolve_var(node.children[i].value))
            i+=3
            
        func = self.symbol_table.get(func_name, 'NOOB')
        func_body = func['body']
        func_parameters = func['parameters']
        
        func_interpreter = Interpreter(func_body, self.terminal)
        i = 0
        while i < len(func_parameters):
            func_interpreter.symbol_table[func_parameters[i]] = {'value': in_parameters[i]}
            i += 1
            
        node.value = func_interpreter.interpret()
        del func_interpreter
        self.terminal.bind('<Return>', self.on_enter)
    
    # evaluates a node's value based on its type, converting literals to their Python equivalents
    def evaluate_value(self, node):
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

    # declares a variable and initializes it with a value if provided
    # raises an error if the variable is already declared
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
    
    # performs a binary operation (e.g., addition, subtraction) on two operands based on the specified operator
    def perform_bin_op(self, operator, operand1, operand2):
        if operand1 == 'FAIL': operand1 = False
        if operand2 == 'FAIL': operand2 = False
        
        try:
            if operator == 'SUM OF':
                if (bool(re.match(l.NUMBR, str(operand1))) and bool(re.match(l.NUMBR, str(operand2)))):
                    return self.type_cast(operand1, "NUMBR") + self.type_cast(operand2, "NUMBR")
                elif (bool(re.match(l.NUMBAR, str(operand1))) or bool(re.match(l.NUMBAR, str(operand2)))):
                    return self.type_cast(operand1, "NUMBAR") + self.type_cast(operand2, "NUMBAR")
            
            elif operator == 'DIFF OF':
                if (bool(re.match(l.NUMBR, str(operand1))) and bool(re.match(l.NUMBR, str(operand2)))):
                    return self.type_cast(operand1, "NUMBR") - self.type_cast(operand2, "NUMBR")
                elif (bool(re.match(l.NUMBAR, str(operand1))) or bool(re.match(l.NUMBAR, str(operand2)))):
                    return self.type_cast(operand1, "NUMBAR") - self.type_cast(operand2, "NUMBAR")
            
            elif operator == 'PRODUKT OF':
                if (bool(re.match(l.NUMBR, str(operand1))) and bool(re.match(l.NUMBR, str(operand2)))):
                    return self.type_cast(operand1, "NUMBR") * self.type_cast(operand2, "NUMBR")
                elif (bool(re.match(l.NUMBAR, str(operand1))) or bool(re.match(l.NUMBAR, str(operand2)))):
                    return self.type_cast(operand1, "NUMBAR") * self.type_cast(operand2, "NUMBAR")
            
            elif operator == 'QUOSHUNT OF':
                if (bool(re.match(l.NUMBR, str(operand1))) and bool(re.match(l.NUMBR, str(operand2)))):
                    return self.type_cast(operand1, "NUMBR") / self.type_cast(operand2, "NUMBR")
                elif (bool(re.match(l.NUMBAR, str(operand1))) or bool(re.match(l.NUMBAR, str(operand2)))):
                    return self.type_cast(operand1, "NUMBAR") / self.type_cast(operand2, "NUMBAR")
            
            elif operator == 'MOD OF':
                if (bool(re.match(l.NUMBR, str(operand1))) and bool(re.match(l.NUMBR, str(operand2)))):
                    return self.type_cast(operand1, "NUMBR") % self.type_cast(operand2, "NUMBR")
                elif (bool(re.match(l.NUMBAR, str(operand1))) or bool(re.match(l.NUMBAR, str(operand2)))):
                    return self.type_cast(operand1, "NUMBAR") % self.type_cast(operand2, "NUMBAR")
            
            elif operator == 'BIGGR OF':
                if (bool(re.match(l.NUMBR, str(operand1))) and bool(re.match(l.NUMBR, str(operand2)))):
                    return max(self.type_cast(operand1, "NUMBR"), self.type_cast(operand2, "NUMBR"))
                elif (bool(re.match(l.NUMBAR, str(operand1))) or bool(re.match(l.NUMBAR, str(operand2)))):
                    return self.type_cast(operand1, "NUMBAR") % self.type_cast(operand2, "NUMBAR")
            
            elif operator == 'SMALLR OF':
                if (bool(re.match(l.NUMBR, str(operand1))) and bool(re.match(l.NUMBR, str(operand2)))):
                    return min(self.type_cast(operand1, "NUMBR"), self.type_cast(operand2, "NUMBR"))
                elif (bool(re.match(l.NUMBAR, str(operand1))) or bool(re.match(l.NUMBAR, str(operand2)))):
                    return self.type_cast(operand1, "NUMBAR") % self.type_cast(operand2, "NUMBAR")
            
            elif operator == 'BOTH OF':
                return 'WIN' if (operand1 and operand2) else 'FAIL'
            
            elif operator == 'EITHER OF':
                return 'WIN' if (operand1 or operand2) else 'FAIL'
            
            elif operator == 'WON OF':
                return 'WIN' if (operand1 or operand2) and not (operand1 and operand2) else 'FAIL'
            
            elif operator == 'BOTH SAEM':
                if (bool(re.match(l.NUMBR, str(operand1))) and bool(re.match(l.NUMBR, str(operand2)))):
                    return 'WIN' if (self.type_cast(operand1, "NUMBR") == self.type_cast(operand2, "NUMBR")) else 'FAIL'
                elif (bool(re.match(l.NUMBAR, str(operand1))) or bool(re.match(l.NUMBAR, str(operand2)))):
                    return 'WIN' if (self.type_cast(operand1, "NUMBAR") == self.type_cast(operand2, "NUMBAR")) else 'FAIL'
                else: 
                    return 'WIN' if (operand1 == operand2) else 'FAIL'
            
            elif operator == 'DIFFRINT':
                return 'WIN' if (operand1 != operand2) else 'FAIL'

        except Exception as e:
            print(str(e))
            raise TypeError("Invalid type: Cannot perform " + str(operator) + " on " + str(operand1) + " and " + str(operand2))
        
        return None 
    
    # performs an operation with multiple operands, such as AND-ing or OR-ing all values
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
    
    # concatenates and prints the resolved values of expression nodes
    def print_visible(self, expr_nodes):
        output = ''
        for node in expr_nodes:
            value = node.value  
            output += str(self.resolve_var(value))
        self.terminal.insert(END, str(output) + '\n')
        print(output)
        # return output
    
    # prompts the user for input, assigns the input to a variable in the symbol table, and updates terminal output
    def gimmeh(self, variable_name, terminal_output):
        # insert input prompt
        # self.terminal.insert(END, f'Enter value for {variable_name}: ')
        self.terminal.see(END)  # Scroll to the end
        self.terminal.focus()
        
        # wait for input
        self.terminal.wait_variable(self.input_ready)
        # get the input, removing the prompt and stripping whitespace
        user_input = self.terminal.get(1.0, END).strip().split('\n')[-1]
        user_input = user_input.replace(f'Enter value for {variable_name}: ', '').strip()

        if variable_name in self.symbol_table:
            var_type = self.symbol_table[variable_name]['type']
            try:

                self.symbol_table[variable_name] = {
                    'value': user_input,
                    'type': var_type
                }
                terminal_output += f"{variable_name} set to {self.symbol_table[variable_name]['value']}\n"
            except ValueError:
                terminal_output += f"Error: Invalid value for {variable_name}.\n"
        else:
            terminal_output += f"Error: {variable_name} not found in symbol table.\n"
        
        return terminal_output  

    # casts a given value to a specified target type following specific type rules
    def type_cast(self, original_value, target_type):
        if original_value == "none":
            if target_type == "TROOF":
                return 'FAIL'
            elif target_type == "NUMBR":
                return 0
            elif target_type == "NUMBAR":
                return 0.0
            elif target_type == "YARN":
                return ""
            else:
                return "NOOB"

        try:
            if target_type == "NUMBR":
                if original_value == "WIN":
                    return 1
                elif original_value == "FAIL":
                    return 0
                elif isinstance(original_value, float):
                    return int(original_value)
                elif isinstance(original_value, str):
                    # if bool(re.match(l.NUMBR, original_value)):
                        return int(original_value)
                elif isinstance(original_value, int):
                    return original_value
                else:
                    print('test')
                    raise TypeError("Invalid type: Cannot perform type casting to NUMBR on" + str(original_value))
            elif target_type == "NUMBAR":
                if original_value == "WIN":
                    return 1.0
                elif original_value == "FAIL":
                    return 0.0
                elif isinstance(original_value, int):
                    return float(original_value)
                elif isinstance(original_value, str):
                    # if bool(re.match(l.NUMBAR, original_value)):
                        return float(original_value)
                elif isinstance(original_value, float):
                    return original_value
                else:
                    raise TypeError("Invalid type: Cannot perform type casting to NUMBAR on" + str(original_value))
            elif target_type == "YARN":
                if isinstance(original_value, float):
                    return str(round(original_value, 2))
                else:
                    return str(original_value)
            elif target_type == "TROOF":
                if isinstance(original_value, bool):
                    return 'WIN' if original_value else 'FAIL'
                elif isinstance(original_value, (int, float)):
                    return 'WIN' if original_value != 0 else 'FAIL'
                elif isinstance(original_value, str):
                    return 'WIN' if len(original_value) > 0 else 'FAIL'
                else:
                    return 'FAIL' 
            else:
                return "NOOB"  # unsupported type results in NOOB
        except (ValueError, TypeError):
           return "NOOB"  # conversion failed