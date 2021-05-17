from django.urls import path, include
from . import views
from rest_framework import routers

# router = routers.SimpleRouter()

# router.register(r'advisor',views.advisor_create)

urlpatterns = [
    path('list/', views.advisor_list, name="product-list"),
    path('advisor/', views.advisor_create, name="product-list"),
]
