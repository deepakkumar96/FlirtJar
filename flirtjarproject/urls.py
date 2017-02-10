"""flirtjarproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from accounts import views
from locations import views as loc_view
from rest_framework_swagger.views import get_swagger_view
from rest_framework.urlpatterns import format_suffix_patterns
# from rest_auth import views, urls
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from django.conf.urls.static import static
from . import settings
from profiles.api.views import GiftsListView

@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
@permission_classes((AllowAny, ))
def schema_view(request):
    generator = schemas.SchemaGenerator(title='FlirtJar API')
    return response.Response(generator.get_schema(request=request))


urlpatterns = [

    url(r'^api/docs/intro/', loc_view.api_doc_intro),
    url(r'^location/user/(?P<pk>[0-9]+)/nearby/(?P<near_by>[0-9]+)/(?P<unit>[A-Za-z]+)$', views.home),
    url(r'^api/users/', include('accounts.urls')),
    url(r'^api/profile/', include('profiles.urls')),
    url(r'^api/location/', include('locations.urls')),
    url(r'^api/notifications/', include('notifications.urls')),
    url(r'^admin/', admin.site.urls),
    # url(r'^api/auth/', include('rest_auth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api/docs/$', get_swagger_view(title='FlirtJar Api')),
    url(r'^docs/', include('rest_framework_docs.urls')),

    # Urls that doesn't belong to any specific app
    url(r'api/gifts/$', GiftsListView.as_view(), name='gift_view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

