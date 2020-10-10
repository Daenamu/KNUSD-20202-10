from django.shortcuts import render
from django.views.generic import ListView, DetailView
from main.models import Post

# Create your views here.


class PostLV(ListView):
    template_name = 'main/post_list.html'
    model = Post


class PostDV(DetailView):
    template_name = 'main/post_detail.html'
    model = Post
