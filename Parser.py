from Scanner import Scanner
from Lookup_Table import Lookup_Table


####################################### Parser Class ##############################################

class Parser:
    # Constructor for the parser that sets it up to be used for parsing tokens from a line
    def __init__(self):
        self.tokens = []
        self.tree = {}
        self.node = self.tree
        self.scanner = Scanner()
        self.position = 0

    # Function that first scans the line for tokens and then parses those tokens
    # to make sure that the grammar of the tokens are correct and builds a parset tree as
    # it parses the tokens
    def parse(self, line):
        self.position = 0
        self.tree.clear()
        self.node = self.tree

        self.scanner.extract_tokens(line)
        self.tokens = self.scanner.tokens
        while self.position < len(self.tokens):
            if self.tokens[self.position].token == Lookup_Table.keywords["REM"] or self.tokens[self.position].token == \
                    Lookup_Table.keywords["END"]:
                self.node["value"] = self.tokens[self.position]
                return
            elif self.tokens[self.position].token == Lookup_Table.keywords["LET"]:
                self.assign_stmt()
            elif self.tokens[self.position].token == Lookup_Table.keywords["PRINT"]:
                self.print_statement()
            elif self.tokens[self.position].token == Lookup_Table.keywords["INPUT"]:
                self.input_statement()
            elif self.tokens[self.position].token == Lookup_Table.keywords["IF"]:
                self.if_statement()

            else:
                raise Exception('Invalid statement, line ' + self.scanner.line_number)

    # Function that formats the parser to display its parse tree when printed
    def __repr__(self):
        return "%s" % self.tree

    # Function that advances the parser's position to the next token if position is less
    #   than the number of tokens scanned
    def next_token(self):
        if self.position < len(self.tokens):
            self.position += 1

    # Function that checks that the tokens scanned macthes the grammar of an assign
    #   statement and adds them correctly to the parse tree
    def assign_stmt(self):
        if self.position + 3 >= len(self.tokens):
            raise Exception('Invalid assignment statement, line ' + self.scanner.line_number)

        boolean_tokens = [Lookup_Table.keywords["AND"], Lookup_Table.keywords["OR"], Lookup_Table.keywords["NOT"],
                          Lookup_Table.symbols[">"], Lookup_Table.symbols[">="], Lookup_Table.symbols["<"],
                          Lookup_Table.symbols["<="], Lookup_Table.symbols["<>"], Lookup_Table.identifiers["BOOL_ID"],
                          Lookup_Table.constants["BOOL_LITERAL"]]

        let_token = self.tokens[self.position]
        self.next_token()
        ltoken = self.tokens[self.position]
        self.next_token()
        equal_token = self.tokens[self.position]
        self.next_token()

        if let_token.token != Lookup_Table.keywords["LET"]:
            raise Exception('Invalid assign statement, line ' + self.scanner.line_number)
        elif ltoken.token < 31 or ltoken.token > 34 or equal_token.lexeme != "=":
            raise Exception('Invalid assign statement, line ' + self.scanner.line_number)

        expr_tokens = []
        bool_tokens = []
        is_bool_expression = False
        while self.position < len(self.tokens) and self.tokens[self.position].lexeme != ":":
            if self.tokens[self.position].token in boolean_tokens:
                is_bool_expression = True
            expr_tokens.append(self.tokens[self.position])
            self.next_token()

        if is_bool_expression:
            bool_tokens = expr_tokens
            while self.position < len(self.tokens) and self.tokens[self.position].lexeme != ":":
                bool_tokens.append(self.tokens[self.position])
                self.next_token()

        # print(expr_tokens)
        if self.position != len(self.tokens):
            self.next_token()

        self.node["value"] = let_token
        self.node["left"] = {}
        self.node = self.node["left"]

        self.node["value"] = equal_token
        self.node["left"] = {"value": ltoken}
        self.node["right"] = {}
        self.node = self.node["right"]

        if len(bool_tokens) == 0:
            self.expression(expr_tokens, 0)
        else:
            self.bool_expression(bool_tokens, 0)

    # Function that checks that the tokens scanned macthes the grammar of a factor
    #   and adds them correctly to the parse tree
    def factor(self, tokens, index):
        if index >= len(tokens):
            raise Exception('Invalid expression, line ' + self.scanner.line_number)
        elif 31 <= tokens[index].token <= 38:
            self.node["value"] = tokens[index]
            return index + 1
        elif tokens[index].token == 15:
            self.node["value"] = tokens[index]
            index += 1
            if tokens[index].lexeme != "(":
                raise Exception('Invalid expression, line ' + self.scanner.line_number)
            else:
                index += 1
                start_index = index
                p_count = 1
                while index < len(tokens) and p_count != 0:
                    if tokens[index].lexeme == "(":
                        p_count += 1
                    elif tokens[index].lexeme == ")":
                        p_count -= 1
                    index += 1
                if p_count != 0:
                    raise Exception('Invalid expression, line ' + self.scanner.line_number)
                else:
                    end_index = index - 1
                    prev_node = self.node
                    self.node["left"] = {}
                    self.node["right"] = {}
                    self.node = self.node["right"]
                    self.expression(tokens[start_index:end_index], 0)
                    self.node = prev_node
                    return index
        elif tokens[index].lexeme != "(":
            raise Exception('Invalid expression, line ' + self.scanner.line_number)
        else:
            index += 1
            start_index = index
            p_count = 1
            while index < len(tokens) and p_count != 0:
                if tokens[index].lexeme == "(":
                    p_count += 1
                elif tokens[index].lexeme == ")":
                    p_count -= 1
                index += 1
            if p_count != 0:
                raise Exception('Invalid expression, line ' + self.scanner.line_number)
            else:
                end_index = index - 1
                prev_node = self.node
                self.expression(tokens[start_index:end_index], 0)
                self.node = prev_node
                return index

    # Function that checks that the tokens scanned macthes the grammar of a term
    #   and adds them correctly to the parse tree
    def term(self, tokens, index):
        if index >= len(tokens):
            raise Exception('Invalid expression, line ' + self.scanner.line_number)

        index = self.factor(tokens, index)
        parent = self.node
        while index != len(tokens) and (tokens[index].lexeme == "*" or tokens[index].lexeme == "/"):
            if "right" in parent:
                temp_node = {"value": parent["value"], "left": parent["left"], "right": parent["right"]}
                parent["value"] = tokens[index]
                parent["left"] = temp_node
                parent["right"] = {}
                self.node = parent["right"]
                index = self.factor(tokens, index + 1)
            elif "left" in parent:
                left_node = parent["left"]
                parent["left"] = {"value": parent["value"]}
                parent["value"] = tokens[index]
                parent["left"]["left"] = left_node
                parent["right"] = {}
                self.node = parent["right"]
                index = self.factor(tokens, index + 1)
            else:
                parent["left"] = {"value": parent["value"]}
                parent["value"] = tokens[index]
                parent["right"] = {}
                self.node = parent["right"]
                index = self.factor(tokens, index + 1)
        return index

    # Function that checks that the tokens scanned macthes the grammar of an expression
    #   and adds them correctly to the parse tree
    def expression(self, tokens, index):
        if len(tokens) == 0:
            raise Exception('Invalid expression, line ' + self.scanner.line_number)

        index = self.term(tokens, index)
        parent = self.node

        while index != len(tokens) and (tokens[index].lexeme == "+" or tokens[index].lexeme == "-"):
            if "right" in parent:
                temp_node = {"value": parent["value"], "left": parent["left"], "right": parent["right"]}

                parent["value"] = tokens[index]
                parent["left"] = temp_node
                parent["right"] = {}
                self.node = parent["right"]
                index = self.term(tokens, index + 1)
            elif "left" in parent:
                left_node = parent["left"]
                parent["left"] = {"value": parent["value"]}
                parent["value"] = tokens[index]
                parent["left"]["left"] = left_node
                parent["right"] = {}
                self.node = parent["right"]
                index = self.term(tokens, index + 1)
            else:
                parent["left"] = {"value": parent["value"]}
                parent["value"] = tokens[index]
                parent["right"] = {}
                self.node = parent["right"]
                index = self.term(tokens, index + 1)
        if index != len(tokens):
            raise Exception('Invalid expression, line ' + self.scanner.line_number)

    # Function that checks that the tokens scanned macthes the grammar of an input
    #    statement and adds them correctly to the parse tree
    def input_statement(self):
        if self.position + 1 >= len(self.tokens):
            raise Exception('Invalid input statement, line ' + self.scanner.line_number)

        input_token = self.tokens[self.position]
        self.node["value"] = input_token

        self.next_token()
        # input x
        if 31 <= self.tokens[self.position].token <= 34:
            prev_token_is_comma = False
            while self.position < len(self.tokens):
                if 31 <= self.tokens[self.position].token <= 34:
                    if "right" in self.node:
                        self.node = self.node["left"]
                        self.node["left"] = {"value": self.tokens[self.position]}
                    elif "left" in self.node:
                        self.node["right"] = {"value": self.tokens[self.position]}
                    elif "value" in self.node:
                        self.node["left"] = {"value": self.tokens[self.position]}
                    else:
                        self.node["value"] = self.tokens[self.position]
                    prev_token_is_comma = False
                elif self.tokens[self.position].lexeme == ",":
                    if prev_token_is_comma:
                        raise Exception('Invalid input statement, line ' + self.scanner.line_number)
                    prev_token_is_comma = True
                else:
                    raise Exception('Invalid input statement, line ' + self.scanner.line_number)
                self.next_token()
        elif self.position + 2 < len(self.tokens) and self.tokens[self.position].token == 35 and self.tokens[
            self.position + 1].token == 28 and 31 <= self.tokens[self.position + 2].token <= 34:
            str_lit = self.tokens[self.position]
            self.next_token()
            input_semicolon = self.tokens[self.position]
            self.next_token()

            self.node["value"] = input_token
            self.node["left"] = {"value": str_lit}
            self.node["right"] = {}
            self.node = self.node["right"]

            prev_token_is_comma = False
            while self.position < len(self.tokens):
                if 31 <= self.tokens[self.position].token <= 34:
                    if "right" in self.node:
                        self.node = self.node["left"]
                        self.node["left"] = {"value": self.tokens[self.position]}
                    elif "left" in self.node:
                        self.node["right"] = {"value": self.tokens[self.position]}
                    elif "value" in self.node:
                        self.node["left"] = {"value": self.tokens[self.position]}
                    else:
                        self.node["value"] = self.tokens[self.position]
                    prev_token_is_comma = False
                elif self.tokens[self.position].lexeme == ",":
                    if prev_token_is_comma:
                        raise Exception('Invalid input statement, line ' + self.scanner.line_number)
                    prev_token_is_comma = True
                else:
                    raise Exception('Invalid input statement, line ' + self.scanner.line_number)
                self.next_token()
        else:
            raise Exception('Invalid input statement, line ' + self.scanner.line_number)

    # Function that checks that the tokens scanned macthes the grammar of a print statement
    #   and adds them correctly to the parse tree
    def print_statement(self):
        if self.position >= len(self.tokens):
            raise Exception('Invalid print statement, line ' + self.scanner.line_number)
        print_token = self.tokens[self.position]
        self.node["value"] = print_token
        self.next_token()
        if self.position != len(self.tokens):
            self.node["right"] = {}
            self.node = self.node["right"]
            print_tokens = []
            bool_tokens = [Lookup_Table.keywords["AND"], Lookup_Table.keywords["OR"], Lookup_Table.keywords["NOT"],
                           Lookup_Table.symbols[">"], Lookup_Table.symbols[">="], Lookup_Table.symbols["<"],
                           Lookup_Table.symbols["<="], Lookup_Table.symbols["<>"], Lookup_Table.identifiers["BOOL_ID"],
                           Lookup_Table.constants["BOOL_LITERAL"]]
            bool_expr = False

            while True:
                while self.tokens[self.position].lexeme != "," and self.tokens[self.position].lexeme != ";" and \
                        self.tokens[self.position].lexeme != ":":
                    if self.tokens[self.position].token in bool_tokens:
                        bool_expr = True
                    print_tokens.append(self.tokens[self.position])
                    self.next_token()
                    if self.position >= len(self.tokens):
                        break
                prev_node = self.node
                if self.position >= len(self.tokens) or self.tokens[self.position].lexeme == ":":
                    if "left" in self.node:
                        self.node["right"] = {}
                        self.node = self.node["right"]
                        if bool_expr:
                            self.bool_expression(print_tokens, 0)
                        else:
                            self.expression(print_tokens, 0)
                        self.node = prev_node
                    else:
                        if bool_expr:
                            self.bool_expression(print_tokens, 0)
                        else:
                            self.expression(print_tokens, 0)
                        self.node = prev_node
                    if self.position < len(self.tokens) and self.tokens[self.position].lexeme == ":":
                        self.next_token()
                    break
                elif self.tokens[self.position].lexeme == "," or self.tokens[self.position].lexeme == ";":
                    if self.position == 1 or len(print_tokens) == 0:
                        raise Exception('Invalid print statement, line ' + self.scanner.line_number)
                    elif "left" in self.node:
                        self.node["right"] = {}
                        self.node = self.node["right"]
                    self.node["value"] = self.tokens[self.position]
                    self.node["left"] = {}
                    prev_node = self.node
                    self.node = self.node["left"]
                    if bool_expr:
                        self.bool_expression(print_tokens, 0)
                    else:
                        self.expression(print_tokens, 0)
                    self.node = prev_node

                    self.next_token()
                    print_tokens.clear()
                    bool_expr = False
                else:
                    raise Exception('Invalid print statement, line ' + self.scanner.line_number)

    # Function that checks that the tokens scanned macthes the grammar of a if statement
    #   and adds them correctly to the parse tree
    def if_statement(self):
        if self.position + 3 >= len(self.tokens):
            raise Exception('Invalid if statement, line ' + self.scanner.line_number)

        if_token = self.tokens[self.position]
        self.next_token()

        bool_expr_tokens = []
        while self.position < len(self.tokens) and self.tokens[self.position].token != 8:
            bool_expr_tokens.append(self.tokens[self.position])
            self.next_token()

        if self.position < len(self.tokens) and self.tokens[self.position].token == 8:
            then_token = self.tokens[self.position]
            self.next_token()

            self.node["value"] = if_token
            self.node["left"] = {"value": then_token}

            self.node = self.node["left"]
            self.node["left"] = {}
            self.node["right"] = {}
            prev_node = self.node
            self.node = self.node["left"]
            self.bool_expression(bool_expr_tokens, 0)
            self.node = prev_node["right"]

            if self.tokens[self.position].token == Lookup_Table.keywords["LET"]:
                self.assign_stmt()
            elif self.tokens[self.position].token == Lookup_Table.keywords["PRINT"]:
                self.print_statement()
            elif self.tokens[self.position].token == Lookup_Table.keywords["INPUT"]:
                self.input_statement()
            else:
                raise Exception('Invalid if statement, line ' + self.scanner.line_number)
        else:
            raise Exception('Invalid if statement, line ' + self.scanner.line_number)

    # Function that checks that the tokens scanned macthes the grammar of a bool
    #   and adds them correctly to the parse tree
    def bool_(self, tokens, index):
        if index >= len(tokens):
            raise Exception('Invalid bool expression, line ' + self.scanner.line_number)
        elif tokens[index].token == 34 or tokens[index].token == 38:
            self.node["value"] = tokens[index]
            return index + 1
        else:
            bool_tokens = [Lookup_Table.keywords["AND"], Lookup_Table.keywords["OR"],
                           Lookup_Table.keywords["NOT"], Lookup_Table.identifiers["BOOL_ID"],
                           Lookup_Table.constants["BOOL_LITERAL"]]
            bool_symbols = [Lookup_Table.symbols[">"], Lookup_Table.symbols[">="], Lookup_Table.symbols["<"],
                            Lookup_Table.symbols["<="], Lookup_Table.symbols["<>"]]

            expr1_tokens = []
            while index < len(tokens) and tokens[index].token not in bool_symbols:
                if tokens[index].token in bool_tokens:
                    raise Exception('Invalid bool expression, line ' + self.scanner.line_number)
                else:
                    expr1_tokens.append(tokens[index])
                    index += 1

            if index < len(tokens) and len(expr1_tokens) > 0 and tokens[index].token in bool_symbols:
                bool_symbol = tokens[index]
                index += 1
                expr2_tokens = []
                while index < len(tokens) and tokens[index].token not in bool_symbols and tokens[
                    index].token not in bool_tokens:
                    expr2_tokens.append(tokens[index])
                    index += 1
                self.node["value"] = bool_symbol
                self.node["left"] = {}
                self.node["right"] = {}
                prev_node = self.node
                self.node = self.node["left"]
                self.expression(expr1_tokens, 0)
                self.node = prev_node["right"]
                self.expression(expr2_tokens, 0)
                self.node = prev_node
                return index
            else:
                raise Exception('Invalid bool expression, line ' + self.scanner.line_number)

    # Function that checks that the tokens scanned macthes the grammar of a bool factor
    #   and adds them correctly to the parse tree
    def bool_factor(self, tokens, index):
        if index >= len(tokens):
            raise Exception('Invalid bool expression, line ' + self.scanner.line_number)
        elif tokens[index].token == 13:
            not_token = tokens[index]
            index += 1
            if index < len(tokens) and tokens[index].lexeme == "(":
                index += 1
                start_index = index
                p_count = 1
                while index < len(tokens) and p_count != 0:
                    if tokens[index].lexeme == "(":
                        p_count += 1
                    elif tokens[index].lexeme == ")":
                        p_count -= 1
                    index += 1
                if p_count != 0:
                    raise Exception('Invalid bool expression, line ' + self.scanner.line_number)
                else:
                    end_index = index - 1
                    self.node["value"] = not_token
                    self.node["left"] = {}
                    prev_node = self.node
                    self.node = self.node["left"]
                    self.bool_expression(tokens[start_index:end_index], 0)
                    self.node = prev_node
                    return index
            else:
                raise Exception('Invalid bool expression, line ' + self.scanner.line_number)
        elif tokens[index].lexeme == "(":
            index += 1
            start_index = index
            p_count = 1
            while index < len(tokens) and p_count != 0:
                if tokens[index].lexeme == "(":
                    p_count += 1
                elif tokens[index].lexeme == ")":
                    p_count -= 1
                index += 1
            if p_count != 0:
                raise Exception('Invalid bool expression, line ' + self.scanner.line_number)
            else:
                end_index = index - 1
                prev_node = self.node
                self.bool_expression(tokens[start_index:end_index], 0)
                self.node = prev_node
                return index
        else:
            return self.bool_(tokens, index)

    # Function that checks that the tokens scanned macthes the grammar of a bool term
    #   and adds them correctly to the parse tree
    def bool_term(self, tokens, index):
        if index >= len(tokens):
            raise Exception('Invalid bool expression, line ' + self.scanner.line_number)
        index = self.bool_factor(tokens, index)
        parent = self.node

        while index != len(tokens) and (tokens[index].lexeme.upper() == "AND"):
            if "right" in parent:
                temp_node = {"value": parent["value"], "left": parent["left"], "right": parent["right"]}
                parent["value"] = tokens[index]
                parent["left"] = temp_node
                parent["right"] = {}
                self.node = parent["right"]
                index = self.bool_factor(tokens, index + 1)
            elif "left" in parent:
                left_node = parent["left"]
                parent["left"] = {"value": parent["value"]}
                parent["value"] = tokens[index]
                parent["left"]["left"] = left_node
                parent["right"] = {}
                self.node = parent["right"]
                index = self.bool_factor(tokens, index + 1)
            else:
                parent["left"] = {"value": parent["value"]}
                parent["value"] = tokens[index]
                parent["right"] = {}
                self.node = parent["right"]
                index = self.bool_factor(tokens, index + 1)
        return index

    # Function that checks that the tokens scanned macthes the grammar of a bool expression
    #   and adds them correctly to the parse tree
    def bool_expression(self, tokens, index):
        if len(tokens) == 0:
            raise Exception('Invalid bool expression, line ' + self.scanner.line_number)

        index = self.bool_term(tokens, index)
        parent = self.node

        while index != len(tokens) and tokens[index].lexeme.upper() == "OR":
            if "right" in parent:
                temp_node = {"value": parent["value"], "left": parent["left"], "right": parent["right"]}

                parent["value"] = tokens[index]
                parent["left"] = temp_node
                parent["right"] = {}
                self.node = parent["right"]
                index = self.bool_term(tokens, index + 1)
            elif "left" in parent:
                left_node = parent["left"]
                parent["left"] = {"value": parent["value"]}
                parent["value"] = tokens[index]
                parent["left"]["left"] = left_node
                parent["right"] = {}
                self.node = parent["right"]
                index = self.bool_term(tokens, index + 1)
            else:
                parent["left"] = {"value": parent["value"]}
                parent["value"] = tokens[index]
                parent["right"] = {}
                self.node = parent["right"]
                index = self.bool_term(tokens, index + 1)
        if index != len(tokens):
            raise Exception('Invalid bool expression, line ' + self.scanner.line_number)
