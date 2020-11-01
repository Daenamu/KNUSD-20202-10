from django.shortcuts import render
from django.views.generic import ListView, DetailView
from main.models import Post

# Create your views here.


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
