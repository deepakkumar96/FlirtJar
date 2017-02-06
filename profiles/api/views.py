from rest_framework import views, viewsets, generics, status
from profiles.models import Rating, ProfileView, UserMatch
from django.db.models import  Q
from django.db import IntegrityError
from accounts.models import Account
from profiles.serializers import *
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from .util import convert_to_reponseid, is_valid_response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import AllowOwner, AllowOwnerOrReadOnly
from .util import get_user_match


class UserRatingeDetail(generics.RetrieveAPIView):
    """
    This returns rating of user profile that includes
    users like, superlike, view, skipped and rating.
    """
    queryset = Account.objects.all()
    serializer_class = UserRatingSerializer
    lookup_field = 'pk'


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
        ---

        request_serializer: VirtialCurrencyOperation
        response_serializer: VirtialCurrencyOperation


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
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        try:
            user = Account.objects.get(pk=kwargs['pk'])
            serializer = UserProfileViewSerializer(user)
        except Account.DoesNotExist:
            raise NotFound('There is no user with given id.')

        # Handling response query param if passed
        response = request.query_params.get('view_type', None)
        if response:
            try:
                is_response_valid = is_valid_response(int(response))
                if not is_response_valid:
                    raise ValueError
            except ValueError:
                raise NotFound('response query value is invalid.')
            responsed_users = [u.user_from for u in user.views.select_related('user_from').filter(response=int(response))]
            serializer = UserInfoSerializer(responsed_users, many=True)

            # filtering response with query parameter view_size
            query_response_size = request.query_params.get('view_size', None)
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

        # print('POST')
        serializer = UserProfileMatchResponseSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            for s in serializer.data:
                # Making User Match
                user_from = Account.objects.get(pk=s['user_from'])
                user_to = Account.objects.get(pk=s['user_to'])
                if s['response'] != 1 and ProfileView.objects.filter(user_from=user_to, user_to=user_from).filter(Q(response=0) | Q(response=2)).count() > 0:
                    try:
                        UserMatch.objects.create(user_from=user_from, user_to=user_to)
                    except IntegrityError:
                        pass
                else:
                    pass
                if s['response'] == 0:
                    user_to.likes += 1

                if s['response'] == 1:
                    user_to.skipped += 1

                if s['response'] == 2:
                    user_to.superlike += 1

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
        from datetime import date
        from django.contrib.gis.measure import D

        # Calculating required_date according given age
        min_age = 18
        max_age = 32
        required_date = date.today()
        required_min_date = required_date.replace(year=required_date.year - min_age)
        required_max_date = required_date.replace(year=required_date.year + max_age)
        # print('date : ', required_date)
        # Distance Calculation
        user_location = request.user.location
        distance = 1000

        gender = request.user.gender
        print(gender)
        users = Account.objects.filter(gender=gender)\
                               .filter(dob__lte=required_min_date)\
                               .filter(location__distance_lte=(user_location, D(km=distance)))\
                               .order_by('location')

        return Response(UserSerializer(users, many=True).data)


