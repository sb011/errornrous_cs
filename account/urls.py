from django.urls import path
from account.views import *
app_name = "account"

urlpatterns = [
    path('', home_view, name="home"),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('account/<user_id>/', account_view, name="view"),
    path('account/<user_id>/edit/', edit_account_view, name="edit"),
    path('search/', account_search_view, name="search"),
]
