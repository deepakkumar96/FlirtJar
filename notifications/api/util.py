
class DeviceType:
    IOS = 'ios'
    ANDROID = 'android'
    UNKNOWN = 'unknown'

    @staticmethod
    def get_device_type(device):
        device = device.lower()
        if device == 'ios':
            return DeviceType.IOS

        elif device == 'android':
            return DeviceType.ANDROID

        else:
            return DeviceType.UNKNOWN
