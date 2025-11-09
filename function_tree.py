# Class function tree
class Function_tree:

    # Dictionary with allowed funcitons and number of arguments
    allowed_functions = {
        "cos" : 1,
        "sin" : 1,
        "tan" : 1,
        "log" : 1,
        "log_" : 2
    }
    

    def __init__(self, input_string):
        """
        The constructor is recursive.
        input_string -> str

        tokens -> [str]
        Algorithm is first tokenize input string and then iterate through tokens backwards until the desired operation is reached, call recursively then return.
        If it's not reached, go to the next operation.
    
        Round brackets are tokenized when the recursive call is made.

        If the input is a single token that's not in parentheses, a base case is reached.
        """

        # Tree data structure
        self.function = '0'
        self.arg1 = None
        self.arg2 = None

        tokens = tokenize(input_string)

        # Do order of operations in reverse

         
        # Addition and subtraction
        for i in range(len(tokens)-1, -1, -1):
            if tokens[i] in set("+-"):
                self.function = tokens[i]
                self.arg1 = Function_tree(detokenize(tokens[0:i]))
                self.arg2 = Function_tree(detokenize(tokens[i+1: len(tokens)]))
                 
                return

        # multiplication and division
        for i in range(len(tokens)-1, 0, -1):
            if tokens[i] in set("*/"):
                self.function = tokens[i]
                self.arg1 = Function_tree(detokenize(tokens[0:i]))
                self.arg2 = Function_tree(detokenize(tokens[i + 1 : len(tokens)]))
                
                return
            
            elif tokens[i - 1] not in self.allowed_functions:
                self.function = '*'
                self.arg1 = Function_tree(detokenize(tokens[0:i]))
                self.arg2 = Function_tree(detokenize(tokens[i:len(tokens)]))
                
                return

        # exponentiation
        for i in range(len(tokens) - 1, 0, -1):
            if tokens[i] == '^':
                self.function = '^'
                self.arg1 = Function_tree(detokenize(tokens[i -1]))
                self.arg2 = Function_tree(detokenize(tokens[i + 1]))
                return

        # factorial
        for i in range(len(tokens) - 1, 0, -1):
            if tokens[i] == '!':
                self.function = '!'
                self.arg1 = Function_tree(detokenize(tokens[i - 1]))
                return
        

        # functions
        for i in range(len(tokens) - 1):
            if tokens[i] in self.allowed_functions:
                self.function = tokens[i]
                self.arg1 = Function_tree(detokenize(tokens[i + 1]))
                return

        # Brackets
        # This only applies if there are nested brackets
        if (len(tokens) == 1 and has_outer_brackets(tokens[0])):
            self.function = Function_tree(tokens[0]).function
            self.arg1 = Function_tree(tokens[0]).arg1
            self.arg2 = Function_tree(tokens[0]).arg2

        # This should only be reached in a base case. TODO: Add checks
        return
                
    # I have no idea if this works yet
    # This only exists for testing purposes
    def __str__(self):
        if self.arg1 != None and self.arg2 != None and self.function != None:
            return str(self.function) + "(" + str(self.arg1) + "," + str(self.arg2) + ")"
        else:
            return self.function

    
    def evaluate(self, x):
        pass


    # Helper functions

def validate_input(input_string):
    """
    This returning True does not mean that the syntax is correct. It only
    checks brackets and characters used
    """

    # ensure only valid characters are in the input string
    valid_characters = set("abcdefghijklmnopqrstuvwxyz .0987654321()+-*/^!_")
    if not(set(input_string).issubset(valid_characters)):
        return False
    if not (input_string[0] in set("abcdefghijklmnopqrstuvwxyz. 1234567890(+/")):
        return False
    # ensure bracket depth is 0 at the end of the string
    bracket_depth = 0
    for i in range(len(input_string)):
        if input_string[i] == '(':
            bracket_depth += 1
        elif input_string[i] == ')':
            bracket_depth -= 1

    if bracket_depth != 0:
        return False

    return True



def get_keyword(input_string, index):
    """
    input_string the string to search,
    the function gives the sequence of consecutive letters (other than x, y, z)
    starting with input_string[index]
    Precondition: input_string[index] is a valid letter
    """

    # this funtion returns empty string if input_string[index] is not a valid letter
    keyword = ""

    # entire alphabet except x, y, and z
    valid_letters = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_'])

    # check each letter starting at input_string[index]
    for i in range(index, len(input_string)):
        if input_string[i] in valid_letters:
            keyword += input_string[i]
        else:
            break

    return keyword



def get_number(input_string, index):
    """get the entire number as a string"""
    number = ''

    valid_digits = set("0987654321.")

    for i in range(index, len(input_string)):
        if input_string[i] in valid_digits:
            number += input_string[i]
            if input_string[i] == '.':
                valid_digits = set("0123456789") # future decimal places treated as new number
        else:
            break
    return number



def find_matching_bracket(input_string, index):
    """
    input_string the string to search,
    index is the index of the '(' that you want the matching ')' for.
    """
    bracket_depth = 0
    for i in range(index + 1, len(input_string)):
        if input_string[i] == '(':
            bracket_depth += 1
        elif input_string[i] == ')':
            if bracket_depth == 0:
                return i
            else:
                bracket_depth -= 1
    else: # In theory, this is only possible if close brackets are missing
        return -1


def get_token(input_string, index):
    """
    input_string -> str
    index -> int
    returns a token (either a number, variable, or function name) starting at the given index

    the token is
     - The consecutive letters (if input_string[i] is a letter and not all consecutive letters are x, y or z)
     - The consecutive digits with up to one '.' (if input_string[i] is a digit or '.')
     - 'x', 'y', or 'z' (if the consecutive letters are all x, y or z)
     - An expression in round brackets (if input_string[i] is '(')
     - the token starting at index i + 1 (if input_string[i] is ' ')
    """

    # Initialize to empty string
    token = ""

    # I am aware that '.' is not a digit but I don't know what else to call this
    digits = set(['0','1','2','3','4','5','6','7','8','9','0','.'])

    # Underscore is included since log_ is a function (with two arguments)
    valid_letters = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_'])

    xyz = set(['x', 'y', 'z'])

    # if token starts with '(', return all the way until ')'
    if input_string[index] == '(':
        end_index = find_matching_bracket(input_string, index)
        if end_index != -1:
            #print(input_string[index:end_index + 1])
            token = input_string[index : end_index + 1]
        else:
            token = "invalid token"

    # The token is the number
    elif input_string[index] in digits:
        token = get_number(input_string, index)

    # the token is some function, variable or constant name
    elif input_string[index] in valid_letters:
        keyword = get_keyword(input_string, index)
        if set(keyword).issubset(xyz): # if the keyword is only variables
            token = keyword[0]
        else:      
            token = keyword

    # The token is determined by what is after the space
    elif input_string[index] == ' ':
        token = get_token(input_string, index + 1) # recursive call

    # The token is the operator
    elif input_string[index] in set("+-*/^!"):
        token = input_string[index]

    return token


def has_outer_brackets(input_string):
    """
    input_string -> str
    Return True if input_string starts with '(' and the matching delimiter is ')' at
    index len(input_string]) - 1
    """

    if (input_string[0] == '(' and
        find_matching_bracket(input_string, 0) == len(input_string) - 1 and
        input_string[len(input_string) - 1] == ')'):
        return True
    else:
        return False


def strip_outer_brackets(input_string):
    """
    input_string -> str
    If the input string is surrounded by round brackets that match each other, strip them.
    Otherwise, return input_string.
    """
    if len(input_string) > 1:
        if (input_string[0] == '(' and
            find_matching_bracket(input_string, 0) == len(input_string) - 1 and
            input_string[len(input_string) - 1] == ')'):

            return input_string[1:len(input_string) - 1]
        else:
            return input_string
    return input_string

def num_consec_spaces(input_string, index):
    """
    input_string -> str
    index -> int
    Return the number of consecutive spaces in the input string starting at index.
    This is needed to tell when the next token starts if there are spaces between tokens.
    """
    result = 0

    for i in range(index, len(input_string)):
        if input_string[i] == ' ':
            result += 1
        else:
            break
    return result


def tokenize(input_string):
    """
    input_string -> str
    Return a list of all the tokens composing input_string.

    tokens -> [str] is a list of "tokens" which are either
     - a sequence of letters,
     - a number,
     - an operator, or
     - an expression enclosed in round brackets.
    """

    # Start by stripping outer bracks if they are present.
    input_string = strip_outer_brackets(input_string)

    # Initialize to empty list.
    tokens = []

    i = 0

    while i < len(input_string):
        token = get_token(input_string, i)    
        if token != "":
            i += (num_consec_spaces(input_string, i) + len(token))

            # Tokens that are surrounded by round brackets are left alone

            tokens.append(token)
        else:
            tokens = ["error"]
            break

    return tokens

def detokenize(tokens):
    """
    tokens -> [str]

    Returns a string that consists of each token separated by a space.
    This is so that passing input to the function looks cleaner and maybe makes it slower.
    """

    input_string = ""

    for i in range(len(tokens)):
        input_string += (tokens[i])
        if i != len(tokens) - 1:
            input_string += " "

    return input_string

    
# For now, this is print debugging.
def main():
    input_string = "(10log_2x+ (302 39 4.234 .23) 4.123 .5/2343)"

    for i in range(len(input_string)):
        print(get_token(input_string, i))

    print(tokenize(input_string))

    print("\n")
    print(Function_tree(input_string))

    
main()
