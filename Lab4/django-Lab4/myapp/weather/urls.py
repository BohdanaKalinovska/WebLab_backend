from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "home"),
    path('delete/<city_name>/', views.delete_city, name='delete_city'),
    path('login', views.MyprojectLoginView.as_view(), name = 'login_page'),
    path('register', views.RegisterUserView.as_view(), name = 'register_page'),
    path('logout', views.MyprojectLogout.as_view(), name = 'logout_page'),
]
