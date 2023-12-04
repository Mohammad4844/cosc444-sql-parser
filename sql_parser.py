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

    def parse(self):
        parse_result = self.parse_table_field(0)
        if parse_result is None:
            return 'Incorrect SQL Code'
        else: 
            return 'Parse Successful'
        
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
        pattern = r"^\d+"
        match = re.search(pattern, self.input[index:])

        if match:
            return index + match.end()
        else:
            return None

    def parse_floating_point(self, index):
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



parser = Parser("first_name")
result = parser.parse()
print(result)
