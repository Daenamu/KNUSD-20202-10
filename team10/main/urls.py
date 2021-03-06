from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/', views.PostLV.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDV.as_view(), name='post_detail'),
    path('popup/', views.PopupView.as_view(), name='popup'),
    path('kakao_redirect/', views.KakaoLoginView.as_view(), name='kakao_redirect'),
    path('kakao_delete/', views.KakaoDeleteView, name='delete'),
    path('kakao_logout/', views.KakaoLogoutView, name='logout'),
    path('create_board/', views.CreateBoardView, name='create_board'),
    path('delete_board/', views.DeleteBoardView, name='board_delete'),
    path('bookmark/', views.BookmarkView, name='bookmark'),
    path('alarm/', views.AlarmView, name='alarm'),
    path('share/', views.ShareView, name='share'),
]
