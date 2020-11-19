from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class MajorList(models.Model):
    major = models.CharField(max_length=20, default=0)

    class Meta:
        db_table = "major_list"

class User(AbstractBaseUser):
    social = models.CharField(max_length=20, blank=True)
    social_login_id = models.CharField(max_length=50, blank=True)
    token = models.TextField('Token', null=True)
    refresh_token = models.TextField('Refresh_token', null=True)
    nickname = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['social', 'social_login_id']

class Bookmark(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.TextField('Posts', null=True)
    alarm = models.BooleanField(default=False)

class BoardList(models.Model):
    board_name = models.CharField(verbose_name='NAME', max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.TextField('Department', null=True)
    alarm = models.BooleanField(default=False)
    
class Post(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=100)
    slug = models.SlugField('SLUG', allow_unicode=True,
                            help_text='calender short title')
    content = models.TextField('Content', blank=True)
    upload_dt = models.DateTimeField('Upload Date')
    department = models.CharField('Department', max_length=50)
    url = models.URLField('URL')

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'main_post'
        ordering = ('-upload_dt', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:post_detail', args=(self.id, ))

    def get_previous(self):
        return self.get_previous_by_upload_dt()

    def get_next(self):
        return self.get_next_by_upload_dt()
