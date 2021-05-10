from Type_Obj import Type_Obj
from Token_Obj import Token_Obj
from Lookup_Table import Lookup_Table


# Scanner class
class Scanner:
    def __init__(self):
        self.line = ""
        self.position = 0
        self.line_number = ""
        self.tokens = []
        self.variables = {}
        self.input_stmt = False

    def is_number(self):
        if self.line[self.position] == "-":
            return '0' <= self.line[self.position + 1] <= '9'
        else:
            return '0' <= self.line[self.position] <= '9'

    def is_letter(self):
        return 'A' <= self.line[self.position] <= 'z'

    # Method that retrieves the line number from the BASIC (.bas) file and stores the line
    # number in a variable
    def extract_line_num(self):
        while self.position < len(self.line) and self.is_number():
            self.line_number += self.line[self.position]
            self.position += 1

    # Method that allows the program to skip unnecessary whitespace
    def skip_whitespace(self):
        while self.position < len(self.line) and (
                self.line[self.position] == ' ' or self.line[self.position] == '\n' or self.line[
            self.position] == '\t' or self.line[self.position] == '\r'):
            self.position += 1

    # Method that resets the positions and the tokens back to zero and empty
    def reset(self):
        self.line_number = ""
        self.position = 0
        self.tokens = []
        self.input_stmt = False

    # Method that returns true if value is an integer value
    def is_type_int(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    # Method that returns true if value is an float value
    def is_type_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    # Method that returns true if boolean value is either "TRUE" or "FALSE"
    def is_type_bool(self, value):
        return value.upper() == "TRUE" or value.upper() == "FALSE"

    # Method that returns the respective identifier type depending on the value's type
    def determine_idtype(self, value):
        if self.is_type_int(value):
            return "INT_ID"
        elif self.is_type_float(value):
            return "REAL_ID"
        elif self.is_type_bool(value):
            return "BOOL_ID"
        else:
            return "STRING_ID"

    # A method that is used for recognizing all of the characters in a lexeme that has
    # been determined by the extract_tokens method to be either a REM(comment), keyword, bool literal,
    # or an identifier. This method will also determine what type of identifier a lexeme is
    # if it has been determined to be an identifier
    def letter_lexeme(self):
        lexeme = ""
        while self.position < len(self.line) and (self.is_letter() or self.is_number()):
            lexeme += self.line[self.position]
            self.position += 1
        if lexeme.upper() == "REM":
            self.tokens.append(Token_Obj(Lookup_Table.keywords["REM"], lexeme))
            self.position = len(self.line)
        elif lexeme.upper() in Lookup_Table.keywords:
            if lexeme.upper() == "INPUT":
                self.input_stmt = True
            self.tokens.append(Token_Obj(Lookup_Table.keywords[lexeme.upper()], lexeme))
        elif lexeme.upper() == "TRUE" or lexeme.upper() == "FALSE":
            self.tokens.append(Token_Obj(Lookup_Table.constants["BOOL_LITERAL"], lexeme))
        elif self.input_stmt:
            self.tokens.append(Token_Obj(Lookup_Table.identifiers["INT_ID"], lexeme))
            self.variables[lexeme] = Type_Obj("INT_ID", '0')
        # This else statement will execute if the lexeme has been determined to be an
        # identifier
        else:
            self.skip_whitespace()
            if len(self.tokens) > 0 and self.tokens[len(self.tokens) - 1].token == Lookup_Table.keywords[
                "LET"] and self.position < len(self.line) and self.line[self.position] == "=":
                for i in range(len(self.line)):
                    if i >= self.position - len(lexeme):
                        break
                    elif self.line[i] == "=":
                        raise Exception("Invalid assign statement (=), line " + self.line_number)

                # search_line will be equal to the string of characters that come after
                # the equal sign in the current line. If there is no equal sign in the line
                # then search_line will be equal to the empty string
                search_line = self.line.partition("=")[2].strip()
                search_index = 0
                lexeme_ahead = ""
                while search_index < len(search_line) and (
                        search_line[search_index] != ' ' and search_line[search_index] != ':'):
                    lexeme_ahead += search_line[search_index]
                    search_index += 1
                if lexeme_ahead in self.variables:
                    variable_type = self.variables[lexeme_ahead].variable_type
                    self.tokens.append(
                        Token_Obj(Lookup_Table.identifiers[variable_type], lexeme))
                    self.variables[lexeme] = Type_Obj(variable_type, search_line)
                else:
                    variable_type = self.determine_idtype(lexeme_ahead)
                    self.tokens.append(Token_Obj(Lookup_Table.identifiers[variable_type], lexeme))
                    self.variables[lexeme] = Type_Obj(variable_type, search_line)
            else:
                # If an equal sign is already in the tokens variable and the lexeme is not defined
                # already in the variables dictionary, then an exception must be thrown since an
                # undefined variable cannot be on the right side of the equal sign
                if lexeme not in self.variables:
                    variable_type = "INT_ID"
                    self.tokens.append(Token_Obj(variable_type, lexeme))
                    self.variables[lexeme] = Type_Obj(variable_type, '0')
                # Add the lexeme to the tokens variable since it's defined an an equal sign was
                # found already
                else:
                    variable_type = self.variables[lexeme].variable_type
                    self.tokens.append(
                        Token_Obj(Lookup_Table.identifiers[variable_type], lexeme))

    # A method that identifies whether the literal is an integer literal or float literal
    def number_lexeme(self):
        lexeme = ""
        dot_count = 0
        while self.position < len(self.line) and (self.is_number() or self.line[self.position] == '.'):
            if self.line[self.position] == '.':
                if dot_count == 1:
                    raise Exception('Invalid number entry ' + self.line_number)
                else:
                    dot_count += 1
            lexeme += self.line[self.position]
            self.position += 1
        if dot_count == 1:
            self.tokens.append(Token_Obj(Lookup_Table.constants["REAL_LITERAL"], lexeme))
        else:
            self.tokens.append(Token_Obj(Lookup_Table.constants["INT_LITERAL"], lexeme))

    # A method that is used for recognizing all of the characters in a lexeme that has
    # been determined by the extract_tokens method to be a symbol
    def symbol_lexeme(self):
        lexeme = self.line[self.position]
        if self.position + 1 < len(self.line) and lexeme + self.line[self.position + 1] in Lookup_Table.symbols:
            lexeme += self.line[self.position + 1]
            self.position += 2
            self.tokens.append(Token_Obj(Lookup_Table.symbols[lexeme], lexeme))
            return
        self.position += 1
        self.tokens.append(Token_Obj(Lookup_Table.symbols[lexeme], lexeme))
        if lexeme == ":":
            self.line = self.line[self.position:]
            self.position = 0
            self.input_stmt = False

    # A method that is used for recognizing all of the characters in a lexeme that has
    # been determined by the extract_tokens method to be a String literal
    def string_lexeme(self):
        lexeme = ""
        self.position += 1
        while self.position < len(self.line) and self.line[self.position] != "\"":
            lexeme += self.line[self.position]
            self.position += 1
        if self.position >= len(self.line):
            raise Exception('Invalid String, line ' + self.line_number)
        else:
            self.position += 1
            self.tokens.append(Token_Obj(Lookup_Table.constants["STRING_LITERAL"], lexeme))

    # A method that is used to extract all of the tokens from a line by finding the
    # lexemes in it and determining what type of token it is from the characters in the
    # lexeme and the value of the lexeme itself. If a lexeme cannot be recognized as any
    # token by this method it'll be assigned to the UNKNOWN token
    def extract_tokens(self, line):
        self.line = line
        self.reset()
        self.extract_line_num()

        if self.line_number == "":
            raise Exception("Missing line number at beginning of line")

        while self.position < len(self.line):
            self.skip_whitespace()
            if self.position >= len(self.line):
                break
            elif self.is_letter():
                self.letter_lexeme()
            elif self.is_number() or self.line[self.position] == '.':
                self.number_lexeme()
            elif self.line[self.position] in Lookup_Table.symbols:
                self.symbol_lexeme()
            elif self.line[self.position] == "\"":
                self.string_lexeme()
            else:

                # lexeme = self.line[self.position]
                # self.position += 1
                #
                # self.tokens.append(Token_Obj(unknown["UNKNOWN"], lexeme))
                raise Exception("Invalid syntax error, line " + self.line_number)
