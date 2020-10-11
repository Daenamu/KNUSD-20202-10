import requests
from bs4 import BeautifulSoup
'''학사공지 crawl'''

PAGE = 1
URL = f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdList.action?btin.page={PAGE}&popupDeco=false&btin.search_type=&btin.search_text=&menu_idx=42"

def extract_indeed_pages(): #last page return
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    pag = soup.find("div", {"class": "paging"})
    link = pag.find("a", {"class": "last"}).attrs["href"]

    max_page = int(link[len("javascript:selectPage("):-2])
    return max_page


def extract_content_url(doc_no, appl_no, note_div, now_page):
    url = f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdViewBtin.action?btin.doc_no={doc_no}&btin.appl_no={appl_no}&btin.page={now_page}&btin.search_type=&btin.search_text=&popupDeco=false&btin.note_div={note_div}&menu_idx=42"
    return url


def find_notice_note_div(html):
    content_href = html.find("a").attrs["href"]
    content_href = content_href[len("javascript:doRead("):-2]
    list = content_href.split("\'")

    for i in range(0, 5):
        del list[i]
    note = list[3]

    return note


def find_content_url_parameter(html, page_num):
    content_href = html.find("a").attrs["href"]
    content_href = content_href[len("javascript:doRead("):-2]
    list = content_href.split("\'")

    for i in range(0, 5):
        del list[i]

    doc = list[0]
    appl = list[1]
    note = list[3]
    now = page_num
    url = extract_content_url(doc, appl, note, now)
    return url


def extract_content_text(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    cont = soup.find("div", {"class": "board_cont"})
    cont = str(cont)
    cont = cont.replace("<br/>", '\n')
    cont = cont.replace('<br>', '')
    cont = cont.replace('</br>', '')
    cont = cont.replace('<div class="board_cont">', '')
    cont = cont.replace('</div>', '')
    cont = cont.replace('<b>', '')
    cont = cont.replace('</b>', '')

    cont = cont.strip()
    return cont


def haksa_crawl(html, page_num):
    title = html.find("a").string
    title = title.strip()
    modify_dt = html.find("td", {"class": "date"}).string
    modify_dt = modify_dt.strip()
    url = find_content_url_parameter(html, page_num)
    content = extract_content_text(url)

    dict = {'title': title, 'modify_dt': modify_dt, 'content': content, 'type': "학사공지", 'url': url}
    return dict


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


def extract_indeed_notices(last_pages):
    notices = []
    page = 1
    loop_extract(notices, page)

    for page in range(2, last_pages + 1):
        link = requests.get(f"https://knu.ac.kr/wbbs/wbbs/bbs/btin/stdList.action?btin.page={page}&popupDeco=false&btin.search_type=&btin.search_text=&menu_idx=42")
        soup = BeautifulSoup(link.text, "html.parser")
        result = soup.find("table", {"title":"학사 공지사항"})
        results = result.find_all("tr")


        for result in results[1:]:
            note = find_notice_note_div(result)
            if (note == "row"):
                notice = haksa_crawl(result, page)
                notices.append(notice)
                #print(haksa_crawl(result, page))
                #haksa_crawl(result, page)

    #print(notices[0])
    return notices