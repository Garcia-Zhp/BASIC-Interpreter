# Class: CS 4308 
# Section 2 
# Term: Spring 2021 
# Names: Layton Williams, Travis Stickney, Jaime Garcia

from Interpreter import Interpreter

# Reads each line from the test.bas file and calls the extract_tokens method of the
# Scanner class for each line to extract all of the tokens in them that are
# a part of the subset of Basic that we're using and prints those tokens out


if __name__ == '__main__':
    while True:
        try:
            print("Enter a basic filename:")
            filename = 'programs/' + input()

            with open(filename, 'r') as basic_program:
                interpreter = Interpreter()
                for line in basic_program:
                    interpreter.interpret(line)

            break
        except FileNotFoundError:
            print("Invalid filename, try again...")
