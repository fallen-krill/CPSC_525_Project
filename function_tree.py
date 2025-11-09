# Class function tree
class Function_tree:

    # Constructor is recursive. Input is a string
    def __init__(self, input_string):
         self.function = NULL
         self.arg1 = NULL
         self.arg2 = NULL

         # TODO: parse input string

         
    # I have no idea if this works yet
    def __str__(self):
        return function + "(" + arg1 + "," + arg2 + ")"

    def evaluate(self, x):
        pass


# Helper functions

# input_string the string to search,
# the function gives the sequence of consecutive letters (other than x, y, z)
# starting with input_string[index]
def get_keyword(input_string, index):

    # this funtion returns empty string if input_string[index] is not a valid letter
    keyword = ''

    # entire alphabet except x, y, and z
    valid_letters = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

    # check each letter starting at input_string[index]
    for i in range(index, len(input_string)):
        if input_string[i] in valid_letters:
            keyword += input_string[i]
        else:
            break
    return keyword


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
    return -1
