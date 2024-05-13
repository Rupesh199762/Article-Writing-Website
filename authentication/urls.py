from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('sign_in', views.sign_in, name="sign_in"),
    path('sign_up', views.sign_up, name="sign_up"),
    path('sign_out',views.sign_out, name="sign_out"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        views.activate, name='activate'), 
    
    path('saveArticle', views.saveArticle, name="saveArticle"),
    path('add_comment', views.add_comment, name="add_comment"),
    path('update_comment', views.update_comment, name="update_comment"),
    path('del_comment/', views.del_comment, name="del_comment"),
    path('upload_image/', views.upload_image, name="upload_image"),
    path('delete_image/', views.delete_image, name="delete_image"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)