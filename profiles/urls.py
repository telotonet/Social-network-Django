from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profiles/', profiles, name='profiles'),
    path('user_ajax/<int:user_id>/', get_user_ajax, name='user_ajax'),
    path('friend-request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('friends/', friendlist, name='friends'),
]