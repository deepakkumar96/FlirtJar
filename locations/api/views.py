from django.db.models import Q
from rest_framework import views, viewsets, generics, status
from rest_framework.exceptions import NotFound
from accounts.models import Account
from profiles.serializers import UserInfoSerializer
from locations.serializers import UserLocationSerializer
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.contrib.gis import measure, geos
from locations.api.utils import get_default_units
from django.contrib.gis.geos import GEOSException


class UserLocationDetail(generics.RetrieveAPIView):
    """
    # Return information including location of a particular user. (http://geojson.org/)

    ### __1. Description__
    Takes either Id of the user and return Location Detail.
    This return users location and important detail to
    showing user on the map.

    ### __2. Parameters__(URL) :
    User id must be passed in the url itself.

    ### __3. Response__
    Return the  information to represent a user in the map.

    * `id` : Unique id of the user
    * `email`: Email of the user
    * `first_name`: First Name of the user
    * `picture`: Profile Picture of the user
    * `location`: Latest location of the user

    ### __4. Example :__
    * `Request - `
          <pre> POST /api/location/user/2/ </pre>

    * `Response - `
          <pre>
          {
             "errors": {},
             "result": {
                "id": 20,
                "email": "example@gmail.com",
                "first_name": "example",
                "picture": "http://facebook/com/picture",
                "location": {
                    "type": "Point",
                    "coordinates": [
                        68.500879846386,
                        10.617657679834
                    ]
                }
             }
          }
          </pre>
    """
    queryset = Account.objects.all()
    serializer_class = UserLocationSerializer
    lookup_field = 'pk'


class UserLocationDetailByEmail(generics.RetrieveAPIView):
    """
    Docs
    """
    queryset = Account.objects.all()
    serializer_class = UserLocationSerializer
    lookup_field = 'email'


class NearByLocationUsers(generics.RetrieveAPIView):
    """
    # To fetch user profile nearby currently logged-in user.

    ### __1. Description__
    This Return a list(Array in json) of all the other users who are near the currently logged-in
    and the response always include current user's location along with others.
    This return users location and important detail to showing user on the map.

    ### __2. Parameters__(URL) :
    * `{near_by_distance}`: Specifies the distance under which other profile will be returned.
    * `{distance_unit}`: Specifies unit of distance`(`Possible units are `km` - Kilometer, `m` - meters, `mm` - milli-meter`)`

    ### __3. Response__
    Return An Array of user profile with the following information.

    * `id` : Unique id of the user
    * `email`: Email of the user
    * `first_name`: First Name of the user
    * `last_name`: First Name of the user
    * `profile_picture`: Profile Picture of the user
    * `location`: Latest location of the user

    ### __4. Example :__
    * `Request - `
          <pre> GET /api/location/nearby/100/km/ </pre>

    * `Response - `
          <pre>
          {
             "errors": {},
             "result": [
                {
                    "id": 20,
                    "email": "example@gmail.com",
                    "first_name": "example",
                    "picture": "http://facebook/com/picture",
                    "location": {
                        "type": "Point",
                        "coordinates": [
                            68.500879846386,
                            10.617657679834
                        ]
                },
                ...
             ]
          }
          </pre>

    ### __5. Possible Errors__
        1. `404` if unit of distance is invalid
        2. `404` if given user's location is undefined
    """
    queryset = Account.objects.all()
    serializer_class = UserInfoSerializer
    # renderer_classes = (JSONRenderer,)

    def get(self, request, near_by, unit):
        if unit not in get_default_units():
            raise NotFound(unit + ' is not a valid unit.')

        try:
            user = request.user
            distance_from_point = {unit: near_by}

            if not user.location:
                raise NotFound('Given users location is undefined.')

            near_by_users = Account.gis.filter(location__distance_lte=(user.location, measure.D(**distance_from_point)))
        except Account.DoesNotExist:
            raise NotFound('User not found.')

        serializer = UserInfoSerializer(near_by_users, many=True)
        return Response(serializer.data)


class NearByCustomLatLong(generics.RetrieveAPIView):
    """
    # To fetch user profile nearby custom latitude & longitude.

    ### __1. Description__
    This endpoint return a list(Array in json) of users nearby a custom latitude & longitude.
    latitude and longitude is provided in query parameters with name 'lat' and
    'long'.

    ### __2. Parameters__(URL) :
    * `{near_by_distance}`: Specifies the distance under which other profile will be returned.
    * `{distance_unit}`: Specifies unit of distance`(`Possible units are `km` - Kilometer, `m` - meters, `mm` - milli-meter`)`

    ### __3. Response__
    Return An Array of user profile with the following information nearby given lat & long.
    * `id` : Unique id of the user
    * `email`: Email of the user
    * `first_name`: First Name of the user
    * `last_name`: First Name of the user
    * `profile_picture`: Profile Picture of the user
    * `location`: Latest location of the user

    ### __4. Example :__
    * `Request - `
          <pre> GET /api/location/nearby/1000000/m/?lat=72&long=23 </pre>

    * `Response - `
          <pre>
          {
             "errors": {},
             "result": [
                {
                    "id": 20,
                    "email": "example@gmail.com",
                    "first_name": "example",
                    "picture": "http://facebook/com/picture",
                    "location": {
                        "type": "Point",
                        "coordinates": [
                            68.500879846386,
                            10.617657679834
                        ]
                },
                ...
             ]
          }
          </pre>

    ### __5. Possible Errors__
        1. `404` if unit of distance is invalid
        2. `404` if given user's location is undefined
    """

    serializer_class = UserSerializer
    queryset = Account.objects.all()

    def get(self, request, *args, **kwargs):
        if kwargs['unit'] not in get_default_units():
            raise NotFound(kwargs['unit']+' is not a valid unit.')

        lati = request.query_params.get('lat', None)
        longi = request.query_params.get('long', None)

        try:

            distance_from_point = {kwargs['unit']: kwargs['near_by']}
            point = "POINT(%s %s)" % (lati, longi)
            location = geos.fromstr(point)
            near_by_users = Account.gis.filter(location__distance_lte=(location, measure.D(**distance_from_point)))

        except Account.DoesNotExist:
            raise NotFound('User not found.')

        except GEOSException:
            raise NotFound('lat or long or both not specified in url query parameters.')

        serializer = UserInfoSerializer(near_by_users, many=True)
        return Response(serializer.data)
