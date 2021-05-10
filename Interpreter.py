from Token_Obj import Token_Obj
from Lookup_Table import Lookup_Table
from Parser import Parser
import operator

class Interpreter:
    # Constructor for the interpeter that sets up the parser to be used
    #   for parsing lines and the other variables needed for interprerting
    #   statements correctly
    def __init__(self):
        self.parser = Parser()
        self.variables = {}
        self.EOF = False

    # Function used for first parsing and generating the parse tree from
    #   a line of code and then determining what function to call to 
    #   process the parse tree and interpret it
    def interpret(self, line):
        if not self.EOF:
            self.parser.parse(line)
            if self.parser.tree["value"].token == Lookup_Table.keywords["LET"]:
                node = self.parser.tree["left"]
                self.interpret_let(node)
            elif self.parser.tree["value"].token == Lookup_Table.keywords["PRINT"]:
                node = self.parser.tree
                self.interpret_print(node)
            elif self.parser.tree["value"].token == Lookup_Table.keywords["IF"]:
                node = self.parser.tree["left"]
                self.interpret_if(node)
            elif self.parser.tree["value"].token == Lookup_Table.keywords["INPUT"]:
                node = self.parser.tree
                self.interpret_input(node)
            elif self.parser.tree["value"].token == Lookup_Table.keywords["REM"]:
                return
            elif self.parser.tree["value"].token == Lookup_Table.keywords["END"]:
                self.EOF = True
                return

    # Function used for interpreting a let statement
    def interpret_let(self, node):
        expr_tokens = [Lookup_Table.symbols["+"], Lookup_Table.symbols["-"], Lookup_Table.symbols["*"], Lookup_Table.symbols["/"], Lookup_Table.keywords["INT"], Lookup_Table.identifiers["INT_ID"], Lookup_Table.identifiers["REAL_ID"], Lookup_Table.constants["INT_LITERAL"], Lookup_Table.constants["REAL_LITERAL"], Lookup_Table.constants["STRING_LITERAL"], Lookup_Table.identifiers["STRING_ID"]]
        if node["right"]["value"].token in expr_tokens:
            self.interpret_expr(node["right"])
        else:
            self.interpret_bool_expr(node["right"])
        variable = node["left"]["value"].lexeme
        self.variables[variable] = {"value": node["right"]["value"], "type": self.determine_type(node["right"]["value"])}
    
    # Function used for interpreting a print statement and 
    #   outputting the results correctly
    def interpret_print(self, node):
        expr_tokens = [Lookup_Table.symbols["+"], Lookup_Table.symbols["-"], Lookup_Table.symbols["*"], Lookup_Table.symbols["/"], Lookup_Table.keywords["INT"], Lookup_Table.identifiers["INT_ID"], Lookup_Table.identifiers["REAL_ID"], Lookup_Table.constants["INT_LITERAL"], Lookup_Table.constants["REAL_LITERAL"]]
        bool_tokens = [Lookup_Table.keywords["AND"], Lookup_Table.keywords["OR"], Lookup_Table.keywords["NOT"],
                       Lookup_Table.symbols[">"], Lookup_Table.symbols[">="], Lookup_Table.symbols["<"],
                       Lookup_Table.symbols["<="], Lookup_Table.symbols["<>"], Lookup_Table.identifiers["BOOL_ID"],
                       Lookup_Table.constants["BOOL_LITERAL"]]
        if "right" in node:
            while "right" in node:
                node = node["right"]
                if node["value"].token in expr_tokens:
                    self.interpret_expr(node)
                    print(node["value"])
                elif node["value"].token in bool_tokens:
                    self.interpret_bool_expr(node)
                    print(node["value"])
                elif isinstance(node["value"], Token_Obj) and (node["value"].token == Lookup_Table.constants["STRING_LITERAL"] or node["value"].token == Lookup_Table.identifiers["STRING_ID"]):
                    print(self.get_token_value(node["value"]))
                elif node["value"].lexeme == ',':
                    prev_node = node
                    node = node["left"]
                    self.interpret_expr(node)
                    print(node["value"], end="\t")
                    node = prev_node
                else:
                    prev_node = node
                    node = node["left"]
                    self.interpret_expr(node)
                    print(node["value"], end=" ")
                    node = prev_node
        else:
            print()

    # Function used for interpreting an if statement and then calling the 
    #   correct function if the if statement is true to interpret the code
    #   after the then part of the if statement
    def interpret_if(self, node):
        bool_node = node["left"]
        self.interpret_bool_expr(bool_node)
        if bool_node["value"] == True:
            then_node = node["right"]
            #finish this once the other functions of the interpreter are 
            if then_node["value"].token == Lookup_Table.keywords["LET"]:
                self.interpret_let(then_node["left"])
            elif then_node["value"].token == Lookup_Table.keywords["PRINT"]:
                self.interpret_print(then_node)
            elif then_node["value"].token == Lookup_Table.keywords["INPUT"]:
                self.interpret_input(then_node)

    # Function used for interpreting an input statement and getting
    #   input from the user
    def interpret_input(self, node):
        if node["left"]["value"].token == Lookup_Table.constants["STRING_LITERAL"]:
            print(node["left"]["value"].lexeme)
            node = node["right"]
        else:
            node = node["left"]
        queue = []
        queue.append(node)
        while len(queue) != 0:
            q_node = queue.pop(0)
            variable = q_node["value"].lexeme
            num_inputted = False
            while not num_inputted:
                user_input = input()
                try:
                    int_input = int(user_input)
                    num_inputted = True
                    self.variables[variable] = {"value": int_input, "type": "INT_ID"}
                    if "left" in q_node:
                        queue.append(q_node["left"])
                    if "right" in q_node:
                        queue.append(q_node["right"])
                except ValueError:
                    try:
                        # print("2: " + user_input)
                        float_input = float(user_input)
                        num_inputted = True
                        self.variables[variable] = {"value": float_input, "type": "REAL_ID"}
                        if "left" in q_node:
                            queue.append(q_node["left"])
                        if "right" in q_node:
                            queue.append(q_node["right"])
                    except ValueError:
                        print("Number expected. Enter a number")

    # Function used for determing what type an identifier should be based
    #   off the data type of the value passed to this function
    def determine_type(self, value):
        if isinstance(value, bool):
            return "BOOL_ID"
        elif isinstance(value, int):
            return "INT_ID"
        elif isinstance(value, float):
            return "REAL_ID"
        else:
            return "STRING_ID"

    # Function used for converting the lexeme of a token_obj to its actual
    #   value in the correct data type
    def get_token_value(self, token_obj):
        if token_obj.lexeme in self.variables and self.variables[token_obj.lexeme]["type"] == "REAL_ID":
            return float(self.variables[token_obj.lexeme]["value"])
        elif token_obj.token == Lookup_Table.identifiers["STRING_ID"]:
            return self.variables[token_obj.lexeme]["value"]
        elif token_obj.token == Lookup_Table.constants["STRING_LITERAL"]:
            return token_obj.lexeme
        elif token_obj.token == Lookup_Table.identifiers["INT_ID"]:
            return int(self.variables[token_obj.lexeme]["value"])
        elif token_obj.token == Lookup_Table.constants["INT_LITERAL"]:
            return int(token_obj.lexeme)
        elif token_obj.token == Lookup_Table.constants["REAL_LITERAL"]:
            return float(token_obj.lexeme)
        elif token_obj.token == Lookup_Table.identifiers["BOOL_ID"]:
            return bool(self.variables[token_obj.lexeme]["value"])
        elif token_obj.lexeme.lower() == "true":
            return True
        elif token_obj.lexeme.lower() == "false":
            return False
        else:
            raise Exception('Invalid expression, line ' + self.parser.scanner.line_number)

    # Function used for interpreting expressions
    def interpret_expr(self, node):
        if "left" not in node and "right" not in node:
            node["value"] = self.get_token_value(node["value"])
            return
        elif node["value"].token == Lookup_Table.keywords["INT"]:
            self.interpret_expr(node["right"])
            node["value"] = int(node["right"]["value"])
            del node["right"]["value"]
            del node["right"]
        else:
            self.interpret_expr(node["left"])
            self.interpret_expr(node["right"])
            ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
            operand1 = node["left"]["value"]
            operand2 = node["right"]["value"]
            node["value"] = ops[node["value"].lexeme](operand1, operand2)
            del node["left"]["value"]
            del node["right"]["value"]
            del node["left"]
            del node["right"]

    # Function used for interpreting bool expressions
    def interpret_bool_expr(self, node):
        expr_tokens = [Lookup_Table.symbols["+"], Lookup_Table.symbols["-"], Lookup_Table.symbols["*"], Lookup_Table.symbols["/"], Lookup_Table.keywords["INT"], Lookup_Table.identifiers["INT_ID"], Lookup_Table.identifiers["REAL_ID"], Lookup_Table.constants["INT_LITERAL"], Lookup_Table.constants["REAL_LITERAL"]]
        if "left" not in node and "right" not in node:
            node["value"] = self.get_token_value(node["value"])
            return
        else:
            expr_ops = {'>': operator.gt, '>=': operator.ge, '<': operator.lt, '<=': operator.le, '<>': operator.ne}
            if node["value"].lexeme in expr_ops:
                self.interpret_expr(node["left"])
                self.interpret_expr(node["right"])
                left_value = node["left"]["value"]
                right_value = node["right"]["value"]
                node["value"] = expr_ops[node["value"].lexeme](left_value, right_value)
                del node["left"]["value"]
                del node["right"]["value"]
                del node["left"]
                del node["right"]
            elif node["value"].token == Lookup_Table.keywords["AND"]:
                self.interpret_bool_expr(node["left"])
                self.interpret_bool_expr(node["right"])
                left_value = node["left"]["value"]
                right_value = node["right"]["value"]
                node["value"] = left_value and right_value
                del node["left"]["value"]
                del node["right"]["value"]
                del node["left"]
                del node["right"]
            elif node["value"].token == Lookup_Table.keywords["OR"]:
                self.interpret_bool_expr(node["left"])
                self.interpret_bool_expr(node["right"])
                left_value = node["left"]["value"]
                right_value = node["right"]["value"]
                node["value"] = left_value or right_value
                del node["left"]["value"]
                del node["right"]["value"]
                del node["left"]
                del node["right"]
            elif node["value"].token == Lookup_Table.keywords["NOT"]:
                self.interpret_bool_expr(node["left"])
                left_value = node["left"]["value"]
                node["value"] = not left_value
                del node["left"]["value"]
                del node["left"]
            else:
                pass