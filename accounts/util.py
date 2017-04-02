
from rest_framework.views import exception_handler
from rest_framework.renderers import JSONRenderer
from .exceptions import DeviceNotFound


def custom_exception_handler(exc, context):
    """
    Custom exception handler for customizing rest_framework
    error responses.
    """
    # print('CUSTOM HANDLER')
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Customizing response
    if response is not None:
        errors = []
        for k, v in response.data.items():
            errors.append("{} : {}".format(k, v))

        response.data = {
            # 'status_code': response.status_code,
            'errors': errors
        }
    return response




class Device(object):

    ANDROID = 'android'
    IOS = 'ios'

    def __init__(self, device_type, user_device):
        self.device_type = device_type
        self.user_device = user_device


    def send_push_notification(self, title, body, extra_data):
        if self.device_type == Device.IOS:
            try:
                print('sending apns push notification')
                self.user_device.send_message(
                        message={
                            'title': title,
                            'body': body
                        },
                        extra=extra_data
                )
                print('apns sent')
            except:
                print('unable to send apns push notifications. to ', self.user_device)

        elif self.device_type == Device.ANDROID:
            try:
                print('sending android push notification')
                self.user_device.send_message(message_title=title,
                                              message_body=body,
                                              data_message=extra_data)
            except:
                print('unable to send push notifications. to ', self.user_device)


def get_user_device(user):
    """
    (*) Can be cashed in production
    Returns a Device object containing device_type and device
    :param user:
    :return: Device
    :raises DeviceNotFound
    :rtype Device
    """
    # Checking for user device in APNS devices
    user_device = user.apnsdevice_set.first()
    if user_device:
        return Device(Device.IOS, user_device)

    # Checking for user device in Android devices
    user_device = user.androiddevice_set.first()
    if user_device:
        return Device(Device.ANDROID, user_device)

    raise DeviceNotFound()  # raise exception if device for given user doesn't exist
