from django.contrib import admin
from .models import *


admin.site.register(Rating)
admin.site.register(ProfileView)
admin.site.register(UserMatch)

admin.site.register(VirtualCurrency)
admin.site.register(Gift)
admin.site.register(UserGifts)
admin.site.register(UserImages)

