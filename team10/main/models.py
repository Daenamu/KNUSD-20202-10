from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=100)
    slug = models.SlugField('SLUG', allow_unicode=True,
                            help_text='calender short title')
    content = models.TextField('Content', blank=True)
    upload_dt = models.DateTimeField('Upload Date')
    department = models.CharField('Department', max_length=50)
    url = models.URLField('URL', unique=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'main_post'
        ordering = ('-upload_dt', )

    def __str__(self):
        return self.title
