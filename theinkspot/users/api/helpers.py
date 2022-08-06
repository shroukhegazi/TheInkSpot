import re


# This function is checking the strgnth of a password
# to contain a number and both uppercase and lowercase letters
def check_password_strength(password):
    return re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])", password)
