from profiles.models import UserMatch

def convert_to_reponseid(response):
    response = int(response)
    if response >= 0 and response <=2:
        return response
    else:
        return -1


def is_valid_response(response):
    if response >= 0 and response <=2:
        return True
    else:
        return False


def get_user_match(user):
    """
    Returns all the matches of the given user
    """
    matches = []
    for um in UserMatch.objects.select_related('user_from').filter(user_to=user.pk):
        matches.append(um.user_from)

    for um in UserMatch.objects.select_related('user_to').filter(user_from=user.pk):
        matches.append(um.user_to)
    return matches
