from django.contrib import admin
from main.models import Post
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'content',
                    'upload_dt', 'department', 'url')
    list_filter = ('upload_dt', )
    search_fields = ('title', 'content', 'slug')
    prepopulated_fields = {'slug': ('title', )}
