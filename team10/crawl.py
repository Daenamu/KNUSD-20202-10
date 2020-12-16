import django
import os
import time
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "knu_reminder.settings")
django.setup()

from main.models import Post
from crawler import haksaCrawl, hanmun_crawl, korean_crawl, childCrawl, fashionCrawl

def update_haksa():
    try:
        key = Post.objects.filter(department="학사공지").latest('upload_dt')
    except:
        key = None

    if key:
        latest = haksaCrawl.check_latest()
        if key.title != latest:
            data_dict = haksaCrawl.extract_latest_notices(key.title)
            for data in data_dict:
                if data['content'] != "":
                    print(f"{data['title']} is updated")
                    fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'])
                    fb.save()   
            return latest
        else:
            return None
    else:
        data_dict = haksaCrawl.extract_indeed_notices(3)
        # data_dict = haksaCrawl.extract_indeed_notices(haksaCrawl.extract_indeed_pages())
        for data in data_dict:
            if data['content'] != "":
                fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'])
                fb.save()
        return haksaCrawl.check_latest()

def update_child():
    try:
        key = Post.objects.filter(department="아동학부").latest('upload_dt')
    except:
        key = None

    if key:
        latest = childCrawl.child_check_latest()
        if key.title != latest:
            data_dict = childCrawl.child_extract_latest_notices(key.title)
            for data in data_dict:
                if data['content'] != "":
                    fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'])
                    fb.save()
            return latest
        else:
            return None
    else:
        # data_dict = childCrawl.child_extract_indeed_notices(3)
        data_dict = childCrawl.child_extract_indeed_notices(childCrawl.child_extract_indeed_pages())
        for data in data_dict:
            if data['content'] != "":
                fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'])
                fb.save()
        return childCrawl.child_check_latest()

def update_fasion():
    try:
        key = Post.objects.filter(department="의류학과").latest('upload_dt')
    except:
        key = None

    if key:
        latest = fashionCrawl.fashion_check_latest()
        if key.title != latest:
            data_dict = fashionCrawl.fashion_extract_latest_notices(key.title)
            for data in data_dict:
                if data['content'] != "":
                    fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'])
                    fb.save()
            return latest
        else:
            return None
    else:
        # data_dict = fashionCrawl.fashion_extract_indeed_notices(3)
        data_dict = fashionCrawl.fashion_extract_indeed_notices(fashionCrawl.fashion_extract_indeed_pages())
        for data in data_dict:
            if data['content'] != "":
                fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'])
                fb.save()
        return fashionCrawl.fashion_check_latest()



def update_hanmun():
    try:
        key = Post.objects.filter(department="한문학과").latest('upload_dt')
    except:
        key = None

    if key:
        latest = hanmun_crawl.check_latest()
        if key.title != latest:
            data_dict = hanmun_crawl.extract_latest_notices(key.title)
            for data in data_dict:
                if data['content'] != "":
                    fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'])
                    fb.save()
            return latest
        else:
            return None
    else:
        data_dict = hanmun_crawl.extract_hanmun_notices(3)
        # data_dict = hanmun_crawl.extract_hanmun_notices(hanmun_crawl.extract_last_pages())
        for data in data_dict:
            if data['content'] != "":
                fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'])
                fb.save()
        return hanmun_crawl.check_latest()

def update_korean():
    try:
        key = Post.objects.filter(department="국어국문학과").latest('upload_dt')
    except:
        key = None

    if key:
        latest = korean_crawl.check_latest()
        if key.title != latest:
            data_dict = korean_crawl.extract_latest_notices(key.title)
            for data in data_dict:
                if data['content'] != "":
                    fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'])
                    fb.save()
            return latest
        else:
            return None
    else:
        data_dict = korean_crawl.extract_korean_notices(3)
        # data_dict = korean_crawl.extract_korean_notices(korean_crawl.extract_last_pages())
        for data in data_dict:
            if data['content'] != "":
                fb = Post(title=data['title'], upload_dt=data['modify_dt'], department=data['type'], content=data['content'], url=data['url'])
                fb.save()
        return korean_crawl.check_latest()


if __name__ == '__main__':
    while True:   
        latest = update_haksa()
        if latest is not None:
            print(f"새 학사 공지: {latest}")
        else:
            print("학사 공지: 최신 상태")

        
        latest = update_child()
        if latest is not None:
            print(f"새 아동학부 공지: {latest}")
        else:
            print("아동학부 공지: 최신 상태")
        
        
        latest = update_fasion()
        if latest is not None:
            print(f"새 의류학과 공지: {latest}")
        else:
            print("의류학과 공지: 최신 상태")
        
        
        latest = update_hanmun()
        if latest is not None:
            print(f"새 한문학과 공지: {latest}")
        else:
            print("한문학과 공지: 최신 상태")
        
        '''
        latest = update_korean()
        if latest is not None:
            print(f"새 국어국문학과 공지: {latest}")
        else:
            print("국어국문학과 공지: 최신 상태")
        '''
        time.sleep(60)