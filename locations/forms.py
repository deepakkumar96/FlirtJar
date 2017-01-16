from django.contrib.gis import forms
from accounts.models import Account


class UserLocationForm(forms.ModelForm):
    """world = forms.MultiPolygonField(widget =
        forms.OSMWidget(attrs = {'map_width': 1024, 'map_height"""
    class Meta:
        model = Account
        fields = ['email', 'first_name', 'location']
