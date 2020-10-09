from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.PostLV.as_view(), name='index'),
    path('post/', views.PostLV.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDV.as_view(), name='post_detail'),
]
