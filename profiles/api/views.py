from django.db.models import Q
from django.contrib.gis.measure import D
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render

from rest_framework import views, viewsets, generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from datetime import date

from notifications.models import Notification
from notifications.util import get_notification_icon, create_notification
from profiles.serializers import *
from accounts.serializers import UserSerializer
from .util import convert_to_reponseid, is_valid_response, get_user_match
from accounts.permissions import AllowOwner, IsInstagramUser


class UserRatingeDetail(generics.RetrieveAPIView):
    """
    This returns rating of user profile that includes
    users like, superlike, view, skipped and rating.
    """
    queryset = Account.objects.all()
    serializer_class = UserRatingSerializer
    lookup_field = 'pk'


class UserImageListView(generics.ListCreateAPIView):
    """
        get:
            # Returns an array of all the user images except profile picture

        example : GET /api/profile/pictures/
        <pre>
            {
                  "errors": {},
                  "result": [

                    {
                      "id": 25,
                      "image": "https://www.getpostman.com/img/download/install_postman.png?0e807c25fad195b7633ac0a64ee99ea2&"
                    },

                    {
                      "id": 24,
                      "image": "http://www.django-rest-framework.org/img/logo.png"
                    },

                  ]
            }
        </pre>
        ---

        post:
            # Takes an array of images and store it for currently logged-in user.

        example : POST /api/profile/pictures/
        Request Body :
        <pre>
            [

{
    "image": "image-url-1"
},

{
    "image": "image-url-2"
}

]
        </pre>

    """

    serializer_class = UserImageSerializer

    def get_queryset(self):
        return UserImages.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = UserImageSerializer(data=request.data, many=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
        except:
            """
                If the errors received from rest_framework.exceptions.ValidationError is of
                type ReturnList then here it is get converted into ReturnDict so that errors
                can be easily handled by custom exception handler(accounts.util.custom_exception_handler)
            """
            validation_errors = \
                serializer.errors if type(serializer.errors) is ReturnDict else serializer.errors[0]
            raise ValidationError(validation_errors)
        return Response({'data': 'saved'})


class UsersImageListView(generics.ListAPIView):
    """
        get:
            # Returns an array of all the images except profile picture for particular given user

        example : GET /api/profile/pictures/user/{id}/
        <pre>
            {
                  "errors": {},
                  "result": [

                    {
                      "id": 25,
                      "image": "https://www.getpostman.com/img/download/install_postman.png?0e807c25fad195b7633ac0a64ee99ea2&"
                    },

                    {
                      "id": 24,
                      "image": "http://www.django-rest-framework.org/img/logo.png"
                    },

                  ]
            }
        </pre>

    """

    serializer_class = UserImageSerializer

    def get_queryset(self):
        try:
            user = Account.objects.get(pk=int(self.kwargs['pk']))
            return UserImages.objects.filter(user=user)
        except Account.DoesNotExist:
            raise NotFound('Account does not exist with given user id.')


class VirtualCurrencyView(generics.RetrieveUpdateAPIView):
    """

    get:
        # To Retrieve User's Virtual Currency.

    put:
        # To Update Value of User's Virtual Currency.
        It takes user id in url parameter and coins
        information in POST data.

        example : /api/profile/currency/user/2

            - {
                "coins" : "100"
              }

        ---
        response_serializer: VirtialCurrencyOperation

    """
    serializer_class = VirtualCurrencySerializer
    # permission_classes = (AllowOwnerOrReadOnly,)

    def get_queryset(self):
        return VirtualCurrency.objects.get(user=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        currency = VirtualCurrency.objects.get(user=self.request.user.pk)
        return Response(VirtualCurrencySerializer(currency).data)

    def put(self, request, *args, **kwargs):
        """
        # To Update, Add, Subtract coins for users

        request body: <pre>{ "coins": 10, "user":1, "operation":"add"}</pre>

        operation can be : <pre>"add" or "sub"</pre>

        """
        operation = self.request.data.get('operation', None)
        coins = self.request.data.get('coins', None)
        user_coins = request.user.coins

        # Updating Coins
        if coins:
            if operation:
                if operation == 'add':
                    user_coins.coins += int(coins)

                if operation == 'sub':
                    user_coins.coins -= int(coins)

                if operation == 'update':
                    user_coins.coins = int(coins)
                user_coins.save()
        else:
            pass

        serializers = VirtualCurrencySerializer(user_coins)
        return Response(serializers.data)


class GiftsListView(generics.ListAPIView):
    serializer_class = GiftSerializer
    queryset = Gift.objects.all()


class UserGiftView(generics.ListAPIView):
    """
    get:
        # To get a list of all the received gifts
    """
    serializer_class = UserGiftSerializer

    def get_queryset(self):
        # Optimized
        return UserGifts.objects.select_related('gift').filter(user_to=self.request.user)


class GiftSendView(generics.CreateAPIView):
    """
    # To send a gift to some other user
    """
    serializer_class = GiftSendSerializer
    queryset = UserGifts.objects.all()

    def create(self, request, *args, **kwargs):
        user_coins = VirtualCurrency.objects.get(user=request.user)
        gift_price = get_object_or_404(Gift, pk=request.data['gift']).price
        if user_coins.coins >= gift_price:
            response = super(GiftSendView, self).create(request, *args, **kwargs)
            user_coins.coins -= gift_price
            user_coins.save()
            return response
        else:
            raise NotFound("Insufficient  Coins")


class UserProfileView(generics.GenericAPIView):
    """
    1.Returns the count of users view, like, superlike and skipped.
       It Accept ID of the user in url parameter

    ---

    2.It can also accept query parameter named response, which
    can be used to get a list of users who have liked, superliked,
    view or skipped the given user.

        Value of response query parameter can be 0, 1, 2, 3 which means
        likes, skipped, superlikes and views respectively.

    example : /api/profile/view/user/2/?response=0

    Will Return a list of all the users who liked user_2.


    POSSIBLE ERRORS :
        2. 404 if given user's id doesn't exist
        3. 404 if value of response parameter is invalid

    """

    serializer_class = UserProfileViewSerializer
    queryset = Account.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            user = request.user  # Account.objects.get(pk=kwargs['pk'])
            serializer = UserProfileViewSerializer(user)
        except Account.DoesNotExist:
            raise NotFound('There is no user with given id.')

        # Handling response query param if passed
        response = request.query_params.get('response', None)
        if response:
            try:
                is_response_valid = is_valid_response(int(response))
                if not is_response_valid:
                    raise ValueError
            except ValueError:
                raise NotFound('response query value is invalid.')

            print('resp : ', response)

            responsed_users = (u.user_from for u in user.views.select_related('user_from').filter(user_to=request.user, response=int(response)))
            # print([r for r in responsed_users])
            serializer = UserInfoSerializer(responsed_users, many=True)

            # filtering response with query parameter response_size
            query_response_size = request.query_params.get('response_size', None)
            if query_response_size:
                if query_response_size == 'full':
                    serializer = UserSerializer(responsed_users, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        # To save user response on cards (** This endpoint performs costly operation).


        It accepts given user response on other user profile
        indicating whether the given user likes, superlike or
        skipped someone profile and accordingly api makes
        match if possible.

        ---
         - Response Format:

           [
                {
                    user_from : id,
                    user_to:    id,
                    response: 0(like) | 1(skipped) | 2(superlike)
                },
                {
                    ...
                }
           ]
        <hr>
        This endpoint should be called in bulk at time to save
        server time.

        """

        serializer = UserProfileMatchResponseSerializer(data=request.data, many=True)
        if serializer.is_valid():
            notifications = []
            for s in serializer.data:
                print('s', s)
                # Checking For UserMatch, Likes, SuperLikes, Views
                user_from = Account.objects.get(pk=s['user_from'])
                user_to = Account.objects.get(pk=s['user_to'])
                if s['response'] != 1 and ProfileView.objects.filter(user_from=user_to, user_to=user_from).filter(Q(response=0) | Q(response=2)).count() > 0:
                    try:
                        print('Enter ', user_from, ' ', user_to)
                        UserMatch.objects.create(user_from=user_from, user_to=user_to)
                        # Notifying User's about their match
                        notifications.append(
                            create_notification(user_from, 'You have a match with ' + user_to.first_name, Notification.MATCH),
                        )
                        notifications.append(
                            create_notification(user_to, 'You have a match with ' + user_from.first_name, Notification.MATCH)
                        )
                    except IntegrityError:
                        pass

                if s['response'] == 0:
                    user_to.likes += 1
                    notifications.append(
                        create_notification(user_to, user_from.first_name + ' likes you.', Notification.LIKE)
                    )

                if s['response'] == 1:
                    user_to.skipped += 1

                if s['response'] == 2:
                    user_to.superlikes += 1
                    notifications.append(
                        create_notification(user_to, user_from.first_name + ' has crush on you.', Notification.CRUSH)
                    )

                user_to.save()
                ProfileView.objects.create(user_from=user_from, user_to=user_to, response=s['response'])

            # Creating Notification Inside Database
            # print(Notification.objects.bulk_create(notifications))
            for notification in notifications:
                notification.save()
        else:
            raise NotFound('Invalid Json Data.')

        return Response({'detail': 'data saved.'})


class UserMatchView(generics.ListAPIView):
    """
    Return a list all the users who have match with
    the given user.
    """
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        return get_user_match(self.request.user)


class CardView(generics.ListAPIView):
    """
    # To return cards
    """
    serializer_class = UserSerializer
    queryset = Account.objects.all()

    def get(self, request, *args, **kwargs):

        # Default values for filter
        min_age = 16
        max_age = 32
        user_location = request.user.location
        distance = 1000

        # Validating
        if user_location is None:
            raise NotFound({'detail': 'Your location is undefined.'})

        # accepting values from query params(if passed) for filtering
        min_age_query = request.query_params.get('min_age', None)
        max_age_query = request.query_params.get('max_age', None)
        gender = request.query_params.get('gender', None)

        try:
            # changing min & max age according to query params if passed
            min_age = int(min_age_query if min_age_query else min_age)
            max_age = int(max_age_query if max_age_query else max_age)
        except:
            pass

        # Calculating required_date according given age
        today = date.today()
        required_min_date = today.replace(year=today.year - min_age)
        required_max_date = today.replace(year=today.year - max_age)

        # Filtering With required date and location
        users = Account.objects.filter(dob__gte=required_max_date, dob__lte=required_min_date)\
                               .filter(location__distance_lte=(user_location, D(km=distance)))\
                               .filter(show_me_on_jar=True)\
                               .order_by('location')

        # Filtering With Gender
        # If gender is passed in query param then it uses that value, else it filters with user's opposite gender
        if gender:
            if gender == 'M':
                users = users.filter(gender='M')
            elif gender == 'F':
                users = users.filter(gender='F')
        else:
            # Else Filtering with opposite gender
            users = users.filter(gender=('F' if request.user.gender == 'M' else 'M'))

        return Response(UserSerializer(users, many=True).data)


class ProfileRecommendationList(generics.ListAPIView):
    """
    This returns a list of recommended profiles for a particular user.
    And this is available for only those users whose 'instagram' account is activated.
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsInstagramUser)

    def get_queryset(self):
        from random import sample
        total_records = Account.objects.all().count()
        result_count = 10

        if result_count > total_records:
            result_count = total_records

        rand_ids = sample(range(1, total_records), result_count-1)
        print(rand_ids)
        return Account.objects.filter(id__in=rand_ids)


