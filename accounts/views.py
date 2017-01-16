from django.shortcuts import render
from locations.forms import UserLocationForm
from accounts.models import Account
from django.contrib.gis import measure


def home(request, pk, unit, near_by):
    try:
        user = Account.objects.get(pk=pk)
        distance_from_point = {unit: near_by}
        print('Location : ', user.location)
        near_by_users = Account.gis.filter(location__distance_lte=(user.location, measure.D(**distance_from_point)))
    except Account.DoesNotExist:
        near_by_users = None

    print('NEAR LOCATION : ', near_by_users)

    context = {
        'label': 'Yo!',
        'user': user,
        'near_by_users': near_by_users,
    }
    return render(request, 'accounts/html/index.html', context)



