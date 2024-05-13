from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    #path('upload_data', views.upload_excel, name="upload_data"),
    path('getting_data', views.getting_data, name="getting_data"),
    path('detailed_view', views.detailed_view, name="detailed_view"),
    path('article_data/<int:a_id>', views.article_data, name="article_data"),


    path('<str:current_url>/detailed_view', views.detailed_view, name="detailed_view"),
    path('user/<str:session_id>/', views.user_page, name="user_page"),
    path('view_articles', views.view_articles, name="view_articles"),
    path('view_try', views.view_try, name="view_try"),


    path('get_company_list/', views.get_company_list, name='get_company_list'),
    path('get_bond_list/', views.get_bond_list, name='get_bond_list'),
    # path('get_items', views.get_items, name='get_items'),



]

