from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from api import views

app_name = 'api'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    path(route='dealership', view=views.dealership, name='dealership'),
    path(route='review', view=views.review, name='review'),
]