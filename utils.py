def validate_reg(data: dict):
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    rep_password = data.get('rep_password')
    if first_name and last_name and email and password and rep_password:
        if password == rep_password:
            return True
    return False


def validate_login(data: dict):
    email = data.get('email')
    password = data.get('password')
    if email and password:
        return True
    return False
