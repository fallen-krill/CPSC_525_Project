# Class function tree
class Function_tree:
    allowed_functions = set(['cos', 'sin', 'tan'])
    
    # Constructor is recursive. Input is a string
    def __init__(self, tokens):
         self.function = '0'
         self.arg1 = None
         self.arg2 = None

         # Do order of operations in reverse
         # Addition or subtraction
         for i in range(len(tokens)):
             if tokens[i] in set("+-"):
                 self.function = tokens[i]
                 self.arg1 = Function_tree(tokens[0:i])
                 self.arg2 = Function_tree(tokens[i+1: len(tokens)])
                 
             return


         for i in range(1, len(tokens)):
             if tokens[i] in set("*/"):
                 self.function = tokens[i]
                 self.arg1 = Function_tree(tokens[0:i])
                 self.arg2 = Function_tree(tokens[i + 1 : len(tokens)])

                 return
             
             elif tokens[i - 1] not in allowed_functions:
                 self.function = '*'
                 self.arg1 = Function_tree(tokens[0:i])
                 self.arg2 = Function_tree(tokens[i:len(tokens)])

                 return

         # exponentiation

         for i in range(1, len(tokens)):
             if tokens[i] == '^':
                 self.function = '^'
                 self.arg1 = Function_tree(tokens[i -1])
                 self.arg2 = Function_tree(tokens[i + 1])
                 return

         # factorial
         for i in range(1,len(tokens)):
             if tokens[i] == '!':
                 self.function = '!'
                 self.arg1 = Function_tree(tokens[i - 1])
                 return
        

         # functions
         for i in range(len(tokens) - 1):
             if tokens[i] in allowed_functions:
                 self.function = tokens[i]
                 self.arg1 = Function_tree(tokens[i + 1])
                 return

         # brackets
         self.function = Function_tree(tokens[0]).function
         self.arg1 = Function_tree(tokens[0]).arg1
         self.arg2 = Function_tree(tokens[0]).arg2

         return
    
        
                
    # I have no idea if this works yet
    # This only exists for testing purposes
    def __str__(self):
        return function + "(" + arg1 + "," + arg2 + ")"

    
    def evaluate(self, x):
        pass


# dictionary for allowed functions
# key is function, value is number of arguments it takes

# Helper functions

# This returning True does not mean that the syntax is correct. It only
# checks brackets and characters used
def validate_input(input_string):
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


# input_string the string to search,
# the function gives the sequence of consecutive letters (other than x, y, z)
# starting with input_string[index]
# Precondition: input_string[index] is a valid letter
def get_keyword(input_string, index):

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


# get the entire number as a string
def get_number(input_string, index):
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
    

# input_string the string to search,
# index is the index of the '(' that you want the matching ')' for.
def find_matching_bracket(input_string, index):
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

    
# returns a token (either a number, variable, or function name) starting at the given index
def get_token(input_string, index):
    token = ""
    # I am aware that '.' is not a digit but I don't know what else to call this
    digits = set(['0','1','2','3','4','5','6','7','8','9','0','.'])
    
    valid_letters = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_'])
    
    xyz = set(['x', 'y', 'z'])

    # if token starts with '(', return all the way until ')'
    if input_string[index] == '(':
        end_index = find_matching_bracket(input_string, index)
        if end_index != -1:
            print(input_string[index:end_index + 1])
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
    if (input_string[0] == '(' and
        find_matching_bracket(input_string, 0) == len(input_string) - 1 and
        input_string[len(input_string) - 1] == ')'):
        return True
    else:
        return False

    
def strip_outer_brackets(input_string):
    if (input_string[0] == '(' and
        find_matching_bracket(input_string, 0) == len(input_string) - 1 and
        input_string[len(input_string) - 1] == ')'):
        
        return input_string[1:len(input_string) - 1]
    else:
        return input_string

def num_consec_spaces(input_string, index):
    result = 0

    for i in range(index, len(input_string)):
        if input_string[i] == ' ':
            result += 1
        else:
            break
    return result

    
def tokenize(input_string):
    input_string = strip_outer_brackets(input_string)
    tokens = []

    i = 0

    while i < len(input_string):
        token = get_token(input_string, i)    
        if token != "":
            i += (num_consec_spaces(input_string, i) + len(token))
            if has_outer_brackets(token):
                token = tokenize(token) #recursive call
            tokens.append(token)
        else:
            tokens = ["error"]
            break
        print(i, token)

    return tokens

# For now, this is print debugging.
def main():
    input_string = "(10log_2x+ (302 39 4.234 .23) 4.123 .5/2343)"

    for i in range(len(input_string)):
        print(get_token(input_string, i))

    print(tokenize(input_string))

    Function_tree(input_string)

    
main()
