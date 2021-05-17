from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView
from . import views

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('<str:user_id>/advisor/<str:id>',
         views.appointment_create, name='create'),
    path('<str:user_id>/advisor/booking/',
         views.booking_list, name='booking_list'),
    path('<str:user_id>/advisor', views.advisor_list, name='advisor'),
]
