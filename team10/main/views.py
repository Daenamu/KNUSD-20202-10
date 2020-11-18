import json
import jwt
import requests
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib import auth
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from main.models import Post, User, MajorList, BoardList, Bookmark
from knu_reminder import secret
from django.db.models import Q

# Create your views here.

def AlarmView(request):
    board_name = request.POST.get('board_name', None)
    if board_name == "bookmark":
        bookmark = Bookmark.objects.get(user=request.user)
        if bookmark.alarm:
            bookmark.alarm = False
            result = False
        else:
            bookmark.alarm = True
            result = True
        bookmark.save()
    else:
        board = BoardList.objects.get(user=request.user, board_name=board_name)
        if board.alarm:
            board.alarm = False
            result = False
        else:
            board.alarm = True
            result = True
        board.save()
    context = {'result':result}
    return HttpResponse(json.dumps(context), content_type="application/json")
    

def BookmarkView(request):
    pk = str(request.POST.get('pk', None))
    bookmark = Bookmark.objects.get(user=request.user)
    jsonDec = json.decoder.JSONDecoder()

    try:
        ids = jsonDec.decode(bookmark.post)
        if pk not in ids:
            ids.append(pk)
            message = "북마크 완료"
            result = True
        else:
            ids.remove(pk)
            message = "북마크 삭제 완료"
            result = False
        bookmark.post = json.dumps(ids)
        bookmark.save()
    except:
        ids = []
        ids.append(pk)
        bookmark.post = json.dumps(ids)
        message = "북마크 완료"
        bookmark.save()
        result = True

    context = {'message': message, 'result':result}
    return HttpResponse(json.dumps(context), content_type="application/json")

def DeleteBoardView(request):
    BoardList.objects.get(board_name=request.GET['board_name'], user=request.user).delete()
    return redirect('main:home')

def CreateBoardView(request):
    try: 
        BoardList.objects.get(board_name=request.POST['board_name'])
        return redirect('main:popup')
    except:
        BoardList(board_name=request.POST['board_name'], department=json.dumps(request.POST.getlist('department[]')), user=request.user).save()
        return HttpResponse('<script type="text/javascript">window.close()</script>')  

def ShareView(request):
    id = request.POST.get('pk', None)
    post = Post.objects.get(id=id)
    ACCESS_TOKEN = request.user.token

    url = 'https://kapi.kakao.com/v1/api/talk/friends'
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    elements = json.loads(response.text).get('elements')
    uuid = elements[0]['uuid']

    url = 'https://kapi.kakao.com/v1/api/talk/friends/message/default/send'
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    body = {
        'receiver_uuids' : [f"{uuid}"],
        'template_object' : json.dumps({ 
            "object_type" : "text",
            "text" : f"{post.title}",
            "link" : {
                "web_url" : f"{post.url}",
                "mobile_web_url" : f"{post.url}",
            }
        })
    }
    response = requests.post(url, headers=headers, data=body)

    context = {'success':response.status_code}

    return HttpResponse(json.dumps(context), content_type="application/json")

def KakaoDeleteView(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    return redirect('main:home')

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
        refresh_token = json.loads(token_kakao_response.text).get('refresh_token')

        url = 'https://kapi.kakao.com/v2/user/me'
        headers = {
            'Authorization' : f'Bearer {access_token}',
            'Content-type' : 'application/x-www-form-urlencoded; charset=utf-8'
        }
        kakao_response = requests.get(url, headers=headers)
        kakao_response = json.loads(kakao_response.text)

        nickname = kakao_response['properties']['nickname']

        if User.objects.filter(social_login_id = kakao_response['id']).exists():
            user = User.objects.get(social_login_id=kakao_response['id'])
            user.token = access_token
            user.refresh_token = refresh_token
            user.save()
            # jwt_token = jwt.encode({'id':user.id}, secret.SECRET_KEY, algorithm='HS256').decode('utf-8')
            auth.login(request,user)

            return redirect('main:home')
        User(
            social_login_id = kakao_response['id'],
            social = 'kakao',
            token = access_token,
            refresh_token= refresh_token,
            nickname= nickname,
        ).save()
        user = User.objects.get(social_login_id=kakao_response['id'])
        Bookmark(
            user=user
        ).save()
        auth.login(request, user)
        
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

        if self.request.user.is_authenticated:
            boards = BoardList.objects.filter(user=self.request.user)
            bookmark = Bookmark.objects.get(user=self.request.user)
            bookmark = bookmark.alarm
        else:
            boards = []
            bookmark = False
        context['boards'] = boards
        context['bookmark'] = bookmark

        return context

class PostLV(ListView):
    template_name = 'main/post_list.html'
    model = Post
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET['board_name'] == "Bookmark":
            bookmark = Bookmark.objects.get(user=self.request.user)
            jsonDec = json.decoder.JSONDecoder()
            try:
                ids = jsonDec.decode(bookmark.post)
            except:
                ids = []
            try:
                search_key = self.request.GET['search_key']
                return Post.objects.filter(Q(title__icontains=search_key) & Q(id__in=ids))
            except:
                return Post.objects.filter(id__in=ids)
        else:
            try:
                board = BoardList.objects.get(user=self.request.user, board_name=self.request.GET['board_name'])
                jsonDec = json.decoder.JSONDecoder()
                departments = jsonDec.decode(board.department)
                try:
                    search_key = self.request.GET['search_key']
                    return Post.objects.filter(Q(title__icontains=search_key) & Q(department__in=departments))
                except:
                    return Post.objects.filter(department__in=departments)
            except: # 전체 공지
                try:
                    search_key = self.request.GET['search_key']
                    return Post.objects.filter(title__icontains=search_key)
                except:
                    return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET['board_name'] == "Bookmark":
            context['board_name'] = 'Bookmark'
            return context
        else:
            try:
                board = BoardList.objects.get(user=self.request.user, board_name=self.request.GET['board_name'])
                jsonDec = json.decoder.JSONDecoder()
                departments = jsonDec.decode(board.department)
                context['departments'] = departments
                context['board_name'] = board.board_name
                return context
            except:
                context['board_name'] = "전체 공지"
                return context

class PostDV(DetailView):
    template_name = 'main/post_detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        bookmark = Bookmark.objects.get(user=self.request.user)
        jsonDec = json.decoder.JSONDecoder()
        try:
            ids = jsonDec.decode(bookmark.post)
        except:
            ids = []

        if str(kwargs['object'].id) in ids:
            context['is_bookmark'] = True
        else:
            context['is_bookmark'] = False
        try:
            context['board_name'] = self.request.GET['board_name']
            return context
        except: return context