'''아동학부 공지 crawl'''

import requests
from bs4 import BeautifulSoup

URL = "http://child.knu.ac.kr/HOME/knuchild/sub.htm?nav_code=knu1468564874"

def child_extract_indeed_pages():  # page href list
    pages = [URL]
    base_url = "http://child.knu.ac.kr"

    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    link = soup.find("div", {"class": "paging"})
    links = link.find_all("a")

    for page in links:
        link = page.attrs["href"]
        link = base_url + link
        pages.append(link)

    return pages

def child_crawl(notice_url):
    link = requests.get(notice_url)
    soup = BeautifulSoup(link.text, "html.parser")
    
    dict_data = {'title': 'title', 'modify_dt': 'modify_dt', 'content': 'content', 'type': "치과대학", 'url': 'url', 'image_url': 'image_url','download_url': 'download_url'}
    return dict_data

def check_fixed_notice(notice_html): #공지사항 상단 고정 확인 인수 반환
    check = notice_html.find("td")
    check = check.attrs["class"]
    return check[-1]

def child_extract_indeed_notices(list_pages):
    notices = []
    count = 0
    base_url = "http://child.knu.ac.kr"

    for page in list_pages: 
        link = requests.get(page)
        soup = BeautifulSoup(link.text, "html.parser")
        result = soup.find("div", {"class":"board_list"})
        results = result.find_all("tr")

        for result in results[1:]:
            che = check_fixed_notice(result)
            if (che == "fst"):
                notice_td = result.find("td", {"class":"subject"})
                notice_url = notice_td. find("a").attrs["href"]
                notice_url = base_url + notice_url
                #notice = child_crawl(notice_url)
                #count = count + 1
                #print(f"{page - 1}page {count}번 게시물 crawling")
                #print(notice)
                #notices.append(notice)
    #return notices
