from .models import Notification


def get_notification_icon(type):

    if type == Notification.LIKE:
        return "like.png"
    elif type == Notification.CRUSH:
        return "crush.png"
    elif type == Notification.COINS:
        return "coin.png"
    elif type == Notification.MATCH:
        return "http://127.0.0.1:8000/media/gifts/1.jpg"
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
