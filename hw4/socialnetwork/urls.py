from django.urls import path
from socialnetwork import views
urlpatterns = [
    path('', views.global_stream, name='home'),
    path('login', views.login_action, name='login'),
    path('logout',views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('global', views.global_stream, name='global'),
    path('follower',views.follower_stream, name='follower'),
    path('profile', views.profile_logged_in, name='profile_logged_in'),
    path('jam', views.jam, name='jam'),
]