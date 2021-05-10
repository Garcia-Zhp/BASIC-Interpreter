class Lookup_Table:
    keywords = {
        "LET": 1,
        "PRINT": 2,
        "REM": 3,
        "GOTO": 4,
        "NEXT": 5,
        "FOR": 6,
        "IF": 7,
        "THEN": 8,
        "TO": 9,
        "INPUT": 10,
        "OR": 11,
        "AND": 12,
        "NOT": 13,
        "END": 14,
        "INT": 15
    }

    symbols = {
        "+": 16,
        "-": 17,
        "*": 18,
        "/": 19,
        "=": 20,
        ">": 21,
        "<": 22,
        "(": 23,
        ")": 24,
        "<=": 25,
        ">=": 26,
        "<>": 27,
        ";": 28,
        ",": 29,
        ":": 30
    }

    identifiers = {
        "STRING_ID": 31,
        "INT_ID": 32,
        "REAL_ID": 33,
        "BOOL_ID": 34
    }

    constants = {
        "STRING_LITERAL": 35,
        "REAL_LITERAL": 36,
        "INT_LITERAL": 37,
        "BOOL_LITERAL": 38
    }
