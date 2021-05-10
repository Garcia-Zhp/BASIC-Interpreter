# Initializes a token each time the class is called
# with specific token and token value (lexeme)
class Token_Obj:
    def __init__(self, token, lexeme):
        self.token = token
        self.lexeme = lexeme

    # Allows each token to be printed out in a representable format
    def __repr__(self):
        return "%s" % self.lexeme