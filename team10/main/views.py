import json
import jwt
import requests
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib import auth
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from main.models import Post, User, MajorList, BoardList
from knu_reminder import secret

# Create your views here.

class BoardView(ListView):
    template_name = 'main/post_list.html'
    model = Post
    paginate_by = 20


def CreateBoardView(request):
    print(request.POST['department'])
    BoardList(board_name=request.POST['board_name'], department=json.dumps(request.POST['department']), user=request.user).save()
    return HttpResponse('<script type="text/javascript">window.close()</script>')  

def KakaoLogoutView(request):
    auth.logout(request)
    print("logout")
    return redirect('main:home')

class KakaoLoginView(View):
    def get(self, request):
        kakao_access_code = request.GET.get('code', None)
        url = 'https://kauth.kakao.com/oauth/token'
        headers = {'Content-type' : 'application/x-www-form-urlencoded; charset=utf-8'}
        body = {'grant_type' : 'authorization_code',
                'client_id' : secret.App_key,
                'redirect_uri' : secret.Redirect_URI,
                'code': kakao_access_code }
        
        token_kakao_response = requests.post(url, headers=headers, data=body)
        access_token = json.loads(token_kakao_response.text).get('access_token')

        url = 'https://kapi.kakao.com/v2/user/me'
        headers = {
            'Authorization' : f'Bearer {access_token}',
            'Content-type' : 'application/x-www-form-urlencoded; charset=utf-8'
        }
        kakao_response = requests.get(url, headers=headers)
        kakao_response = json.loads(kakao_response.text)

        if User.objects.filter(social_login_id = kakao_response['id']).exists():
            user = User.objects.get(social_login_id=kakao_response['id'])
            # jwt_token = jwt.encode({'id':user.id}, secret.SECRET_KEY, algorithm='HS256').decode('utf-8')
            print('user logged in')
            auth.login(request,user)

            return redirect('main:home')
        
        User(
            social_login_id = kakao_response['id'],
            social = 'kakao',
        ).save()
        user = User.objects.get(social_login_id=kakao_response['id'])
        auth.login(request, user)
        print('user saved')
        
        return redirect('main:home')

class PopupView(TemplateView):
    template_name = 'main/home_popup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        major_list = MajorList.objects.all()
        context['departments'] = major_list
        return context

class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_key'] = secret.App_key
        context['redirect_uri'] = secret.Redirect_URI

        if self.request.user is not None:
            boards = BoardList.objects.filter(user=self.request.user)
        else:
            boards = []
        context['boards'] = boards

        return context

class PostLV(ListView):
    template_name = 'main/post_list.html'
    model = Post
    paginate_by = 20

    def get_queryset(self):
        try:
            search_key = self.request.GET['search_key']
            return Post.objects.filter(title__icontains=search_key)
        except:
            return Post.objects.all()

class PostDV(DetailView):
    template_name = 'main/post_detail.html'
    model = Post
