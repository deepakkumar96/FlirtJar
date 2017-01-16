from rest_framework import views, viewsets, generics, status, serializers as rest_serializer
from accounts.models import Account
from accounts.serializers import UserSerializer, UserSerializerWithoutOAuthId
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from accounts.permissions import AllowOwnerOrReadOnly, AllowOwner


class UserListView(generics.ListCreateAPIView):
    """
        get:
            # Return instance of all users

            ### __1. Description__ :

            This endpoint return a list of all the users account,
            It has no particular use in application.


        post:
            # To Create a new User and Get Authentication Token.

            ### __1. Description__ :

            This endpoint can be used to create user account .
            It Accepts user information in json format in which
            email and oauth_id field is mandatory and if operation
            is successful then it returns Authorization Token and
            this Token must be included in --Authorization Header
            of every other request.

            ### __2. Parameters__(Post) :
            ####Mandatory
                * `email` : unique across all the users
                * `oauth_id` : facebook id in this case

            ####OPtional
                `first_name, last_name, dob, language, hairs_color etc...`

            ### __3. Response__
            Response return Authentication Token With a unique user id which must be
            saved by client for further request.

            * `id` : Unique id that must be saved by client for further request
            * `email`: Email must also be saved as it will be passed when making changes to user profile
            * `Token`: Authentication Token that must passed with every request

            ### __4. Example :__
            * `Request - `
                  <pre>
                  POST /api/users/
                  {
                    "email": "example@gmail.com",
                    "oauth_id": "2312",
                    "first_name": "name",
                     ...
                  }
                  </pre>

            * `Response - `
                  <pre>
                  {
                     "errors": {},
                     "result": {
                        "id": 20,
                        "email": "example@gmail.com",
                        "Token": "g56uy234jhnf83487i723h"
                     }
                  }
                  </pre>

    """
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    # lookup_field = 'pk'
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        email = request.data.get('email', None)
        oauth_id = request.data.get('oauth_id', None)

        try:
            # Checking if user already exist
            if email is not None and oauth_id is not None:
                existing_user = Account.objects.get(email=email, oauth_id=oauth_id)
                return Response({
                    'id': existing_user.pk,
                    'email': existing_user.email,
                    'Token': Token.objects.get(user=existing_user).key
                })
        except Account.DoesNotExist:
            pass

        serializer.is_valid(raise_exception=True)
        serializer.save()
        new_user = Account.objects.get(email=request.data['email'])
        # Return the success message with OK HTTP status
        return Response(
            {
                'id': new_user.pk,
                'email': new_user.email,
                'Token': Token.objects.get(user=new_user).key
            },
            status=status.HTTP_200_OK
        )


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
        get:
            # Return user information

            ### __1. Description__:
            This return information about any user and response
            includes all the basic information about the user.


            ### __2. Parameter__(URL):
            * `id`: Unique id of the user.

            ### __3. Response :__
            Return all the user information.

            ### __4. Example :__
            * `Request : `
                <pre> POST /api/users/2/ </pre>
            * `Response : `
                <pre>
                {
                    "errors": { },
                    "result": {
                        "id": "2",
                        "email": "xyz@gmail.com",
                        "first_name": "Name",
                        ...
                    }
                }
                </pre>

        delete:
            # Remove an existing User with given id in url.

        patch:
            # Update one or more fields on an existing user with given id in url.
            ####(Docs for this endpoint is same as `PUT /api/users/{id}/`)

        put:
            # Update a user with given id in url.
            ####(Docs for this endpoint is same as `PUT /api/users/me`)

            ### __1. Example__ (To Update Users `last_name`) __:__
            * `Request - `
                   <pre>
                        POST /api/users/{id}/
                        {
                            "email": "example@gmail.com", (> email field is mandatory in request.)
                            "last_name": "Name Changes"
                            "other_field": "changes..."
                        }
                   </pre>`
            * `Response - `
                    <pre>
                        {
                            "errors": {},
                            "result": {
                                "id": 294,
                                "email": "example@gmail.com",
                                ...(This include complete updated information.)
                            }
                        }
                    </pre>

        """
    queryset = Account.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowOwnerOrReadOnly,)
    lookup_field = 'pk'


class CurrentUserDetail(generics.RetrieveUpdateAPIView):
    """
        get:
            # Return information about currently logged-In User

            ### __1. Description__:
            This endpoint return information about the user
            who is currently logged-in client can use this
            endpoint instead of `/api/user/{id}` to get information
            about current user.

            ### __2. Parameters__:
            This endpoint takes no parameter as it is available only
            for currently logged-in user.

            `/api/user/{id}` should be used get information
            about other user.

            ### __3. Response :__
            Return all the user information.

            ### __4. Example :__
            * `Request : `
                <pre> POST /api/users/me/ </pre>
            * `Response : `
                <pre>
                {
                    "errors": { },
                    "result": {
                        "id": "2",
                        "email": "xyz@gmail.com",
                        "first_name": "Name",
                        ...
                    }
                }
                </pre>


        put:
            # To Update information about current user
            (Below Documentation of this endpoint is also same for endpoint `POST /api/users/{id}/`)

            ### __1. Description__:
            This endpoint can be used to update current user
            information or profile changes. email must be presented
            in POST body of the request.

            ### __2. Parameters__(POST Body) :
            ####Mandatory
            * `email` : this filed must be present in post body

            ####Optional
                `Any other possible field can be passed with POST body for changes.`

            ### __4. Response__
            Return updated user information.

            ### __3. Example__ (To Update Users `last_name`) __:__
            * `Request - `
                    <pre>
                        POST /api/users/me/
                        {
                            "email": "example@gmail.com",
                            "last_name": "Name Changes"
                            "other_field": "changes..."
                        }
                    </pre>
            * `Response - `
                    <pre>
                        {
                            "errors": {},
                            "result": {
                                "id": 294,
                                "email": "example@gmail.com",
                                ...(This include complete updated information.)
                            }
                        }
                    </pre>
        patch:
            # To make partial changes to the currently logged-in user.
            (Docs for this endpoint is same as `PUT /api/users/me`)

    """
    serializer_class = UserSerializerWithoutOAuthId
    queryset = Account.objects.all()

    def get_object(self):
        return self.request.user




