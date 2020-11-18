import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "knu_reminder.settings")
django.setup()

from main.models import Post
from crawler import haksaCrawl, hanmun_crawl, korean_crawl #, dentistryCrawl

def update_haksa():
    try:
        key = Post.objects.filter(department="학사공지").latest('upload_dt')
    except:
        key = None

    if key:
        print(f"{key} is latest saved post")
        latest = haksaCrawl.check_latest()
        if key.title != latest:
            print(f"{latest} post is latest post.")
            data_dict = haksaCrawl.extract_latest_notices(key.title)
            for data in data_dict:
                print(f"{data['title']} is updated")
                fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'], image_url=data['image_url'], download_url=['download_url'])
                fb.save()
        else:
            print("학사 공지 is latest version")
    else:
        data_dict = haksaCrawl.extract_indeed_notices(3)
        # data_dict = haksaCrawl.extract_indeed_notices(haksaCrawl.extract_indeed_pages())
        for data in data_dict:
            fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'], image_url=data['image_url'], download_url=['download_url'])
            fb.save()

def update_hanmun():
    try:
        key = Post.objects.filter(department="한문학과").latest('upload_dt')
    except:
        key = None

    if key:
        print(f"{key} is latest saved post")
        latest = hanmun_crawl.check_latest()
        if key.title != latest:
            print(f"{latest} post is latest post.")
            data_dict = hanmun_crawl.extract_latest_notices(key.title)
            for data in data_dict:
                print(f"{data['title']} is updated")
                fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'], image_url=data['image_url'], download_url=['download_url'])
                fb.save()
        else:
            print("한문학과 is latest version")
    else:
        data_dict = hanmun_crawl.extract_hanmun_notices(3)
        # data_dict = hanmun_crawl.extract_hanmun_notices(hanmun_crawl.extract_last_pages())
        for data in data_dict:
            fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'], image_url=data['image_url'], download_url=['download_url'])
            fb.save()

def update_korean():
    try:
        key = Post.objects.filter(department="국어국문학과").latest('upload_dt')
    except:
        key = None

    if key:
        print(f"{key} is latest saved post")
        latest = korean_crawl.check_latest()
        if key.title != latest:
            print(f"{latest} post is latest post.")
            data_dict = korean_crawl.extract_latest_notices(key.title)
            for data in data_dict:
                print(f"{data['title']} is updated")
                fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'], image_url=data['image_url'], download_url=['download_url'])
                fb.save()
        else:
            print("국어국문학과 is latest version")
    else:
        data_dict = korean_crawl.extract_korean_notices(3)
        # data_dict = korean_crawl.extract_korean_notices(korean_crawl.extract_last_pages())
        for data in data_dict:
            fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'], image_url=data['image_url'], download_url=['download_url'])
            fb.save()

'''
def update_dentistry():
    try:
        key = Post.objects.filter(department="치과대학").latest('upload_dt')
    except:
        key = None

    if key:
        print(f"{key} is latest saved post")
        latest = dentistryCrawl.dent_check_latest()
        if key.title != latest:
            print(f"{latest} post is latest post.")
            data_dict = dentistryCrawl.dent_extract_latest_notices(key.title)
            for data in data_dict:
                print(f"{data['title']} is updated")
                fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'], image_url=data['image_url'], download_url=['download_url'])
                fb.save()
        else:
            print("치과대학 is latest version")
    else:
        data_dict = dentistryCrawl.dent_extract_indeed_notices(3)
        # data_dict = dentistryCrawl.dent_extract_indeed_notices(dentistryCrawl.dent_extract_indeed_pages())
        for data in data_dict:
            fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'], image_url=data['image_url'], download_url=['download_url'])
            fb.save()
'''

if __name__ == '__main__':
    update_haksa()
    update_hanmun()
    # update_korean()
    # update_dentistry()