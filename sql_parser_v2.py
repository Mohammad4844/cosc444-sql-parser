from collections import defaultdict
import re

keyword_list = [
    ',', '.', ';', 'SELECT', 'DISTINCT', 'FROM', 'WHERE', 'GROUP', 'BY', 'HAVING', 'ORDER', 'DELETE', 'UPDATE', 'SET', 'INSERT', 'INTO', 'VALUES',
    'ASC', 'DESC', 'RIGHT', 'LEFT', 'INNER', 'FULL', 'JOIN', 'ON', 'AS', 
    'SUM', 'AVG', 'COUNT', 'MAX', 'MIN', 'UPPER', 'LOWER', 'AND', 'OR', 'LIKE', 'IS', 'NOT', 'NULL', 
    'users', 'orders', 'id', 'email', 'first_name', 'last_name', 'user_id', 'date', 'amount',
    '<=', '>=', '!=', '+', '-', '*', '/', '=', '<', '>', '(', ')'
]

keywords = defaultdict(set)
for k in keyword_list:
    keywords[len(k)].add(k)

class Parser:
    def __init__(self, input):
        self.input, self.input_index_map = self.tokenize(input)
        
        self.index = 0

    def tokenize(self, input):
        tokenized_input = []
        index_map = []
        i = 0
        while i < len(input):
            i = self.skip_whitespace(input, i)
            token = None
            substring = input[i:]

            # string
            match = re.search(r"^'(.*?)'", substring)
            if not token and match:
                token = substring[match.start():match.end()]

            # float - its important to do this before int
            match = re.search(r"^\d+\.\d+", substring)
            if not token and match:
                token = substring[match.start():match.end()]

            # integer
            match = re.search(r"^\d+", substring)
            if not token and match:
                token = substring[match.start():match.end()]

            # multi-line comments
            match = re.search(r"^/\*.*?\*/", substring)
            if not token and match:
                token = substring[match.start():match.end()]

            if not token:    
                for l in sorted(keywords.keys(), reverse=True):
                    if substring[:l] in keywords[l]:
                        token = substring[:l]
                        break
            
            if token is not None:
                tokenized_input.append(token)
                index_map.append((i, i + len(token)))
                i += len(token)
            elif substring.strip() == '': # check for empty string
                break
            else:
                raise Exception(f'Failed to tokenize input. Error encountered on character {i}')
        
        return tokenized_input, index_map
    
    def skip_whitespace(self, input, i):
        pattern = r'\S'
        match = re.search(pattern, input[i:])
        if match:
            return i + match.end() - 1
        else:
            return i
        
    def consume(self, token):
        try:
            if self.peek() == token:
                self.index += 1
            else:
                self.raise_exception(token)
        except IndexError as e:
            raise self.raise_exception(token, len(self.input - 1), 'None') # TODO: fix the length calculation here

    def peek(self):
        if self.index < len(self.input):
            return self.input[self.index]
        else:
            return None
    
    def look_ahead(self):
        if self.index + 1 < len(self.input):
            return self.input[self.index + 1]
        else: 
            return None

    def look_ahead_n(self, n):
        if self.index + n < len(self.input):
            return self.input[self.index + n]
        else: 
            return None

    def raise_exception(self, expected, i = None, got = None):
        # i = token index
        error_stmt = f'Syntax Error at {i if i else self.index }. Got {got if got else self.peek()}, but expected {"one of:" if isinstance(expected, list) else ""}{expected}'
        raise SyntaxError(error_stmt)

    def parse(self):
        try:
            self.parse_condition()
            if self.index == len(self.input):
                return 'Parsed'
            else:
                self.raise_exception('<longer input>')
        except SyntaxError as e:
            return e.msg

    # databas tables & fields
    def parse_table(self):
        tables = ['users', 'orders']
        if self.peek() in tables:    
            self.consume(self.peek())
        else:
            self.raise_exception(tables)

    def parse_field(self):
        fields = ['id', 'email', 'first_name', 'last_name', 'user_id', 'date', 'amount']
        if self.peek() in fields:    
            self.consume(self.peek())
        else:
            self.raise_exception(fields)
        
    def parse_table_field(self):
        fields = ['id', 'email', 'first_name', 'last_name', 'user_id', 'date', 'amount']
        if self.peek() in fields:
            self.parse_field()
        else:
            self.parse_table()
            self.consume('.')
            self.parse_field()
        
    # basic definitions
    def parse_string(self):
        match = re.search(r"^'[^']*'$", self.peek())
        if match:
            self.consume(self.peek())
        else:
            self.raise_exception('<string>')
        
    def parse_float(self):
        match = re.search(r"^\d+\.\d+$", self.peek())
        if match:
            self.consume(self.peek())
        else:
            self.raise_exception('<float>')

    def parse_integer(self):
        match = re.search(r"^\d+$", self.peek())
        if match:
            self.consume(self.peek())
        else:
            self.raise_exception('<float>')

    def parse_value(self):
        if self.peek() is not None and re.search(r"^'[^']*'$", self.peek()):
            self.parse_string()
        elif self.peek() is not None and re.search(r"^\d+\.\d+$", self.peek()): # important that float be done first since it overlaps with integer definition
            self.parse_float()
        elif self.peek() is not None and  re.search(r"^\d+$", self.peek()):
            self.parse_integer()
        else:
            self.raise_exception(['<string>', '<float>', '<integer>'])

    def parse_alias(self):
        self.parse_string()
    
    def parse_function(self):
        functions = ['SUM', 'AVG', 'COUNT', 'MAX', 'MIN', 'UPPER', 'LOWER']
        if self.peek() in functions:
             self.consume(self.peek())
        else:
            self.raise_exception(functions)
    
    def parse_math_operator(self):
        math_operators = ['+', '-', '*', '/']
        if self.peek() in math_operators:
             self.consume(self.peek())
        else:
            self.raise_exception(math_operators)
        
    def parse_comparison_operator(self):
        comparison_operators = ['<=', '>=', '!=', '=', '<', '>']
        if self.peek() in comparison_operators:
             self.consume(self.peek())
        else:
            self.raise_exception(comparison_operators)

    def parse_term(self):
        if self.peek() == '(':
            self.consume('(')
            self.parse_math_expression()
            self.consume(')')
        elif self.peek() is not None and (re.search(r"^'[^']*'$", self.peek()) or re.search(r"^\d+\.\d+$", self.peek()) or re.search(r"^\d+$", self.peek())):
            self.parse_value()
        else:
            self.parse_table_field()
        
    def parse_math_expression(self):
        functions = ['SUM', 'AVG', 'COUNT', 'MAX', 'MIN', 'UPPER', 'LOWER']
        math_operators = ['+', '-', '*', '/']
        if self.peek() in functions:
            self.parse_function()
            self.consume('(')
            self.parse_function_body()
            self.consume(')')
        else:
            self.parse_term()
            if self.peek() in math_operators: # optional part
                self.parse_optional_math_clause()
        
    def parse_function_body(self):
        if self.peek() == '*':
            self.consume('*')
        else:
            self.parse_math_expression()

    def parse_optional_math_clause(self):
        math_operators = ['+', '-', '*', '/']
        self.parse_math_operator() 
        self.parse_term()
        if self.peek() in math_operators: # optional part
            self.parse_optional_math_clause()

    def parse_boolean_expression(self):
        tables = ['users', 'orders']
        fields = ['id', 'email', 'first_name', 'last_name', 'user_id', 'date', 'amount']
        if (self.peek() in fields and self.look_ahead() in ['LIKE', 'IS']) or \
           (self.peek() in tables and self.look_ahead() == '.' and self.look_ahead_n(2) in fields and self.look_ahead_n(3) in ['LIKE', 'IS']): # look-ahead for <table-field> followed by LIKE or IS
            self.parse_table_field()
            if self.peek() == 'LIKE':
                self.consume('LIKE')
                self.parse_string()
            elif self.peek() == 'IS':
                self.consume('IS')
                if self.peek() == 'NOT': # optional
                    self.consume('NOT')
                self.consume('NULL')
            else:
                self.raise_exception(['LIKE <string>', 'IS [NOT] NULL'])
        else:
            self.parse_math_expression()
            self.parse_comparison_operator()
            self.parse_math_expression()
    
    def parse_condition(self):
        self.parse_boolean_expression()
        if self.peek() in ['AND', 'OR']:
            self.consume(self.peek())
            self.parse_condition()

        
        
                
        





test_cases = [
    "users.id = 3 AND",
]

for test in test_cases:
    parser = Parser(test)
    print(parser.parse())

 