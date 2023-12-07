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
        self.input = self.tokenize(input)
        self.index = 0

    def tokenize(self, input):
        tokenized_input = []
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
                i += len(token)
            elif substring.strip() == '': # check for empty string
                break
            else:
                raise Exception(f'Failed to tokenize input. Error encounterede on character {i}')
        
        return tokenized_input
    
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
        raise Exception('fix this first')
        return self.input[self.index + n]

    def raise_exception(self, expected, i = None, got = None):
        # i = token index
        error_stmt = f'Syntax Error at {i if i else self.index }. Got {got if got else self.peek()}, but expected {"one of:" if isinstance(expected, list) else ""}{expected}'
        raise SyntaxError(error_stmt)

    def parse(self):
        try:
            self.parse_table_field()
            return 'Parsed'
        except SyntaxError as e:
            return e

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
        







strings = [
    'users.id',
    'email',
    'orders.amount',
    'orders)'
]
for s in strings:
    parser = Parser(s)
    print(parser.parse())

 