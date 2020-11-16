from django.contrib import admin
from main.models import Post, SocialPlatform, MajorList, User
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'content',
                    'upload_dt', 'department', 'url')
    list_filter = ('upload_dt', )
    search_fields = ('title', 'content', 'slug')
    prepopulated_fields = {'slug': ('title', )}

@admin.register(SocialPlatform)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'platform')

@admin.register(MajorList)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'major')
    
@admin.register(User)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'social_login_id')