
from rest_framework.renderers import JSONRenderer


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

