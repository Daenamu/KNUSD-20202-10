import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "knu_reminder.settings")
django.setup()

from main.models import Post
from crawler.haksaCrawl import extract_indeed_notices, check_latest, extract_latest_notices, extract_indeed_pages

def update_haksa():
    key = Post.objects.filter(department="학사공지").latest('upload_dt')

    if key:
        print(f"{key} is latest saved post")
        latest = check_latest()
        if key.title != latest:
            print(f"{latest} post is latest post.")
            data_dict = extract_latest_notices(key.title)
            for data in data_dict:
                print(f"{data['title']} is updated")
                fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'])
                fb.save()
        else:
            print("학사 공지 is latest version")
    else:
        data_dict = extract_indeed_notices(extract_indeed_pages())
        for data in data_dict:
            fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'])
            fb.save()

if __name__ == '__main__':
    update_haksa()