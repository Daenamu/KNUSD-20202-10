from django.db import models
from django.urls import reverse

# Create your models here.

class MajorList(models.Model):
    major = models.CharField(max_length=20, default=0)

    class Meta:
        db_table = "major_list"

class SocialPlatform(models.Model):
    platform = models.CharField(max_length=20, default=0)

    class Meta:
        db_table = "social_platform"

class User(models.Model):
    social = models.ForeignKey(SocialPlatform, on_delete=models.CASCADE, max_length=20, blank=True, default=1)
    social_login_id = models.CharField(max_length=50, blank=True)
    

class Post(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=100)
    slug = models.SlugField('SLUG', allow_unicode=True,
                            help_text='calender short title')
    content = models.TextField('Content', blank=True)
    upload_dt = models.DateTimeField('Upload Date')
    department = models.CharField('Department', max_length=50)
    url = models.URLField('URL')
    image_url = models.URLField('URL', blank=True, null=True)
    download_url = models.URLField('URL', blank=True, null=True)

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