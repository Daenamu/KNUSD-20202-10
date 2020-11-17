from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/', views.PostLV.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDV.as_view(), name='post_detail'),
    path('board/', views.PopupView.as_view(), name='board'),
    path('kakao_redirect/', views.KakaoLoginView.as_view(), name='kakao_redirect'),
    path('kakao_logout/', views.KakaoLogoutView, name='logout'),
    path('create_board/', views.CreateBoardView, name='create_board'),
]
