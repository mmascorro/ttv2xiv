from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.twitch_login, name='login'),
    path('logout/', views.twitch_logout, name='logout'),
    path('authorize/', views.authorize, name='authorize'),
    path('about/', views.about, name='about'),
    path('lodestone_search/<str:world>/<str:name>/', views.lodestone_search, name='lodestone_search'),
    path('lodestone_check/<int:id>/', views.lodestone_check, name='lodestone_check'),
    path('delete/', views.delete_user, name='delete_user'),
    path('api/v1/users/<str:twitch_id>/', views.users_endpoint, name='users_endpoint'),
] 



