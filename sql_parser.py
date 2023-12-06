import re

def flatten_and_reduce(lst):
    flattened = []
    for item in lst:
        if isinstance(item, list):
            # Recursively flatten the sublist
            flattened.extend(flatten_and_reduce(item))
        elif item is not None:
            # Include non-None items
            flattened.append(item)
    return list(set(flattened))



# def log_function_call(func):
#     log_function_call.depth = 0

#     def wrapper(*args, **kwargs):
#         indent = ' ' * 4 * log_function_call.depth
#         print(f"{indent}Calling function: {func.__name__}")
#         log_function_call.depth += 1
#         result = func(*args, **kwargs)
#         log_function_call.depth -= 1
#         return result

#     return wrapper

# def decorate_all_methods(decorator):
#     def decorate(cls):
#         for attr in cls.__dict__:
#             if callable(getattr(cls, attr)):
#                 setattr(cls, attr, decorator(getattr(cls, attr)))
#         return cls
#     return decorate

# @decorate_all_methods(log_function_call)
class Parser:
    """
    Each parse function should be defined:
    Args:
    - index (int) : a valid index you want to start searching from
    Return:
    - indices (Arr[int]) : an array of integers that contain legal inidices
    
    """
    def __init__(self, input):
        self.input = input.strip()

    def skip_whitespace(self, index):
        pattern = r'\S'
        match = re.search(pattern, self.input[index:])
        if match:
            return index + match.end() - 1
        else:
            return None

    def skip_whitespaces(self, indices):
        for i in range(len(indices)):
            indices[i] = self.skip_whitespace(indices[i])
        return flatten_and_reduce(indices)

    def parse(self):
        parse_result = self.parse_condition(0)
        if not parse_result or len(self.input) not in parse_result:
            return f'Incorrect SQL Code'
        else: 
            return f'Parse Successful'

    def parse_table(self, index):
        """
        <table> := users | orders
        """
        if index > len(self.input):
            return []
        
        tables = ['users', 'orders']
        indices = []
        for table in tables:
            if self.input[index:].startswith(table):
                indices.append(index + len(table))
            else:
                indices.append(None)
        return flatten_and_reduce(indices)

    def parse_field(self, index):
        """
        <field> := id | email | first_name | last_name | user_id | date | amount
        """
        if index > len(self.input):
            return []
        
        fields = ['id', 'email', 'first_name', 'last_name', 'user_id', 'date', 'amount']
        indices = []
        for field in fields:
            if self.input[index:].startswith(field):
                indices.append(index + len(field))
            else:
                indices.append(None)
        return flatten_and_reduce(indices)
    
    def parse_table_field(self, index):
        """
        <table-field> := <table>.<field> | <field>
        """
        if index > len(self.input):
            return []
        
        index = self.skip_whitespace(index)
        if index is None:
            return []
        
        indices = []
        indices += self.parse_table_field_1(index)
        indices += self.parse_table_field_2(index)
        return flatten_and_reduce(indices)
        
    def parse_table_field_1(self, index):
        indices = self.parse_table(index)
        
        for i in range(len(indices)):
            if self.input[indices[i]:].startswith('.'):
                indices[i] += 1
            else:
                indices[i] = None
        indices = flatten_and_reduce(indices)
        
        for i in range(len(indices)):
            indices[i] = self.parse_field(indices[i])

        return flatten_and_reduce(indices)

    def parse_table_field_2(self, index):
        return flatten_and_reduce(self.parse_field(index))
        
    def parse_string(self, index):
        """
        <string> := **all legal strings in between single qoutes**
        """
        if index > len(self.input):
            return []
        index = self.skip_whitespace(index)
        pattern = r"^'(.*?)'"
        match = re.search(pattern, self.input[index:])

        if match:
            return [index + match.end()]
        else:
            return []
    
    def parse_integer(self, index):
        """
        <integer> := **all legal integers**
        """
        if index > len(self.input):
            return []
        index = self.skip_whitespace(index)
        pattern = r"^\d+"
        match = re.search(pattern, self.input[index:])

        if match:
            return [index + match.end()]
        else:
            return []

    def parse_float(self, index):
        """
        <float> := **all legal floats of the form XX.XX**
        """
        if index > len(self.input):
            return []
        index = self.skip_whitespace(index)
        pattern = r"^\d+\.\d+"
        match = re.search(pattern, self.input[index:])

        if match:
            return [index + match.end()]
        else:
            return []
    
    def parse_alias(self, index):
        """
        <alias> := <string>
        """
        index = self.skip_whitespace(index)
        if index is None:
            return []
        return flatten_and_reduce(self.parse_string(index))
    
    def parse_operator(self, index):
        """
        <operator> := + | - | * | / | = | != | < | > | <= | >= 
        """
        if index > len(self.input):
            return []
        index = self.skip_whitespace(index)
        if index is None:
            return []
        operators = ['+', '-', '*', '/', '=', '!=', '<', '>', '<=', '>=']
        indices = []
        for operator in operators:
            if self.input[index:].startswith(operator):
                indices.append(index + len(operator))
            else:
                indices.append(None)
        return flatten_and_reduce(indices)
    
    def parse_function(self, index):
        """
        <function> := SUM | AVG | COUNT | MAX | MIN | UPPER | LOWER
        """
        if index > len(self.input):
            return []
        index = self.skip_whitespace(index)
        if index is None:
            return []
        functions = ['SUM', 'AVG', 'COUNT', 'MAX', 'MIN', 'UPPER', 'LOWER']
        indices = []
        for function in functions:
            if self.input[index:].startswith(function):
                indices.append(index + len(function))
            else:
                indices.append(None)
        return flatten_and_reduce(indices)
    
    def parse_term(self, index):
        """
        <term> := <table-field> | <string> | <integer> | <float> | (<expression>)
        """
        if index > len(self.input):
            return []
        
        index = self.skip_whitespace(index)
        if index is None:
            return []
        
        indices = []
        indices += self.parse_term_1(index)
        indices += self.parse_term_2(index)
        indices += self.parse_term_3(index)
        indices += self.parse_term_4(index)
        indices += self.parse_term_5(index)
        return flatten_and_reduce(indices)
        
    def parse_term_1(self, index):
        return self.parse_table_field(index)

    def parse_term_2(self, index):
        return self.parse_string(index)

    def parse_term_3(self, index):
        return self.parse_float(index)
    
    def parse_term_4(self, index):
        return self.parse_integer(index)
    
    def parse_term_5(self, index):        
        if self.input[index:].startswith('('):
            index += 1
        else:
            return []
        
        index = self.skip_whitespace(index)
        if index is None:
            return []

        indices = self.parse_expression(index)
        indices = self.skip_whitespaces(indices)
        
        for i in range(len(indices)):
            if self.input[indices[i]:].startswith(')'):
                indices[i] += 1
            else:
                indices[i] = None
        
        return flatten_and_reduce(indices)

    def parse_expression(self, index):
        """
        <expression> := <term> | <term> <operator> <term> | <function> ( <expression> ) | <table-field> LIKE <string> | ( <select-query> )
        """
        if index > len(self.input):
            return []
        
        index = self.skip_whitespace(index)
        if index is None:
            return []
        
        indices = []
        indices += self.parse_expression_1(index)
        indices += self.parse_expression_2(index)
        indices += self.parse_expression_3(index)
        indices += self.parse_expression_4(index)
        indices += self.parse_expression_5(index)
        return flatten_and_reduce(indices)

    def parse_expression_1(self, index):
        return self.parse_term(index)
    
    def parse_expression_2(self, index):
        indices = self.parse_term(index)
        indices = self.skip_whitespaces(indices)

        for i in range(len(indices)):
            indices[i] = self.parse_operator(indices[i])
        indices = flatten_and_reduce(indices)

        indices = self.skip_whitespaces(indices)
        for i in range(len(indices)):
            indices[i] = self.parse_term(indices[i])

        return flatten_and_reduce(indices)
    
    def parse_expression_3(self, index):
        indices = self.parse_function(index)
        indices = self.skip_whitespaces(indices)

        for i in range(len(indices)):
            if self.input[indices[i]:].startswith('('):
                indices[i] += 1
            else:
                indices[i] = None
        indices = self.skip_whitespaces(flatten_and_reduce(indices))

        for i in range(len(indices)):
            indices[i] = self.parse_expression(indices[i])
        indices = flatten_and_reduce(indices)

        for i in range(len(indices)):
            if self.input[indices[i]:].startswith(')'):
                indices[i] += 1
            else:
                indices[i] = None

        return flatten_and_reduce(indices)
    
    def parse_expression_4(self, index):
        indices = self.parse_table_field(index)
        indices = self.skip_whitespaces(indices)
        
        for i in range(len(indices)):
            if self.input[indices[i]:].startswith('LIKE'):
                indices[i] += 4
            else:
                indices[i] = None
        indices = self.skip_whitespaces(flatten_and_reduce(indices))
        
        for i in range(len(indices)):
            indices[i] = self.parse_string(indices[i])
        
        return flatten_and_reduce(indices)

    def parse_expression_5(self, index):
        # TODO
        return flatten_and_reduce([])

    def parse_condition(self, index):
        """
        <condition> = <expression> | <expression> AND <condition> | <expression> OR <condition>
        """
        if index > len(self.input):
            return []
        
        index = self.skip_whitespace(index)
        if index is None:
            return []
        
        indices = []
        indices += self.parse_condition_1(index)
        indices += self.parse_condition_2(index)
        indices += self.parse_condition_3(index)
        return flatten_and_reduce(indices)

    def parse_condition_1(self, index):
        return self.parse_expression(index)
    
    def parse_condition_2(self, index):
        indices = self.parse_expression(index)
        indices = self.skip_whitespaces(indices)
        
        for i in range(len(indices)):
            if self.input[indices[i]:].startswith('AND'):
                indices[i] += 3
            else:
                indices[i] = None
        indices = self.skip_whitespaces(flatten_and_reduce(indices))

        for i in range(len(indices)):
            indices[i] = self.parse_condition(indices[i])
        
        return flatten_and_reduce(indices)
    
    def parse_condition_3(self, index):
        indices = self.parse_expression(index)
        indices = self.skip_whitespaces(indices)
        
        for i in range(len(indices)):
            if self.input[indices[i]:].startswith('OR'):
                indices[i] += 3
            else:
                indices[i] = None
        indices = self.skip_whitespaces(flatten_and_reduce(indices))

        for i in range(len(indices)):
            indices[i] = self.parse_condition(indices[i])
        
        return flatten_and_reduce(indices)





    def parse_field_list(self, index):

        if index > len(self.input):
            return []
        
        index = self.skip_whitespace(index)
        if index is None:
            return []
        
        indices = []
        indices += self.parse_field_list_1(index)
        indices += self.parse_field_list_2(index)

        return flatten_and_reduce(indices)

    def parse_field_list_1(self, index):
        # checking: <table-field>
        return flatten_and_reduce(self.parse_table_field(index))

    def parse_field_list_2(self, index):
        # checking: <table-field>, <field-list>

        # <table-field>
        indices = self.parse_table_field(index)

        indices = self.skip_whitespaces(indices)
        
        # ,
        for i in range(len(indices)):
            if self.input[indices[i]:].startswith(','):
                indices[i] += 1
            else:
                indices[i] = None

        indices = flatten_and_reduce(indices)

        indices = self.skip_whitespaces(indices)

        # <field-list>
        for i in range(len(indices)):
            indices[i] = self.parse_field_list(indices[i])
        # indices = self.skip_whitespaces(indices)
        
        return flatten_and_reduce(indices)



    def parse_expression_list(self, index):

        if index > len(self.input):
            return []
        
        index = self.skip_whitespace(index)
        if index is None:
            return []
        
        indices = []
        indices += self.parse_expression_list_1(index)
        indices += self.parse_expression_list_2(index)

        return flatten_and_reduce(indices)

    def parse_expression_list_1(self, index):
        # checking: <expression>
        return flatten_and_reduce(self.parse_expression(index))

    def parse_expression_list_2(self, index):
        # checking: <expression>, <expression-list>

        # <expression>
        indices = self.parse_expression(index)
        indices = self.skip_whitespaces(indices)
        
        # ,
        for i in range(len(indices)):
            if self.input[indices[i]:].startswith(','):
                indices[i] += 1
            else:
                indices[i] = None

        indices = flatten_and_reduce(indices)
        indices = self.skip_whitespaces(indices)

        # <field-list>
        for i in range(len(indices)):
            indices[i] = self.parse_expression_list(indices[i])
            
        
        return flatten_and_reduce(indices)



    def parse_select_clause(self, index):

        if index > len(self.input):
            return []
        
        index = self.skip_whitespace(index)
        if index is None:
            return []
        
        indices = []
        indices += self.parse_select_clause_1(index)
        indices += self.parse_select_clause_2(index)

        return flatten_and_reduce(indices)

    def parse_select_clause_1(self, index):
        # checking: *

        # *
        indices = []
        if self.input[index:].startswith('*'):
            indices.append(index + 1)
        else:
            indices.append(None)

        return flatten_and_reduce(indices)

    def parse_select_clause_2(self, index):
        # checking: <field-alias-list>

        # <field-alias-list>
        return flatten_and_reduce(self.parse_field_alias_list(index))



    def parse_field_alias_list(self, index):

        if index > len(self.input):
            return []
        
        index = self.skip_whitespace(index)
        if index is None:
            return []
        
        indices = []
        indices += self.parse_field_alias_list_1(index)
        indices += self.parse_field_alias_list_2(index)

        return flatten_and_reduce(indices)

    def parse_field_alias_list_1(self, index):
        # checking: <field-alias>

        # <field-alias>
        return flatten_and_reduce(self.parse_field_alias(index))

    def parse_field_alias_list_2(self, index):
        # checking: <field-alias>, <field-alias-list>

        # <field-alias>
        indices = flatten_and_reduce(self.parse_field_alias(index))
        indices = self.skip_whitespaces(indices)

        # ,
        for i in range(len(indices)):
            if self.input[indices[i]:].startswith(','):
                indices[i] += 1
            else:
                indices[i] = None

        indices = flatten_and_reduce(indices)
        indices = self.skip_whitespaces(indices)

        # <field-alias-list>
        for i in range(len(indices)):
            indices[i] = self.parse_field_alias_list(indices[i])
            
        return flatten_and_reduce(indices)



    def parse_field_alias(self, index):

        if index > len(self.input):
            return []
        
        index = self.skip_whitespace(index)
        if index is None:
            return []
        
        indices = []
        indices += self.parse_field_alias_1(index)
        indices += self.parse_field_alias_2(index)

        return flatten_and_reduce(indices)

    def parse_field_alias_1(self, index):
        # checking: <table-field>

        # <table-field>
        return flatten_and_reduce(self.parse_table_field(index))

    def parse_field_alias_2(self, index):
        # checking: <table-field> as <alias>

        # <table-field>
        indices = flatten_and_reduce(self.parse_table_field(index))
        indices = self.skip_whitespaces(indices)

        # as
        for i in range(len(indices)):
            if self.input[indices[i]:].startswith('as'):
                indices[i] += 2
            else:
                indices[i] = None

        indices = flatten_and_reduce(indices)
        indices = self.skip_whitespaces(indices)

        # <alias>
        for i in range(len(indices)):
            indices[i] = self.parse_alias(indices[i])

            
        return flatten_and_reduce(indices)




    def parse_table_alias_list(self, index):

        if index > len(self.input):
            return []
        
        index = self.skip_whitespace(index)
        if index is None:
            return []
        
        indices = []
        indices += self.parse_table_alias_list_1(index)
        indices += self.parse_table_alias_list_2(index)

        return flatten_and_reduce(indices)

    def parse_table_alias_list_1(self, index):
        # checking: <table-alias>

        # <table-alias>
        return flatten_and_reduce(self.parse_table_alias(index))

    def parse_table_alias_list_2(self, index):
        # checking: <table-alias>, <table-alias-list>

        # <<table-alias>
        indices = flatten_and_reduce(self.parse_table_alias(index))
        indices = self.skip_whitespaces(indices)

        # ,
        for i in range(len(indices)):
            if self.input[indices[i]:].startswith(','):
                indices[i] += 1
            else:
                indices[i] = None

        indices = flatten_and_reduce(indices)
        indices = self.skip_whitespaces(indices)

        # <table-alias-list>
        for i in range(len(indices)):
            indices[i] = self.parse_table_alias_list(indices[i])
            
        return flatten_and_reduce(indices)



    def parse_table_alias(self, index):

        if index > len(self.input):
            return []
        
        index = self.skip_whitespace(index)
        if index is None:
            return []
        
        indices = []
        indices += self.parse_table_alias_1(index)
        indices += self.parse_table_alias_2(index)

        return flatten_and_reduce(indices)

    def parse_table_alias_1(self, index):
        # checking: <table>

        return flatten_and_reduce(self.parse_table(index))
        
    def parse_table_alias_2(self, index):
        # checking: <table> as <alias>

        # <table>
        indices = flatten_and_reduce(self.parse_table(index))
        indices = self.skip_whitespaces(indices)

        # as
        for i in range(len(indices)):
            if self.input[indices[i]:].startswith('as'):
                indices[i] += 2
            else:
                indices[i] = None

        indices = flatten_and_reduce(indices)
        indices = self.skip_whitespaces(indices)

        # <alias>
        for i in range(len(indices)):
            indices[i] = self.parse_alias(indices[i])

            
        return flatten_and_reduce(indices)

if __name__ == '__main__':
    strings = [
        "first_name = 30 AND amount > 4"
    ]

    strings = [
        "id = 5",                                    # Simple equality
        "email = 'example@email.com'",               # String equality
        "first_name = 'John' AND amount > 100",      # Combination with AND
        "amount < 200 OR first_name = 'Alice'",      # Combination with OR
        "id IS NOT NULL",                            # NULL check
        "first_name LIKE 'J%'",                      # Pattern matching with LIKE
        "email = 'user@example.com' OR amount >= 150 AND amount <= 300", # Complex combination 
    ]
    for s in strings:
        parser = Parser(s)
        result = parser.parse()
        print(result)
