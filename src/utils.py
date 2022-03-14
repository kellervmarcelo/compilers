def is_a_number(arg):
    """Evaluates if given argument can be converted to an Integer"""
    try:
        int(arg)
        return True
    except:
        return False
