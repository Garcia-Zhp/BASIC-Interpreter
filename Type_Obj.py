# Class specifies what each variable(identifier) holds with its specific variable type
class Type_Obj:
    def __init__(self, variable_type, string_value):
        self.variable_type = variable_type
        self.string_value = string_value

    def __repr__(self):
        return "[ Variable Type: %s | Value: %s ]" % (self.variable_type, self.string_value)
