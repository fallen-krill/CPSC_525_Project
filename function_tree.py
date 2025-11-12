import math
class Function_tree:

    """
    Dictionary with allowed funcitons and number of arguments. Any string of letters not in
    this dictionary is treated as a constant. Undefined constants will give an error in the evaluation stage.
    """   
    allowed_functions = {

        "sin" : 1,
        "cos" : 1,
        "tan" : 1,
        "log" : 1,
        "log_" : 2,
        "ln" : 1,
        "csc" : 1,
        "sec" : 1,
        "cot" : 1,
        "asin" : 1,
        "acos" : 1,
        "atan" : 1,
        "sqrt" : 1,
    }

    """
    Dictionary with a few constants. In theory, we can add functionality later for users
    to define their own constants and add them in here.
    """
    allowed_constants = {
        "e" : 2.718281828459045235360287471352,
        "pi":3.141592653589323846264
    }

    
    def __init__(self, input_string):
        """
        The constructor is recursive.
        input_string -> str

        tokens -> [str]
        Algorithm is first tokenize input string and then iterate through tokens backwards until the
        desired operation is reached, call recursively then return.
        
        If it's not reached, go to the next operation.

        It regroups tokens depending on which operation is being checked.
        
        Round brackets are tokenized when the recursive call is made.

        If the input is a single token that's not in parentheses, a base case is reached.
        """

        # Tree data structure
        self.function = "error"
        self.arg1 = None
        self.arg2 = None

        # Ensure string is made of valid characters and all round brackets match.
        if validate_input(input_string) == False:
            return
        
        tokens = tokenize(input_string)

        if tokens == []:
            return
        
        # Do order of operations in reverse:

        # Addition and subtraction
        for i in range(len(tokens)-1, -1, -1):
            if tokens[i] in set("+-"):
                self.function = tokens[i]
                self.arg1 = Function_tree(detokenize(tokens[0:i]))
                self.arg2 = Function_tree(detokenize(tokens[i+1: len(tokens)]))

                return

        # multiplication and division

        # anything that isn't multiplied together should be a single token
        tokens = group_exp_fact(group_func_args(tokenize(input_string), self.allowed_functions))
        
        for i in range(len(tokens)-1, 0, -1):

            if tokens[i] in set("*/"):
                self.function = tokens[i][0]
                self.arg1 = Function_tree(detokenize(tokens[0:i]))
                self.arg2 = Function_tree(detokenize(tokens[i + 1 : len(tokens)]))
                
                return

            elif tokens[i-1] != "*":
                self.function = '*'
                self.arg1 = Function_tree(detokenize(tokens[0:i]))
                self.arg2 = Function_tree(detokenize(tokens[i : len(tokens)]))
                return

        # exponentiation

        # functions and thier arguments should be a single token
        tokens = group_func_args(tokenize(input_string), self.allowed_functions)
        for i in range(len(tokens) - 1, 0, -1):
            if tokens[i] == "^":
                self.function = '^'
                self.arg1 = Function_tree(detokenize(tokens[0:i]))
                self.arg2 = Function_tree(detokenize(tokens[i+ 1: len(tokens)]))
                
                return

        # note that in here, functions are evaluated starting from the right, so iterating forward
        tokens = group_factorials(tokenize(input_string))
        # functions
        for i in range(len(tokens) - 1):
            if tokens[i] in self.allowed_functions:
                num_args = self.allowed_functions[tokens[i]]
                self.function = tokens[i]
                if num_args == 1:
                    self.arg1 = Function_tree(detokenize(tokens[i+1: len(tokens)]))
                elif num_args == 2:
                    if i < len(tokens) - 2:
                        self.arg1 = Function_tree(tokens[i + 1])
                        self.arg2 = Function_tree(detokenize(tokens[i+2: len(tokens)]))

                return


        # factorial

        # No longer want tokens grouped together
        tokens = tokenize(input_string)

        if tokens[len(tokens) - 1] == "!": # all multiplication and function evaluation is done at this point
            self.function = '!'
            self.arg1 = Function_tree(detokenize(tokens[0: len(tokens) - 1]))
            
        # Brackets
        # This only applies if there are nested brackets
        if (len(tokens) == 1):
        
            if (has_outer_brackets(tokens[0])):
                self.function = Function_tree(tokens[0]).function
                self.arg1 = Function_tree(tokens[0]).arg1
                self.arg2 = Function_tree(tokens[0]).arg2

                return

            else:
                self.function = tokens[0]
                self.arg1 = None
                self.arg2 = None

                # if there is only one token and it is not defined
                if (self.function not in set("+-*/^!") and not is_number(self.function)
                    and self.function not in self.allowed_constants and self.function not in set("xyz")):
                    self.function = "error"
                    self.arg1 = None
                    self.arg2 = None
                    
                return
            
        # This should never be reached   
        return

         
    def __str__(self):
        """
        Returns a string with the order of evaluation given by round brackets
        """
        if self.arg1 != None and self.arg2 != None and self.function != None:
            return self.function + "(" + str(self.arg1) + "," + str(self.arg2) + ")"
        elif self.function != None and self.arg1 != None:
            return self.function + "(" + str(self.arg1) + ")"
        elif self.function != None:
            return self.function
        else:
            return "error"

        
    def is_valid(self):
        """
        Validates a function tree
        Return True if no "error" in function tree
        Otherwise, return false
        """
        if self.function == "error":
            return False

        if self.arg1 == None and self.arg2 == None:
            return True
        
        elif self.arg1 == None and self.arg2 != None:
            return self.arg2.is_valid()

        elif self.arg1 != None and self.arg2 == None:
            return self.arg1.is_valid()

        else:
            return self.arg1.is_valid() and self.arg2.is_valid()

        
    def evaluate(self, x):
        """
        x -> double
        Evaluates the function at a given x.
        If time, add support for y and z.

        Zero division errors and domain errors and stuff like that should be handled by graphics.
        Simply don't graph x at such points.
        """

        if self.arg1 == None and self.arg2 == None:
            if is_number(self.function):
                return float(self.function)
            elif self.function in self.allowed_constants:
                return self.allowed_constants[self.function]
            elif self.function == 'x':
                return x
            else:
                raise ValueError(self.function+" is not defined.")

        match self.function:
            case '+':
                return self.arg1.evaluate(x) + self.arg2.evaluate(x)
            case '-':
                return self.arg1.evaluate(x) - self.arg2.evaluate(x)
            case '*':
                return self.arg1.evaluate(x) * self.arg2.evaluate(x)
            case '/':
                return self.arg1.evaluate(x) / self.arg2.evaluate(x)
            case '^':
                return self.arg1.evaluate(x) ** self.arg2.evaluate(x)
            case '!': # We use gamma function in place of factorials
                return math.gamma(self.arg1.evaluate(x))
            case "sin":
                return math.sin(self.arg1.evaluate(x))
            case "cos":
                return math.cos(self.arg1.evaluate(x))
            case "tan":
                return math.tan(self.arg1.evaluate(x))
            case "csc":
                return 1.0/math.sin(self.arg1.evaluate(x))
            case "sec":
                return 1.0/math.cos(self.arg1.evaluate(x))
            case "cot":
                return 1.0/math.tan(self.arg1.evaluate(x))
            case "asin":
                return math.asin(self.arg1.evaluate(x))
            case "acos":
                return math.acos(self.arg1.evaluate(x))
            case "atan":
                return math.atan(self.arg1.evaluate(x))
            case "log":
                return math.log10(self.arg1.evaluate(x))
            case "log_":
                return math.log(self.arg2.evaluate(x), self.arg1.evaluate(x))
            case "ln":
                return math.log(2.718281828459045235360287471352, self.arg1.evaluate(x))
            case "sqrt":
                return math.sqrt(self.arg1.evaluate(x))
            case _: # should never be reached
                raise ValueError(self.function+" is not defined at x="+str(x))
            
        return 0


# Helper functions

def validate_input(input_string):
    """
    This returning True does not mean that the syntax is correct.
    This function checks
     - nonempty
     - bracket depth
     - allowed characters
    """

    if len(input_string) == 0:
        return False
    
    # ensure only valid characters are in the input string
    valid_characters = set("abcdefghijklmnopqrstuvwxyz .0987654321()+-*/^!_")
    if not(set(input_string).issubset(valid_characters)):
        return False
    if (input_string[0] not in set("abcdefghijklmnopqrstuvwxyz. 1234567890(+/")):
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
    input_string -> str
    index -> int
    the function gives the sequence of consecutive letters (other than x, y, z)
    starting with input_string[index]
    Precondition: input_string[index] is a valid letter
    """

    # this funtion returns empty string if input_string[index] is not a valid letter
    keyword = ""

    # entire alphabet
    valid_letters = set("abcdefghijklmnopqrstuvwxyz")

    # check each letter starting at input_string[index]
    for i in range(index, len(input_string)):
        if input_string[i] in valid_letters:
            keyword += input_string[i]
        else:
            if input_string[i] == '_': # underscore can only be at the end of a function.
                keyword += input_string[i]
            break

    return keyword


def get_number(input_string, index):
    """
    input_string -> str
    index -> int
    Return the entire number as a string.
    """
    
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


def is_number(input_string):
    """
    input_string -> str
    return True if this is a valid decimal represenation of some number. Otherwise, return False.
    """
    
    for i in range(len(input_string)):
        valid_digits = set("0987654321.")
        if input_string[i] in valid_digits:
            if input_string[i] == '.':
                valid_digits = set("0123456789") # future decimal places treated as new number
        else:
            return False
        
    return True


def find_matching_bracket(input_string, index):
    """
    input_string -> str : the string to search,
    index -> int: the index of the '(' that you want the matching ')' for.
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
    digits = set("0123456789.")

    # Underscore is included since log_ is a function (with two arguments)
    valid_letters = set("abcdefghijklmnopqrstuvwxyz_")

    xyz = set(['x', 'y', 'z'])

    # if token starts with '(', return all the way until ')'
    if input_string[index] == '(':
        end_index = find_matching_bracket(input_string, index)
        if end_index != -1:
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
        if index + 1 < len(input_string): # this should always be true and I will probably delete later
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


def num_consec_factorial(tokens, index):
    """
    tokens -> [str]
    index -> int
    This returns the number of consecutive "!" symbols in tokens that end with tokens[index]
    """

    result = 0
    for i in range(index, -1, -1):
        if tokens[i] == "!":
            result += 1
        else:
            break

    return result


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
        
    # Start by stripping outer brackets and whitespace if they are present.
    input_string = input_string.strip(" ")
    input_string = strip_outer_brackets(input_string)
    input_string = input_string.strip(" ")
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


def group_factorials(tokens):
    """
    tokens -> str

    combines tokens that are part of an expression consisting only of
    factorials into a single token, and returns the new tokens.
    """
    
    new_tokens = [tokens[0]]
    for i in range(1,len(tokens)):
        if tokens[i] == "!":
            new_tokens[len(new_tokens) - 1] += tokens[i]
        else:
            new_tokens.append(tokens[i])

    return new_tokens


def group_exp_fact(tokens):
    """
    tokens -> str

    combines tokens that are part of an expression consisting only of exponentiation
    and factorials into a single token, and returns the new tokens.
    """
    
    new_tokens = [tokens[0]]
    for i in range(1, len(tokens)):
        if tokens[i] == "!" or tokens[i] == "^" or tokens[i-1] == "^":
            new_tokens[len(new_tokens)-1] += tokens[i]
        else:
            new_tokens.append(tokens[i])
    return new_tokens


def group_func_args(tokens, allowed_functions):
    """
    tokens -> [str]
    allowed_functions -> dict

    combines tokens corresponding to a function and its arguments into one token,
    and returns the new tokens.
    """
    
    tokens = group_factorials(tokens)
    new_tokens = [tokens[0]]
    for i in range(1, len(tokens)):
        
        if tokens[i - 1] in allowed_functions:
            new_tokens[len(new_tokens) - 1] += " " + tokens[i]
        elif i > 1:
            
            if tokens[i-2] in allowed_functions: # If the function takes 2 arguments
                if allowed_functions[tokens[i - 2]] == 2:
                    new_tokens[len(new_tokens) - 1] += " " + tokens[i]

        # If none of the above conditions fulfiled, token doesn't get combined to the previous token.
                else:
                    new_tokens.append(tokens[i])
            else:
                new_tokens.append(tokens[i])
        else:
            new_tokens.append(tokens[i])
            
    return new_tokens


def detokenize(tokens):
    """
    tokens -> [str]

    Returns a string that consists of each token separated by a space.
    This is so that passing input to the function looks cleaner and maybe makes it slower.
    It probably won't matter since the size of the string is pretty small.
    """

    input_string = ""

    for i in range(len(tokens)):
        input_string += (tokens[i] + " ")

    return input_string.strip(" ")

    
# For now, this is print debugging. You can test out expressions in stdin.
def main():
    #input_string = "(10log x+ (302 39 4.234 .23) 4.123 .5/2343)"

    print("To exit, press ENTER without typing in a function.\n")

    i = 1
    input_string = input("f"+str(i)+"(x) = ")
    
    while input_string != "":


        # print("Tokens: ",tokenize(input_string))
        # print("Group factorials: ",group_factorials(tokenize(input_string)))
        # print("Group factorials and exponents", group_exp_fact(tokenize(input_string)))
        # print("Group functions: ",group_func_args(tokenize(input_string), Function_tree.allowed_functions)
        function_tree = None
        try:
            function_tree = Function_tree(input_string)
            print("\nFunction tree: ", str(function_tree), "\n")
           
        except ValueError as e:
            print(e, "\n")
        

        print("Valid function: " + str(function_tree.is_valid()) + "\n")
        if function_tree.is_valid():      
            step = 0.5
            for x in range(-20, 21):
                try:
                    print("f"+str(i)+"("+str(step*x)+") = ", function_tree.evaluate(step*x))
                except (ZeroDivisionError):
                    print("not defined at x=", step*x)
                except ValueError as e:
                    print(e)
                except TypeError as e:
                    print("not defined at x=", step*x)

        print("\n")
        
        i+=1
        input_string = input("f"+str(i)+"(x) = ")


    
main()
