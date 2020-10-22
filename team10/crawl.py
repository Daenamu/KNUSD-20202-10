import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "knu_reminder.settings")
django.setup()

from main.models import Post
from crawler.haksaCrawl import extract_indeed_notices

data_dict = extract_indeed_notices()
for data in data_dict:
    fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'])
    fb.save()