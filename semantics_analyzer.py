import lexemes as l

class SemanticAnalyzer:
    def __init__(self, parse_tree, symbol_table):
        self.parse_tree = parse_tree
        self.symbol_table = symbol_table
        self.errors = []

    def analyze(self):
        """
        Perform semantic analysis on the parse tree
        """
        self.analyze_node(self.parse_tree)
        return self.errors, self.symbol_table

    def analyze_node(self, node):
        """
        Recursively analyze each node in the parse tree
        """
        # Variable Declaration Analysis
        if node.type == 'VAR_DECL':
            self.analyze_variable_declaration(node)

        # Assignment Statement Analysis
        elif node.type == 'ASSIGN_STMT':
            self.analyze_assignment(node)

        # Type Conversion Analysis
        elif node.type == 'TYPE_STMT':
            self.analyze_type_conversion(node)

        # Function Declaration Analysis
        elif node.type == 'FUNC_DECL_STMT':
            self.analyze_function_declaration(node)

        # Function Call Analysis
        elif node.type == 'FUNC_CALL_STMT':
            self.analyze_function_call(node)

        # Traverse child nodes
        for child in node.children:
            self.analyze_node(child)

    def analyze_variable_declaration(self, node):
        """
        Analyze variable declarations
        - Check for duplicate variable names
        - Infer or validate variable type
        """
        if len(node.children) >= 1:
            var_name = node.children[1].value
            
            # Check for duplicate variable declaration
            if var_name in self.symbol_table:
                self.errors.append(f"Semantic Error: Variable '{var_name}' already declared")
            
            # If initial value is provided, infer type
            if len(node.children) > 1:
                value_node = node.children[1]
                inferred_type = self.infer_type(value_node)
                self.symbol_table[var_name] = {
                    'value': None,
                    'type': inferred_type
                }
            else:
                # Default to NOOB if no initial value
                self.symbol_table[var_name] = {
                    'value': None,
                    'type': 'NOOB'
                }

    def analyze_assignment(self, node):
        """
        Analyze assignment statements
        - Type compatibility
        - Value validation
        """
        if len(node.children) >= 2:
            var_name = node.parent.children[0].value
            value_node = node.children[0]
            
            if var_name not in self.symbol_table:
                self.errors.append(f"Semantic Error: Variable '{var_name}' not declared before assignment")
                return
            
            inferred_type = self.infer_type(value_node)
            
            # Update symbol table with new value and type
            self.symbol_table[var_name] = {
                'value': value_node.value,
                'type': inferred_type
            }

    def analyze_type_conversion(self, node):
        """
        Analyze type conversion statements
        """
        if len(node.children) >= 2:
            var_name = node.parent.children[0].value
            target_type = node.children[0].value
            
            if var_name not in self.symbol_table:
                self.errors.append(f"Semantic Error: Variable '{var_name}' not declared before type conversion")
                return
            
            # Update symbol table with new type
            self.symbol_table[var_name]['type'] = target_type

    def analyze_function_declaration(self, node):
        """
        Analyze function declarations
        - Check for duplicate function names
        - Validate parameters
        """
        if len(node.children) >= 1:
            func_name = node.children[0].value
            
            # Check for duplicate function declaration
            if func_name in self.symbol_table:
                self.errors.append(f"Semantic Error: Function '{func_name}' already declared")
            
            # Store function information
            self.symbol_table[func_name] = {
                'type': 'FUNCTION',
                'parameters': self.extract_parameters(node)
            }

    def analyze_function_call(self, node):
        """
        Analyze function calls
        - Check if function exists
        - Validate number and types of arguments
        """
        if len(node.children) >= 1:
            func_name = node.children[0].value
            
            if func_name not in self.symbol_table:
                self.errors.append(f"Semantic Error: Function '{func_name}' not declared")
                return
            
            # Validate arguments
            expected_params = self.symbol_table[func_name].get('parameters', [])
            actual_args = [child for child in node.children[1:] if child.type == 'EXPRESSION']
            
            if len(actual_args) != len(expected_params):
                self.errors.append(f"Semantic Error: Incorrect number of arguments for function '{func_name}'")

    def extract_parameters(self, node):
        """
        Extract function parameters
        """
        parameters = []
        for child in node.children:
            if child.type == 'PARAMETER':
                param_names = [c.value for c in child.children if c.type == 'IDENTIFIER']
                parameters.extend(param_names)
        return parameters

    def infer_type(self, node):
        """
        Infer the type of an expression node
        """
        if node.type == 'NUMBR':
            return 'NUMBR'
        elif node.type == 'NUMBAR':
            return 'NUMBAR'
        elif node.type == 'YARN':
            return 'YARN'
        elif node.type == 'TROOF':
            return 'TROOF'
        elif node.type in ['BIN_EXPR', 'INF_EXPR', 'CONCAT_EXPR', 'TYPE_EXPR']:
            # Complex expressions might require additional logic
            return self.infer_type(node.children[0])
        
        return 'NOOB'