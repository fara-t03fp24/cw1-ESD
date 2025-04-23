from django.urls import path
from . import views

urlpatterns = [
    path('', views.CityListView.as_view(), name='city_list'),
    path('city/<int:pk>/', views.CityDetailView.as_view(), name='city_detail'),
]