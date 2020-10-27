'''학사공지 crawl'''

import requests
from bs4 import BeautifulSoup
<<<<<<< HEAD:team10/crawling/crawl/haksaCrawl.py
import re
'''학사공지 crawl'''
=======
>>>>>>> master:team10/crawler/haksaCrawl.py

PAGE = 1
URL = f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdList.action?btin.page={PAGE}&popupDeco=false&btin.search_type=&btin.search_text=&menu_idx=42"

def extract_indeed_pages():  # last page return
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    pag = soup.find("div", {"class": "paging"})
    link = pag.find("a", {"class": "last"}).attrs["href"]

    max_page = int(link[len("javascript:selectPage("):-2])
    return max_page


def extract_content_url(doc_no, appl_no, note_div, now_page): #notice content url return
    url = f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdViewBtin.action?btin.doc_no={doc_no}&btin.appl_no={appl_no}&btin.page={now_page}&btin.search_type=&btin.search_text=&popupDeco=false&btin.note_div={note_div}&menu_idx=42"
    return url


def find_notice_note_div(html): #notice top or row return
    content_href = html.find("a").attrs["href"]
    content_href = content_href[len("javascript:doRead("):-2]
<<<<<<< HEAD:team10/crawling/crawl/haksaCrawl.py
    list = content_href.split(",")

    note = list[3].strip()
    note = note[1:-1]
=======
    List = content_href.split("\'")

    for i in range(0, 5):
        del List[i]
    note = List[3]
>>>>>>> master:team10/crawler/haksaCrawl.py

    return note


def find_content_url_parameter(html, page_num):
    content_href = html.find("a").attrs["href"]
    content_href = content_href[len("javascript:doRead("):-2]
    List = content_href.split("\'")

    for i in range(0, 5):
        del List[i]

    doc = List[0]
    appl = List[1]
    note = List[3]
    now = page_num
    url = extract_content_url(doc, appl, note, now)
    return url


def extract_content_text(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    cont = soup.find("div", {"class": "board_cont"})

    cont = str(cont)
    cont = cont.replace("<br/>", '\n')
    content_text = re.sub("<.+?>",'', cont, 0).strip()

    return content_text


def extract_content_image(url): # 본문 이미지
    images = []
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    cont = soup.find("div", {"class": "board_cont"})
    image = cont.find_all("img")

    for img in image:
        src = img.attrs["src"]
        images.append(src)
    return images

def extract_content_attach(url): #본문 첨부파일
    attach = []
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    cont = soup.find("div", {"class": "attach"})

    attach_hrefs = cont.find_all("li")

    for attach_href in attach_hrefs:
        href = attach_href.find("a").attrs["href"]
        attach_href = href[len("javascript:doDownload("):-2]
        List = attach_href.split(",")

        for i in range(0,3):
            li = List[i].strip()
            List[i] = li[1:-1]
        
        attach_url = f"http://my.knu.ac.kr/stpo/stpo/bbs/btin/downloadServlet.action?appFile.file_nbr={list[2]}&appFile.doc_no={list[0]}&appFile.appl_no={list[1]}&appFile.bbs_cde=812&bbs_cde=812&btin.bbs_cde=812&btin.doc_no={list[0]}&btin.appl_no={list[1]}"
        attach.append(attach_url)
    
    return attach

def haksa_crawl(html, page_num):
    title = html.find("a").string
    title = title.strip()
    modify_dt = html.find("td", {"class": "date"}).string
    modify_dt = modify_dt.strip()
    url = find_content_url_parameter(html, page_num)
    content = extract_content_text(url)
    image_url = extract_content_image(url)
    download_url = extract_content_attach(url)

<<<<<<< HEAD:team10/crawling/crawl/haksaCrawl.py
    dict = {'title': title, 'modify_dt': modify_dt, 'content': content, 'type': "학사공지", 'url': url, 'image_url': image_url,'download_url': download_url}
    return dict


def extract_indeed_notices(last_pages):
=======
    dict_data = {'title': title, 'modify_dt': modify_dt,
            'content': content, 'type': "학사공지", 'url': url}
    return dict_data


def loop_extract(notices, page):
    link = requests.get(
        f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdList.action?btin.page={page}&popupDeco=false&btin.search_type=&btin.search_text=&menu_idx=42")
    soup = BeautifulSoup(link.text, "html.parser")
    result = soup.find("table", {"title": "학사 공지사항"})
    results = result.find_all("tr")

    for result in results[1:]:
        notice = haksa_crawl(result, page)
        notices.append(notice)
        #print(haksa_crawl(result, page))
        #haksa_crawl(result, page)


def extract_indeed_notices():
    count = 0
    last_pages = extract_indeed_pages()
>>>>>>> master:team10/crawler/haksaCrawl.py
    notices = []

<<<<<<< HEAD:team10/crawling/crawl/haksaCrawl.py
    for page in range(1, last_pages + 1):
        link = requests.get(f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdList.action?btin.page={page}&popupDeco=false&btin.search_type=&btin.search_text=&menu_idx=42")
=======
    for page in range(2, last_pages + 1):
        count = 0
        link = requests.get(
            f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdList.action?btin.page={page}&popupDeco=false&btin.search_type=&btin.search_text=&menu_idx=42")
>>>>>>> master:team10/crawler/haksaCrawl.py
        soup = BeautifulSoup(link.text, "html.parser")
        result = soup.find("table", {"title": "학사 공지사항"})
        results = result.find_all("tr")

        for result in results[1:]:
            note = find_notice_note_div(result)
            #print(note)
            #print(len(note))
            if (note == "row"):
                notice = haksa_crawl(result, page)
                notices.append(notice)
                count = count + 1
                print(f"{page - 1}page {count}번 게시물 crawling")
                #print(haksa_crawl(result, page))
                #haksa_crawl(result, page)
    #print(notices[0])
    return notices


<<<<<<< HEAD:team10/crawling/crawl/haksaCrawl.py
def check_latest(): # latest notice title return
    page = 1
    link = requests.get(f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdList.action?btin.page={page}&popupDeco=false&btin.search_type=&btin.search_text=&menu_idx=42")
    soup = BeautifulSoup(link.text, "html.parser")
    result = soup.find("table", {"title": "학사 공지사항"})
    results = result.find_all("tr")

=======
# 가장 최근의 게시물의 제목을 str로 return
def check_latest():
    page = 1
    link = requests.get(
            f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdList.action?btin.page={page}&popupDeco=false&btin.search_type=&btin.search_text=&menu_idx=42")
    soup = BeautifulSoup(link.text, "html.parser")
    result = soup.find("table", {"title": "학사 공지사항"})
    results = result.find_all("tr")
>>>>>>> master:team10/crawler/haksaCrawl.py
    for result in results[1:2]:
        notice = haksa_crawl(result, page)
    return notice['title']

<<<<<<< HEAD:team10/crawling/crawl/haksaCrawl.py

def extract_latest_notices(latest): # 게시물 업데이트
    notices = []
    page = 1
    link = requests.get(f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdList.action?btin.page={page}&popupDeco=false&btin.search_type=&btin.search_text=&menu_idx=42")
=======
# 게시물 업데이트
def extract_latest_notices(latest):
    notices = []
    page = 1
    link = requests.get(
            f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdList.action?btin.page={page}&popupDeco=false&btin.search_type=&btin.search_text=&menu_idx=42")
>>>>>>> master:team10/crawler/haksaCrawl.py
    soup = BeautifulSoup(link.text, "html.parser")
    result = soup.find("table", {"title": "학사 공지사항"})
    results = result.find_all("tr")

    for result in results[1:]:
        notice = haksa_crawl(result, page)
        if notice['title'] == latest: 
            break
        notices.append(notice)

    return notices
