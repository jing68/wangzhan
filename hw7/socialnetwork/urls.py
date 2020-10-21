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
    path('otherprofile/<int:user_id>', views.other_profile, name='other_profile'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('add-comment/<int:id>',views.add_comment),
    path('get-list', views.get_list),
    path('refresh-global',views.refresh_global),
    path('refresh-follower',views.refresh_follower),

  
]