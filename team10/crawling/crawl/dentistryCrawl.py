'''치과대학 공지 crawl'''
'''
    본문 표 구현하기
    본문 크롤링하기
    치과대학 공지에는 이미지 존재 X
'''


import requests
from bs4 import BeautifulSoup
import re

URL = "https://dent.knu.ac.kr/community/notice/list.jsp?page=1&gubun=&svalue=&group="

def dent_extract_indeed_pages():  # last page return
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")

    links = soup.find_all("a", {"onfocus": "this.blur()"})
    link = links[-2]
    link = link.attrs["href"]
    link = re.findall("\d+", link)
    max_page = int(link[0])

    return max_page

def dentistry_crawl(notice_url):
    link = requests.get(notice_url)
    soup = BeautifulSoup(link.text, "html.parser")
    title_html = soup.find("td", {"height":"30"})
    title = title_html.string

    dt_html = soup.find_all("td", {"width":"90"})
    modify_dt = dt_html[2].string

    #dent_content_text(notice_url)

    url = notice_url
    download_url = dent_extract_content_attach(notice_url)

    dict_data = {'title': title, 'modify_dt': modify_dt, 'content': 'content', 'type': "치과대학", 'url': url, 'image_url': 'image_url','download_url': download_url}
    #print(dict_data)
    #print("---------------------------------")
    return dict_data

'''
def dent_content_text(notice_url):
    link = requests.get(notice_url)
    soup = BeautifulSoup(link.text, "html.parser")
    cont_html = soup.find("td", {"style":"padding:15 15 15 15;"})
    conts = cont_html.find_all("p") #모든 p가 포함됨. table안의 p도 포함되서 중복 출력됨. 수정해야함.
    for cont in conts:
        try:
            table_html = cont.find("table")
            tables = table_html.find_all("td")
        except AttributeError as e:
            print(cont.get_text())
            print("NONE")
        else:
            print(table_html)
'''
def dent_extract_content_attach(notice_url): #본문 첨부파일
    attach = []
    extension = [] # 첨부파일 확장자
    basic_url = "https://dent.knu.ac.kr"
    result = requests.get(notice_url)
    soup = BeautifulSoup(result.text, "html.parser")

    attach_html = soup.find("td", {"width":"650"})
    attach_hrefs = attach_html.find_all("a", {"onfocus": "this.blur()"})

    try:
        attach_hrefs = attach_html.find_all("a", {"onfocus": "this.blur()"})
        attach_urls = attach_hrefs
    except AttributeError as e:
        return attach

    for attach_url in attach_urls:
        attach_extension = attach_url.get_text()
        attach_extension = attach_extension[-3:]
        extension.append(attach_extension)

        sub_url = attach_url.attrs["href"]
        final_url = basic_url + sub_url
        attach.append(final_url)

    return attach

    
def dent_extract_indeed_notices(last_pages):
    notices = []
    count = 0

    for page in range(1,last_pages+1): #last_pages+1로 변경
        link = requests.get(f"https://dent.knu.ac.kr/community/notice/list.jsp?page={page}&gubun=&svalue=&group=")
        soup = BeautifulSoup(link.text, "html.parser")
        results = soup.find_all("td", {"width":"345"})

        for result in results[1:]:
            notice_url = result.find("a").attrs["href"]
            notice_url = "https://dent.knu.ac.kr/community/notice/" + notice_url
            count = count + 1
            print(f"{page - 1}page {count}번 게시물 crawling")
            dentistry_crawl(notice_url)