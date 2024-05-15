from django.urls import include, path
from rest_framework import routers
from apis.view import *

router = routers.DefaultRouter()
router.register(r'article', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]

