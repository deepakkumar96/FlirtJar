
from rest_framework.views import exception_handler
from rest_framework.renderers import JSONRenderer


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
        print('exception msg : ', response.data, type(response.data))
        for k, v in response.data.items():
            errors.append("{} : {}".format(k, v))

        response.data = {
            # 'status_code': response.status_code,
            'errors': errors
        }
    return response


class CustomJSONRenderer(JSONRenderer):
    """
        Override the render method of the django rest framework JSONRenderer to allow the following:
        * adding a resource_name root element to all GET requests formatted with JSON
        * reformatting paginated results to the following structure {meta: {}, resource_name: [{},{}]}

        NB: This solution requires a custom pagination serializer and an attribute of 'resource_name'
            defined in the serializer
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {}
        # print('CUSTOM RENDERER')
        #determine the resource name for this request - default to objects if not defined
        # resource = getattr(renderer_context.get('view').get_serializer().Meta, 'resource_name', 'objects')

        #check if the results have been paginated

            # response_data[resource] = data

        # print('contains errors : ', data.get('errors', None))
        response_data['errors'] = {}
        if isinstance(data, dict):
            errors = data.get('errors', None)
            if errors:
                response_data['errors'] = errors
                del (data['errors'])

        response_data['result'] = data
        # call super to render the response
        response = super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)

        return response
