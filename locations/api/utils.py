from accounts import choices

def get_default_units():
    return ['km', 'm', 'mm', ]


def is_valid_status(status):
    return True


def is_valid_gender(gender):
    if gender == 'M' or gender == 'F':
        return True
    else:
        return False
