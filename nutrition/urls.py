from django.urls import path
from . import views

urlpatterns = [
    path('accounts/login/', views.login_signup_view, name='login_signup'),
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('reset_password/', views.reset_password_view, name='reset_password'),
    path('nutrition/dashboard/', views.dashboard_views, name='dashboard'),
    path('nutrition/clubs/', views.clubs_views, name='clubs'),
    path('nutrition/clubs_add/', views.add_clubs_views, name='clubs_add'),
    path('nutrition/clubs/request_info/<int:id>', views.request_club_info_views, name='request_info'),
    path('profile/account/', views.account_views, name='account'),
    path('nutrition/players/', views.players_views, name='players'),
    path('nutrition/foods/', views.foods_views, name='foods'),
    path('nutrition/archive_players/',
         views.archive_players_views, name='archive_players') 
    ]
