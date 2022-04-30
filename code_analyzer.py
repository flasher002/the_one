import sys
import os
import re
import ast


class Visitor(ast.NodeVisitor):
    """Append all found issues into 3 different lists which are then combined into the issues_list and printed
    """

    def visit_FunctionDef(self, node):
        """ Search for non snake_case arguments, mutable arguments
         and non snake_case variables defined in functions

         there are 3 lists 'snake_case_arg_issues', 'snake_case_var_issues' and 'mut_default_arg_issues'
         all found issues are appended into these respectively
         with this form ['error_code', 'corresponding message', 'line_number_where_found']
        """
        for argument in node.args.args:
            if not re.match(" *[a-z0-9_]+$", argument.arg):
                snake_case_arg_issues.append(["S010", "parameters should be snake_case", argument.lineno])
                break
        default_val = node.args.defaults
        for default_obj in default_val:
            if isinstance(default_obj, ast.List) or isinstance(default_obj, ast.Set) \
                    or isinstance(default_obj, ast.Dict):
                mut_default_arg_issues.append(["S012", "dont use mutable default parameter", node.lineno])
                break

        for i in node.body:
            if isinstance(i, ast.Assign):
                for j in i.targets:
                    if isinstance(j, ast.Attribute):
                        if not re.match(" *[a-z0-9_]+$", j.value.id):
                            snake_case_var_issues.append(
                                ["S011", "variables should be written in snake case", j.lineno])
                    else:
                        if not re.match(" *[a-z0-9_]+$", j.id):
                            snake_case_var_issues.append(
                                ["S011", "variables should be written in snake case", j.lineno])


    def visit_Assign(self, node):
        """ Search for non snake case variable names and append them into 'snake_case_var_issues'  """
        for names in node.targets:
            if not re.match(" *[a-z0-9_]+$", names.id):
                snake_case_var_issues.append(["S011", "variables should be written in snake case", names.lineno])
                break


def check_line_length(code_line: "The line to check") -> None:
    if len(code_line) > 79:
        issues_list.append(["S001", "Line too long"])


def check_indentation(code_line: "The line to check") -> None:
    striped_line = code_line.lstrip()
    if (len(striped_line) - len(code_line)) % 4 != 0 and len(striped_line) != 0:
        issues_list.append(["S002", "Wrong indentation should be a multiple of 4"])


def check_semicolon(code_line: "The line to check") -> None:
    code_comment = filter_out_comment(code_line)
    stripped_line = code_comment[0].rstrip("\n").rstrip()
    if len(stripped_line) > 0:
        if stripped_line[-1] == ";":
            issues_list.append(["S003", "You dont need a semicolon at the end"])


def check_spaces_before_comment(code_line: "The line to check") -> None:
    code_comment = filter_out_comment(code_line)
    stripped_code_part = code_comment[0].rstrip("\n")
    if len(code_comment[0]) == 0:  # check if there is even a comment or 2 lines down a piece of code
        return
    elif len(code_comment[1]) == 0:
        return
    elif stripped_code_part[-1] == " " and stripped_code_part[-2] == " ":  # check if its declared correctly
        return
    else:
        issues_list.append(["S004", "There should be 2 spaces after the code ends"])


def check_todo(code_line: "The line to check") -> None:
    comment = filter_out_comment(code_line)[1]
    if comment.upper().count("TODO"):
        issues_list.append(["S005", "found TODO"])


def check_preceding_blanks(code_line: "The line to check") -> None:
    global blanks

    if len(code_line.strip("\n").strip()) == 0:
        blanks += 1
    else:
        if blanks >= 3:
            issues_list.append(["S006", "More than 2 blank lines before this one"])
        blanks = 0


def check_constructor_spaces(code_line: "Line to check") -> None:
    def_constructor = filter_out_constructor(code_line, "def")
    if def_constructor:
        if re.match(" *def {2,}", def_constructor):
            issues_list.append(["S007", "Too many spaces after def"])
        return

    class_constructor = filter_out_constructor(code_line, "class")
    if class_constructor:
        if re.match(" *class {2,}", class_constructor):
            issues_list.append(["S007", "Too many spaces after class"])
        return


def check_constructor_name(code_line: "Line to check") -> None:
    def_constructor = filter_out_constructor(code_line, "def")
    if def_constructor:
        if not re.match(r" *def *[_a-z][^A-Z]*\(", def_constructor):  # check after snake_case then reverse
            issues_list.append(["S009", "function name should be written in snake_case"])
        return

    class_constructor = filter_out_constructor(code_line, "class")
    if class_constructor:
        if not re.match(r" *class *[A-Z][^_]*:", class_constructor):  # check after CamelCase then reverse
            issues_list.append(["S008", "class name should be CamelCase"])
        return


def check_arg_name(line_num):
    """ check if the currently scanned line is the  same as the line number of an issue found with the
    visitor() function and if yes add this to the issues_list to be printed after which this one issue gets
     deleted to make way for the next one which is checked every iteration
     """
    if len(snake_case_arg_issues) >= 1:
        if line_num == snake_case_arg_issues[0][2]:
            issues_list.append([snake_case_arg_issues[0][0], snake_case_arg_issues[0][1]])
            snake_case_arg_issues.pop(0)


def check_var_name(line_num):
    """ same as 'check_arg_name' just with different appended list """
    if len(snake_case_var_issues) >= 1:
        if line_num == snake_case_var_issues[0][2]:
            issues_list.append([snake_case_var_issues[0][0], snake_case_var_issues[0][1]])
            snake_case_var_issues.pop(0)


def check_arg_mutability(line_num):
    """ same as 'check_arg_name' just with different appended list """
    if len(mut_default_arg_issues) >= 1:
        if line_num == mut_default_arg_issues[0][2]:
            issues_list.append([mut_default_arg_issues[0][0], mut_default_arg_issues[0][1]])
            mut_default_arg_issues.pop(0)


def filter_out_constructor(code_line, search_constructor: str) -> str | None:
    """Return the entire constructor upto and including the :

    Search for the given constructor in the specified code line and return the entire constructor
    if it was found else return none

    >>> filter_out_constructor(code_line, "class")
    class TheReturnedOne(PossibleParent):  or None
    """
    if search_constructor == "def":
        if re.match(r" *def", code_line):
            return re.match(r" *def *\w[\w\d]*\([{\[}\]\w\d\s'\":=,]*\):", code_line).group()
    elif search_constructor == "class":
        if re.match(r" *class", code_line):
            return re.match(r" *class *\w[\w\d]*\(*[\w\d\s'\":=,]*\)*:", code_line).group()


def filter_out_comment(code_line, only_true_false=False):
    """Return a list with the code fragment and the comment where [0] is the code and [1] the comment

    When the optional parameter only_true_false is given then the return value is no list
    but just True if there is a comment and False if there is none

    >>> filter_out_comment(code_line)
    ["print("Hello bro"), "  nice isnt it hm"]
    """
    code_list = list()
    comment_list = list()
    mode = "code"

    single_quote_string = False
    double_quote_string = False
    escape_char = False
    for char in code_line:
        # check after special characters that change the mode so # ' " \
        if char == "'" and not double_quote_string and mode == "code" and not escape_char:
            code_list.append(char)
            single_quote_string = not single_quote_string

        elif char == '"' and not single_quote_string and mode == "code" and not escape_char:
            code_list.append(char)
            double_quote_string = not double_quote_string

        # check if there is a # for the beginning of the comment, and it isn't in a string
        elif char == "#" and not double_quote_string and not single_quote_string:
            comment_list.append(char)
            mode = "comment"

        # check in which mode the function is to decide where to append the symbols ether code or comment
        elif mode == "code":
            code_list.append(char)

        elif mode == "comment":
            comment_list.append(char)
            if only_true_false:
                return True

        escape_char = False
        if char == "\\":
            escape_char = True

    if only_true_false:
        return False

    code_list = "".join(code_list)
    comment_list = "".join(comment_list)
    return [code_list, comment_list]


def find_ast_issues(code):
    tree = ast.parse(code)
    Visitor().visit(tree)


def print_issues(line_count: "The line number") -> None:
    """print all the found PEP8 issues and their corresponding messages"""
    if len(issues_list) == 0:
        return
    if len(issues_list) == 1:
        print(f"{current_checking_path}: Line {line_count}: {issues_list[0][0]} {issues_list[0][1]}")
    else:
        for i in issues_list:
            print(f'{current_checking_path}: Line {line_count}: {i[0]} {i[1]}')


def pep8_check() -> None:
    """main loop to check for all PEP8 issues

     all the issues after which should be checked are called here
     """

    #  open the file once read it and make an AST with it then close it again to not cause conflicts
    with open(checking_code_file, "r") as read_file:
        code = read_file.read()
        find_ast_issues(code)

    with open(checking_code_file) as check_file:
        count = 1

        for line in check_file:
            # print(snake_case_arg_issues, snake_case_var_issues, mut_default_arg_issues, sep="\n")
            issues_list.clear()
            check_line_length(line)
            check_indentation(line)
            check_semicolon(line)
            check_spaces_before_comment(line)
            check_todo(line)
            check_preceding_blanks(line)
            check_constructor_spaces(line)
            check_constructor_name(line)
            check_arg_name(count)
            check_var_name(count)
            check_arg_mutability(count)

            print_issues(count)

            count += 1


issues_list = list()
snake_case_arg_issues = list()
snake_case_var_issues = list()
mut_default_arg_issues = list()
blanks = 0

args = sys.argv
# this var is always updated with the file that is now checked
checking_code_file = args[1]
# and this holds the absolute path to the file
current_checking_path = checking_code_file
file_to_test_list = list()
base_dir = "/home/luc/PycharmProjects/Static Code Analyzer/Static Code Analyzer/task"
os.chdir(base_dir)

if os.path.isdir(checking_code_file):
    base_dir = os.path.join(base_dir, checking_code_file)
    os.chdir(base_dir)

    for check_file in os.listdir():
        if check_file[-3:] == ".py" and (check_file.count("_") != 2 and check_file.count("_") != 3):
            path_to_file = os.path.join(base_dir, check_file)
            file_to_test = check_file
            file_to_test_list.append([file_to_test, path_to_file])
else:
    pep8_check()
    quit()


file_to_test_list.sort()
for file in file_to_test_list:
    checking_code_file = file[0]
    current_checking_path = file[1]
    pep8_check()
