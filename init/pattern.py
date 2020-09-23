import re

def check_pattern(s, type):
    if type == "str":
        reg = "^[A-Za-z]{1,32}$"
    elif type == "pwd":
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    elif type == "int":
        reg = "^\d$"

    # compiling regex
    pat = re.compile(reg)

    # searching regex
    mat = re.search(pat, s)

    # validating conditions
    if mat:
        return True
    else:
        return False