from .models import Notification


def get_notification_icon(type):

    url = "http://139.59.44.13/media/notification_icons/"

    if type == Notification.LIKE:
        return "like.png"
    elif type == Notification.CRUSH:
        return "crush.png"
    elif type == Notification.COINS:
        return url+'coins.png'
    elif type == Notification.MATCH:
        return url+'match.png'
    elif type == Notification.VIEW:
        return "profile_view.png"
    elif type == Notification.FJ:
        return "flirtjar.png"

    return "error.png"


def create_notification(user, text, notification_type):
    return Notification(
        user=user,
        notification_text=text,
        notification_icon=get_notification_icon(notification_type),
        notification_type=notification_type
    )
