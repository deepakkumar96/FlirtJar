from chat.models import Message


def get_all_messages(user_from, user_to):
    for msg in Message.objects.filter(user_to=user_to, user_from=user_from, is_seen=False)[:25]:
        yield msg

    for msg in Message.objects.filter(user_from=user_to, user_to=user_from, is_seen=False)[:25]:
        yield msg
