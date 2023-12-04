import re

class Parser:
    def __init__(self, input):
        self.input = input
        self.index = 0

    def consume(self, char):
        if self.index < len(self.input) and self.input[self.index] == char:
            self.index += 1
        else:
            raise ValueError(f"Unexpected character at index {self.index}: expected '{char}', got '{self.input[self.index]}'")

    def parse(self):
        parse_result = self.parse_condition(0)
        if parse_result is None or parse_result != len(self.input):
            return f'Incorrect SQL Code: {len(self.input)} - {parse_result}'
        else: 
            return f'Parse Successful: {len(self.input)} - {parse_result}'

    def parse_table(self, index):
        """
        <table> := users | orders
        """
        if index > len(self.input):
            return None
        
        tables = ['users', 'orders']
        for table in tables:
            if self.input[index:].startswith(table):
                return index + len(table)
        return None

    def parse_field(self, index):
        """
        <field> := id | email | first_name | last_name | user_id | date | amount
        """
        if index > len(self.input):
            return None
        
        fields = ['id', 'email', 'first_name', 'last_name', 'user_id', 'date', 'amount']
        for field in fields:
            if self.input[index:].startswith(field):
                return index + len(field)
        return None
    
    def parse_table_field(self, index):
        """
        <table-field> := <table>.<field> | <field>
        """
        if index > len(self.input):
            return None
        start_index = index
        
        index = self.parse_table_field_1(start_index)
        if index is not None:
            return index

        index = self.parse_table_field_2(start_index)
        return index
        
    def parse_table_field_1(self, index):
        index = self.parse_table(index)
        if index is None:
            return None
        
        if self.input[index:].startswith('.'):
            index += 1
        else:
            return None
        
        index = self.parse_field(index)
        return index

    def parse_table_field_2(self, index):
        return self.parse_field(index)
        
    def parse_string(self, index):
        """
        <string> := **all legal strings in between single qoutes**
        """
        if index > len(self.input):
            return None
        pattern = r"^'(.*?)'"
        match = re.search(pattern, self.input[index:])

        if match:
            return index + match.end()
        else:
            return None
    
    def parse_integer(self, index):
        """
        <integer> := **all legal integers**
        """
        if index > len(self.input):
            return None
        pattern = r"^\d+\s"
        match = re.search(pattern, self.input[index:])

        if match:
            return index + match.end()
        else:
            return None

    def parse_float(self, index):
        """
        <float> := **all legal floats of the form XX.XX**
        """
        if index > len(self.input):
            return None
        pattern = r"^\d+\.\d+"
        match = re.search(pattern, self.input[index:])

        if match:
            return index + match.end()
        else:
            return None
    
    def parse_alias(self, index):
        """
        <alias> := <string>
        """
        if index > len(self.input):
            return None
        return self.parse_string(index)
    
    def parse_operator(self, index):
        """
        <operator> := + | - | * | / | = | != | < | > | <= | >= 
        """
        if index > len(self.input):
            return None
        operators = ['+', '-', '*', '/', '=', '!=', '<', '>', '<=', '>=']
        for operator in operators:
            if self.input[index:].startswith(operator):
                return index + len(operator)
        return None
    
    def parse_function(self, index):
        """
        <function> := SUM | AVG | COUNT | MAX | MIN | UPPER | LOWER
        """
        if index > len(self.input):
            return None
        functions = ['SUM', 'AVG', 'COUNT', 'MAX', 'MIN', 'UPPER', 'LOWER']
        for function in functions:
            if self.input[index:].startswith(function):
                return index + len(function)
        return None
    
    def parse_term(self, index):
        """
        <term> := <table-field> | <string> | <integer> | <float> | (<expression>)
        """
        if index > len(self.input):
            return None
        start_index = index
        
        index = self.parse_term_1(start_index)
        if index is not None:
            return index
        
        index = self.parse_term_2(start_index)
        if index is not None:
            return index
        
        index = self.parse_term_3(start_index)
        if index is not None:
            return index
        
        index = self.parse_term_4(start_index)
        if index is not None:
            return index
        
        index = self.parse_term_5(start_index)
        return index
        
    def parse_term_1(self, index):
        return self.parse_table_field(index)

    def parse_term_2(self, index):
        return self.parse_string(index)

    def parse_term_3(self, index):
        return self.parse_integer(index)
    
    def parse_term_4(self, index):
        return self.parse_float(index)
    
    def parse_term_5(self, index):        
        if self.input[index:].startswith('('):
            index += 1
        else:
            return None
        
        index = self.parse_expression(index)
        if index is None:
            return None
        
        if self.input[index:].startswith(')'):
            index += 1
        else:
            return None
        
        return index

    def parse_expression(self, index):
        """
        <expression> := <term> | <term> <operator> <term> | <function> ( <expression> ) | <table-field> LIKE <string> | ( <select-query> )
        """
        if index > len(self.input):
            return None
        start_index = index
        
        index = self.parse_expression_1(start_index)
        if index is not None:
            return index
        
        index = self.parse_expression_2(start_index)
        if index is not None:
            return index
        
        index = self.parse_expression_3(start_index)
        if index is not None:
            return index
        
        index = self.parse_expression_4(start_index)
        if index is not None:
            return index
        
        index = self.parse_expression_5(start_index)
        return index

    def parse_expression_1(self, index):
        return self.parse_term(index)
    
    def parse_expression_2(self, index):
        index = self.parse_term(index)
        if index is None:
            return None

        index = self.parse_operator(index)
        if index is None:
            return None
        
        index = self.parse_term(index)
        if index is None:
            return None
        
        return index
    
    def parse_expression_3(self, index):
        index = self.parse_function(index)
        if index is None:
            return None
        
        if self.input[index:].startswith('('):
            index += 1
        else:
            return None
        
        index = self.parse_expression(index)
        if index is None:
            return None
        
        if self.input[index:].startswith(')'):
            index += 1
        else:
            return None
        
        return index
    
    def parse_expression_4(self, index):
        index = self.parse_table_field(index)
        if index is None:
            return None
        
        if self.input[index:].startswith('LIKE'):
            index += 4
        else:
            return None
        
        index = self.parse_string(index)
        if index is None:
            return None
        
        return index

    def parse_expression_5(self, index):
        # TODO
        return None

    def parse_condition(self, index):
        """
        <condition> = <expression> | <expression> AND <condition> | <expression> OR <condition>
        """
        if index > len(self.input):
            return None
        start_index = index
        
        index = self.parse_condition_1(start_index)
        if index is not None:
            return index
        
        index = self.parse_condition_2(start_index)
        if index is not None:
            return index
        
        index = self.parse_condition_3(start_index)
        return index

    def parse_condition_1(self, index):
        return self.parse_expression(index)
    
    def parse_condition_2(self, index):
        index = self.parse_expression(index)
        if index is None:
            return None
        
        if self.input[index:].startswith('AND'):
            index += 3
        else:
            return None
        
        index = self.parse_condition(index)
        if index is None:
            return None
        
        return index
    
    def parse_condition_3(self, index):
        index = self.parse_expression(index)
        if index is None:
            return None
        
        if self.input[index:].startswith('OR'):
            index += 2
        else:
            return None
        
        index = self.parse_condition(index)
        if index is None:
            return None
        
        return index







strings = [
    'users.id',
    'id',
    "'hello in am under the water'",
    '32 ',
    '23.11111',
    '11.1a',
    'users.',
    "'hello' "
]
for s in strings:
    parser = Parser(s)
    result = parser.parse()
    print(result)
