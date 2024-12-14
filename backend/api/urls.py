from django.urls import path
from . import views

urlpatterns = [
    path('predictions/user/', views.PredictionListCreate.as_view(), name='user-predictions'),
    path('predictions/all/', views.AllPredictionListCreate.as_view(), name='all-predictions'),
    path('predictions/delete/<int:pk>/', views.PredictionDelete.as_view(), name='delete-prediction'),
    path('user-info/', views.user_info, name='user-info'),
]